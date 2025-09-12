"""
Configuration management for Gemini HTML Manager
"""
import os
import yaml
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self._config = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from YAML file"""
        # Try to load user config first, fallback to example config
        config_files = [self.config_path, "config.example.yaml"]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        self._config = yaml.safe_load(f) or {}
                    print(f"Loaded configuration from {config_file}")
                    return
                except Exception as e:
                    print(f"Error loading config from {config_file}: {e}")
        
        # If no config file found, use defaults
        self._config = self.get_default_config()
        print("Using default configuration")
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "google": {
                "scopes": [
                    "https://www.googleapis.com/auth/documents",
                    "https://www.googleapis.com/auth/drive",
                    "https://www.googleapis.com/auth/drive.file"
                ],
                "credentials_file": "credentials.json",
                "token_file": "token.json"
            },
            "html_manager": {
                "export_directory": "html_exports",
                "max_file_size": 10,
                "supported_extensions": [".html", ".htm"],
                "default_sharing": {
                    "type": "anyone",
                    "role": "reader"
                }
            },
            "web_interface": {
                "host": "localhost",
                "port": 5000,
                "debug": False
            },
            "conversion": {
                "preserve_formatting": True,
                "convert_images": True,
                "max_doc_size": 1000000
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config_ref = self._config
        
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
        
        config_ref[keys[-1]] = value
    
    def save_config(self) -> None:
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, default_flow_style=False, indent=2)
            print(f"Configuration saved to {self.config_path}")
        except Exception as e:
            print(f"Error saving configuration: {e}")


# Global configuration instance
config = Config()