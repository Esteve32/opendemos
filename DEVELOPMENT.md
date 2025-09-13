# Development Setup for Visual Studio Code

This guide helps you set up a development environment for the Gemini HTML Manager project in Visual Studio Code.

## Quick Setup

### 1. Prerequisites
- Python 3.8+ (tested with Python 3.12.3)
- Visual Studio Code
- Git

### 2. Initial Setup
```bash
# Clone the repository (if not already done)
git clone https://github.com/Esteve32/opendemos.git
cd opendemos

# Install Python dependencies
pip3 install -r requirements.txt

# Run setup script (optional - for Google Workspace integration)
./setup.sh
```

### 3. VS Code Setup
The repository includes pre-configured VS Code settings in `.vscode/`:

- **settings.json**: Python development settings, linting, formatting
- **launch.json**: Debug configurations for CLI and web interface
- **tasks.json**: Common development tasks
- **extensions.json**: Recommended extensions

#### Recommended Extensions
Install these VS Code extensions for the best development experience:
- Python (ms-python.python)
- Pylint (ms-python.pylint)
- Black Formatter (ms-python.black-formatter)
- isort (ms-python.isort)
- Flake8 (ms-python.flake8)
- YAML (redhat.vscode-yaml)
- GitHub Copilot (github.copilot)

### 4. Development Workflow

#### Running the Application
- **CLI Interface**: Use F5 with "Gemini Manager CLI" configuration
- **Web Interface**: Use F5 with "Web Interface" configuration
- **Current File**: Use F5 with "Python: Current File" configuration

#### Available Tasks (Ctrl+Shift+P → "Tasks: Run Task")
- Install Dependencies
- Run Setup Script
- Start Web Interface
- Run Tests
- Lint Python Code
- Format Python Code

## Project Structure

```
opendemos/
├── .vscode/                 # VS Code configuration
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
├── config.example.yaml     # Configuration template
└── setup.sh               # Setup script
```

## Development Tips

### 1. Code Quality
- Code formatting is automatically applied on save (Black formatter)
- Linting is enabled (Flake8, Pylint)
- Import sorting is configured (isort with Black profile)

### 2. Debugging
- Set breakpoints in Python code and use the debug configurations
- Use the integrated terminal for command-line testing
- Web interface debugging available on port 5000

### 3. Testing
- Tests can be run via the "Run Tests" task
- Debug tests using the "Python: Debug Tests" configuration

### 4. Configuration
- Copy `config.example.yaml` to `config.yaml` for local configuration
- Sensitive files (credentials.json, config.yaml) are in .gitignore

## Restructuring Guidelines

When restructuring this repository:

1. **Maintain Module Structure**: Keep the core functionality in `gemini_html_manager/`
2. **Preserve CLI Interface**: The `scripts/gemini_manager.py` provides the main user interface
3. **Keep Configuration Flexible**: The YAML configuration system allows easy customization
4. **Maintain Google Integration**: The Google Workspace integration is a key feature
5. **Preserve Web Interface**: The Flask web app provides user-friendly access

## Common Commands

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run CLI help
python3 scripts/gemini_manager.py --help

# Start web interface
python3 scripts/gemini_manager.py web

# Import a file
python3 scripts/gemini_manager.py import-file path/to/file.html

# List files
python3 scripts/gemini_manager.py list-files

# Test Google integration (requires credentials.json)
python3 scripts/gemini_manager.py setup
```

## Troubleshooting

### Python Path Issues
The project uses relative imports. Make sure to run commands from the project root directory.

### Google Workspace Setup
For Google Drive/Docs integration:
1. Set up Google Cloud Console project
2. Enable Drive and Docs APIs
3. Download credentials.json
4. Run setup command

### Dependencies
If you encounter import errors, ensure all dependencies are installed:
```bash
pip3 install -r requirements.txt
```

## Next Steps for Restructuring

Consider these areas for improvement:
1. **Testing**: Add comprehensive unit tests
2. **Documentation**: Expand API documentation
3. **Packaging**: Consider making it pip-installable
4. **Configuration**: Add environment variable support
5. **Error Handling**: Improve error messages and logging
6. **Performance**: Add file caching and batch operations optimization