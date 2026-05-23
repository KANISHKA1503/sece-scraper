#!/usr/bin/env python3
"""
Quick test script to verify spider can run without full execution
Usage: python scripts/quick_test.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...")
    
    try:
        import scrapy
        print("  ✓ scrapy")
    except ImportError as e:
        print(f"  ✗ scrapy: {e}")
        return False
    
    try:
        from scrapy_playwright.page import PageMethod
        print("  ✓ scrapy_playwright")
    except ImportError as e:
        print(f"  ✗ scrapy_playwright: {e}")
        return False
    
    try:
        import fitz
        print("  ✓ PyMuPDF (fitz)")
    except ImportError as e:
        print(f"  ✗ PyMuPDF: {e}")
        return False
    
    try:
        import easyocr
        print("  ✓ easyocr")
    except ImportError as e:
        print(f"  ✗ easyocr: {e}")
        return False
    
    try:
        from sece_scraper.spiders.sece_master_spider import SECEMasterSpider
        print("  ✓ SECEMasterSpider")
    except ImportError as e:
        print(f"  ✗ SECEMasterSpider: {e}")
        return False
    
    try:
        from sece_scraper.helpers.pdf_processor import PDFProcessor
        print("  ✓ PDFProcessor")
    except ImportError as e:
        print(f"  ✗ PDFProcessor: {e}")
        return False
    
    try:
        from sece_scraper.helpers.image_processor import ImageProcessor
        print("  ✓ ImageProcessor")
    except ImportError as e:
        print(f"  ✗ ImageProcessor: {e}")
        return False
    
    try:
        from sece_scraper.helpers.data_cleaner import DataCleaner
        print("  ✓ DataCleaner")
    except ImportError as e:
        print(f"  ✗ DataCleaner: {e}")
        return False
    
    try:
        from sece_scraper.utils.storage import JSONLStorage
        print("  ✓ JSONLStorage")
    except ImportError as e:
        print(f"  ✗ JSONLStorage: {e}")
        return False
    
    return True

def test_pdf_processor():
    """Test PDF processor functions"""
    print("\nTesting PDF Processor...")
    
    try:
        from sece_scraper.helpers.pdf_processor import PDFProcessor
        
        # Test link conversion
        test_url = "https://drive.google.com/file/d/ABC123/view"
        converted = PDFProcessor.convert_drive_link(test_url)
        expected = "https://drive.google.com/uc?export=download&id=ABC123"
        
        if converted == expected:
            print("  ✓ Google Drive link conversion works")
        else:
            print(f"  ✗ Link conversion: got {converted}, expected {expected}")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_data_cleaner():
    """Test data cleaner functions"""
    print("\nTesting Data Cleaner...")
    
    try:
        from sece_scraper.helpers.data_cleaner import DataCleaner
        
        # Test boilerplate removal
        text = "Header\nAdmission Open\nMain content here\nPrivacy Policy"
        cleaned = DataCleaner.remove_boilerplate(text)
        
        if "Admission" not in cleaned and "Main content" in cleaned:
            print("  ✓ Boilerplate removal works")
        else:
            print("  ✗ Boilerplate removal didn't work as expected")
            return False
        
        # Test whitespace normalization
        text = "text  with   multiple    spaces"
        normalized = DataCleaner.normalize_whitespace(text)
        
        if "  " not in normalized:
            print("  ✓ Whitespace normalization works")
        else:
            print("  ✗ Whitespace normalization didn't work")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_storage():
    """Test storage functions"""
    print("\nTesting Storage...")
    
    try:
        from sece_scraper.utils.storage import JSONLStorage
        import tempfile
        import os
        
        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            temp_file = f.name
        
        try:
            # Test append
            item = {"type": "test", "data": "test content"}
            JSONLStorage.append_to_jsonl(temp_file, item)
            print("  ✓ JSONL append works")
            
            # Test read
            items = JSONLStorage.read_jsonl(temp_file)
            if len(items) == 1 and items[0]['type'] == 'test':
                print("  ✓ JSONL read works")
            else:
                print("  ✗ JSONL read didn't return expected data")
                return False
            
            # Test stats
            stats = JSONLStorage.get_file_stats(temp_file)
            if stats['lines'] == 1:
                print("  ✓ JSONL stats works")
            else:
                print("  ✗ JSONL stats incorrect")
                return False
            
            return True
        finally:
            os.unlink(temp_file)
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_directory_structure():
    """Test if directory structure exists"""
    print("\nTesting Directory Structure...")
    
    required_dirs = [
        'data/raw',
        'data/cleaned',
        'logs',
        'scripts',
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/ missing")
            all_ok = False
    
    return all_ok

def main():
    print("=" * 60)
    print("SECE SCRAPER - QUICK TEST")
    print("=" * 60)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("PDF Processor", test_pdf_processor),
        ("Data Cleaner", test_data_cleaner),
        ("Storage", test_storage),
        ("Directory Structure", test_directory_structure),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} failed with exception: {e}")
            results.append((name, False))
    
    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    all_passed = all(r for _, r in results)
    
    print()
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYou can now run: python scripts/run_spider.py --clean")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease install missing dependencies: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
