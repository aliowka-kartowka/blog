#!/usr/bin/env python3
"""
Comprehensive blog restoration script that discovers and fetches pages
from multiple sources: Google Cache, Internet Archive, and Google search history.
"""

import os
import re
import json
import requests
from urllib.parse import quote, urlparse, urljoin
from bs4 import BeautifulSoup
import time
from datetime import datetime

class BlogRestorer:
    def __init__(self, domain):
        self.domain = domain
        self.output_dir = "restored-blog"
        self.discovered_urls = set()
        self.fetched_urls = set()
        
    def search_google(self):
        """Search Google for cached pages."""
        print(f"\n🔍 Searching Google for {self.domain} pages...")
        
        # Common blog page patterns
        patterns = [
            "",
            "index.html",
            "about",
            "about.html",
            "blog",
            "blog.html",
            "posts",
            "archive",
            "contact",
            "contact.html",
            "sitemap.xml",
            "robots.txt",
        ]
        
        for pattern in patterns:
            if pattern:
                url = f"https://{self.domain}/{pattern}"
            else:
                url = f"https://{self.domain}"
            
            self.discovered_urls.add(url)
            print(f"  Added: {url}")
        
        return self.discovered_urls
    
    def check_wayback_machine(self):
        """Check Internet Archive for available snapshots."""
        print(f"\n📚 Checking Internet Archive for {self.domain}...")
        
        api_url = f"http://archive.org/wayback/available?url={self.domain}"
        
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('archived_snapshots', {}).get('closest'):
                    snapshot = data['archived_snapshots']['closest']
                    wayback_url = snapshot.get('url')
                    timestamp = snapshot.get('timestamp')
                    
                    if wayback_url:
                        print(f"  ✅ Found snapshot from {timestamp}")
                        print(f"  URL: {wayback_url}")
                        
                        # Get the calendar view to find all snapshots
                        calendar_url = f"https://web.archive.org/web/*/{self.domain}"
                        print(f"  View all: {calendar_url}")
                        
                        return wayback_url
                else:
                    print("  ⚠️  No snapshots found")
            else:
                print(f"  ⚠️  Could not access Archive API")
        except Exception as e:
            print(f"  ⚠️  Error: {e}")
        
        return None
    
    def fetch_from_google_cache(self, url):
        """Fetch a page from Google's cache."""
        cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{quote(url)}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(cache_url, headers=headers, timeout=30)
            
            if response.status_code == 200 and len(response.text) > 1000:
                return response.text
            else:
                return None
                
        except Exception as e:
            print(f"    Error: {e}")
            return None
    
    def fetch_from_wayback(self, url):
        """Fetch a page from Internet Archive."""
        api_url = f"http://archive.org/wayback/available?url={url}"
        
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('archived_snapshots', {}).get('closest'):
                    wayback_url = data['archived_snapshots']['closest'].get('url')
                    
                    if wayback_url:
                        # Fetch the actual content
                        content_response = requests.get(wayback_url, timeout=30)
                        if content_response.status_code == 200:
                            return content_response.text
        except Exception as e:
            print(f"    Error: {e}")
        
        return None
    
    def clean_html(self, html_content, source="cache"):
        """Clean up HTML from cache artifacts."""
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        if source == "cache":
            # Remove Google cache elements
            for element in soup.find_all(['div', 'table'], {'style': lambda x: x and 'background' in x}):
                element.decompose()
            
            # Remove Google cache scripts
            for script in soup.find_all('script'):
                if 'google' in str(script).lower():
                    script.decompose()
        
        elif source == "wayback":
            # Remove Wayback Machine toolbar
            for element in soup.find_all(id=re.compile('wm-', re.I)):
                element.decompose()
            
            for element in soup.find_all(class_=re.compile('wayback', re.I)):
                element.decompose()
            
            # Remove Wayback scripts
            for script in soup.find_all('script'):
                if 'archive.org' in str(script) or 'wayback' in str(script).lower():
                    script.decompose()
        
        return str(soup)
    
    def save_page(self, html_content, url):
        """Save HTML content to file."""
        parsed = urlparse(url)
        path = parsed.path.strip('/') or 'index.html'
        
        if not path.endswith('.html') and not path.endswith('.xml') and not path.endswith('.txt'):
            path = os.path.join(path, 'index.html')
        
        output_path = os.path.join(self.output_dir, path)
        os.makedirs(os.path.dirname(output_path) or self.output_dir, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"    💾 Saved to: {output_path}")
        return output_path
    
    def extract_links(self, html_content):
        """Extract links from HTML to discover more pages."""
        if not html_content:
            return set()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # Convert relative URLs to absolute
            if href.startswith('/'):
                href = f"https://{self.domain}{href}"
            
            # Only keep URLs from the same domain
            if self.domain in href:
                # Remove fragments and query strings for discovery
                clean_url = href.split('#')[0].split('?')[0]
                links.add(clean_url)
        
        return links
    
    def restore(self):
        """Main restoration process."""
        print("=" * 70)
        print(f"🚀 BLOG RESTORATION FOR {self.domain}")
        print("=" * 70)
        
        # Step 1: Discover URLs
        self.search_google()
        wayback_url = self.check_wayback_machine()
        
        # Step 2: Try to fetch and discover more URLs
        print(f"\n📥 Fetching discovered pages...")
        print("-" * 70)
        
        all_urls = list(self.discovered_urls)
        attempts = 0
        max_attempts = 50  # Limit to prevent infinite loops
        
        while all_urls and attempts < max_attempts:
            url = all_urls.pop(0)
            
            if url in self.fetched_urls:
                continue
            
            attempts += 1
            print(f"\n[{attempts}] Fetching: {url}")
            
            # Try Google Cache first
            print("  Trying Google Cache...")
            html_content = self.fetch_from_google_cache(url)
            source = "cache"
            
            # If cache fails, try Wayback Machine
            if not html_content:
                print("  Trying Internet Archive...")
                html_content = self.fetch_from_wayback(url)
                source = "wayback"
            
            if html_content:
                print(f"  ✅ Success ({source})")
                
                # Clean the HTML
                cleaned_html = self.clean_html(html_content, source)
                
                # Save the page
                self.save_page(cleaned_html, url)
                self.fetched_urls.add(url)
                
                # Extract and add new links
                new_links = self.extract_links(cleaned_html)
                for link in new_links:
                    if link not in self.fetched_urls and link not in all_urls:
                        all_urls.append(link)
                        print(f"    🔗 Discovered: {link}")
                
                # Be nice to servers
                time.sleep(1)
            else:
                print("  ❌ Not found in cache or archive")
        
        # Step 3: Summary
        print("\n" + "=" * 70)
        print("📊 RESTORATION SUMMARY")
        print("=" * 70)
        print(f"✅ Successfully fetched: {len(self.fetched_urls)} pages")
        print(f"📁 Output directory: {self.output_dir}/")
        print(f"🌐 Discovered URLs: {len(self.discovered_urls)}")
        
        if self.fetched_urls:
            print(f"\n📄 Fetched pages:")
            for url in sorted(self.fetched_urls):
                print(f"  - {url}")
        
        # Save URL list for reference
        urls_file = os.path.join(self.output_dir, "fetched_urls.txt")
        with open(urls_file, 'w') as f:
            f.write('\n'.join(sorted(self.fetched_urls)))
        print(f"\n💾 URL list saved to: {urls_file}")
        
        print("\n🎉 Restoration complete!")
        print("\nNext steps:")
        print("1. Review the fetched content in the 'restored-blog/' directory")
        print("2. Create a GitHub Pages repository")
        print("3. Push the content to deploy your blog")

def main():
    domain = "alexeyvishnevsky.com"
    restorer = BlogRestorer(domain)
    restorer.restore()

if __name__ == "__main__":
    main()
