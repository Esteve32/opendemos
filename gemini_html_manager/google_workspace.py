"""
Google Workspace API integration for managing HTML files
"""
import os
import json
import pickle
from typing import List, Dict, Optional, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from .config import config
import io


class GoogleWorkspaceManager:
    """Manages Google Workspace API interactions"""
    
    def __init__(self):
        self.credentials = None
        self.drive_service = None
        self.docs_service = None
        self.initialize_services()
    
    def initialize_services(self) -> None:
        """Initialize Google API services"""
        self.credentials = self.get_credentials()
        if self.credentials:
            self.drive_service = build('drive', 'v3', credentials=self.credentials)
            self.docs_service = build('docs', 'v1', credentials=self.credentials)
    
    def get_credentials(self) -> Optional[Credentials]:
        """Get or create Google API credentials"""
        scopes = config.get('google.scopes')
        token_file = config.get('google.token_file')
        credentials_file = config.get('google.credentials_file')
        
        creds = None
        
        # Load existing token
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(credentials_file):
                    print(f"Credentials file not found: {credentials_file}")
                    print("Please download credentials from Google Cloud Console")
                    return None
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_file, scopes)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error during authentication: {e}")
                    return None
            
            # Save the credentials for the next run
            try:
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)
            except Exception as e:
                print(f"Error saving token: {e}")
        
        return creds
    
    def upload_html_file(self, file_path: str, title: Optional[str] = None) -> Optional[str]:
        """Upload HTML file to Google Drive"""
        if not self.drive_service:
            print("Google Drive service not initialized")
            return None
        
        try:
            if not title:
                title = os.path.basename(file_path)
            
            file_metadata = {
                'name': title,
                'parents': [self.get_or_create_gemini_folder()]
            }
            
            media = MediaFileUpload(file_path, mimetype='text/html')
            
            file_result = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            # Make file publicly viewable
            self.share_file(file_result['id'])
            
            print(f"Uploaded {title} to Google Drive")
            return file_result['id']
            
        except Exception as e:
            print(f"Error uploading file {file_path}: {e}")
            return None
    
    def convert_html_to_google_doc(self, file_path: str, title: Optional[str] = None) -> Optional[str]:
        """Convert HTML file to Google Docs"""
        if not self.drive_service:
            print("Google Drive service not initialized")
            return None
        
        try:
            if not title:
                title = os.path.basename(file_path).replace('.html', '')
            
            # Read HTML content
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Upload as Google Doc
            file_metadata = {
                'name': title,
                'parents': [self.get_or_create_gemini_folder()],
                'mimeType': 'application/vnd.google-apps.document'
            }
            
            media = MediaIoBaseUpload(
                io.BytesIO(html_content.encode('utf-8')),
                mimetype='text/html',
                resumable=True
            )
            
            file_result = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            # Share the document
            self.share_file(file_result['id'])
            
            print(f"Converted {title} to Google Docs")
            return file_result['id']
            
        except Exception as e:
            print(f"Error converting file {file_path}: {e}")
            return None
    
    def get_or_create_gemini_folder(self) -> str:
        """Get or create Gemini HTML exports folder in Google Drive"""
        folder_name = "Gemini HTML Exports"
        
        try:
            # Search for existing folder
            results = self.drive_service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                fields="files(id, name)"
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                return folders[0]['id']
            
            # Create new folder
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            print(f"Created folder: {folder_name}")
            return folder['id']
            
        except Exception as e:
            print(f"Error creating folder: {e}")
            return 'root'  # Fallback to root folder
    
    def share_file(self, file_id: str) -> None:
        """Make file publicly viewable"""
        try:
            sharing_config = config.get('html_manager.default_sharing')
            
            permission = {
                'type': sharing_config.get('type', 'anyone'),
                'role': sharing_config.get('role', 'reader')
            }
            
            self.drive_service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
            
        except Exception as e:
            print(f"Error sharing file {file_id}: {e}")
    
    def list_gemini_files(self) -> List[Dict[str, Any]]:
        """List all files in Gemini HTML exports folder"""
        if not self.drive_service:
            return []
        
        try:
            folder_id = self.get_or_create_gemini_folder()
            
            results = self.drive_service.files().list(
                q=f"'{folder_id}' in parents",
                fields="files(id, name, mimeType, size, createdTime, webViewLink)"
            ).execute()
            
            return results.get('files', [])
            
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def batch_upload_html_files(self, directory_path: str) -> List[str]:
        """Upload all HTML files from a directory"""
        uploaded_files = []
        supported_extensions = config.get('html_manager.supported_extensions', ['.html', '.htm'])
        
        if not os.path.exists(directory_path):
            print(f"Directory not found: {directory_path}")
            return uploaded_files
        
        for filename in os.listdir(directory_path):
            if any(filename.lower().endswith(ext) for ext in supported_extensions):
                file_path = os.path.join(directory_path, filename)
                file_id = self.upload_html_file(file_path)
                if file_id:
                    uploaded_files.append(file_id)
        
        print(f"Uploaded {len(uploaded_files)} HTML files")
        return uploaded_files
    
    def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific file"""
        if not self.drive_service:
            return None
        
        try:
            file_info = self.drive_service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, size, createdTime, webViewLink, webContentLink"
            ).execute()
            
            return file_info
            
        except Exception as e:
            print(f"Error getting file info for {file_id}: {e}")
            return None