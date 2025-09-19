# Open Demos

A simple, extensible structure for hosting and browsing multiple demos from a single, nice-looking index page.

## Shareable link
Once GitHub Pages is enabled (Settings → Pages → Deploy from a branch → main + root `/`), your public URL will be:

- https://esteve32.github.io/opendemos/

## Repository structure
```
opendemos/
├─ index.html              # Main index page (cards, search, links to demos)
├─ demos.json              # Manifest consumed by index.html
├─ assets/
│  ├─ styles.css
│  └─ script.js
├─ demos/
│  ├─ hello-world/
│  │  ├─ index.html
│  │  └─ meta.json
└─ tools/
   └─ build-manifest.mjs   # Optional: auto-generate demos.json from demos/*
```

## Add a new demo
1. Create a new folder under `demos/<your-demo-id>/`.
2. Add:
   - `index.html` (the demo)
   - Optional: `thumbnail.(png|jpg|webp)` (a small preview image)
   - `meta.json` with:
     ```json
     {
       "title": "My Demo",
       "description": "One-liner about the demo",
       "tags": ["tag1", "tag2"]
     }
     ```
3. Update `demos.json` with your new demo entry (or run the optional build script below).

## Optional: auto-generate `demos.json`
If you prefer not to hand-edit `demos.json`, run:
```
node tools/build-manifest.mjs
```
This scans each `demos/*` folder and creates/updates the manifest.

## Local preview
You can open `index.html` directly, but `fetch` of `demos.json` may require a local server:
```
# one-liners (pick one)
npx http-server -p 8080 .
python3 -m http.server 8080
```
Then visit http://localhost:8080

---

## Legacy: OpenDemos - Visual Mockups Gallery

This repository also includes the comprehensive Gemini HTML Manager for managing AI-generated content and web applications.

## 🌟 Features

- **🎨 Public Demo Gallery**: Beautiful landing page showcasing visual mockups and interactive demos
- **📁 Gemini HTML Manager**: Full-featured web application for managing HTML exports from Google Gemini
- **☁️ Google Drive Integration**: Upload HTML files to Google Drive with automatic sharing
- **📄 Google Docs Conversion**: Convert HTML files to Google Docs for collaborative editing
- **🔍 Advanced Search**: Search files by filename, title, or content
- **🌐 Modern Web Interface**: Clean, responsive design with Bootstrap
- **⚡ CLI Tools**: Command-line interface for automation and batch operations
- **🔄 Batch Operations**: Upload multiple files at once, cleanup duplicates
- **📊 Analytics**: File statistics and organization by date

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Esteve32/opendemos.git
cd opendemos

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Demo Gallery

**Simple Server Launch:**
```bash
python start_server.py
```

**Or using the CLI:**
```bash
python scripts/gemini_manager.py web
```

**Access Points:**
- **🏠 Public Demo Gallery**: http://localhost:5000/
- **🛠️ Gemini HTML Manager**: http://localhost:5000/gemini-manager
- **📁 File Browser**: http://localhost:5000/gemini-manager/files

### 3. Setup Google Workspace Integration (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Drive API** and **Google Docs API**
4. Create **OAuth 2.0 Client ID** for Desktop application
5. Download credentials as `credentials.json` in the project root

### 4. Command Line Usage

```bash
# Import HTML file
python scripts/gemini_manager.py import-file path/to/your/file.html

# Upload to Google Drive
python scripts/gemini_manager.py upload path/to/file.html --convert

# Batch operations
python scripts/gemini_manager.py batch-upload
```

## 📋 Demo Gallery

### Live Interactive Demos

- **🛠️ Gemini HTML Manager**: Full web application for managing AI-generated HTML content with Google Workspace integration
- **📊 Data Visualization Canvas**: Interactive infographic showcasing data visualization trends (Gemini AI-generated)
- **📈 Marketing Strategy Presentation**: Comprehensive marketing strategy with modern design (AI-generated)
- **💻 Colibri OS Dashboard**: Modern operating system interface mockup with interactive widgets

### Static Mockups & Visual Content

The gallery includes various HTML files in:
- `html_exports/` - AI-generated content from Google Gemini Canvas
- `projects/` - Custom dashboard mockups and UI designs

