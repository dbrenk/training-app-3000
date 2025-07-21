import logging.config
import os
import yaml

def setup_logging(config_path='logging.yaml'):
    # Ensure log directory exists
    os.makedirs('logs', exist_ok=True)

    # Load YAML logging config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Allow dynamic log level override from environment
    env_log_level = os.getenv("LOG_LEVEL", "INFO").upper() # Default to INFO if env var is not set
    if env_log_level:
        config['root']['level'] = env_log_level.upper()

    logging.config.dictConfig(config)