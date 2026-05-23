import easyocr
import logging
import requests
from io import BytesIO
from PIL import Image
import cv2
import numpy as np

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Handle image OCR extraction for events and achievements"""
    
    def __init__(self, languages=['en']):
        """Initialize EasyOCR reader"""
        try:
            self.reader = easyocr.Reader(languages)
        except Exception as e:
            logger.error(f"Error initializing OCR reader: {str(e)}")
            self.reader = None

    def download_image(self, image_url, timeout=30):
        """Download image from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(image_url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except Exception as e:
            logger.error(f"Error downloading image from {image_url}: {str(e)}")
            return None

    def preprocess_image(self, image):
        """
        Preprocess image for better OCR results
        - Convert to grayscale
        - Apply contrast enhancement
        - Denoise
        """
        try:
            # Convert PIL Image to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(enhanced)
            
            return denoised
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return None

    def extract_text_from_image(self, image_url):
        """
        Complete workflow: download -> preprocess -> OCR
        """
        try:
            if self.reader is None:
                logger.warning("OCR reader not initialized")
                return None
            
            # Download image
            image = self.download_image(image_url)
            if image is None:
                return None
            
            # Preprocess
            processed_image = self.preprocess_image(image)
            if processed_image is None:
                processed_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Run OCR
            results = self.reader.readtext(processed_image)
            
            # Extract and organize text
            text = "\n".join([detection[1] for detection in results])
            return text if text.strip() else None
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            return None

    def batch_extract_from_images(self, image_urls):
        """Process multiple images and return OCR texts"""
        results = []
        for url in image_urls:
            text = self.extract_text_from_image(url)
            if text:
                results.append({
                    "url": url,
                    "text": text
                })
        return results
