# SECE Scraper - File Manifest

## Overview
This document lists all files in the SECE Deep Web Scraper project and their purposes.

## Core Configuration Files

### 1. `requirements.txt`
**Purpose**: Python package dependencies  
**Usage**: `pip install -r requirements.txt`  
**Contains**: Scrapy, Playwright, PyMuPDF, EasyOCR, and supporting libraries  
**Size**: ~20 packages, ~300MB total installation

### 2. `scrapy.cfg`
**Purpose**: Scrapy project configuration  
**Format**: INI-style configuration  
**Auto-generated**: Yes, standard Scrapy config  
**Modified**: Rarely (if renaming project)

### 3. `.env.template`
**Purpose**: Environment variables template  
**Usage**: Copy to `.env` and customize if needed  
**Optional**: Yes, sensible defaults provided  
**Contents**: Proxy settings, custom headers, output options

### 4. `.gitignore`
**Purpose**: Git exclusion rules  
**Auto-generated**: No, customized for project  
**Excludes**: __pycache__, logs, data files, environment files

## Documentation Files

### 1. `README.md` (Comprehensive)
**Purpose**: Complete project reference  
**Length**: ~600 lines  
**Contents**:
- Feature overview
- Installation instructions
- Configuration details
- Phase explanations
- Troubleshooting guide
- Performance metrics

### 2. `QUICKSTART.md` (5-Minute Guide)
**Purpose**: Quick start for impatient users  
**Length**: ~150 lines  
**Contents**:
- 5-minute setup
- Basic operations
- Common issues
- Success indicators

### 3. `SETUP_INSTRUCTIONS.md` (This-is-Where-to-Start)
**Purpose**: Main entry point with all phases  
**Length**: ~400 lines  
**Contents**:
- Overview of 5 phases
- Step-by-step instructions
- Data output examples
- Success checklist
- Next steps

### 4. `IMPLEMENTATION_GUIDE.md` (Advanced)
**Purpose**: Technical deep-dive for advanced users  
**Length**: ~500 lines  
**Contents**:
- Architecture overview
- Component descriptions
- API reference
- Configuration options
- Performance tuning
- Extension guide

### 5. `FILE_MANIFEST.md` (This File)
**Purpose**: Documentation index  
**Contents**: All files, their purposes, and relationships

## Main Application Code

### Package: `sece_scraper/`

#### Configuration & Pipelines

**`sece_scraper/__init__.py`**
- Empty file marking package
- Allows: `import sece_scraper`

**`sece_scraper/settings.py`**
- Scrapy settings and configuration
- Key settings:
  - `CONCURRENT_REQUESTS`: 4 (adjust for performance)
  - `PLAYWRIGHT_BROWSER_TYPE`: chromium
  - `DATA_RAW_PATH`: Output location for raw data
  - `DATA_CLEANED_PATH`: Output location for cleaned data

**`sece_scraper/pipelines.py`**
- Data processing pipeline (3 stages)
- `DuplicationPipeline`: Remove duplicate content
- `DataCleaningPipeline`: Clean text, add timestamp
- `JSONLStoragePipeline`: Store in JSONL format

#### Spiders: `sece_scraper/spiders/`

**`sece_scraper/spiders/__init__.py`**
- Package marker for spiders

**`sece_scraper/spiders/sece_master_spider.py`** (Main Spider)
- **Purpose**: Core web scraper
- **Size**: ~200 lines
- **Key Methods**:
  - `start_requests()`: Entry point
  - `parse_main()`: Parse CSE main page
  - `parse_subpage()`: Parse events/achievements
  - `handle_year_buttons()`: Prepare for year filtering
- **Browser Automation**: Uses Playwright for dynamic content
- **Error Handling**: Graceful error handlers included

#### Helpers: `sece_scraper/helpers/`

**`sece_scraper/helpers/__init__.py`**
- Package marker

**`sece_scraper/helpers/pdf_processor.py`** (PDF Extraction)
- **Purpose**: Extract text from PDFs
- **Size**: ~150 lines
- **Key Functions**:
  - `convert_drive_link()`: Transform Google Drive URLs
  - `download_pdf()`: Download PDF from URL
  - `extract_text_from_pdf()`: Extract text using PyMuPDF
  - `process_pdf_url()`: Complete workflow
