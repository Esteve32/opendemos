# API Documentation

The Gemini HTML Manager provides both REST API endpoints and Python API for programmatic access.

## REST API

### Base URL
```
http://localhost:5000
```

### Authentication
No authentication required for local deployment. For production, implement appropriate authentication.

### Endpoints

#### Search Files
```http
GET /api/search?q={query}
```

**Parameters:**
- `q` (string, optional): Search query for filename, title, or content

**Response:**
```json
{
  "files": [
    {
      "filename": "example.html",
      "path": "/path/to/file.html",
      "title": "Example Document",
      "size_mb": 1.2,
      "word_count": 500,
      "created_time": "2024-01-15T10:30:00",
      "has_images": true,
      "has_links": false,
      "is_gemini_canvas": true
    }
  ]
}
```

#### Upload to Google Drive
```http
POST /api/upload_to_drive
```

**Request Body:**
```json
{
  "file_path": "/path/to/file.html",
  "title": "Custom Title",
  "convert": false
}
```

**Response:**
```json
{
  "success": true,
  "file_id": "1ABC123...",
  "file_type": "HTML file",
  "name": "example.html",
  "link": "https://drive.google.com/file/d/1ABC123.../view"
}
```

#### Batch Upload to Google Drive
```http
POST /api/batch_upload_to_drive
```

**Request Body:**
```json
{
  "convert": false
}
```

**Response:**
```json
{
  "total_files": 10,
  "successful_uploads": 8,
  "results": [
    {
      "filename": "example1.html",
      "success": true,
      "file_id": "1ABC123...",
      "file_type": "HTML file"
    },
    {
      "filename": "example2.html",
      "success": false,
      "error": "Upload failed"
    }
  ]
}
```

#### Get File Metadata
```http
GET /api/file_metadata/{filename}
```

**Response:**
```json
{
  "filename": "example.html",
  "path": "/path/to/file.html",
  "size_bytes": 1048576,
  "size_mb": 1.0,
  "created_time": "2024-01-15T10:30:00",
  "modified_time": "2024-01-15T11:00:00",
  "title": "Example Document",
  "description": "An example HTML document",
  "word_count": 500,
  "has_images": true,
  "has_links": false,
  "is_gemini_canvas": true,
  "checksum": "d41d8cd98f00b204e9800998ecf8427e"
}
```

#### Cleanup Duplicates
```http
POST /api/cleanup_duplicates
```

**Response:**
```json
{
  "removed_files": ["duplicate1.html", "duplicate2.html"],
  "count": 2
}
```

## Python API

### File Manager

```python
from gemini_html_manager.file_manager import HTMLFileManager

# Initialize
manager = HTMLFileManager()

# Import file
file_path = manager.import_html_file('/path/to/source.html', 'new-name')

# List files
files = manager.list_html_files()

# Search files
results = manager.search_files('search query')

# Get metadata
metadata = manager.get_file_metadata('/path/to/file.html')

# Organize by date
organized = manager.organize_files_by_date()

# Cleanup duplicates
duplicates = manager.cleanup_duplicates()

# Export file list
filename = manager.export_file_list('csv')
```

### Google Workspace Manager

```python
from gemini_html_manager.google_workspace import GoogleWorkspaceManager

# Initialize
workspace = GoogleWorkspaceManager()

# Upload HTML file
file_id = workspace.upload_html_file('/path/to/file.html', 'Custom Title')

# Convert to Google Docs
doc_id = workspace.convert_html_to_google_doc('/path/to/file.html', 'Doc Title')

# List files in Drive
files = workspace.list_gemini_files()

# Get file info
info = workspace.get_file_info(file_id)

# Batch upload
uploaded_files = workspace.batch_upload_html_files('/path/to/directory')
```

### Configuration

```python
from gemini_html_manager.config import config

# Get configuration value
export_dir = config.get('html_manager.export_directory')

# Set configuration value
config.set('web_interface.port', 8080)

# Save configuration
config.save_config()
```

## Error Handling

### Common HTTP Status Codes
- `200 OK`: Success
- `400 Bad Request`: Invalid parameters
- `404 Not Found`: File or resource not found
- `500 Internal Server Error`: Server error

### Error Response Format
```json
{
  "error": "Error description",
  "details": "Additional error details"
}
```

## Rate Limiting

### Google APIs
- Google Drive API: 1,000 requests per 100 seconds per user
- Google Docs API: 300 requests per 100 seconds per user

### Best Practices
- Implement exponential backoff for retries
- Cache frequently accessed data
- Use batch operations when possible
- Monitor quota usage in Google Cloud Console

## Examples

### Upload Single File
```python
import requests

response = requests.post('http://localhost:5000/api/upload_to_drive', json={
    'file_path': '/path/to/file.html',
    'title': 'My Document',
    'convert': True
})

result = response.json()
if result['success']:
    print(f"Uploaded: {result['link']}")
```

### Search Files
```python
import requests

response = requests.get('http://localhost:5000/api/search', params={
    'q': 'gemini canvas'
})

files = response.json()['files']
for file in files:
    print(f"Found: {file['filename']} - {file['title']}")
```

### Batch Operations
```python
import requests

response = requests.post('http://localhost:5000/api/batch_upload_to_drive', json={
    'convert': False
})

result = response.json()
print(f"Uploaded {result['successful_uploads']} of {result['total_files']} files")
```

## WebSocket Support (Future)

Future versions may include WebSocket support for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:5000/ws');

ws.on('upload_progress', (data) => {
    console.log(`Upload progress: ${data.percent}%`);
});

ws.on('file_added', (data) => {
    console.log(`New file: ${data.filename}`);
});
```

## Webhooks (Future)

Future versions may support webhooks for integration with external systems:

```http
POST /api/webhooks/register
```

```json
{
  "url": "https://your-site.com/webhook",
  "events": ["file_uploaded", "file_converted"],
  "secret": "webhook_secret"
}
```