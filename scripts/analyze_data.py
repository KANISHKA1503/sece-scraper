#!/usr/bin/env python3
"""
Data analysis and statistics tool for SECE scraper
Usage: python scripts/analyze_data.py [--file FILE] [--stats] [--types] [--sample N]
"""

import json
import sys
import os
import argparse
from collections import Counter
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sece_scraper.utils.storage import JSONLStorage

def analyze_file(file_path):
    """Load and analyze JSONL file"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    items = JSONLStorage.read_jsonl(file_path)
    print(f"✓ Loaded {len(items)} items from {file_path}\n")
    return items

def print_statistics(items):
    """Print data statistics"""
    if not items:
        print("No items to analyze")
        return
    
    print("=" * 60)
    print("DATA STATISTICS")
    print("=" * 60)
    
    # Basic stats
    total_items = len(items)
    total_size = sum(len(json.dumps(item)) for item in items)
    
    print(f"Total items:        {total_items}")
    print(f"Total size (bytes): {total_size:,}")
    print(f"Average item size:  {total_size // total_items if total_items else 0:,}")
    
    # Type breakdown
    types = Counter(item.get('type', 'unknown') for item in items)
    print(f"\nTypes distribution:")
    for item_type, count in types.most_common():
        percentage = (count / total_items * 100)
        print(f"  {item_type:20s}: {count:5d} ({percentage:5.1f}%)")
    
    # Content length analysis
    data_lengths = [len(item.get('data', '')) for item in items if 'data' in item]
    if data_lengths:
        print(f"\nContent length statistics:")
        print(f"  Min:    {min(data_lengths):,} characters")
        print(f"  Max:    {max(data_lengths):,} characters")
        print(f"  Mean:   {sum(data_lengths) // len(data_lengths):,} characters")
        print(f"  Total:  {sum(data_lengths):,} characters")
    
    # Timestamp analysis
    if items and 'timestamp' in items[0]:
        timestamps = [item.get('timestamp') for item in items if 'timestamp' in item]
        if timestamps:
            print(f"\nTimestamp range:")
            print(f"  First:  {min(timestamps)}")
            print(f"  Last:   {max(timestamps)}")
    
    print("\n" + "=" * 60)

def print_type_breakdown(items):
    """Print detailed type breakdown"""
    if not items:
        return
    
    print("=" * 60)
    print("TYPE BREAKDOWN")
    print("=" * 60)
    
    types = {}
    for item in items:
        item_type = item.get('type', 'unknown')
        if item_type not in types:
            types[item_type] = []
        types[item_type].append(item)
    
    for item_type in sorted(types.keys()):
        items_of_type = types[item_type]
        print(f"\n{item_type.upper()} ({len(items_of_type)} items):")
        
        if items_of_type:
            # Show sample
            sample = items_of_type[0]
            print(f"  Source:     {sample.get('source_url', 'N/A')[:60]}...")
            data = sample.get('data', '')
            preview = data[:100].replace('\n', ' ') + ('...' if len(data) > 100 else '')
            print(f"  Preview:    {preview}")
            print(f"  Size:       {len(data):,} characters")

def print_sample(items, num_samples=3):
    """Print sample items"""
    if not items:
        return
    
    print("=" * 60)
    print(f"SAMPLE ITEMS (showing first {min(num_samples, len(items))})")
    print("=" * 60)
    
    for i, item in enumerate(items[:num_samples], 1):
        print(f"\nItem {i}:")
        print(f"  Type:      {item.get('type', 'unknown')}")
        print(f"  URL:       {item.get('source_url', 'N/A')[:60]}...")
        
        data = item.get('data', '')
        if len(data) > 200:
            preview = data[:200] + "..."
        else:
            preview = data
        
        preview = preview.replace('\n', ' ')
        print(f"  Data:      {preview}")
        print(f"  Size:      {len(data):,} characters")
        print(f"  Timestamp: {item.get('timestamp', 'N/A')}")

def deduplicate_check(items):
    """Check for potential duplicates"""
    if not items:
        return
    
    print("=" * 60)
    print("DUPLICATION CHECK")
    print("=" * 60)
    
    hashes = {}
    duplicates = []
    
    for idx, item in enumerate(items):
        data = item.get('data', '')
        data_hash = hash(data)
        
        if data_hash in hashes:
            duplicates.append((hashes[data_hash], idx))
        else:
            hashes[data_hash] = idx
    
    if duplicates:
        print(f"\n⚠ Found {len(duplicates)} potential duplicates:")
        for orig_idx, dup_idx in duplicates[:5]:  # Show first 5
            print(f"  Item {dup_idx} is duplicate of Item {orig_idx}")
        if len(duplicates) > 5:
            print(f"  ... and {len(duplicates) - 5} more")
    else:
        print("\n✓ No duplicates found")

def main():
    parser = argparse.ArgumentParser(
        description='Analyze SECE scraper data'
    )
    
    parser.add_argument(
        '--file', '-f',
        default='data/raw/weekly_data.jsonl',
        help='Path to JSONL file (default: data/raw/weekly_data.jsonl)'
    )
    
    parser.add_argument(
        '--stats', '-s',
        action='store_true',
        help='Show statistics'
    )
    
    parser.add_argument(
        '--types', '-t',
        action='store_true',
        help='Show type breakdown'
    )
    
    parser.add_argument(
        '--sample', '-n',
        type=int,
        default=3,
        help='Show N sample items (default: 3)'
    )
    
    parser.add_argument(
        '--duplicates', '-d',
        action='store_true',
        help='Check for duplicates'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all analyses'
    )
    
    args = parser.parse_args()
    
    # Load data
    items = analyze_file(args.file)
    if not items:
        sys.exit(1)
    
    # Run analyses
    if args.all or args.stats:
        print_statistics(items)
    
    if args.all or args.types:
        print_type_breakdown(items)
    
    if args.all or args.sample:
        print_sample(items, args.sample)
    
    if args.all or args.duplicates:
        deduplicate_check(items)
    
    # Default: show stats if no option specified
    if not (args.stats or args.types or args.sample or args.duplicates or args.all):
        print_statistics(items)

if __name__ == "__main__":
    main()
