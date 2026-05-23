#!/usr/bin/env python3
"""
Validation script to check if SECE scraper is properly set up
Usage: python scripts/validate_setup.py
"""

import sys
import os
import importlib
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("[1/8] Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (Required: 3.8+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("[2/8] Checking dependencies...")
    
    required_packages = [
        'scrapy',
        'scrapy_playwright',
        'playwright',
        'fitz',  # PyMuPDF
        'easyocr',
        'cv2',  # OpenCV
        'PIL',  # Pillow
        'requests',
        'lxml',
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (NOT INSTALLED)")
            missing.append(package)
    
    if missing:
        print(f"\n  Install missing packages:")
        print(f"  pip install {' '.join(missing)}")
        return False
    return True

def check_playwright_browsers():
    """Check if Playwright browsers are installed"""
    print("[3/8] Checking Playwright browsers...")
    
    try:
        from playwright.async_api import async_playwright
        print("  ✓ Playwright module found")
        
        # Check for chromium
        browsers_path = Path.home() / ".cache" / "ms-playwright"
        if browsers_path.exists():
            print(f"  ✓ Playwright browsers found at {browsers_path}")
            return True
        else:
            print("  ✗ Playwright browsers not found")
            print("  Install with: python -m playwright install chromium")
            return False
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False

def check_project_structure():
    """Check if project structure is correct"""
    print("[4/8] Checking project structure...")
    
    required_dirs = [
        'sece_scraper',
        'sece_scraper/spiders',
        'sece_scraper/helpers',
        'sece_scraper/utils',
        'data/raw',
        'data/cleaned',
        'scripts',
        'logs',
    ]
    
    required_files = [
        'scrapy.cfg',
        'requirements.txt',
        'sece_scraper/__init__.py',
        'sece_scraper/settings.py',
        'sece_scraper/pipelines.py',
        'sece_scraper/spiders/sece_master_spider.py',
        'sece_scraper/helpers/pdf_processor.py',
        'sece_scraper/helpers/image_processor.py',
        'sece_scraper/helpers/data_cleaner.py',
        'sece_scraper/utils/storage.py',
        'scripts/run_spider.py',
        'scripts/analyze_data.py',
    ]
    
    all_ok = True
    
    # Check directories
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/ (NOT FOUND)")
            all_ok = False
    
    # Check files
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (NOT FOUND)")
            all_ok = False
    
    return all_ok

def check_imports():
    """Check if project modules can be imported"""
    print("[5/8] Checking project imports...")
    
    modules = [
        'sece_scraper',
        'sece_scraper.settings',
        'sece_scraper.pipelines',
        'sece_scraper.spiders.sece_master_spider',
        'sece_scraper.helpers.pdf_processor',
        'sece_scraper.helpers.image_processor',
        'sece_scraper.helpers.data_cleaner',
        'sece_scraper.utils.storage',
    ]
    
    sys.path.insert(0, os.getcwd())
    
    all_ok = True
    for module_name in modules:
        try:
            importlib.import_module(module_name)
            print(f"  ✓ {module_name}")
        except Exception as e:
            print(f"  ✗ {module_name}: {str(e)}")
            all_ok = False
    
    return all_ok

def check_file_permissions():
    """Check if scripts have execute permissions"""
    print("[6/8] Checking file permissions...")
    
    scripts = [
        'scripts/run_spider.py',
        'scripts/analyze_data.py',
    ]
    
    all_ok = True
    for script in scripts:
        if os.path.isfile(script):
            print(f"  ✓ {script}")
        else:
            print(f"  ✗ {script} (NOT FOUND)")
            all_ok = False
    
    return all_ok

def check_scrapy_project():
    """Verify Scrapy project is valid"""
    print("[7/8] Checking Scrapy project configuration...")
    
    try:
        from scrapy.utils.project import get_project_settings
        settings = get_project_settings()
        print(f"  ✓ Scrapy project found")
        print(f"  ✓ Spider modules: {settings.get('SPIDER_MODULES')}")
        print(f"  ✓ Raw data path: {settings.get('DATA_RAW_PATH')}")
        print(f"  ✓ Cleaned data path: {settings.get('DATA_CLEANED_PATH')}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False

def check_system_resources():
    """Check system resources"""
    print("[8/8] Checking system resources...")
    
    try:
        import psutil
        
        # RAM
        mem = psutil.virtual_memory()
        print(f"  ✓ Available RAM: {mem.available / (1024**3):.1f} GB")
        
        # Disk
        disk = psutil.disk_usage('.')
        print(f"  ✓ Free disk space: {disk.free / (1024**3):.1f} GB")
        
        return True
    except ImportError:
        print("  ⚠ psutil not available (optional)")
        return True

def main():
    print("=" * 60)
    print("SECE SCRAPER VALIDATION")
    print("=" * 60)
    print()
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_playwright_browsers(),
        check_project_structure(),
        check_imports(),
        check_file_permissions(),
        check_scrapy_project(),
        check_system_resources(),
    ]
    
    print()
    print("=" * 60)
    
    if all(checks):
        print("✓ ALL CHECKS PASSED - Ready to use!")
        print()
        print("Next steps:")
        print("  1. Run: python scripts/run_spider.py --clean")
        print("  2. Analyze: python scripts/analyze_data.py --all")
        print("  3. Setup automation: scripts/schedule_cron.bat install")
        return 0
    else:
        print("✗ SOME CHECKS FAILED - Please fix the issues above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