## 📖 Usage Guide

### Managing HTML Files

#### Import Files
- **Web Interface**: Use the Upload page to drag & drop or select files
- **CLI**: `python scripts/gemini_manager.py import-file <path> --name "new-name"`

#### View and Organize
- Files are automatically organized by date
- Search functionality for quick finding
- Metadata extraction (title, word count, images, etc.)

### Google Workspace Integration

#### Upload to Google Drive
- Files are uploaded to "Gemini HTML Exports" folder
- Automatic public sharing (anyone with link can view)
- Preserves original formatting

#### Convert to Google Docs
- HTML content converted to editable Google Docs
- Maintains structure and formatting where possible
- Enables collaborative editing and comments

### Batch Operations

#### Upload Multiple Files
```bash
# Upload all files in export directory
python scripts/gemini_manager.py batch-upload

# Upload from specific directory
python scripts/gemini_manager.py batch-upload --directory /path/to/html/files

# Convert all to Google Docs
python scripts/gemini_manager.py batch-upload --convert
```

#### Cleanup and Maintenance
```bash
# Remove duplicate files
python scripts/gemini_manager.py cleanup

# Export file list
python scripts/gemini_manager.py export-list --format csv
```

## 🔧 Configuration

Copy `config.example.yaml` to `config.yaml` and customize:

```yaml
google:
  scopes:
    - https://www.googleapis.com/auth/documents
    - https://www.googleapis.com/auth/drive
  credentials_file: credentials.json

html_manager:
  export_directory: html_exports
  max_file_size: 10  # MB
  default_sharing:
    type: anyone
    role: reader

web_interface:
  host: localhost
  port: 5000
  debug: false
```

## 📖 API Reference

### REST API Endpoints

- `GET /api/search?q=query` - Search files
- `POST /api/upload_to_drive` - Upload single file to Google Drive
- `POST /api/batch_upload_to_drive` - Batch upload to Google Drive
- `GET /api/file_metadata/<filename>` - Get file metadata
- `POST /api/cleanup_duplicates` - Remove duplicate files

### CLI Commands

```bash
# File management
python scripts/gemini_manager.py import-file <path>
python scripts/gemini_manager.py list-files
python scripts/gemini_manager.py search <query>

# Google Drive integration
python scripts/gemini_manager.py upload <file> [--convert]
python scripts/gemini_manager.py batch-upload [--directory <path>] [--convert]
python scripts/gemini_manager.py list-drive-files

# Maintenance
python scripts/gemini_manager.py cleanup
python scripts/gemini_manager.py export-list [--format csv|json]
```

## 💡 Use Cases

### For Individual Users
- Store and organize Gemini Canvas exports
- Share infographics with colleagues
- Convert presentations to collaborative docs
- Archive important AI-generated content

### For Teams
- Centralized repository of AI-generated materials
- Collaborative editing of Gemini outputs
- Standardized sharing workflows
- Team knowledge base from AI interactions

### For Organizations
- Systematic management of AI-generated content
- Integration with existing Google Workspace workflows
- Bulk processing of AI outputs
- Long-term archival and searchability

## 🛠️ Development

### Project Structure
```
opendemos/
├── gemini_html_manager/     # Core Python package
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── file_manager.py     # Local file operations
│   ├── google_workspace.py # Google APIs integration
│   └── web_interface.py    # Flask web app
├── scripts/
│   └── gemini_manager.py   # CLI interface
├── templates/              # Web interface templates
├── html_exports/           # Local HTML file storage
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
└── config.example.yaml     # Configuration template
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## 🤝 Support

- **Issues**: Report bugs or request features on GitHub Issues
- **Documentation**: Check the `docs/` directory for detailed guides
- **Community**: Share your use cases and tips

## 🔮 Roadmap

- [ ] Support for more file formats (PDF, DOCX)
- [ ] Advanced analytics and reporting
- [ ] Integration with other cloud storage providers
- [ ] Mobile-friendly web interface
- [ ] Automated content analysis and tagging
- [ ] Webhook support for automated workflows

---

**Made for managing Google Gemini exports with ❤️**
