import fitz  # PyMuPDF
import requests
import logging
import os
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handle PDF extraction from Google Drive links"""
    
    @staticmethod
    def convert_drive_link(drive_link):
        """
        Convert Google Drive view link to downloadable link
        Example: /view?usp=sharing -> /uc?export=download
        """
        try:
            # Extract file ID from Google Drive URL
            if 'drive.google.com' in drive_link:
                if '/view' in drive_link or '/edit' in drive_link:
                    # Extract file ID from URL
                    if '/d/' in drive_link:
                        file_id = drive_link.split('/d/')[1].split('/')[0]
                        return f"https://drive.google.com/uc?export=download&id={file_id}"
                    elif 'id=' in drive_link:
                        file_id = parse_qs(urlparse(drive_link).query).get('id', [None])[0]
                        if file_id:
                            return f"https://drive.google.com/uc?export=download&id={file_id}"
            return drive_link
        except Exception as e:
            logger.error(f"Error converting drive link: {str(e)}")
            return drive_link

    @staticmethod
    def download_pdf(pdf_url, timeout=30):
        """Download PDF from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(pdf_url, headers=headers, timeout=timeout, stream=True)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error downloading PDF from {pdf_url}: {str(e)}")
            return None

    @staticmethod
    def extract_text_from_pdf(pdf_content):
        """
        Extract text from PDF content using PyMuPDF
        """
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            text = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.get_text()
            doc.close()
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return None

    @staticmethod
    def process_pdf_url(pdf_url):
        """
        Complete workflow: convert link -> download -> extract text
        """
        try:
            # Convert Google Drive link if needed
            download_url = PDFProcessor.convert_drive_link(pdf_url)
            
            # Download PDF
            pdf_content = PDFProcessor.download_pdf(download_url)
            if pdf_content is None:
                return None
            
            # Extract text
            text = PDFProcessor.extract_text_from_pdf(pdf_content)
            return text
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            return None
