# Usage Examples

This document provides practical examples of how to use the Gemini HTML Manager for various scenarios.

## Scenario 1: Individual User - Managing Personal Gemini Exports

### Setup
```bash
# Quick setup
./setup.sh

# Start using immediately
python scripts/gemini_manager.py import-file ~/Downloads/my_gemini_export.html
python scripts/gemini_manager.py web
```

### Daily Workflow
```bash
# Import new Gemini Canvas export
python scripts/gemini_manager.py import-file ~/Downloads/gemini_infographic.html --name "Q4-Sales-Analysis"

# View all files
python scripts/gemini_manager.py list-files

# Search for specific content
python scripts/gemini_manager.py search "sales data"

# Upload to Google Drive
python scripts/gemini_manager.py upload html_exports/Q4-Sales-Analysis.html --convert
```

## Scenario 2: Team Lead - Sharing with Colleagues

### Bulk Upload for Team Sharing
```bash
# Upload all files to Google Drive at once
python scripts/gemini_manager.py batch-upload --convert

# Get list of all uploaded files with links
python scripts/gemini_manager.py list-drive-files
```

### Web Interface for Team Access
```bash
# Start web interface for team to access
python scripts/gemini_manager.py web

# Team members can:
# - Browse and search files at http://localhost:5000
# - View HTML previews
# - Upload files to Google Drive with one click
# - Download original files
```

## Scenario 3: Organization - Systematic Content Management

### Automated Workflow
```python
# Custom Python script for automated processing
import os
from gemini_html_manager.file_manager import HTMLFileManager
from gemini_html_manager.google_workspace import GoogleWorkspaceManager

def process_gemini_exports(source_directory):
    """Process all Gemini exports from a directory"""
    file_manager = HTMLFileManager()
    workspace_manager = GoogleWorkspaceManager()
    
    # Import all HTML files
    for filename in os.listdir(source_directory):
        if filename.endswith('.html'):
            file_path = os.path.join(source_directory, filename)
            imported_path = file_manager.import_html_file(file_path)
            
            if imported_path:
                # Upload to Google Drive and convert to Docs
                doc_id = workspace_manager.convert_html_to_google_doc(imported_path)
                print(f"Processed: {filename} -> Google Doc ID: {doc_id}")

# Usage
process_gemini_exports('/path/to/weekly/exports')
```

### Regular Maintenance
```bash
# Weekly cleanup script
#!/bin/bash

# Remove duplicates
python scripts/gemini_manager.py cleanup

# Export file inventory
python scripts/gemini_manager.py export-list --format csv

# Backup to Google Drive
python scripts/gemini_manager.py batch-upload
```

## Scenario 4: API Integration

### Using REST API
```python
import requests

# Search for files
response = requests.get('http://localhost:5000/api/search', params={'q': 'marketing'})
files = response.json()['files']

# Upload file to Google Drive
response = requests.post('http://localhost:5000/api/upload_to_drive', json={
    'file_path': '/path/to/file.html',
    'title': 'Marketing Strategy 2024',
    'convert': True
})

if response.json()['success']:
    print(f"Uploaded: {response.json()['link']}")
```

### Webhook Integration (Future)
```python
# Example webhook handler for automated processing
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/webhook/gemini-export', methods=['POST'])
def handle_gemini_export():
    """Handle new Gemini export notification"""
    data = request.json
    file_url = data['file_url']
    
    # Download and process file
    response = requests.post('http://localhost:5000/api/upload_to_drive', json={
        'file_path': download_file(file_url),
        'convert': True
    })
    
    return {'status': 'processed'}
```

## Scenario 5: Content Creator - Portfolio Management

### Organizing Creative Work
```bash
# Import with descriptive names
python scripts/gemini_manager.py import-file ~/Downloads/gemini_logo_concepts.html --name "Logo-Concepts-ClientABC"
python scripts/gemini_manager.py import-file ~/Downloads/gemini_color_palette.html --name "ColorPalette-BrandRefresh"

# Create searchable portfolio
python scripts/gemini_manager.py search "logo"
python scripts/gemini_manager.py search "color"
python scripts/gemini_manager.py search "client"
```

### Client Sharing
```bash
# Convert specific files to Google Docs for client collaboration
python scripts/gemini_manager.py upload html_exports/Logo-Concepts-ClientABC.html --convert --title "Logo Concepts for Review"

# Share portfolio via web interface
python scripts/gemini_manager.py web
# Share http://localhost:5000 with clients for browsing
```

## Scenario 6: Educational Institution - Course Materials

### Course Content Management
```python
# Organize by semester and course
import os
from gemini_html_manager.file_manager import HTMLFileManager

manager = HTMLFileManager()

def organize_course_materials(semester, course_code):
    """Organize course materials by semester and course"""
    files = manager.list_html_files()
    
    course_files = [f for f in files if course_code in f['title'] or course_code in f['filename']]
    
    for file_info in course_files:
        # Add metadata tags
        new_title = f"{semester}_{course_code}_{file_info['title']}"
        # Process and upload to institutional Google Drive
```

### Student Access
```bash
# Batch convert all course materials to Google Docs
python scripts/gemini_manager.py batch-upload --convert

# Set up shared access portal
python scripts/gemini_manager.py web
# Configure for institutional access
```

## Advanced Configuration Examples

### Custom Configuration
```yaml
# config.yaml for production use
google:
  scopes:
    - https://www.googleapis.com/auth/documents
    - https://www.googleapis.com/auth/drive
    - https://www.googleapis.com/auth/spreadsheets  # For analytics

html_manager:
  export_directory: /shared/gemini_exports
  max_file_size: 50  # MB for larger files
  default_sharing:
    type: domain  # Restrict to organization domain
    role: writer  # Allow editing

web_interface:
  host: 0.0.0.0  # Allow external access
  port: 8080
  debug: false

conversion:
  preserve_formatting: true
  convert_images: true
  max_doc_size: 5000000  # Larger documents
```

### Environment Variables for Production
```bash
# .env file for production deployment
export GEMINI_MANAGER_CONFIG=/etc/gemini-manager/config.yaml
export GOOGLE_CREDENTIALS=/secure/credentials.json
export FLASK_ENV=production
export FLASK_PORT=8080
```

## Troubleshooting Common Scenarios

### Large File Handling
```bash
# For large Gemini Canvas exports
# Increase max file size in config.yaml
# Use compression for storage
python -c "
from gemini_html_manager.file_manager import HTMLFileManager
manager = HTMLFileManager()
manager.config.set('html_manager.max_file_size', 100)  # 100MB
"
```

### Network Issues
```bash
# Retry upload with exponential backoff
for i in {1..3}; do
    python scripts/gemini_manager.py upload file.html && break
    sleep $((2**i))
done
```

### Bulk Operations
```bash
# Process files in parallel
find html_exports -name "*.html" | xargs -P 4 -I {} python scripts/gemini_manager.py upload {}
```

These examples demonstrate the flexibility and power of the Gemini HTML Manager across different use cases and organizational needs.