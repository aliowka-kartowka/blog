#!/usr/bin/env python3
"""
Script to fetch cached pages from Google Cache and save them locally.
"""

import os
import re
import requests
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup
import time

def fetch_google_cache(url):
    """
    Fetch a page from Google's cache.
    
    Args:
        url: The original URL to fetch from cache
        
    Returns:
        HTML content or None if not found
    """
    cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{quote(url)}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(cache_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Successfully fetched: {url}")
            return response.text
        else:
            print(f"❌ Failed to fetch: {url} (Status: {response.status_code})")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def clean_cached_html(html_content):
    """
    Clean up Google cache artifacts from HTML.
    
    Args:
        html_content: Raw HTML from Google cache
        
    Returns:
        Cleaned HTML content
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove Google cache header/banner
    for element in soup.find_all(['div', 'table'], {'style': lambda x: x and 'background' in x}):
        element.decompose()
    
    # Remove Google cache styling
    for style in soup.find_all('style'):
        if 'google' in str(style).lower():
            style.decompose()
    
    return str(soup)

def save_page(html_content, output_path):
    """
    Save HTML content to a file.
    
    Args:
        html_content: HTML to save
        output_path: Path to save the file
    """
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"💾 Saved to: {output_path}")

def extract_links_from_html(html_content, base_domain):
    """
    Extract internal links from HTML content.
    
    Args:
        html_content: HTML to parse
        base_domain: Base domain to filter links
        
    Returns:
        Set of URLs
    """
    if not html_content:
        return set()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if base_domain in href or href.startswith('/'):
            links.add(href)
    
    return links

def main():
    """Main function to orchestrate the cache recovery."""
    
    # Configuration
    DOMAIN = "alexeyvishnevsky.com"
    OUTPUT_DIR = "restored-blog"
    
    print(f"🔍 Starting cache recovery for {DOMAIN}")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("-" * 60)
    
    # List of URLs to fetch (you'll need to add more)
    urls_to_fetch = [
        f"https://{DOMAIN}",
        f"https://{DOMAIN}/index.html",
        # Add more URLs as you discover them from Google search
    ]
    
    fetched_urls = set()
    
    for url in urls_to_fetch:
        if url in fetched_urls:
            continue
        
        print(f"\n📥 Fetching: {url}")
        
        # Fetch from cache
        html_content = fetch_google_cache(url)
        
        if html_content:
            # Clean the HTML
            cleaned_html = clean_cached_html(html_content)
            
            # Determine output path
            parsed = urlparse(url)
            path = parsed.path.strip('/') or 'index.html'
            
            if not path.endswith('.html'):
                path = os.path.join(path, 'index.html')
            
            output_path = os.path.join(OUTPUT_DIR, path)
            
            # Save the page
            save_page(cleaned_html, output_path)
            
            fetched_urls.add(url)
            
            # Extract more links to fetch
            # new_links = extract_links_from_html(cleaned_html, DOMAIN)
            # urls_to_fetch.extend(new_links)
        
        # Be nice to Google's servers
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"✅ Recovery complete! Pages saved to: {OUTPUT_DIR}/")
    print(f"📊 Total pages fetched: {len(fetched_urls)}")
    print("\nNext steps:")
    print("1. Review the fetched pages")
    print("2. Add more URLs to urls_to_fetch list if needed")
    print("3. Create GitHub Pages repository")
    print("4. Push the restored content")

if __name__ == "__main__":
    main()