- **Dependencies**: PyMuPDF, requests

**`sece_scraper/helpers/image_processor.py`** (OCR)
- **Purpose**: Extract text from images via OCR
- **Size**: ~200 lines
- **Key Methods**:
  - `download_image()`: Download from URL
  - `preprocess_image()`: Enhance image quality
  - `extract_text_from_image()`: Run EasyOCR
  - `batch_extract_from_images()`: Process multiple
- **Dependencies**: EasyOCR, OpenCV, PIL, Pillow
- **Processing Pipeline**: Download → Grayscale → CLAHE → Denoise → OCR

**`sece_scraper/helpers/data_cleaner.py`** (Data Cleaning)
- **Purpose**: Prepare data for AI training
- **Size**: ~180 lines
- **Key Functions**:
  - `remove_boilerplate()`: Remove common navigation
  - `normalize_whitespace()`: Fix spacing
  - `remove_urls()`: Strip URLs
  - `clean_text()`: Apply all steps
  - `deduplicate()`: Remove duplicates
  - `tag_data()`: Create instruction-context pairs
  - `prepare_for_training()`: Complete pipeline
- **Boilerplate Patterns**: 15+ patterns for removal

#### Utilities: `sece_scraper/utils/`

**`sece_scraper/utils/__init__.py`**
- Package marker

**`sece_scraper/utils/storage.py`** (JSONL Storage)
- **Purpose**: File operations for JSONL format
- **Size**: ~120 lines
- **Key Methods**:
  - `append_to_jsonl()`: Add item to file
  - `read_jsonl()`: Read all items
  - `write_jsonl()`: Overwrite file
  - `get_file_stats()`: File statistics
- **Thread-Safe**: Safe for concurrent access
- **Format**: One JSON object per line

## Scripts & Tools

### Directory: `scripts/`

**`scripts/run_spider.py`** (Main Executable)
- **Purpose**: Execute scraper from command line
- **Size**: ~150 lines
- **Usage**: `python scripts/run_spider.py [--spider NAME] [--clean] [--input FILE] [--output FILE]`
- **Functions**:
  - `run_spider()`: Execute Scrapy spider
  - `clean_and_prepare_data()`: Data cleaning workflow
  - `main()`: CLI argument parsing
- **Error Handling**: Complete with logging
- **Return**: Exit code 0 (success) or 1 (failure)

**`scripts/analyze_data.py`** (Data Analysis)
- **Purpose**: Analyze collected JSONL data
- **Size**: ~250 lines
- **Usage**: `python scripts/analyze_data.py [--file FILE] [--stats] [--types] [--sample N] [--duplicates] [--all]`
- **Functions**:
  - `print_statistics()`: Summary stats
  - `print_type_breakdown()`: Per-type analysis
  - `print_sample()`: Show sample items
  - `deduplicate_check()`: Find duplicates
- **Output**: Colorized terminal display
- **No Dependencies**: Uses only built-in + project modules

**`scripts/validate_setup.py`** (Full Validation)
- **Purpose**: Comprehensive setup verification
- **Size**: ~350 lines
- **Usage**: `python scripts/validate_setup.py`
- **Checks**:
  1. Python version (3.8+)
  2. All dependencies installed
  3. Playwright browsers available
  4. Project structure correct
  5. Module imports working
  6. File permissions
  7. Scrapy configuration
  8. System resources
- **Output**: 8-point checklist with ✓/✗ indicators

**`scripts/quick_test.py`** (Quick Validation)
- **Purpose**: Fast sanity check before running
- **Size**: ~200 lines
- **Usage**: `python scripts/quick_test.py`
- **Tests**:
  - Module imports
  - PDF processor functions
  - Data cleaner functions
  - Storage operations
  - Directory structure
- **Runtime**: <5 seconds

**`scripts/schedule_cron.bat`** (Windows Automation)
- **Purpose**: Windows Task Scheduler integration
- **Format**: Batch file (.bat)
- **Commands**:
  - `install`: Create scheduled task
  - `run`: Execute immediately
  - `check`: Show task details
