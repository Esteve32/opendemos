"""
Basic tests for the CLI interface
"""
import subprocess
import sys
import os

def test_cli_help():
    """Test that the CLI help command works"""
    # Get the path to the script
    script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'gemini_manager.py')
    
    # Run the help command
    result = subprocess.run(
        [sys.executable, script_path, '--help'],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(__file__))
    )
    
    # Check that it runs successfully
    assert result.returncode == 0, f"CLI help failed with error: {result.stderr}"
    assert "Gemini HTML Manager" in result.stdout
    assert "Commands:" in result.stdout

def test_cli_version():
    """Test that the CLI version command works"""
    script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'gemini_manager.py')
    
    result = subprocess.run(
        [sys.executable, script_path, '--version'],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(__file__))
    )
    
    # Check that it runs successfully
    assert result.returncode == 0, f"CLI version failed with error: {result.stderr}"
    assert "1.0.0" in result.stdout or "version" in result.stdout.lower()

def test_cli_list_files():
    """Test that the list-files command works"""
    script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'gemini_manager.py')
    
    result = subprocess.run(
        [sys.executable, script_path, 'list-files'],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(__file__))
    )
    
    # Should run successfully (even if no files found)
    assert result.returncode == 0, f"list-files failed with error: {result.stderr}"