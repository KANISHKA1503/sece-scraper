#!/usr/bin/env python3
"""
Main entry point for running the SECE scraper
Usage: python scripts/run_spider.py [--clean] [--output OUTPUT_FILE]
"""

import sys
import os
import logging
import argparse
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sece_scraper.helpers.data_cleaner import DataCleaner
from sece_scraper.utils.storage import JSONLStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/spider.log')
    ]
)
logger = logging.getLogger(__name__)

def run_spider(spider_name="sece_deep_crawl"):
    """Run the Scrapy spider"""
    logger.info("Starting spider process...")
    
    # Get Scrapy settings
    settings = get_project_settings()
    
    # Create crawler process
    process = CrawlerProcess(settings)
    
    # Crawl
    process.crawl(spider_name)
    process.start()
    
    logger.info("Spider process completed")

def clean_and_prepare_data(input_file=None, output_file=None):
    """
    Clean raw data and prepare for AI training
    """
    logger.info("Starting data cleaning and preparation...")
    
    settings = get_project_settings()
    input_file = input_file or settings.get('DATA_RAW_PATH')
    output_file = output_file or settings.get('DATA_CLEANED_PATH')
    
    # Read raw data
    raw_items = JSONLStorage.read_jsonl(input_file)
    logger.info(f"Read {len(raw_items)} items from raw data")
    
    # Clean and prepare
    cleaned_items = DataCleaner.prepare_for_training(raw_items)
    logger.info(f"Cleaned to {len(cleaned_items)} items")
    
    # Save cleaned data
    JSONLStorage.write_jsonl(output_file, cleaned_items)
    logger.info(f"Saved cleaned data to {output_file}")
    
    # Print statistics
    raw_stats = JSONLStorage.get_file_stats(input_file)
    clean_stats = JSONLStorage.get_file_stats(output_file)
    
    logger.info(f"Raw data: {raw_stats}")
    logger.info(f"Cleaned data: {clean_stats}")

def main():
    parser = argparse.ArgumentParser(
        description='SECE CSE Department Web Scraper'
    )
    
    parser.add_argument(
        '--spider',
        default='sece_deep_crawl',
        help='Spider name to run (default: sece_deep_crawl)'
    )
    
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean and prepare data after scraping'
    )
    
    parser.add_argument(
        '--input',
        help='Input file for data cleaning'
    )
    
    parser.add_argument(
        '--output',
        help='Output file for cleaned data'
    )
    
    args = parser.parse_args()
    
    # Create logs directory if not exists
    os.makedirs('logs', exist_ok=True)
    
    try:
        # Run spider
        logger.info(f"Running spider: {args.spider}")
        run_spider(args.spider)
        
        # Clean data if requested
        if args.clean:
            clean_and_prepare_data(args.input, args.output)
        
        logger.info("Process completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
