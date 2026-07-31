# OpenDemos — ArboraOS Experimentation Playground

A public experimentation playground for **ArboraOS** concepts, interactive browser demos, and tooling workflows.

This repository combines:
- a visual demo gallery,
- AI-assisted HTML project experiments,
- and the **Gemini HTML Manager** for importing, organizing, and publishing HTML artifacts.

---

## 🌟 What this repo is for

OpenDemos is the sandbox where ArboraOS ideas are tested quickly and shared visibly.

### Core goals
- Prototype ArboraOS UI/UX and interaction patterns in the browser
- Experiment with AI-generated HTML content and workflows
- Keep demos reproducible, lightweight, and easy to run
- Provide practical tooling for export, search, organization, and publishing

---

## 🧩 Features

- **🎨 Public Demo Gallery**: Landing page for visual mockups and interactive demos
- **🖥️ ArboraOS-Oriented Experiments**: Browser-first sandbox for OS-like interfaces and component ideas
- **📁 Gemini HTML Manager**: Manage HTML exports from Google Gemini
- **☁️ Google Drive Integration**: Upload HTML files with sharing controls
- **📄 Google Docs Conversion**: Convert HTML to collaborative Google Docs
- **🔍 Advanced Search**: Search by filename, title, or content
- **🌐 Modern Web Interface**: Responsive Bootstrap-based UI
- **⚡ CLI Tools**: Automation and batch workflows
- **🔄 Batch Operations**: Multi-file upload and duplicate cleanup
- **📊 Metadata/Analytics**: File metadata and date-based organization

---

## 🚀 Quick Start

### 1) Installation

```bash
git clone https://github.com/Esteve32/opendemos.git
cd opendemos
pip install -r requirements.txt
```

### 2) Start the playground

**Simple launch:**
```bash
python start_server.py
```

**Or via CLI:**
```bash
python scripts/gemini_manager.py web
```

### 3) Open in browser

- **🏠 Demo Gallery**: http://localhost:5000/
- **🛠️ Gemini HTML Manager**: http://localhost:5000/gemini-manager
- **📁 File Browser**: http://localhost:5000/gemini-manager/files

---

## 🧪 ArboraOS Experimentation Workflow

A recommended loop for this repo:

1. **Prototype** UI concepts in HTML demos (`projects/`, `html_exports/`, or dedicated demo files)
2. **Review** visually in the local gallery
3. **Refine** content and structure with CLI/web tooling
4. **Publish/Share** via Google Drive or convert to Docs for collaboration
5. **Iterate** quickly with small, isolated updates

---

## 📋 Demo Gallery

### Live interactive demos
- **🛠️ Gemini HTML Manager**: Web app for AI-generated HTML management + Google Workspace integration
- **📊 Data Visualization Canvas**: Interactive infographic demo
- **📈 Marketing Strategy Presentation**: AI-assisted presentation demo
- **💻 Colibri OS Dashboard**: OS-style interactive dashboard mockup (useful reference for ArboraOS UI exploration)

### Static mockups and visual content
- `html_exports/` — AI-generated exports from Google Gemini Canvas
- `projects/` — custom dashboard mockups and UI designs

---

## 📖 Usage Guide

### Manage HTML files

**Import**
- Web: Upload page (drag/drop or picker)
- CLI:
```bash
python scripts/gemini_manager.py import-file <path> --name "new-name"
```

**Organize**
- Date-based organization
- Search by metadata/content
- Metadata extraction (title, word count, images, etc.)

---

## ☁️ Google Workspace Integration (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select a project
3. Enable **Google Drive API** and **Google Docs API**
4. Create **OAuth 2.0 Client ID** (Desktop app)
5. Save credentials as `credentials.json` in project root

### Upload to Google Drive
- Uploads to **Gemini HTML Exports** folder
- Supports sharing links
- Preserves source formatting where possible

### Convert to Google Docs
- Converts HTML into editable Docs
- Keeps structure/formatting as much as possible
- Enables collaborative editing/comments

---

## 🔄 Batch operations

```bash
# Upload all files in default export directory
python scripts/gemini_manager.py batch-upload

# Upload from specific directory
python scripts/gemini_manager.py batch-upload --directory /path/to/html/files

# Convert batch to Google Docs
python scripts/gemini_manager.py batch-upload --convert

# Cleanup duplicates
python scripts/gemini_manager.py cleanup

# Export inventory list
python scripts/gemini_manager.py export-list --format csv
```

---

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

---

## 📖 API Reference

### REST endpoints
- `GET /api/search?q=query` — Search files
- `POST /api/upload_to_drive` — Upload a file to Drive
- `POST /api/batch_upload_to_drive` — Batch upload
- `GET /api/file_metadata/<filename>` — Read metadata
- `POST /api/cleanup_duplicates` — Remove duplicates

### CLI commands
```bash
# File management
python scripts/gemini_manager.py import-file <path>
python scripts/gemini_manager.py list-files
python scripts/gemini_manager.py search <query>

# Drive integration
python scripts/gemini_manager.py upload <file> [--convert]
python scripts/gemini_manager.py batch-upload [--directory <path>] [--convert]
python scripts/gemini_manager.py list-drive-files

# Maintenance
python scripts/gemini_manager.py cleanup
python scripts/gemini_manager.py export-list [--format csv|json]
```

---

## 🛠️ Development

### Project structure
```text
opendemos/
├── gemini_html_manager/     # Core Python package
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── file_manager.py      # Local file operations
│   ├── google_workspace.py  # Google APIs integration
│   └── web_interface.py     # Flask web app
├── scripts/
│   └── gemini_manager.py    # CLI interface
├── templates/               # Web interface templates
├── html_exports/            # Local HTML file storage
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
└── config.example.yaml      # Configuration template
```

### Contribution
1. Fork the repository
2. Create a feature branch
3. Make focused changes
4. Add tests where applicable
5. Open a pull request

---

## ✅ Experimentation Principles

- Keep experiments small and isolated
- Prefer readable HTML/CSS/JS + minimal Python helpers
- Document how to run each demo quickly
- Avoid heavy dependencies unless necessary
- Never commit secrets or credentials

---

## 🔮 Roadmap

- [ ] More ArboraOS UI/interaction experiment packs
- [ ] Additional file format support (PDF, DOCX)
- [ ] Enhanced analytics and tagging
- [ ] More cloud storage integrations
- [ ] Mobile-first gallery refinements
- [ ] Optional automation/webhooks for experiment workflows

---

## 📄 License

This project is open source. Add or update the specific license file (e.g., MIT) as needed.

---

**Built as an experimentation playground for ArboraOS + AI HTML workflows.**
