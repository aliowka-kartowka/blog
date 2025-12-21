#!/usr/bin/env python3
"""Extract CSS files from Wayback Machine for alexeyvishnevsky.com"""

import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urlparse, urljoin

# Read one of the HTML files to get CSS URLs
html_file = 'restored-blog-clean/index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find all CSS links
css_links = soup.find_all('link', rel='stylesheet')
css_urls = []

print(f"Found {len(css_links)} CSS references\n")

for link in css_links:
    href = link.get('href', '')
    if 'web.archive.org' in href and 'alexeyvishnevsky.com' in href:
        # Extract the original URL from the Wayback URL
        match = re.search(r'web\.archive\.org/web/\d+cs_/(.*)', href)
        if match:
            original_url = match.group(1)
            # Clean up the URL
            original_url = original_url.replace('http://web.archive.org/web/20201130143950cs_/', '')
            if original_url.startswith('http://'):
                css_urls.append((href, original_url))
                print(f"CSS: {original_url}")

print(f"\n{'='*60}")
print(f"Total CSS files to fetch: {len(css_urls)}\n")

# Create CSS directory
os.makedirs('restored-blog-clean/css', exist_ok=True)

# Fetch each CSS file
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

successful = []
failed = []

for wayback_url, original_url in css_urls:
    filename = original_url.split('/')[-1].split('?')[0]
    
    # Determine subdirectory based on URL
    if 'themes/simple-style' in original_url:
        filepath = 'restored-blog-clean/css/theme-style.css'
    elif 'crayon' in original_url:
        filepath = f'restored-blog-clean/css/crayon-{filename}'
    else:
        filepath = f'restored-blog-clean/css/{filename}'
    
    print(f"Fetching: {filename}")
    print(f"  From: {wayback_url}")
    
    try:
        response = requests.get(wayback_url, headers=headers, timeout=15)
        if response.status_code == 200:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"  ✓ Saved to: {filepath}")
            successful.append(filename)
        else:
            print(f"  ✗ Failed with status {response.status_code}")
            failed.append(filename)
    except Exception as e:
        print(f"  ✗ Error: {e}")
        failed.append(filename)
    print()

print(f"\n{'='*60}")
print(f"Successfully fetched: {len(successful)} CSS files")
print(f"Failed: {len(failed)} CSS files")
if failed:
    print(f"\nFailed files:")
    for f in failed:
        print(f"  - {f}")
