import requests
from lxml import html as lxml_html

url = 'https://sece.ac.in/department-computer-science-engineering-2/'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers, timeout=10)
tree = lxml_html.fromstring(response.content)

# Test selector
faculty_items = tree.xpath('//div[@class="elementor-widget-container"]/h2[a[contains(text(), "Dr.") or contains(text(), "Mr.") or contains(text(), "Ms.") or contains(text(), "Prof")]]/..')
print(f'Faculty items found: {len(faculty_items)}')

# Find HOD
hod_heading = tree.xpath('//h2[text()="Head of the department"]')
if hod_heading:
    print('Found HOD heading')
    
# Summary
print(f'\n✓ Total faculty h2 headings (should be 20+): {len(tree.xpath("//h2[a]"))}')
print(f'✓ Faculty names in links: {len(tree.xpath("//a[contains(text(), \"Dr.\") or contains(text(), \"Mr.\") or contains(text(), \"Ms.\")]"))}')
