"""
Configuration Management for MareArts ANPR Server
"""
import os
import yaml
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
DATABASE_PATH = BASE_DIR / "anpr_history.db"

# Create directories
UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Load server config from YAML file (optional)
def load_server_config():
    """Load server configuration from server_config.yaml"""
    config_file = BASE_DIR / "server_config.yaml"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load server_config.yaml: {e}")
            return {}
    return {}

yaml_config = load_server_config()

# Server settings (from env vars or YAML)
HOST = os.getenv("ANPR_HOST", yaml_config.get('server', {}).get('host', "0.0.0.0"))
PORT = int(os.getenv("ANPR_PORT", yaml_config.get('server', {}).get('port', 8000)))

# Load MareArts credentials from environment or config file
def load_marearts_credentials():
    """Load credentials from environment variables or ~/.marearts/.marearts_env file"""
    # Try environment variables first
    username = os.getenv("MAREARTS_ANPR_USERNAME")
    serial_key = os.getenv("MAREARTS_ANPR_SERIAL_KEY")
    signature = os.getenv("MAREARTS_ANPR_SIGNATURE")
    
    # If not found, try loading from config file (like ma-anpr does)
    if not all([username, serial_key, signature]):
        config_file = Path.home() / ".marearts" / ".marearts_env"
        if config_file.exists():
            print(f"Loading credentials from {config_file}")
            with open(config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('export '):
                        line = line[7:]  # Remove 'export '
                    
                    if '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        value = value.strip().strip('"').strip("'")
                        
                        if key == 'MAREARTS_ANPR_USERNAME':
                            username = value
                        elif key == 'MAREARTS_ANPR_SERIAL_KEY':
                            serial_key = value
                        elif key == 'MAREARTS_ANPR_SIGNATURE':
                            signature = value
    
    return username, serial_key, signature

# MareArts ANPR Credentials
MAREARTS_USERNAME, MAREARTS_SERIAL_KEY, MAREARTS_SIGNATURE = load_marearts_credentials()

# Model settings (from env vars or YAML, env vars take priority)
models_config = yaml_config.get('models', {})
DETECTOR_MODEL = os.getenv("ANPR_DETECTOR", models_config.get('detector', "micro_320p_fp32"))
OCR_MODEL = os.getenv("ANPR_OCR", models_config.get('ocr', "small_fp32"))
REGION = os.getenv("ANPR_REGION", models_config.get('region', "eup"))
BACKEND = os.getenv("ANPR_BACKEND", models_config.get('backend', "cpu"))
CONFIDENCE_THRESHOLD = float(os.getenv("ANPR_CONFIDENCE", models_config.get('confidence', 0.25)))

# Storage settings (from env vars or YAML, env vars take priority)
storage_config = yaml_config.get('storage', {})
MAX_HISTORY_ENTRIES = int(os.getenv("ANPR_MAX_HISTORY", storage_config.get('max_history', 1000)))
SAVE_IMAGES = os.getenv("ANPR_SAVE_IMAGES", str(storage_config.get('save_images', True))).lower() == "true"
MAX_LOG_ENTRIES = int(os.getenv("ANPR_MAX_LOGS", storage_config.get('max_logs', 500)))

def validate_credentials():
    """Validate that credentials are configured"""
    if not all([MAREARTS_USERNAME, MAREARTS_SERIAL_KEY, MAREARTS_SIGNATURE]):
        return False
    return True

