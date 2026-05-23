#!/usr/bin/env python
"""Deep analysis to find actual CSS selectors used by website"""

import requests
from lxml import html as lxml_html
from lxml import etree
import re

url = 'https://sece.ac.in/department-computer-science-engineering-2/'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers, timeout=10)

# Get raw HTML content
raw_html = response.text

# Search for faculty member patterns in HTML
print('=== SEARCHING FOR FACULTY PATTERNS IN HTML ===')

# Find faculty names and their context
faculty_names = ['Dr.H.Anandakumar', 'Dr.V.S.Akshaya', 'Dr.S.Sampath Kumar']
for name in faculty_names[:1]:
    if name in raw_html:
        idx = raw_html.find(name)
        # Look at 500 chars before to find container
        before = raw_html[max(0, idx-500):idx]
        after = raw_html[idx:idx+200]
        
        # Find opening div tag before the name
        div_starts = [m.start() for m in re.finditer(r'<div[^>]*>', before)]
        if div_starts:
            last_div_start = div_starts[-1]
            context = before[last_div_start:] + after
            print(f'\n{name} context:')
            print(context[:700])
            
            # Extract class from the div
            class_match = re.search(r'<div[^>]*class="([^"]*)"', context)
            if class_match:
                print(f'\nDiv class: {class_match.group(1)}')

# Parse with lxml
tree = lxml_html.fromstring(response.content)

# Find elements by text content
print('\n\n=== FINDING ACTUAL CONTAINERS ===')
anandakumar = tree.xpath('//text()[contains(., "Dr.H.Anandakumar")]')
if anandakumar:
    elem = anandakumar[0]
    parent = elem.getparent()
    grandparent = parent.getparent()
    ggp = grandparent.getparent()
    
    print(f'Text element: {elem.text}')
    print(f'Parent (immediate): {parent.tag}, class={parent.get("class", "")}')
    print(f'Grandparent: {grandparent.tag}, class={grandparent.get("class", "")}')
    print(f'Great-grandparent: {ggp.tag}, class={ggp.get("class", "")}')
    
    print(f'\nGrandparent HTML:')
    print(etree.tostring(grandparent, encoding='unicode', pretty_print=True)[:500])

# Try to find all similar containers
print('\n\n=== FINDING ALL FACULTY ITEM CONTAINERS ===')
faculty_containers = tree.xpath('//*[h2[contains(text(), "Dr.") or contains(text(), "Mr.") or contains(text(), "Ms.")]]')
print(f'Containers with faculty heading found: {len(faculty_containers[:10])}')

if faculty_containers:
    print(f'First container class: {faculty_containers[0].get("class", "")}')

print('\n✓ Analysis complete')
