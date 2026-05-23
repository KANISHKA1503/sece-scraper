# Scrapy settings for sece_scraper project

BOT_NAME = 'sece_scraper'

SPIDER_MODULES = ['sece_scraper.spiders']
NEWSPIDER_MODULE = 'sece_scraper.spiders'

# Respect robots.txt
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests per domain
CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# Disable cookies (optional)
COOKIES_ENABLED = False

# Playwright configuration
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_BROWSER_TYPE = "chromium"

# Enable playwright for all requests by default
PLAYWRIGHT_LAUNCH_ARGS = {
    "headless": True,
    "args": ["--disable-blink-features=AutomationControlled"],
}

# User agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Pipelines
ITEM_PIPELINES = {
    'sece_scraper.pipelines.DuplicationPipeline': 300,
    'sece_scraper.pipelines.DataCleaningPipeline': 400,
    'sece_scraper.pipelines.JSONLStoragePipeline': 500,
}

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/spider.log'

# Data paths
DATA_RAW_PATH = 'data/raw/weekly_data.jsonl'
DATA_CLEANED_PATH = 'data/cleaned/cleaned_data.jsonl'

# Timeouts
DOWNLOAD_TIMEOUT = 30
