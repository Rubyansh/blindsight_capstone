"""
CLI version of Blind Vision Assistant
CBSE AI Capstone Project 2025
"""

import argparse
import asyncio
import sys
from pathlib import Path
import logging

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))

from src.vision_ai import get_image_description
from src.tts_engine import generate_speech
from src.utils import cleanup_old_files
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def process_image(image_path, model_name, voice, rate, cleanup=False):
    """
    Process image and generate audio description
    
    Args:
        image_path (str): Path to image file
        model_name (str): Ollama model to use
        voice (str): TTS voice
        rate (str): Speech rate
        cleanup (bool): Whether to cleanup old files
    """
    try:
        # Validate image path
        image_path = Path(image_path)
        if not image_path.exists():
            logger.error(f"Image file not found: {image_path}")
            return False
        
        logger.info(f"Processing image: {image_path}")
        
        # Generate image description
        logger.info("Generating image description...")
        description = get_image_description(str(image_path))
        
        if not description:
            logger.error("Failed to generate description")
            return False
        
        print(f"\n📝 Description: {description}\n")
        
        # Generate TTS
        logger.info("Generating speech...")
        audio_file = await generate_speech(description, voice, rate)
        
        if audio_file:
            print(f"🎵 Audio saved to: {audio_file}")
            
            # Optional: Play audio automatically
            play_audio = input("Play audio now? (y/n): ").lower().strip()
            if play_audio == 'y':
                await play_audio_file(audio_file)
        else:
            logger.error("Failed to generate audio")
            return False
        
        # Cleanup old files if requested
        if cleanup:
            logger.info("Cleaning up old files...")
            cleanup_old_files(config.AUDIO_FOLDER, max_age_hours=24)
            cleanup_old_files(config.UPLOAD_FOLDER, max_age_hours=24)
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return False

async def play_audio_file(audio_path):
    """Play audio file using system player"""
    import platform
    import subprocess
    
    system = platform.system()
    
    try:
        if system == "Windows":
            subprocess.run(["start", audio_path], shell=True, check=True)
        elif system == "Darwin":  # macOS
            subprocess.run(["afplay", audio_path], check=True)
        else:  # Linux
            # Try different players
            players = ['mpv', 'mplayer', 'aplay']
            for player in players:
                try:
                    subprocess.run([player, audio_path], check=True)
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            else:
                print("No suitable audio player found. Please play the file manually.")
    except Exception as e:
        logger.error(f"Error playing audio: {e}")
        print(f"Audio file saved at: {audio_path}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='Blind Vision Assistant - CLI Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python src/app.py image.jpg
  python src/app.py photo.png --voice en-US-JennyNeural --rate +15%
  python src/app.py picture.jpg --model llava --cleanup
        """
    )
    
    parser.add_argument('image_path', help='Path to the image file')
    parser.add_argument('--model', default=config.MODEL_NAME, 
                       help=f'Ollama model to use (default: {config.MODEL_NAME})')
    parser.add_argument('--voice', default=config.DEFAULT_VOICE,
                       help=f'TTS voice to use (default: {config.DEFAULT_VOICE})')
    parser.add_argument('--rate', default=config.SPEECH_RATE,
                       help=f'Speech rate (default: {config.SPEECH_RATE})')
    parser.add_argument('--cleanup', action='store_true',
                       help='Clean up old audio and upload files')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run the main processing
    success = asyncio.run(process_image(
        args.image_path,
        args.model,
        args.voice,
        args.rate,
        args.cleanup
    ))
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()