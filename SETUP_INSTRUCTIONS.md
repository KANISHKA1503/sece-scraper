# SECE Deep Web Scraper - Complete Setup & Execution Guide

## 🎯 Overview

This is a production-ready web scraper for extracting data from the SECE CSE department website. It handles:

- ✅ PDF extraction from Google Drive links
- ✅ OCR processing of event images
- ✅ Browser automation via Playwright
- ✅ Data cleaning and deduplication
- ✅ Scheduled weekly execution
- ✅ JSONL output format (ideal for LLM training)

## 📋 Implementation Phases

### Phase 1: Technical Stack
Tools and libraries pre-configured and ready to use.

### Phase 2: Logic Flow
Spider automatically handles:
- Discovery of CSE pages
- PDF link detection and extraction
- Image OCR processing
- Recursive link following

### Phase 3: Master Script
Complete Scrapy spider with browser automation, PDF processing, and OCR.

### Phase 4: Data Cleaning
Automatic removal of boilerplate, deduplication, and contextual tagging for AI training.

### Phase 5: Weekly Automation
Windows Task Scheduler or Linux cron setup for automatic weekly runs.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies (2 minutes)

```bash
cd c:\Users\Kanishka\Desktop\bot

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium
```

### Step 2: Verify Installation (1 minute)

```bash
# Quick validation test
python scripts/quick_test.py
```

Expected output: "✓ ALL TESTS PASSED!"

### Step 3: Run First Scrape (2 minutes)

```bash
# Run scraper with automatic data cleaning
python scripts/run_spider.py --clean
```

**What happens:**
- Scrapes SECE CSE main page
- Extracts PDFs and runs OCR on images
- Cleans data and stores in JSONL format
- Creates `data/raw/weekly_data.jsonl` and `data/cleaned/cleaned_data.jsonl`

---

## 📊 Analyzing Results

### View Statistics
```bash
python scripts/analyze_data.py --all
```

Shows:
- Total items collected
- Breakdown by type
- Content size analysis
- Duplicate detection

### Sample Items
```bash
python scripts/analyze_data.py --sample 5
```

Shows first 5 collected items with preview.

---

## ⏰ Phase 5: Weekly Automation Setup

### Windows (Recommended for Windows users)

```bash
# Navigate to scripts directory
cd scripts

# Install as Windows scheduled task
schedule_cron.bat install

# Verify installation
tasklist /FI "TASKNAME eq SECE-WebScraper-Weekly"
```

**Task Details:**
- Name: `SECE-WebScraper-Weekly`
- Schedule: Every Sunday at 00:00 (midnight)
- Action: Runs `python scripts/run_spider.py --clean`
- Logs: `logs/weekly_schedule.log`

To modify time:
```bash
# Edit and re-run installation, or use:
schtasks /change /tn "SECE-WebScraper-Weekly" /st 02:00
```

### Linux/Mac (Alternative)

```bash
# Make script executable
chmod +x scripts/schedule_cron.sh

# Install cron job
bash scripts/schedule_cron.sh install

# Verify
bash scripts/schedule_cron.sh check
```

Cron format: `0 0 * * 0` = Every Sunday at midnight

---

## 📁 Project Structure

```
bot/
├── 📖 README.md                    ← Full documentation
├── 📖 QUICKSTART.md                ← 5-minute guide
├── 📖 IMPLEMENTATION_GUIDE.md       ← Advanced configuration
├── 📋 requirements.txt              ← Dependencies to install
├── 🔧 scrapy.cfg                   ← Scrapy configuration
│
├── 🕷️ sece_scraper/                ← Main scraper package
│   ├── settings.py                 ← Scrapy settings
│   ├── pipelines.py                ← Data processing pipelines
│   │
│   ├── spiders/
│   │   └── sece_master_spider.py   ← Main crawler (Phase 3)
│   │
│   ├── helpers/
│   │   ├── pdf_processor.py        ← PDF extraction
│   │   ├── image_processor.py      ← OCR extraction
│   │   └── data_cleaner.py         ← Data cleaning (Phase 4)
│   │
│   └── utils/
│       └── storage.py              ← JSONL file operations
│
├── 📊 scripts/
│   ├── run_spider.py               ← Execute scraper
│   ├── analyze_data.py             ← Analyze collected data
│   ├── validate_setup.py           ← Full validation
│   ├── quick_test.py               ← Quick validation
│   ├── schedule_cron.bat           ← Windows automation
│   └── schedule_cron.sh            ← Linux automation
│
└── 💾 data/
    ├── raw/                        ← Raw scraped data
    │   └── weekly_data.jsonl
    └── cleaned/                    ← AI training-ready data
        └── cleaned_data.jsonl
```

---

## 🔍 Data Output Examples

### Raw Data (before cleaning)
```json
{
  "type": "syllabus",
  "source_url": "https://sece.ac.in/...",
  "data": "CSE Syllabus 2023: Module 1...",
  "original_link": "https://drive.google.com/...",
  "timestamp": "2024-05-14T10:30:00"
}
```

