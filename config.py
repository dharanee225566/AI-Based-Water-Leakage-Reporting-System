import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'aquawatch-ai-secret-key-2026-immersion-project')
    DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'water_leakage.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    SAMPLE_IMAGES_FOLDER = os.path.join(BASE_DIR, 'static', 'images', 'sample_leaks')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Default map center (Metropolitan center)
    DEFAULT_MAP_LAT = 12.9716
    DEFAULT_MAP_LNG = 77.5946
    DEFAULT_MAP_COORDS = (DEFAULT_MAP_LAT, DEFAULT_MAP_LNG)
    DEFAULT_MAP_ZOOM = 13
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = True