- **Schedule**: Every Sunday at 00:00
- **Logging**: Appends to `logs/weekly_schedule.log`

**`scripts/schedule_cron.sh`** (Linux/Mac Automation)
- **Purpose**: Unix cron integration
- **Format**: Bash shell script (.sh)
- **Commands**:
  - `install`: Add cron job
  - `run`: Execute immediately
  - `check`: Verify installation
  - `remove`: Delete cron job
- **Schedule**: 0 0 * * 0 (Sunday midnight)
- **Colors**: Colored output for readability

## Data Directories

### `data/raw/`
- **Purpose**: Store raw scraped data
- **Format**: JSONL (one JSON per line)
- **File**: `weekly_data.jsonl`
- **Growth**: Appends each week
- **Size**: Depends on website content (typical: 1-10MB/week)

### `data/cleaned/`
- **Purpose**: Store cleaned, AI-training-ready data
- **Format**: JSONL with instruction-context pairs
- **File**: `cleaned_data.jsonl`
- **Growth**: Regenerated weekly from raw data
- **Size**: Typically 20-30% smaller than raw

## Logs Directory

### `logs/`
- **spider.log**: Main spider execution log
- **weekly_schedule.log**: Scheduled task execution log

## Configuration Environment

### `.env` (Optional)
- **Created From**: `.env.template`
- **Format**: Key=value pairs
- **Contents**:
  - Proxy settings
  - Custom headers
  - Output format options
  - Advanced tuning parameters
- **Optional**: Yes, defaults work fine

## File Relationships

```
requirements.txt
    ↓
    ├─→ sece_scraper/
    │   ├─→ settings.py (configure here)
    │   ├─→ spiders/sece_master_spider.py (main crawler)
    │   ├─→ helpers/ (processing modules)
    │   └─→ utils/storage.py (output)
    │
    └─→ scripts/
        ├─→ run_spider.py (execute spider)
        ├─→ analyze_data.py (view results)
        └─→ schedule_cron.bat (automate)

    Data Flow:
    Website → Spider → Pipelines → data/raw/weekly_data.jsonl
                         ↓
                    DataCleaner → data/cleaned/cleaned_data.jsonl
```

## File Statistics

| Category | Count | Total Lines | Purpose |
|----------|-------|-------------|---------|
| Core Code | 8 files | 1200+ | Spider & helpers |
| Scripts | 6 files | 1200+ | Execution & automation |
| Documentation | 5 files | 2000+ | Guides & references |
| Configuration | 2 files | 100+ | Settings & env |
| **Total** | **21 files** | **4500+** | **Complete scraper** |

## Installation Checklist

- [ ] `requirements.txt` installed
- [ ] `sece_scraper/` package structure intact
- [ ] `scripts/` directory executable
- [ ] `data/` directory writable
- [ ] `logs/` directory writable
- [ ] Playwright browsers installed
- [ ] Quick test passes: `python scripts/quick_test.py`

## First-Time User: File Reading Order

1. Start: `SETUP_INSTRUCTIONS.md` (this guide)
2. Quick Start: `QUICKSTART.md` (5 minutes)
3. Full Ref: `README.md` (comprehensive)
4. Advanced: `IMPLEMENTATION_GUIDE.md` (customization)
5. Code: `sece_scraper/spiders/sece_master_spider.py` (spider logic)

## Maintenance Files

**Files to Monitor:**
- `logs/spider.log` - Check for errors
- `logs/weekly_schedule.log` - Verify scheduling
- `data/raw/weekly_data.jsonl` - Check item count growth
- `data/cleaned/cleaned_data.jsonl` - Verify data quality

**Files to Update (if needed):**
- `sece_scraper/spiders/sece_master_spider.py` - If website structure changes
- `sece_scraper/settings.py` - If adjusting performance
- `scripts/schedule_cron.bat` - If changing schedule

**Files to Backup:**
- `data/raw/weekly_data.jsonl` - Your collected data
- `data/cleaned/cleaned_data.jsonl` - Cleaned dataset

---

**Document Version**: 1.0  
**Created**: 2024-05-14  
**Project Status**: Production Ready ✅
