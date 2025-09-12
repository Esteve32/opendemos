#!/usr/bin/env python3
"""
Simple server launcher for OpenDemos
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini_html_manager.web_interface import app

if __name__ == '__main__':
    print("🚀 Starting OpenDemos Server...")
    print("📍 Public demo gallery: http://localhost:5000/")
    print("🛠️  Gemini HTML Manager: http://localhost:5000/gemini-manager")
    print("📁 Static files served from: html_exports/ and projects/")
    print("\n👆 Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=5000, debug=False)