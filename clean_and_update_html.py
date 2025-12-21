#!/usr/bin/env python3
"""
Clean HTML files and update to use local CSS
Removes Wayback Machine artifacts and updates links
"""

import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def clean_html_file(filepath):
    """Clean a single HTML file"""
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    changes_made = False
    
    # Remove all Wayback Machine scripts
    for script in soup.find_all('script'):
        src = script.get('src', '')
        script_content = str(script.string) if script.string else ''
        if 'archive.org' in src or 'archive.org' in script_content or '__wm' in script_content:
            script.decompose()
            changes_made = True
    
    # Remove Wayback Machine stylesheets
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if 'archive.org' in href:
            link.decompose()
            changes_made = True
    
    # Remove Wayback toolbar div
    for div in soup.find_all('div', id=lambda x: x and 'wm' in x.lower()):
        div.decompose()
        changes_made = True
    
    # Calculate relative path to CSS
    depth = filepath.count('/') - filepath.count('restored-blog-clean/')
    css_path = '../' * (depth - 1) + 'css/main.css'
    
    # Add our custom CSS link in the head
    head = soup.find('head')
    if head:
        # Remove old WordPress CSS links
        for link in head.find_all('link', rel='stylesheet'):
            href = link.get('href', '')
            if 'alexeyvishnevsky.com' in href or 'wp-content' in href:
                link.decompose()
                changes_made = True
        
        # Add new CSS link
        new_css = soup.new_tag('link', rel='stylesheet', href=css_path, type='text/css')
        head.append(new_css)
        changes_made = True
    
    # Fix internal links - remove Wayback URLs
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'web.archive.org' in href:
            # Extract original URL
            match = re.search(r'alexeyvishnevsky\.com(/.*?)(?:\?|$|")', href)
            if match:
                new_href = match.group(1)
                # Make it relative
                if new_href.startswith('/'):
                    new_href = new_href[1:]
                a['href'] = new_href
                changes_made = True
        elif href.startswith('http://alexeyvishnevsky.com') or href.startswith('https://alexeyvishnevsky.com'):
            # Convert absolute to relative
            new_href = href.replace('http://alexeyvishnevsky.com/', '').replace('https://alexeyvishnevsky.com/', '')
            a['href'] = '/' + new_href if new_href else '/'
            changes_made = True
    
    # Fix image sources
    for img in soup.find_all('img', src=True):
        src = img['src']
        if 'web.archive.org' in src:
            # Try to extract original URL
            match = re.search(r'alexeyvishnevsky\.com(/.*?)(?:\s|$|")', src)
            if match:
                img['src'] = match.group(1)
                changes_made = True
    
    if changes_made:
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        return True
    
    return False

# Process all HTML files
html_files = []
for root, dirs, files in os.walk('restored-blog-clean'):
    # Skip the css directory
    if 'css' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

print(f"Found {len(html_files)} HTML files to clean\n")
print("Processing files...")
print("=" * 60)

cleaned = 0
for filepath in html_files:
    rel_path = filepath.replace('restored-blog-clean/', '')
    print(f"Cleaning: {rel_path}")
    
    if clean_html_file(filepath):
        cleaned += 1
        print(f"  ✓ Updated")
    else:
        print(f"  - No changes needed")

print("\n" + "=" * 60)
print(f"✓ Cleaned {cleaned} out of {len(html_files)} files")
print(f"✓ All files now use: css/main.css")
