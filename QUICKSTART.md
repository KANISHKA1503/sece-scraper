# SECE Deep Web Scraper - Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies (2 minutes)
```bash
cd c:\Users\Kanishka\Desktop\bot
pip install -r requirements.txt
python -m playwright install chromium
```

### 2. Run Your First Scrape (3 minutes)
```bash
python scripts/run_spider.py --clean
```

**What happens:**
- Scrapes SECE CSE department pages
- Extracts PDF syllabi and converts Google Drive links
- Performs OCR on event images
- Cleans and stores data in JSONL format
- Outputs: `data/raw/weekly_data.jsonl` and `data/cleaned/cleaned_data.jsonl`

## Daily Operations

### Analyze Collected Data
```bash
python scripts/analyze_data.py --all
```

Shows:
- Total items collected
- Breakdown by type (syllabus, event, achievement)
- Sample content preview
- Duplicate detection

### Check Data Files
```bash
# Windows
type data\raw\weekly_data.jsonl | find /c "^"  :: Count items

# Linux/Mac
wc -l data/raw/weekly_data.jsonl
```

## Weekly Automation

### Windows (Recommended)
```bash
cd scripts
schedule_cron.bat install
```

Verify:
```bash
tasklist /FI "TASKNAME eq SECE-WebScraper-Weekly"
```

### Linux/Mac
```bash
bash scripts/schedule_cron.sh install

# Verify
bash scripts/schedule_cron.sh check
```

## Troubleshooting Checklist

### ✓ Installation
- [ ] Python 3.8+ installed: `python --version`
- [ ] Requirements installed: `pip list | findstr scrapy`
- [ ] Playwright browsers: `python -m playwright install chromium`

### ✓ First Run
- [ ] Can navigate to project: `cd c:\Users\Kanishka\Desktop\bot`
- [ ] Logs directory exists: `ls logs/`
- [ ] Can import modules: `python -c "import sece_scraper"`

### ✓ Data Collection
- [ ] Raw data file created: `ls data/raw/weekly_data.jsonl`
- [ ] Contains items: `wc -l data/raw/weekly_data.jsonl` > 0
- [ ] Cleaned data file: `ls data/cleaned/cleaned_data.jsonl`

### ✓ Automation
- [ ] Scheduled task created: Windows Task Scheduler shows "SECE-WebScraper-Weekly"
- [ ] Log file updated: `data_modified(logs/weekly_schedule.log) is recent`

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'scrapy'` | Run: `pip install -r requirements.txt` |
| `TimeoutError` on PDF download | Increase timeout in `sece_scraper/settings.py` |
| No images in OCR output | Website may require JavaScript; Playwright handles this |
| Task Scheduler not running | Check script path and Python executable location |
| Memory issues with OCR | Process images in batches; use GPU: `pip install torch --cu...` |

## File Structure Summary

```
bot/
├── 📄 requirements.txt          ← Install dependencies
├── 📄 README.md                 ← Full documentation
├── 📄 QUICKSTART.md             ← This file
│
├── 📁 sece_scraper/
│   ├── sece_master_spider.py    ← Main crawler
│   ├── pdf_processor.py         ← PDF extraction
│   ├── image_processor.py       ← OCR processing
│   └── data_cleaner.py          ← Data preparation
│
├── 📁 scripts/
│   ├── run_spider.py            ← Execute: python run_spider.py --clean
│   ├── analyze_data.py          ← Execute: python analyze_data.py --all
│   ├── schedule_cron.bat        ← Windows automation (execute: schedule_cron.bat install)
│   └── schedule_cron.sh         ← Linux automation (execute: bash schedule_cron.sh install)
│
└── 📁 data/
    ├── raw/                     ← Raw scraped data (JSONL)
    └── cleaned/                 ← AI-training ready data (JSONL)
```

## Next Steps

1. ✅ Run first scrape: `python scripts/run_spider.py --clean`
2. ✅ Analyze results: `python scripts/analyze_data.py --all`
3. ✅ Setup automation: Windows → `schedule_cron.bat install` / Linux → `bash schedule_cron.sh install`
4. ✅ Monitor logs: `logs/spider.log` and `logs/weekly_schedule.log`

## Performance Expectations

| Operation | Time |
|-----------|------|
| First run (full scrape) | 5-10 minutes |
| PDF extraction | 1-2 sec per PDF |
| Image OCR | 2-5 sec per image |
| Data cleaning | <1 sec per 1000 items |
| Subsequent runs (append) | 5-10 minutes |

## Success Indicators

✅ All of these should be true:
1. `data/raw/weekly_data.jsonl` exists and contains items
2. `data/cleaned/cleaned_data.jsonl` exists with cleaned items
3. `logs/spider.log` shows successful execution
4. No error messages in console output
5. Scheduled task runs automatically (check logs after first scheduled run)

## Data Format Example

```json
{"instruction": "What is included in the 2023 CSE syllabus?", "context": "CSE Syllabus 2023: Module 1 covers...", "type": "syllabus", "metadata": {}}
{"instruction": "List recent CSE student achievements.", "context": "Achievement: Student Name received award...", "type": "achievement", "metadata": {}}
```

---

**Need help?** Check README.md for detailed documentation.
