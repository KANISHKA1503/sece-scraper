import json
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class JSONLStorage:
    """Handle JSONL file operations"""
    
    @staticmethod
    def append_to_jsonl(file_path, data_dict):
        """Append a single dictionary as JSON line"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            
            with open(file_path, 'a', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False)
                f.write('\n')
            
            return True
        except Exception as e:
            logger.error(f"Error appending to JSONL file: {str(e)}")
            return False
    
    @staticmethod
    def read_jsonl(file_path):
        """Read all items from JSONL file"""
        items = []
        try:
            if not os.path.exists(file_path):
                return items
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        items.append(json.loads(line))
        except Exception as e:
            logger.error(f"Error reading JSONL file: {str(e)}")
        
        return items
    
    @staticmethod
    def write_jsonl(file_path, items):
        """Write multiple items to JSONL file (overwrite)"""
        try:
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                for item in items:
                    json.dump(item, f, ensure_ascii=False)
                    f.write('\n')
            
            return True
        except Exception as e:
            logger.error(f"Error writing JSONL file: {str(e)}")
            return False
    
    @staticmethod
    def get_file_stats(file_path):
        """Get statistics about the JSONL file"""
        if not os.path.exists(file_path):
            return {
                'exists': False,
                'size': 0,
                'lines': 0,
                'last_modified': None
            }
        
        try:
            size = os.path.getsize(file_path)
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
            
            return {
                'exists': True,
                'size': size,
                'lines': lines,
                'last_modified': mtime.isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting file stats: {str(e)}")
            return None
