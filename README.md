# SECE CSE Department Deep Web Scraper

A comprehensive web scraper for extracting syllabus PDFs, event details, and student achievements from the SECE Computer Science Engineering department website. This tool uses advanced techniques like Playwright for browser automation, PyMuPDF for PDF extraction, and EasyOCR for text extraction from images.

## Features

✅ **PDF Extraction**: Automatically converts Google Drive links and extracts syllabus text  
✅ **Image OCR**: Processes event posters and achievements with EasyOCR  
✅ **Browser Automation**: Uses Playwright to interact with dynamic page elements  
✅ **Deduplication**: Prevents duplicate data from being stored  
✅ **Data Cleaning**: Removes boilerplate and formats data for AI training  
✅ **Scheduled Automation**: Runs weekly via Windows Task Scheduler  
✅ **JSONL Storage**: Ideal format for LLM training and fine-tuning

## Project Structure

```
bot/
├── scrapy.cfg                          # Scrapy project config
├── requirements.txt                    # Python dependencies
├── sece_scraper/
│   ├── settings.py                     # Scrapy settings
│   ├── pipelines.py                    # Data processing pipelines
│   ├── spiders/
│   │   └── sece_master_spider.py      # Main crawler spider
│   ├── helpers/
│   │   ├── pdf_processor.py            # PDF extraction (Phase 3)
│   │   ├── image_processor.py          # OCR extraction (Phase 3)
│   │   └── data_cleaner.py             # Data cleaning (Phase 4)
│   └── utils/
│       └── storage.py                  # JSONL file operations
├── data/
│   ├── raw/                            # Raw scraped data
│   │   └── weekly_data.jsonl          # Raw JSONL storage
│   └── cleaned/                        # Processed data
│       └── cleaned_data.jsonl         # AI training-ready data
├── logs/                               # Execution logs
├── scripts/
│   ├── run_spider.py                   # Main execution script
│   └── schedule_cron.bat               # Windows scheduler (Phase 5)
└── README.md                           # This file
```

## Phase 1: Installation

### Prerequisites
- Python 3.8+ (tested with 3.10+)
- Windows (for Task Scheduler integration) or Linux (modify cron job)
- Internet connection

### Step 1: Clone/Create Project
```bash
cd c:\Users\Kanishka\Desktop\bot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- **Scrapy 2.11.0**: Web scraping framework
- **scrapy-playwright**: Browser automation integration
- **Playwright**: Headless browser control
- **PyMuPDF**: PDF text extraction
- **EasyOCR**: Image text extraction
- **Other dependencies**: requests, aiohttp, Pillow, OpenCV, lxml

### Step 3: Initialize Playwright Browsers
```bash
python -m playwright install chromium
```

## Phase 2: Configuration

The project is pre-configured. Key settings in `sece_scraper/settings.py`:

```python
PLAYWRIGHT_BROWSER_TYPE = "chromium"  # Use Chromium browser
CONCURRENT_REQUESTS = 4               # Max concurrent requests
DATA_RAW_PATH = 'data/raw/weekly_data.jsonl'
DATA_CLEANED_PATH = 'data/cleaned/cleaned_data.jsonl'
LOG_FILE = 'logs/spider.log'
```

## Phase 3: Running the Scraper

### Quick Start (Scrape Only)
```bash
python scripts/run_spider.py
```

### Scrape + Clean Data
```bash
python scripts/run_spider.py --clean
```

### Custom Options
```bash
python scripts/run_spider.py --spider sece_deep_crawl --clean --output my_data.jsonl
```

### Expected Output
The spider will:
1. Visit `https://sece.ac.in/department-computer-science-engineering-2/`
2. Extract PDF links from Google Drive
3. Convert `/view` links to `/uc?export=download`
4. Download and extract text from PDFs
5. Navigate to Events and Achievements pages
6. Perform OCR on images
7. Save results to `data/raw/weekly_data.jsonl`