### Cleaned Data (AI training format)
```json
{
  "instruction": "What is included in the 2023 CSE syllabus?",
  "context": "CSE Syllabus 2023: Module 1 covers data structures...",
  "type": "syllabus",
  "metadata": {}
}
```

---

## ✅ Success Criteria (Phase 5 Checklist)

✔️ **PDF Link Conversion**
```
Check: Google Drive /view URLs converted to /uc?export=download
Location: logs/spider.log
Search for: "PDF link converted"
```

✔️ **Image Load Waiting**
```
Check: Playwright waits for dynamic content
Configuration: PageMethod("wait_for_load_state", "networkidle")
Result: Images load before OCR processing
```

✔️ **Data Accumulation**
```
Check: Data appended to same JSONL file
Command: wc -l data/raw/weekly_data.jsonl
Result: Line count increases weekly
```

---

## 🛠️ Common Operations

### Run Scraper Only (Without Cleaning)
```bash
python scripts/run_spider.py
```

### Clean Existing Data
```bash
python scripts/run_spider.py --clean
```

### Full Validation Check
```bash
python scripts/validate_setup.py
```

### Monitor Logs in Real-Time
```bash
# Windows
type logs\spider.log | tail -n 50

# Linux/Mac
tail -f logs/spider.log
```

### Check Scheduled Task Status
```bash
# Windows
schtasks /query /tn "SECE-WebScraper-Weekly" /v

# Linux
crontab -l | grep sece
```

### View Data Statistics
```bash
# Total items
find data\raw -name "*.jsonl" -exec wc -l {} +

# Data size
dir /s data\
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'scrapy'` | Run: `pip install -r requirements.txt` |
| `Playwright browsers not found` | Run: `python -m playwright install chromium` |
| `No items collected` | Check logs: `type logs\spider.log` |
| Scheduler doesn't run | Check: Task Scheduler UI, verify path to Python |
| OCR returns empty text | Website may need JS enabled; spider uses Playwright |
| Memory issues | Reduce concurrent requests in `settings.py` |

### Get Help
1. Check logs: `logs/spider.log` and `logs/weekly_schedule.log`
2. Run validation: `python scripts/validate_setup.py`
3. Review: `IMPLEMENTATION_GUIDE.md` for advanced configuration

---

## 📈 Performance Tips

- **First Run**: 5-10 minutes (depends on site size)
- **Subsequent Runs**: Data appends, same time
- **OCR Processing**: 2-5 seconds per image (GPU optional)
- **Data Cleaning**: <1 second per 1000 items

### Optimization
```python
# In sece_scraper/settings.py
CONCURRENT_REQUESTS = 8         # Increase for faster crawling
DOWNLOAD_TIMEOUT = 60           # Increase if network is slow
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Complete reference documentation |
| `QUICKSTART.md` | 5-minute quick start |
| `IMPLEMENTATION_GUIDE.md` | Advanced configuration and customization |
| `SETUP_INSTRUCTIONS.md` | This file - phase-by-phase guide |

---

## 🎓 Learning Path

1. **Beginner**: Follow QUICKSTART.md (5 min)
2. **Intermediate**: Run full spider and analyze data
3. **Advanced**: Customize selectors and rules in IMPLEMENTATION_GUIDE.md
4. **Expert**: Extend spider for new data types

---

## 📞 Support & Resources

### Online Resources
- Scrapy Documentation: https://docs.scrapy.org/
- Playwright Guide: https://playwright.dev/python/
- PyMuPDF Docs: https://pymupdf.readthedocs.io/
- EasyOCR Guide: https://github.com/JaidedAI/EasyOCR

### Debugging
```bash
# Enable debug mode
set SCRAPY_LOGLEVEL=DEBUG
python scripts/run_spider.py

# Validate data
python scripts/validate_setup.py

# Analyze results
python scripts/analyze_data.py --all
```

---

## 🎯 Next Steps

1. ✅ Complete 5-minute quick start above
2. ✅ Run: `python scripts/analyze_data.py --all`
3. ✅ Setup automation: `scripts/schedule_cron.bat install` (Windows)
4. ✅ Monitor first scheduled run: Check `logs/weekly_schedule.log`
5. ✅ Fine-tune settings if needed (see IMPLEMENTATION_GUIDE.md)

---

## 📝 Notes

- Data is stored in JSONL format (one JSON object per line)
- Each line is a valid JSON object
- Ideal for LLM training and fine-tuning
- Automatic deduplication prevents duplicate content
- Boilerplate removal ensures clean data

---

## ⚖️ Legal & Ethical Usage

Ensure compliance with:
- SECE website's `robots.txt` and terms of service
- Data protection regulations (GDPR, etc.)
- Copyright laws for extracted content
- Fair use principles for automated access

---

**Setup Version**: 1.0  
**Last Updated**: 2024-05-14  
**Status**: Production Ready ✅

---

## 🎉 You're All Set!

Your SECE CSE Department Deep Web Scraper is now ready to use.

### To get started:
```bash
cd c:\Users\Kanishka\Desktop\bot
python scripts/run_spider.py --clean
```

Happy scraping! 🚀
