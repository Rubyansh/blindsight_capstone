"""
Utility functions for Blind Vision Assistant
"""

import base64
import logging
from pathlib import Path
from werkzeug.utils import secure_filename
import config

# Configure logging
logger = logging.getLogger(__name__)

def image_to_base64(image_path):
    """Convert image to Base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        logger.error(f"Error converting image to base64: {e}")
        raise

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def secure_filename_with_timestamp(filename):
    """Generate secure filename with timestamp"""
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = filename.rsplit('.', 1)
    secure_name = secure_filename(name)
    return f"{secure_name}_{timestamp}.{ext}"

def cleanup_old_files(directory, max_age_hours=24):
    """Clean up files older than specified hours"""
    from datetime import datetime, timedelta
    import os
    
    cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
    
    for file_path in directory.glob('*'):
        if file_path.is_file():
            file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_time < cutoff_time:
                try:
                    file_path.unlink()
                    logger.info(f"Cleaned up old file: {file_path}")
                except Exception as e:
                    logger.error(f"Error cleaning up file {file_path}: {e}")