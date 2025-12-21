import os
from bs4 import BeautifulSoup

# Test on one file
filepath = 'restored-blog-clean/index.html'

print(f"Testing cleanup on: {filepath}\n")

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()
    soup = BeautifulSoup(content, 'html.parser')

print(f"Original file size: {len(content)} bytes")
print(f"\nChecking for Wayback artifacts:")
print(f"  - Scripts with archive.org: {len([s for s in soup.find_all('script') if 'archive.org' in str(s)])}")
print(f"  - Links with archive.org: {len([l for l in soup.find_all('link') if 'archive.org' in str(l.get('href', ''))])}")
print(f"  - Links with alexeyvishnevsky.com CSS: {len([l for l in soup.find_all('link', rel='stylesheet') if 'alexeyvishnevsky.com' in str(l.get('href', ''))])}")

# Count CSS links
css_links = soup.find_all('link', rel='stylesheet')
print(f"\nTotal CSS link tags: {len(css_links)}")
for i, link in enumerate(css_links[:5], 1):
    print(f"  {i}. {link.get('href', 'NO HREF')[:80]}")

