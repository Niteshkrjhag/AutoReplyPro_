import json
import os
from pathlib import Path
import logging

class ConfigManager:
    """Manages application configuration and settings persistence"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.default_config = {
            'api_key': '',
            'persona_name': 'Nitesh',
            'language_mix': 'Hindi-English',
            'tone': 'warm',
            'max_length': 20,
            'temperature': 0.8,
            'platform': 'WhatsApp',
            'check_interval': 5,
            'show_debug': False
        }
    
    def load_config(self):
        """Load configuration from file, or create default if not exists"""
        try:
            if self.config_file.exists() and os.path.getsize(self.config_file) > 0:
                with open(self.config_file, 'r') as f:
                    try:
                        config = json.load(f)
                        logging.info(f"Configuration loaded from {self.config_file}")
                        return config
                    except json.JSONDecodeError:
                        logging.warning(f"Invalid JSON in config file, using defaults")
                        return self.default_config.copy()
            else:
                logging.info("No configuration file found, using defaults")
                return self.default_config.copy()
        except Exception as e:
            logging.error(f"Error loading configuration: {str(e)}")
            return self.default_config.copy()
    
    
    def save_config(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            logging.info(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            logging.error(f"Error saving configuration: {str(e)}")
            return False
    
    def get_value(self, key, default=None):
        """Get a specific configuration value"""
        config = self.load_config()
        return config.get(key, default)
    
    def set_value(self, key, value):
        """Set a specific configuration value"""
        config = self.load_config()
        config[key] = value
        return self.save_config(config)