### Example Raw Output
```json
{"type": "syllabus", "source_url": "https://sece.ac.in/...", "data": "CSE Syllabus 2023...", "timestamp": "2024-05-14T10:30:00"}
{"type": "event", "source_url": "https://sece.ac.in/events/", "data": "Event details extracted via OCR...", "timestamp": "2024-05-14T10:31:00"}
```

## Phase 4: Data Cleaning for AI Training

When you run with `--clean`, the data cleaning pipeline:

1. **Boilerplate Removal**: Strips headers, footers, nav elements
2. **Deduplication**: Removes duplicate content
3. **Normalization**: Fixes whitespace, removes URLs
4. **Tagging**: Creates instruction-context pairs for LLM training

### Cleaned Output Format
```json
{
  "instruction": "What is included in the 2023 CSE syllabus?",
  "context": "CSE Syllabus 2023: Module 1...",
  "type": "syllabus",
  "metadata": {}
}
```

## Phase 5: Weekly Automation (Windows)

### Method 1: Using Batch Script (Recommended)
```bash
cd scripts
schedule_cron.bat install
```

This creates a Windows scheduled task:
- **Task Name**: SECE-WebScraper-Weekly
- **Schedule**: Every Sunday at 00:00 (midnight)
- **Action**: Runs `python scripts/run_spider.py --clean`
- **Logs**: Stored in `logs/weekly_schedule.log`

### Method 2: Manual Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Name: "SECE-WebScraper-Weekly"
4. Trigger: Weekly, Sunday, 00:00
5. Action: `python C:\Users\Kanishka\Desktop\bot\scripts\run_spider.py --clean`
6. Start in: `C:\Users\Kanishka\Desktop\bot`

### Method 3: Linux/Unix (Cron)
```bash
# Edit crontab
crontab -e

# Add this line (runs every Sunday at midnight)
0 0 * * 0 cd /path/to/bot && python scripts/run_spider.py --clean >> logs/weekly_schedule.log 2>&1
```

## Success Criteria (Phase 5 Checklist)

✅ **PDF Link Conversion**
```python
# Verify in logs: "PDF link converted from /view to /uc?export=download"
```

✅ **Image Load Waiting**
```python
# Playwright waits 2-3 seconds after clicking year buttons
PageMethod("wait_for_load_state", "networkidle")
```

✅ **Data Accumulation**
```bash
# Check combined JSONL file
type data\raw\weekly_data.jsonl | find /c "^" :: Count lines
```

## File Descriptions

### Core Modules

#### `sece_scraper/spiders/sece_master_spider.py`
The main Scrapy spider that:
- Starts at the CSE main page
- Extracts all PDF links
- Navigates to Events and Achievements
- Handles image OCR
- Uses Playwright for browser automation

Key methods:
- `start_requests()`: Initial page request
- `parse_main()`: Parse CSE main page, extract PDFs
- `parse_subpage()`: Parse Events/Achievements, handle OCR
- `handle_year_buttons()`: Prepare for year-wise filtering

#### `sece_scraper/helpers/pdf_processor.py`
Handles PDF extraction:
```python
PDFProcessor.convert_drive_link(url)      # /view -> /uc?export=download
PDFProcessor.process_pdf_url(url)         # Download and extract text
```

#### `sece_scraper/helpers/image_processor.py`
Handles image OCR:
```python
processor = ImageProcessor()
text = processor.extract_text_from_image(url)  # Download, preprocess, OCR
```

#### `sece_scraper/helpers/data_cleaner.py`
Data preparation for AI:
```python
cleaned = DataCleaner.prepare_for_training(raw_items)  # Full pipeline
```

#### `sece_scraper/pipelines.py`
Scrapy pipelines for processing:
- `DuplicationPipeline`: Remove duplicates
- `DataCleaningPipeline`: Clean text data
- `JSONLStoragePipeline`: Store in JSONL format

#### `sece_scraper/utils/storage.py`
JSONL file operations:
```python
JSONLStorage.append_to_jsonl(path, item)   # Add single item
JSONLStorage.read_jsonl(path)              # Read all items
JSONLStorage.get_file_stats(path)          # Get statistics
```

