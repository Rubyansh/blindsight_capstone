"""
Text-to-Speech engine using Edge TTS
"""

import edge_tts
import asyncio
import logging
from datetime import datetime
from pathlib import Path
import config

logger = logging.getLogger(__name__)

class TTSEngine:
    def __init__(self, voice=config.DEFAULT_VOICE, rate=config.SPEECH_RATE):
        self.voice = voice
        self.rate = rate
        self.audio_folder = config.AUDIO_FOLDER
        
    async def text_to_speech(self, text, voice=None, rate=None):
        """
        Convert text to speech and save as audio file
        
        Args:
            text (str): Text to convert to speech
            voice (str): Voice to use (optional)
            rate (str): Speech rate (optional)
            
        Returns:
            str: Path to generated audio file
        """
        if voice is None:
            voice = self.voice
        if rate is None:
            rate = self.rate
            
        try:
            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.audio_folder / f"description_{timestamp}.mp3"
            
            # Generate and save audio
            communicate = edge_tts.Communicate(text, voice, rate=rate)
            await communicate.save(str(output_file))
            
            if output_file.exists():
                logger.info(f"Audio successfully saved to: {output_file}")
                return str(output_file)
            else:
                logger.error(f"Failed to save audio to: {output_file}")
                return None
                
        except Exception as e:
            logger.error(f"Error in TTS generation: {e}")
            # Try fallback voice
            return await self._fallback_tts(text, rate)
    
    async def _fallback_tts(self, text, rate):
        """Fallback TTS with different voice"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.audio_folder / f"description_{timestamp}_fallback.mp3"
            
            communicate = edge_tts.Communicate(text, config.FALLBACK_VOICE, rate=rate)
            await communicate.save(str(output_file))
            
            if output_file.exists():
                logger.info(f"Fallback audio saved to: {output_file}")
                return str(output_file)
            else:
                logger.error(f"Failed to save fallback audio to: {output_file}")
                return None
                
        except Exception as e:
            logger.error(f"Fallback TTS also failed: {e}")
            return None

async def generate_speech(text, voice=config.DEFAULT_VOICE, rate=config.SPEECH_RATE):
    """Convenience function to generate speech"""
    tts_engine = TTSEngine(voice, rate)
    return await tts_engine.text_to_speech(text)