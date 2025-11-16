"""
Vision AI module for image analysis using Ollama
"""

import ollama
import logging
from src.utils import image_to_base64
import config

logger = logging.getLogger(__name__)

class VisionAI:
    def __init__(self, model_name=config.MODEL_NAME, temperature=config.MODEL_TEMPERATURE):
        self.model_name = model_name
        self.temperature = temperature
        self.system_prompt = config.SYSTEM_PROMPT
        
    def analyze_image(self, image_path):
        """
        Analyze image and generate description
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: Generated description
        """
        try:
            # Convert image to base64
            image_base64 = image_to_base64(image_path)
            
            # Generate description using Ollama
            response = ollama.chat(
                model=self.model_name,
                options={"temperature": self.temperature},
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", 
                     "content": "List objective observations about this image.",
                     "images": [image_base64]}
                ]
            )
            
            description = response["message"]["content"].strip()
            
            if not description:
                logger.warning("Empty description returned from model")
                return "Unable to generate description for this image."
            
            logger.info("Successfully generated image description")
            return description
            
        except Exception as e:
            logger.error(f"Error in vision AI analysis: {e}")
            raise

def get_image_description(image_path):
    """Convenience function to get image description"""
    vision_ai = VisionAI()
    return vision_ai.analyze_image(image_path)