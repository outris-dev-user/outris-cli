"""
Configuration management for Outris CLI
Stores API key, org info in ~/.outris/config.json
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

CONFIG_DIR = Path.home() / ".outris"
CONFIG_FILE = CONFIG_DIR / "config.json"

def ensure_config_dir():
    """Create ~/.outris directory if it doesn't exist"""
    CONFIG_DIR.mkdir(exist_ok=True)

def load_config() -> Dict[str, Any]:
    """Load configuration from ~/.outris/config.json"""
    if not CONFIG_FILE.exists():
        return {}
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config: Dict[str, Any]):
    """Save configuration to ~/.outris/config.json"""
    ensure_config_dir()
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_api_key() -> Optional[str]:
    """Get stored API key"""
    config = load_config()
    return config.get("api_key")

def get_org_id() -> Optional[str]:
    """Get stored org ID"""
    config = load_config()
    return config.get("org_id")

def clear_config():
    """Clear stored configuration (logout)"""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
