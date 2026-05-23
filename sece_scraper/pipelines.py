import logging
from datetime import datetime
from scrapy.exceptions import DropItem
from sece_scraper.helpers.data_cleaner import DataCleaner
from sece_scraper.utils.storage import JSONLStorage

logger = logging.getLogger(__name__)

class DuplicationPipeline:
    """Remove duplicate items"""
    
    def __init__(self):
        self.seen = set()
    
    def process_item(self, item, spider):
        # Create a hash of the data to detect duplicates
        data_hash = hash(item.get('data', ''))
        
        if data_hash in self.seen:
            logger.debug(f"Dropping duplicate item")
            raise DropItem(f"Duplicate item found: {item}")
        
        self.seen.add(data_hash)
        return item

class DataCleaningPipeline:
    """Clean data before storage"""
    
    def process_item(self, item, spider):
        # Clean the text data
        if 'data' in item:
            cleaned_text = DataCleaner.clean_text(item['data'])
            if cleaned_text:
                item['data'] = cleaned_text
                item['cleaned'] = True
            else:
                logger.warning(f"Failed to clean item: {item}")
                raise DropItem("Data cleaning resulted in empty content")
        
        # Add timestamp
        item['timestamp'] = datetime.utcnow().isoformat()
        
        return item

class JSONLStoragePipeline:
    """Store items in JSONL format"""
    
    def __init__(self, data_path):
        self.data_path = data_path
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            data_path=crawler.settings.get('DATA_RAW_PATH')
        )
    
    def process_item(self, item, spider):
        # Convert item to dict if necessary
        item_dict = dict(item) if not isinstance(item, dict) else item
        
        # Store in JSONL
        if JSONLStorage.append_to_jsonl(self.data_path, item_dict):
            logger.info(f"Stored item: {item_dict.get('type', 'unknown')}")
        
        return item

