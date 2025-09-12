#!/usr/bin/env python3
"""
Command Line Interface for Gemini HTML Manager
"""
import click
import os
import sys
from typing import List

# Add the parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_html_manager.file_manager import HTMLFileManager
from gemini_html_manager.google_workspace import GoogleWorkspaceManager
from gemini_html_manager.config import config


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Gemini HTML Manager - Manage HTML exports from Google Gemini with Google Workspace integration"""
    pass


@cli.command()
@click.argument('source_path', type=click.Path(exists=True))
@click.option('--name', '-n', help='New name for the imported file')
def import_file(source_path: str, name: str):
    """Import an HTML file to the export directory"""
    manager = HTMLFileManager()
    result = manager.import_html_file(source_path, name)
    
    if result:
        click.echo(f"Successfully imported: {result}")
    else:
        click.echo("Failed to import file", err=True)
        sys.exit(1)


@cli.command()
@click.option('--format', 'output_format', type=click.Choice(['table', 'json']), default='table')
def list_files(output_format: str):
    """List all HTML files in the export directory"""
    manager = HTMLFileManager()
    files = manager.list_html_files()
    
    if not files:
        click.echo("No HTML files found in export directory")
        return
    
    if output_format == 'json':
        import json
        click.echo(json.dumps(files, indent=2, default=str))
    else:
        # Table format
        click.echo(f"{'Filename':<30} {'Size (MB)':<10} {'Title':<40} {'Created':<20}")
        click.echo("-" * 100)
        
        for file_info in files:
            filename = file_info.get('filename', '')[:29]
            size_mb = file_info.get('size_mb', 0)
            title = file_info.get('title', '')[:39]
            created = file_info.get('created_time', '')[:19]
            
            click.echo(f"{filename:<30} {size_mb:<10.2f} {title:<40} {created:<20}")


@cli.command()
@click.argument('query')
def search(query: str):
    """Search HTML files by filename, title, or content"""
    manager = HTMLFileManager()
    results = manager.search_files(query)
    
    if not results:
        click.echo(f"No files found matching: {query}")
        return
    
    click.echo(f"Found {len(results)} files matching '{query}':")
    click.echo(f"{'Filename':<30} {'Title':<40}")
    click.echo("-" * 70)
    
    for file_info in results:
        filename = file_info.get('filename', '')[:29]
        title = file_info.get('title', '')[:39]
        click.echo(f"{filename:<30} {title:<40}")


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--title', '-t', help='Title for the uploaded file')
@click.option('--convert', is_flag=True, help='Convert to Google Docs instead of uploading as HTML')
def upload(file_path: str, title: str, convert: bool):
    """Upload HTML file to Google Drive"""
    workspace_manager = GoogleWorkspaceManager()
    
    if not workspace_manager.credentials:
        click.echo("Google Workspace authentication failed. Please check credentials.", err=True)
        sys.exit(1)
    
    if convert:
        file_id = workspace_manager.convert_html_to_google_doc(file_path, title)
        file_type = "Google Doc"
    else:
        file_id = workspace_manager.upload_html_file(file_path, title)
        file_type = "HTML file"
    
    if file_id:
        file_info = workspace_manager.get_file_info(file_id)
        if file_info:
            click.echo(f"Successfully uploaded {file_type}: {file_info['name']}")
            click.echo(f"View link: {file_info['webViewLink']}")
        else:
            click.echo(f"Uploaded {file_type} with ID: {file_id}")
    else:
        click.echo(f"Failed to upload {file_type}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--directory', '-d', default=None, help='Directory to upload from (default: export directory)')
@click.option('--convert', is_flag=True, help='Convert to Google Docs instead of uploading as HTML')
def batch_upload(directory: str, convert: bool):
    """Upload all HTML files from a directory to Google Drive"""
    workspace_manager = GoogleWorkspaceManager()
    
    if not workspace_manager.credentials:
        click.echo("Google Workspace authentication failed. Please check credentials.", err=True)
        sys.exit(1)
    
    if not directory:
        directory = config.get('html_manager.export_directory', 'html_exports')
    
    if not os.path.exists(directory):
        click.echo(f"Directory not found: {directory}", err=True)
        sys.exit(1)
    
    # Get list of HTML files
    manager = HTMLFileManager()
    if directory == manager.export_directory:
        files = manager.list_html_files()
        file_paths = [f['path'] for f in files]
    else:
        # Scan directory for HTML files
        supported_extensions = config.get('html_manager.supported_extensions', ['.html', '.htm'])
        file_paths = []
        for filename in os.listdir(directory):
            if any(filename.lower().endswith(ext) for ext in supported_extensions):
                file_paths.append(os.path.join(directory, filename))
    
    if not file_paths:
        click.echo(f"No HTML files found in {directory}")
        return
    
    click.echo(f"Found {len(file_paths)} HTML files to upload...")
    
    uploaded_count = 0
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        
        try:
            if convert:
                file_id = workspace_manager.convert_html_to_google_doc(file_path)
                file_type = "Google Doc"
            else:
                file_id = workspace_manager.upload_html_file(file_path)
                file_type = "HTML file"
            
            if file_id:
                uploaded_count += 1
                click.echo(f"✓ Uploaded {filename} as {file_type}")
            else:
                click.echo(f"✗ Failed to upload {filename}")
                
        except Exception as e:
            click.echo(f"✗ Error uploading {filename}: {e}")
    
    click.echo(f"\nCompleted: {uploaded_count}/{len(file_paths)} files uploaded successfully")


@cli.command()
def list_drive_files():
    """List files in Google Drive Gemini folder"""
    workspace_manager = GoogleWorkspaceManager()
    
    if not workspace_manager.credentials:
        click.echo("Google Workspace authentication failed. Please check credentials.", err=True)
        sys.exit(1)
    
    files = workspace_manager.list_gemini_files()
    
    if not files:
        click.echo("No files found in Google Drive Gemini folder")
        return
    
    click.echo(f"Found {len(files)} files in Google Drive:")
    click.echo(f"{'Name':<40} {'Type':<20} {'Size':<10} {'Created':<20}")
    click.echo("-" * 90)
    
    for file_info in files:
        name = file_info.get('name', '')[:39]
        mime_type = file_info.get('mimeType', '').split('.')[-1][:19]
        size = file_info.get('size', 'N/A')
        if size != 'N/A':
            size = f"{int(size) / 1024 / 1024:.2f}MB"
        created = file_info.get('createdTime', '')[:19]
        
        click.echo(f"{name:<40} {mime_type:<20} {size:<10} {created:<20}")


@cli.command()
def cleanup():
    """Remove duplicate files based on checksum"""
    manager = HTMLFileManager()
    duplicates = manager.cleanup_duplicates()
    
    if duplicates:
        click.echo(f"Removed {len(duplicates)} duplicate files:")
        for filename in duplicates:
            click.echo(f"  - {filename}")
    else:
        click.echo("No duplicates found")


@cli.command()
@click.option('--format', 'export_format', type=click.Choice(['csv', 'json']), default='csv')
def export_list(export_format: str):
    """Export file list to CSV or JSON"""
    manager = HTMLFileManager()
    filename = manager.export_file_list(export_format)
    click.echo(f"Exported file list to: {filename}")


@cli.command()
def setup():
    """Setup Google Workspace credentials"""
    click.echo("Setting up Google Workspace integration...")
    
    # Check if credentials file exists
    credentials_file = config.get('google.credentials_file')
    if not os.path.exists(credentials_file):
        click.echo(f"\nCredentials file not found: {credentials_file}")
        click.echo("To set up Google Workspace integration:")
        click.echo("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
        click.echo("2. Create a new project or select existing one")
        click.echo("3. Enable Google Drive API and Google Docs API")
        click.echo("4. Create credentials (OAuth 2.0 Client ID) for Desktop application")
        click.echo("5. Download the credentials JSON file")
        click.echo(f"6. Save it as '{credentials_file}' in this directory")
        return
    
    # Test authentication
    workspace_manager = GoogleWorkspaceManager()
    if workspace_manager.credentials:
        click.echo("✓ Google Workspace authentication successful!")
        
        # Test API access
        files = workspace_manager.list_gemini_files()
        click.echo(f"✓ Found {len(files)} files in Google Drive")
        
    else:
        click.echo("✗ Authentication failed. Please check your credentials.")


@cli.command()
def web():
    """Start web interface"""
    try:
        from gemini_html_manager.web_interface import app
        host = config.get('web_interface.host', 'localhost')
        port = config.get('web_interface.port', 5000)
        debug = config.get('web_interface.debug', False)
        
        click.echo(f"Starting web interface at http://{host}:{port}")
        app.run(host=host, port=port, debug=debug)
        
    except ImportError:
        click.echo("Web interface dependencies not available. Install Flask to use this feature.")


if __name__ == '__main__':
    cli()