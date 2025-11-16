"""
Configuration settings for Blind Vision Assistant
CBSE AI Capstone Project 2025
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Model settings
MODEL_NAME = os.getenv('OLLAMA_MODEL', 'llava')
MODEL_TEMPERATURE = float(os.getenv('MODEL_TEMPERATURE', '0.1'))

# TTS settings
DEFAULT_VOICE = os.getenv('TTS_VOICE', 'en-US-GuyNeural')
FALLBACK_VOICE = os.getenv('FALLBACK_VOICE', 'en-US-JennyNeural')
SPEECH_RATE = os.getenv('SPEECH_RATE', '+25%')

# Web settings
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
AUDIO_FOLDER = BASE_DIR / 'audio'

# System prompt
SYSTEM_PROMPT = """You are a visual assistant for blind users. Describe only:
- Clearly visible objects and text
- Colors and basic shapes
- People's appearance (clothing, hair)
- Spatial relationships
No speculation, emotions, or metaphors. 2-3 phrases under 60 words."""

# Create necessary directories
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)