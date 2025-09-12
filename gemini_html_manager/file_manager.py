"""
HTML file management utilities
"""
import os
import shutil
import glob
from typing import List, Dict, Optional, Any
from datetime import datetime
import hashlib
from bs4 import BeautifulSoup
import html2text
from .config import config


class HTMLFileManager:
    """Manages local HTML files and metadata"""
    
    def __init__(self):
        self.export_directory = config.get('html_manager.export_directory', 'html_exports')
        self.ensure_export_directory()
    
    def ensure_export_directory(self) -> None:
        """Ensure export directory exists"""
        if not os.path.exists(self.export_directory):
            os.makedirs(self.export_directory)
            print(f"Created export directory: {self.export_directory}")
    
    def import_html_file(self, source_path: str, new_name: Optional[str] = None) -> Optional[str]:
        """Import HTML file to export directory"""
        if not os.path.exists(source_path):
            print(f"Source file not found: {source_path}")
            return None
        
        # Check file size
        max_size_mb = config.get('html_manager.max_file_size', 10)
        file_size_mb = os.path.getsize(source_path) / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            print(f"File too large: {file_size_mb:.2f}MB (max: {max_size_mb}MB)")
            return None
        
        try:
            # Generate destination path
            if new_name:
                filename = new_name if new_name.endswith('.html') else f"{new_name}.html"
            else:
                filename = os.path.basename(source_path)
            
            # Add timestamp if file exists
            destination_path = os.path.join(self.export_directory, filename)
            if os.path.exists(destination_path):
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{timestamp}{ext}"
                destination_path = os.path.join(self.export_directory, filename)
            
            # Copy file
            shutil.copy2(source_path, destination_path)
            
            print(f"Imported {filename} to {self.export_directory}")
            return destination_path
            
        except Exception as e:
            print(f"Error importing file {source_path}: {e}")
            return None
    
    def list_html_files(self) -> List[Dict[str, Any]]:
        """List all HTML files in export directory with metadata"""
        files = []
        supported_extensions = config.get('html_manager.supported_extensions', ['.html', '.htm'])
        
        for ext in supported_extensions:
            pattern = os.path.join(self.export_directory, f"*{ext}")
            for file_path in glob.glob(pattern):
                try:
                    file_info = self.get_file_metadata(file_path)
                    if file_info:
                        files.append(file_info)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
        
        # Sort by creation time (newest first)
        files.sort(key=lambda x: x.get('created_time', ''), reverse=True)
        return files
    
    def get_file_metadata(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Extract metadata from HTML file"""
        if not os.path.exists(file_path):
            return None
        
        try:
            stat = os.stat(file_path)
            
            metadata = {
                'filename': os.path.basename(file_path),
                'path': file_path,
                'size_bytes': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'checksum': self.calculate_checksum(file_path)
            }
            
            # Extract HTML metadata
            html_metadata = self.extract_html_metadata(file_path)
            metadata.update(html_metadata)
            
            return metadata
            
        except Exception as e:
            print(f"Error getting metadata for {file_path}: {e}")
            return None
    
    def extract_html_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from HTML content"""
        metadata = {
            'title': '',
            'description': '',
            'word_count': 0,
            'has_images': False,
            'has_links': False,
            'is_gemini_canvas': False
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                metadata['title'] = title_tag.get_text().strip()
            
            # Extract description from meta tags
            desc_tag = soup.find('meta', attrs={'name': 'description'})
            if desc_tag:
                metadata['description'] = desc_tag.get('content', '').strip()
            
            # Convert to text for word count
            text_content = html2text.html2text(content)
            metadata['word_count'] = len(text_content.split())
            
            # Check for images
            metadata['has_images'] = bool(soup.find('img'))
            
            # Check for links
            metadata['has_links'] = bool(soup.find('a'))
            
            # Check if it's from Gemini Canvas (look for specific markers)
            if any(indicator in content.lower() for indicator in ['gemini', 'canvas', 'google ai']):
                metadata['is_gemini_canvas'] = True
            
        except Exception as e:
            print(f"Error extracting HTML metadata from {file_path}: {e}")
        
        return metadata
    
    def calculate_checksum(self, file_path: str) -> str:
        """Calculate MD5 checksum of file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ''
    
    def organize_files_by_date(self) -> Dict[str, List[Dict[str, Any]]]:
        """Organize files by creation date"""
        files = self.list_html_files()
        organized = {}
        
        for file_info in files:
            try:
                created_time = datetime.fromisoformat(file_info['created_time'])
                date_key = created_time.strftime('%Y-%m-%d')
                
                if date_key not in organized:
                    organized[date_key] = []
                
                organized[date_key].append(file_info)
                
            except Exception as e:
                print(f"Error organizing file {file_info.get('filename')}: {e}")
        
        return organized
    
    def search_files(self, query: str) -> List[Dict[str, Any]]:
        """Search files by title, filename, or content"""
        files = self.list_html_files()
        results = []
        
        query_lower = query.lower()
        
        for file_info in files:
            # Search in filename and title
            if (query_lower in file_info.get('filename', '').lower() or
                query_lower in file_info.get('title', '').lower() or
                query_lower in file_info.get('description', '').lower()):
                results.append(file_info)
                continue
            
            # Search in content (if needed)
            try:
                with open(file_info['path'], 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if query_lower in content:
                        results.append(file_info)
            except Exception as e:
                print(f"Error searching in file {file_info['path']}: {e}")
        
        return results
    
    def cleanup_duplicates(self) -> List[str]:
        """Remove duplicate files based on checksum"""
        files = self.list_html_files()
        checksum_map = {}
        duplicates = []
        
        for file_info in files:
            checksum = file_info.get('checksum')
            if not checksum:
                continue
            
            if checksum in checksum_map:
                # This is a duplicate - remove the newer one
                try:
                    os.remove(file_info['path'])
                    duplicates.append(file_info['filename'])
                    print(f"Removed duplicate: {file_info['filename']}")
                except Exception as e:
                    print(f"Error removing duplicate {file_info['path']}: {e}")
            else:
                checksum_map[checksum] = file_info
        
        return duplicates
    
    def export_file_list(self, format_type: str = 'csv') -> str:
        """Export file list to CSV or JSON"""
        files = self.list_html_files()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type.lower() == 'csv':
            import csv
            filename = f"gemini_files_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if files:
                    fieldnames = files[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(files)
        
        elif format_type.lower() == 'json':
            import json
            filename = f"gemini_files_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(files, jsonfile, indent=2, default=str)
        
        else:
            raise ValueError("Unsupported format. Use 'csv' or 'json'")
        
        print(f"Exported file list to {filename}")
        return filename