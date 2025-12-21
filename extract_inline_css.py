#!/usr/bin/env python3
"""Extract all inline CSS and style blocks from HTML files"""

import os
from bs4 import BeautifulSoup
import re

def extract_css_from_html(html_path):
    """Extract all CSS from an HTML file"""
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    css_content = []
    
    # Extract inline style blocks
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            css_content.append(style_tag.string)
    
    return '\n\n'.join(css_content)

# Scan all HTML files in restored-blog-clean
html_files = []
for root, dirs, files in os.walk('restored-blog-clean'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

print(f"Found {len(html_files)} HTML files\n")

# Extract CSS from all files
all_css = []
for html_file in html_files[:5]:  # Sample first 5 files
    print(f"Extracting from: {html_file}")
    css = extract_css_from_html(html_file)
    if css:
        all_css.append(f"/* From {html_file} */\n{css}")
        print(f"  Found {len(css)} bytes of CSS")

# Combine and deduplicate CSS
combined_css = '\n\n'.join(all_css)

# Save to file
output_file = 'restored-blog-clean/css/extracted-inline.css'
os.makedirs('restored-blog-clean/css', exist_ok=True)
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(combined_css)

print(f"\n✓ Saved {len(combined_css)} bytes to {output_file}")
print(f"\nPreview (first 500 chars):")
print(combined_css[:500])
