"""
Web interface for Gemini HTML Manager
"""
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, send_from_directory
import os
import sys
from datetime import datetime

# Add the parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_html_manager.file_manager import HTMLFileManager
from gemini_html_manager.google_workspace import GoogleWorkspaceManager
from gemini_html_manager.config import config

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Initialize managers
file_manager = HTMLFileManager()
workspace_manager = GoogleWorkspaceManager()


@app.route('/')
def public_index():
    """Serve the public landing page"""
    # Check if we have the new GitHub Pages index.html or fall back to Flask landing
    try:
        # Try to serve the new GitHub Pages compatible index
        return send_from_directory(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
    except:
        # Fallback to Flask-based landing page if the new index doesn't exist
        return send_from_directory(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index-flask-landing.html')

@app.route('/flask-landing')
def flask_landing():
    """Serve the original Flask landing page for comparison"""
    return send_from_directory(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index-flask-landing.html')

@app.route('/gemini-manager')
@app.route('/gemini-manager/')
def index():
    """Main dashboard"""
    files = file_manager.list_html_files()
    organized_files = file_manager.organize_files_by_date()
    
    stats = {
        'total_files': len(files),
        'total_size_mb': sum(f.get('size_mb', 0) for f in files),
        'gemini_canvas_files': sum(1 for f in files if f.get('is_gemini_canvas', False)),
        'files_with_images': sum(1 for f in files if f.get('has_images', False))
    }
    
    return render_template('dashboard.html', 
                         files=files[:10],  # Show latest 10 files
                         organized_files=organized_files,
                         stats=stats)


@app.route('/gemini-manager/files')
def list_files():
    """List all files"""
    search_query = request.args.get('search', '')
    
    if search_query:
        files = file_manager.search_files(search_query)
    else:
        files = file_manager.list_html_files()
    
    return render_template('files.html', files=files, search_query=search_query)


@app.route('/gemini-manager/file/<path:filename>')
def view_file(filename):
    """View HTML file"""
    file_path = os.path.join(file_manager.export_directory, filename)
    
    if not os.path.exists(file_path):
        flash(f'File not found: {filename}', 'error')
        return redirect(url_for('list_files'))
    
    # Get file metadata
    metadata = file_manager.get_file_metadata(file_path)
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        flash(f'Error reading file: {e}', 'error')
        return redirect(url_for('list_files'))
    
    return render_template('view_file.html', 
                         filename=filename,
                         metadata=metadata,
                         content=content)


@app.route('/gemini-manager/upload', methods=['GET', 'POST'])
def upload_file():
    """Upload file to local storage"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file:
            try:
                # Save temporary file
                temp_path = os.path.join('/tmp', file.filename)
                file.save(temp_path)
                
                # Import to manager
                new_name = request.form.get('new_name')
                result = file_manager.import_html_file(temp_path, new_name)
                
                # Clean up temp file
                os.remove(temp_path)
                
                if result:
                    flash(f'Successfully uploaded: {os.path.basename(result)}', 'success')
                else:
                    flash('Failed to upload file', 'error')
                    
            except Exception as e:
                flash(f'Error uploading file: {e}', 'error')
    
    return render_template('upload.html')


@app.route('/gemini-manager/google_drive')
def google_drive():
    """Google Drive integration page"""
    if not workspace_manager.credentials:
        flash('Google Workspace not configured. Please run setup first.', 'warning')
        return render_template('google_drive.html', files=[], authenticated=False)
    
    try:
        drive_files = workspace_manager.list_gemini_files()
        return render_template('google_drive.html', files=drive_files, authenticated=True)
    except Exception as e:
        flash(f'Error accessing Google Drive: {e}', 'error')
        return render_template('google_drive.html', files=[], authenticated=False)


@app.route('/api/upload_to_drive', methods=['POST'])
def api_upload_to_drive():
    """API endpoint to upload file to Google Drive"""
    data = request.json
    file_path = data.get('file_path')
    convert = data.get('convert', False)
    title = data.get('title')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 400
    
    if not workspace_manager.credentials:
        return jsonify({'error': 'Google Workspace not configured'}), 400
    
    try:
        if convert:
            file_id = workspace_manager.convert_html_to_google_doc(file_path, title)
            file_type = 'Google Doc'
        else:
            file_id = workspace_manager.upload_html_file(file_path, title)
            file_type = 'HTML file'
        
        if file_id:
            file_info = workspace_manager.get_file_info(file_id)
            return jsonify({
                'success': True,
                'file_id': file_id,
                'file_type': file_type,
                'name': file_info.get('name') if file_info else title,
                'link': file_info.get('webViewLink') if file_info else None
            })
        else:
            return jsonify({'error': 'Upload failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch_upload_to_drive', methods=['POST'])
def api_batch_upload_to_drive():
    """API endpoint for batch upload to Google Drive"""
    data = request.json
    convert = data.get('convert', False)
    
    if not workspace_manager.credentials:
        return jsonify({'error': 'Google Workspace not configured'}), 400
    
    try:
        files = file_manager.list_html_files()
        results = []
        
        for file_info in files:
            try:
                file_path = file_info['path']
                filename = file_info['filename']
                
                if convert:
                    file_id = workspace_manager.convert_html_to_google_doc(file_path)
                    file_type = 'Google Doc'
                else:
                    file_id = workspace_manager.upload_html_file(file_path)
                    file_type = 'HTML file'
                
                if file_id:
                    results.append({
                        'filename': filename,
                        'success': True,
                        'file_id': file_id,
                        'file_type': file_type
                    })
                else:
                    results.append({
                        'filename': filename,
                        'success': False,
                        'error': 'Upload failed'
                    })
                    
            except Exception as e:
                results.append({
                    'filename': file_info.get('filename', 'unknown'),
                    'success': False,
                    'error': str(e)
                })
        
        successful_uploads = sum(1 for r in results if r['success'])
        
        return jsonify({
            'total_files': len(files),
            'successful_uploads': successful_uploads,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['GET'])
def api_search():
    """API endpoint for searching files"""
    query = request.args.get('q', '')
    
    if not query:
        files = file_manager.list_html_files()
    else:
        files = file_manager.search_files(query)
    
    return jsonify({'files': files})


@app.route('/api/file_metadata/<path:filename>')
def api_file_metadata(filename):
    """API endpoint to get file metadata"""
    file_path = os.path.join(file_manager.export_directory, filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    metadata = file_manager.get_file_metadata(file_path)
    return jsonify(metadata)


@app.route('/api/cleanup_duplicates', methods=['POST'])
def api_cleanup_duplicates():
    """API endpoint to cleanup duplicate files"""
    try:
        duplicates = file_manager.cleanup_duplicates()
        return jsonify({
            'removed_files': duplicates,
            'count': len(duplicates)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/gemini-manager/download/<path:filename>')
def download_file(filename):
    """Download HTML file"""
    file_path = os.path.join(file_manager.export_directory, filename)
    
    if not os.path.exists(file_path):
        flash(f'File not found: {filename}', 'error')
        return redirect(url_for('list_files'))
    
    return send_file(file_path, as_attachment=True)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                         error_code=500,
                         error_message="Internal server error"), 500


@app.route('/html_exports/<path:filename>')
def serve_html_exports(filename):
    """Serve HTML export files"""
    return send_from_directory(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'html_exports'), filename)

@app.route('/projects/<path:filename>')
def serve_projects(filename):
    """Serve project files"""
    return send_from_directory(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'projects'), filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve static assets for GitHub Pages index"""
    return send_from_directory(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets'), filename)

@app.route('/demos/<path:filename>')
def serve_demos(filename):
    """Serve demo files"""
    return send_from_directory(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'demos'), filename)

@app.route('/demos.json')
def serve_demos_manifest():
    """Serve demos manifest for GitHub Pages index"""
    return send_from_directory(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'demos.json')

if __name__ == '__main__':
    host = config.get('web_interface.host', 'localhost')
    port = config.get('web_interface.port', 5000)
    debug = config.get('web_interface.debug', False)
    
    app.run(host=host, port=port, debug=debug)