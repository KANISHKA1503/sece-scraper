# SECE Scraper - Implementation & Configuration Guide

This document provides detailed implementation details and configuration options for advanced users.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       SECE SCRAPER SYSTEM                        │
└─────────────────────────────────────────────────────────────────┘
         │
         ├─ PHASE 1: DISCOVERY
         │  ├─ Main CSE page (https://sece.ac.in/...)
         │  ├─ Extract PDF links (Google Drive)
         │  └─ Identify sub-pages (events, achievements)
         │
         ├─ PHASE 2: INTERACTION (Playwright)
         │  ├─ Click dropdown menus
         │  ├─ Click year-wise buttons (2023, 2022, etc.)
         │  ├─ Wait for dynamic content loading
         │  └─ Extract revealed content
         │
         ├─ PHASE 3: PDF PROCESSING
         │  ├─ Detect Google Drive links
         │  ├─ Convert /view → /uc?export=download
         │  ├─ Download PDF files
         │  ├─ Extract text using PyMuPDF
         │  └─ Return extracted text
         │
         ├─ PHASE 3: IMAGE PROCESSING
         │  ├─ Identify image tags
         │  ├─ Download images
         │  ├─ Preprocess (grayscale, CLAHE, denoise)
         │  ├─ Run EasyOCR
         │  └─ Return extracted text
         │
         ├─ PHASE 4: DATA CLEANING
         │  ├─ Remove boilerplate
         │  ├─ Normalize whitespace
         │  ├─ Remove URLs
         │  ├─ Deduplicate content
         │  ├─ Create instruction-context pairs
         │  └─ Generate metadata
         │
         └─ PHASE 5: STORAGE & AUTOMATION
            ├─ Store raw → data/raw/weekly_data.jsonl
            ├─ Store cleaned → data/cleaned/cleaned_data.jsonl
            └─ Schedule weekly execution
```

## Component Descriptions

### 1. Scrapy Spider (`sece_master_spider.py`)

**Key Methods:**

- `start_requests()`: Initial entry point
  - Yields request to main CSE page
  - Enables Playwright for browser automation
  
- `parse_main(response)`: Parse main CSE page
  - Extracts all PDF links
  - Processes PDFs for text extraction
  - Identifies sub-pages for further crawling
  
- `parse_subpage(response)`: Parse events/achievements pages
  - Extracts images and applies OCR
  - Extracts text content
  - Handles year-wise button interactions

**Playwright Integration:**

```python
meta={
    "playwright": True,
    "playwright_include_page": True,
    "playwright_page_methods": [
        PageMethod("click", ".dropdown-selector"),
        PageMethod("wait_for_selector", ".content"),
    ]
}
```

### 2. PDF Processor (`pdf_processor.py`)

**Key Features:**

- **Google Drive Link Conversion**
  ```python
  # Input:  https://drive.google.com/file/d/ABC123/view
  # Output: https://drive.google.com/uc?export=download&id=ABC123
  ```

- **PDF Text Extraction**
  ```python
  text = PDFProcessor.process_pdf_url(pdf_url)
  # Returns: Extracted text from all pages
  ```

### 3. Image Processor (`image_processor.py`)

**OCR Pipeline:**

1. Download image from URL
2. Convert to OpenCV format
3. Preprocess:
   - Convert to grayscale
   - Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
   - Denoise using fastNlMearsDenoising
4. Run EasyOCR
5. Extract and concatenate text

### 4. Data Cleaner (`data_cleaner.py`)

**Boilerplate Patterns Removed:**

- Navigation elements: "skip to content", "quick links"
- Footers: "privacy policy", "terms of service"
- Sidebars: "admission open", "apply now"
- Contact info: emails, phone numbers
- Copyright notices

**Output Format:**

```json
{
  "instruction": "What is the 2023 CSE syllabus?",
  "context": "[Extracted PDF text about syllabus]",
  "type": "syllabus",
  "metadata": {"year": 2023, "source": "google_drive"}
}
```

### 5. Storage Utilities (`storage.py`)

**JSONL Operations:**

```python
# Append item
JSONLStorage.append_to_jsonl('file.jsonl', {'type': 'syllabus', 'data': '...'})

# Read all items
items = JSONLStorage.read_jsonl('file.jsonl')

# Get file statistics
stats = JSONLStorage.get_file_stats('file.jsonl')
# Returns: {'exists': True, 'size': 1024, 'lines': 10, 'last_modified': '...'}
```

### 6. Scrapy Pipelines (`pipelines.py`)

**Pipeline Chain:**

```
Item → DuplicationPipeline → DataCleaningPipeline → JSONLStoragePipeline
```

- **DuplicationPipeline**: Removes items with duplicate content (hash-based)
- **DataCleaningPipeline**: Cleans text, adds timestamp
- **JSONLStoragePipeline**: Appends to JSONL file

## Configuration

### Scrapy Settings (`sece_scraper/settings.py`)

**Critical Settings:**

```python
# Concurrency
CONCURRENT_REQUESTS = 4              # Max requests simultaneously
CONCURRENT_REQUESTS_PER_DOMAIN = 2   # Max per domain

# Playwright
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_ARGS = {
    "headless": True,
    "args": ["--disable-blink-features=AutomationControlled"]
}

# Timeouts
DOWNLOAD_TIMEOUT = 30               # Seconds per download
ROBOTSTXT_OBEY = False              # Ignore robots.txt (configure as needed)

# Paths
DATA_RAW_PATH = 'data/raw/weekly_data.jsonl'
DATA_CLEANED_PATH = 'data/cleaned/cleaned_data.jsonl'
```

### Environment Variables (`.env`)

Create `.env` from `.env.template` for custom configuration:

```bash
cp .env.template .env
# Edit .env with your settings
```

## Advanced Usage

### Custom Spider Configuration

**Modify target URL:**

Edit `sece_master_spider.py`:
```python
start_urls = ["https://sece.ac.in/your-custom-page/"]
```

**Add custom year buttons:**

```python
YEAR_BUTTONS = ["2024", "2023", "2022", "2021", "2020", "2019", "2018"]
```

### Custom Selectors

If page structure changes:

```python
# In parse_main():
pdf_links = response.css("your-custom-selector::attr(href)").getall()
```

### Performance Tuning

**For Large Datasets:**

```python
# In settings.py
CONCURRENT_REQUESTS = 8              # Increase parallelism
DOWNLOAD_TIMEOUT = 60                # Increase timeout
ITEM_PIPELINES['JSONLStoragePipeline'].batch_size = 100
```

**For Slow Networks:**

```python
DOWNLOAD_TIMEOUT = 120
ROBOTSTXT_OBEY = False
COMPRESS_ENABLED = True
```

**For OCR Optimization:**

```python
# Use GPU if available
# In image_processor.py:
import torch
USE_GPU = torch.cuda.is_available()
# reader = easyocr.Reader(['en'], gpu=USE_GPU)
```

### Scheduling

#### Windows Task Scheduler (Advanced)

```powershell
# View task
schtasks /query /tn "SECE-WebScraper-Weekly"

# Modify task
schtasks /change /tn "SECE-WebScraper-Weekly" /st 02:00

# Delete task
schtasks /delete /tn "SECE-WebScraper-Weekly" /f
```

#### Linux Cron (Advanced)

```bash
# Edit crontab
EDITOR=nano crontab -e

# Example: Run at 2 AM every Sunday, email on completion
0 2 * * 0 cd /path/to/bot && python3 scripts/run_spider.py --clean 2>&1 | mail -s "SECE Scraper Report" your@email.com

# View all cron jobs
crontab -l
```

## Monitoring & Troubleshooting

### Log Files

**Location:** `logs/spider.log`

**Read logs (Windows):**
```bash
type logs\spider.log | tail -n 50  # Last 50 lines
findstr "ERROR" logs\spider.log      # Find errors
```

**Read logs (Linux):**
```bash
tail -f logs/spider.log              # Real-time
grep "ERROR" logs/spider.log         # Find errors
```

### Debug Mode

```bash
set SCRAPY_LOGLEVEL=DEBUG
python scripts/run_spider.py
```

### Performance Monitoring

```bash
# Check process memory (Windows)
tasklist /FI "IMAGENAME eq python.exe" /V

# Monitor in real-time (Linux)
top -p $(pgrep -f run_spider.py)
```

### Data Validation

```bash
# Count items
for /f %a in ('find /c /v "" ^< data\raw\weekly_data.jsonl') do echo Items: %a

# Validate JSON
python scripts/validate_jsonl.py data/raw/weekly_data.jsonl

# Check file integrity
python -c "import json; [json.loads(l) for l in open('data/raw/weekly_data.jsonl')]"
```

## API Reference

### PDFProcessor

```python
from sece_scraper.helpers.pdf_processor import PDFProcessor

# Convert Google Drive link
url = PDFProcessor.convert_drive_link("https://drive.google.com/file/d/ID/view")

# Download and extract
text = PDFProcessor.process_pdf_url(url)
```

### ImageProcessor

```python
from sece_scraper.helpers.image_processor import ImageProcessor

processor = ImageProcessor(languages=['en'])

# Extract text from image
text = processor.extract_text_from_image(img_url)

# Batch processing
results = processor.batch_extract_from_images(img_urls_list)
```

### DataCleaner

```python
from sece_scraper.helpers.data_cleaner import DataCleaner

# Clean text
cleaned = DataCleaner.clean_text(raw_text)

# Prepare for training
training_data = DataCleaner.prepare_for_training(raw_items)

# Tag data
tagged = DataCleaner.tag_data('syllabus', text, metadata)
```

### JSONLStorage

```python
from sece_scraper.utils.storage import JSONLStorage

# Append
JSONLStorage.append_to_jsonl('file.jsonl', item_dict)

# Read
items = JSONLStorage.read_jsonl('file.jsonl')

# Write (overwrite)
JSONLStorage.write_jsonl('file.jsonl', items_list)

# Stats
stats = JSONLStorage.get_file_stats('file.jsonl')
```

## Extending the Scraper

### Add New Data Types

1. Update spider to extract new data
2. Add new "type" in yield statements
3. Update DataCleaner.tag_data() with new type
4. Modify instruction templates if needed

### Add New Processing Steps

1. Create new helper in `sece_scraper/helpers/`
2. Import in spider
3. Call in appropriate parse method
4. Add to pipeline if needed

### Custom Pipeline

```python
# In pipelines.py
class CustomPipeline:
    def process_item(self, item, spider):
        # Your custom logic
        return item

# In settings.py
ITEM_PIPELINES = {
    # ... existing pipelines ...
    'sece_scraper.pipelines.CustomPipeline': 600,
}
```

## Best Practices

1. **Monitor First Run**: Watch logs to identify selector/link issues
2. **Regular Backups**: Archive old JSONL files monthly
3. **Test Changes**: Run spider on small subset before scheduling
4. **Validate Output**: Use analyze_data.py to check quality
5. **Update Selectors**: Website structure may change; monitor logs
6. **Resource Allocation**: OCR is memory-intensive; adjust as needed
7. **Error Handling**: Check logs for systematic failures

## Troubleshooting Checklist

- [ ] All dependencies installed: `pip show scrapy`
- [ ] Playwright browsers available: Check `.cache/ms-playwright`
- [ ] Log file readable: `tail logs/spider.log`
- [ ] Data directory writable: `ls -la data/`
- [ ] Scheduler working: Check `logs/weekly_schedule.log`
- [ ] Network connectivity: Ping website manually
- [ ] Selector valid: Check if website changed
- [ ] Memory available: Monitor with `top` or Task Manager

---

**Document Version:** 1.0  
**Last Updated:** 2024-05-14
