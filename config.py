import os

class Config:
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    TRAINING_SET_ROOT_DIR = os.environ.get('TRAINING_SET_ROOT_DIR', 'training_sets')