### Configuration Files

#### `scrapy.cfg`
Standard Scrapy project configuration

#### `sece_scraper/settings.py`
Scrapy settings:
- Concurrency limits
- Playwright configuration
- Pipeline registration
- Data paths
- Timeouts

## Troubleshooting

### Issue: "No images found" or empty OCR results
**Solution**: The website may require JavaScript to load images. The spider uses Playwright with `wait_for_load_state("networkidle")` to handle this.

### Issue: PDF extraction returns None
**Solution**: 
1. Verify Google Drive link is public
2. Check if link format is correct
3. Ensure network connectivity

### Issue: Task Scheduler not running
**Solution**:
1. Check Windows Task Scheduler logs
2. Verify Python path is correct
3. Ensure script has execute permissions
4. Check `logs/weekly_schedule.log` for errors

### Issue: Memory issues with large datasets
**Solution**:
1. Process data in batches
2. Increase timeout in settings
3. Clear `data/raw/` directory periodically
4. Archive old JSONL files

## Example Usage Scenarios

### Scenario 1: Initial Full Scrape
```bash
# Clean start
del data\raw\weekly_data.jsonl 2>nul
python scripts/run_spider.py --clean
```

### Scenario 2: Incremental Scrape (Append)
```bash
# Appends to existing data
python scripts/run_spider.py
python scripts/run_spider.py --clean  # Re-clean with all data
```

### Scenario 3: Check Data Quality
```bash
# View first 10 items
for /f "skip=10" %f in (data\raw\weekly_data.jsonl) do @echo %f
```

## Performance Metrics

- **Initial crawl**: ~5-10 minutes (depends on site size)
- **PDF processing**: 1-2 seconds per PDF
- **Image OCR**: 2-5 seconds per image (GPU recommended)
- **Data cleaning**: ~1 second per 1000 items
- **JSONL write**: <1 second per 1000 items

## Requirements Summary

### Language & Runtime
- Python 3.8+

### Core Libraries (See requirements.txt)
- Scrapy: Crawling framework
- Playwright: Browser automation
- PyMuPDF: PDF processing
- EasyOCR: Image text extraction

### System Requirements
- 2+ GB RAM (base)
- 4+ GB RAM recommended (for large datasets with OCR)
- 500+ MB free disk space
- Internet connection

### For GPU-accelerated OCR (Optional)
- CUDA 11.0+ (for EasyOCR on GPU)
- Install: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Initialize Playwright: `python -m playwright install chromium`
3. ✅ Run initial test: `python scripts/run_spider.py --clean`
4. ✅ Setup weekly automation: `scripts\schedule_cron.bat install`
5. ✅ Monitor logs: `logs/spider.log` and `logs/weekly_schedule.log`

## File Locations

- **Raw Data**: `data/raw/weekly_data.jsonl`
- **Cleaned Data**: `data/cleaned/cleaned_data.jsonl`
- **Logs**: `logs/spider.log`, `logs/weekly_schedule.log`
- **Configuration**: `sece_scraper/settings.py`

## Notes

- The spider respects reasonable delays between requests
- PDFs are processed in-memory (not stored)
- Images are downloaded on-demand for OCR processing
- All data is stored in JSONL format (one JSON object per line)
- Deduplication prevents the same content from being stored multiple times

## Support & Debugging

For detailed logs:
```bash
tail -f logs/spider.log              # Real-time logs
type logs/weekly_schedule.log        # Task scheduler logs
```

To run with verbose output:
```bash
set SCRAPY_LOGLEVEL=DEBUG
python scripts/run_spider.py
```

## License & Attribution

This scraper is designed to work with SECE CSE department website. Ensure compliance with:
- Website's robots.txt
- Terms of service
- Copyright and data usage policies

---

**Created**: 2024-05-14  
**Version**: 1.0.0  
**Status**: Production-Ready
