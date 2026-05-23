#!/usr/bin/env python
"""Simple CSS selector finder"""

import requests
from lxml import html as lxml_html

url = 'https://sece.ac.in/department-computer-science-engineering-2/'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers, timeout=10)
tree = lxml_html.fromstring(response.content)

# Find faculty items by looking for h2 with faculty name links
print('=== CSS SELECTORS FOR FACULTY ===')

faculty_items = tree.xpath('//h2[a[contains(text(), "Dr.") or contains(text(), "Mr.") or contains(text(), "Ms.")]]')
print(f'Faculty heading items found: {len(faculty_items)}')

if faculty_items:
    # Check parent structure
    parent = faculty_items[0].getparent()
    gp = parent.getparent()
    ggp = gp.getparent()
    
    print(f'Immediate parent: {parent.tag} class={parent.get("class", "")}')
    print(f'Grandparent: {gp.tag} class={gp.get("class", "")}')
    print(f'Great-grandparent: {ggp.tag} class={ggp.get("class", "")}')

# Try CSS selector for faculty items
print('\n=== TESTING CSS SELECTORS ===')
selectors_to_test = [
    'h2 > a[href*="popup"]',
    '.elementor-widget-container h2',
    'h2[class*="heading"]',
    '.elementor-element h2',
    'div > h2 > a',
]

for sel in selectors_to_test:
    count = len(tree.cssselect(sel))
    if count > 20:  # Faculty section should have many items
        print(f'✓ {sel}: {count} items')

# Find the actual container that holds all faculty
print('\n=== FINDING FACULTY CONTAINER ===')
# Get all h2 with faculty names and find common parent
all_faculty_h2 = tree.xpath('//h2[contains(., "Dr.") or contains(., "Mr.") or contains(., "Ms.")]')
print(f'Total h2 with faculty names: {len(all_faculty_h2)}')

# Find the container for "FACULTY MEMBERS" section specifically
faculty_section_heading = tree.xpath('//h2[text()="FACULTY MEMBERS"]')
if faculty_section_heading:
    # Find all h2s that come after this heading and before the next major section
    print('Found FACULTY MEMBERS section')
    # All faculty items probably share a common ancestor after the heading
    
# Simply: look for all divs that contain h2 with faculty names as direct child
faculty_divs = tree.xpath('//div[h2[contains(text(), "Dr.") or contains(text(), "Mr.") or contains(text(), "Ms.")]]')
print(f'\nDivs containing faculty heading h2: {len(faculty_divs)}')

if faculty_divs:
    sample_div = faculty_divs[0]
    classes = sample_div.get('class', '')
    print(f'Sample div classes: {classes[:100]}')
    
# Try broader selector
print('\n=== SIMPLE XPATH THAT WORKS ===')
# All h2 after FACULTY MEMBERS heading
results = tree.xpath('//h2[text()="FACULTY MEMBERS"]/../..//*[self::div][h2[starts-with(., "Dr") or starts-with(., "Mr") or starts-with(., "Ms")]]')
print(f'Found with XPath: {len(results)}')

print('\n✓ Done')
