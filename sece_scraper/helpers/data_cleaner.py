import re
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class DataCleaner:
    """Clean and prepare data for AI training"""
    
    BOILERPLATE_PATTERNS = [
        r'admission\s+open',
        r'apply\s+now',
        r'skip\s+to\s+content',
        r'follow\s+us\s+on',
        r'quick\s+links',
        r'recent\s+posts',
        r'categories',
        r'archives',
        r'search\s+the\s+site',
        r'privacy\s+policy',
        r'terms\s+of\s+service',
        r'cookie\s+policy',
        r'contact\s+us',
        r'phone:\s*\+?\d+',
        r'email:\s*[\w\.-]+@[\w\.-]+',
        r'©\s+\d{4}',
    ]
    
    @staticmethod
    def remove_boilerplate(text):
        """Remove common boilerplate text"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip if line matches boilerplate patterns
            if not any(re.search(pattern, line, re.IGNORECASE) 
                      for pattern in DataCleaner.BOILERPLATE_PATTERNS):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    @staticmethod
    def normalize_whitespace(text):
        """Normalize whitespace and remove excessive blank lines"""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Replace multiple newlines with double newline
        text = re.sub(r'\n\n+', '\n\n', text)
        return text.strip()
    
    @staticmethod
    def remove_urls(text):
        """Remove URLs from text"""
        return re.sub(r'https?://\S+|www\.\S+', '', text)
    
    @staticmethod
    def clean_text(text):
        """Apply all cleaning steps"""
        if not text:
            return None
        
        text = DataCleaner.remove_boilerplate(text)
        text = DataCleaner.remove_urls(text)
        text = DataCleaner.normalize_whitespace(text)
        
        # Ensure minimum length
        if len(text) < 50:
            return None
        
        return text
    
    @staticmethod
    def deduplicate(items, key='data'):
        """
        Remove duplicate items based on content hash
        items: list of dictionaries
        key: field to use for deduplication
        """
        seen = set()
        unique_items = []
        
        for item in items:
            content_hash = hash(item.get(key, ''))
            if content_hash not in seen:
                seen.add(content_hash)
                unique_items.append(item)
        
        return unique_items
    
    @staticmethod
    def tag_data(item_type, text, metadata=None):
        """
        Create contextual tags for AI training
        Returns instruction-context pairs
        """
        instruction_map = {
            'syllabus': f"What is included in the {metadata.get('year', 'CSE')} syllabus?",
            'event': "What are the recent CSE department events?",
            'achievement': "List recent CSE student achievements.",
            'curriculum': "What is the CSE curriculum?",
            'faculty': f"Who is {metadata.get('name', 'the faculty member')} and what is their expertise?",
            'hod': "Who is the Head of the CSE Department and what is their background?",
            'recruiter': f"Which companies recruit from the CSE department?",
            'testimonial': "What do alumni say about their experience at SECE CSE?",
            'placement_stat': "What are the placement statistics for the CSE department?",
        }
        
        instruction = instruction_map.get(item_type, "Provide information about the CSE department.")
        
        return {
            "instruction": instruction,
            "context": text,
            "type": item_type,
            "metadata": metadata or {}
        }
    
    @staticmethod
    def prepare_for_training(raw_items):
        """
        Complete data preparation pipeline
        """
        processed_items = []
        
        for item in raw_items:
            # Clean text
            cleaned_text = DataCleaner.clean_text(item.get('data', ''))
            if not cleaned_text:
                continue
            
            # Create training pair
            training_item = DataCleaner.tag_data(
                item_type=item.get('type', 'other'),
                text=cleaned_text,
                metadata=item.get('metadata', {})
            )
            
            processed_items.append(training_item)
        
        # Deduplicate
        unique_items = DataCleaner.deduplicate(processed_items)
        
        return unique_items
