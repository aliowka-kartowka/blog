#!/usr/bin/env python3
"""
URL Discovery Tool - Find all URLs from your blog that might be cached.
This script helps you build the list of URLs to fetch from cache.
"""

import os

def print_instructions():
    """Print instructions for finding cached URLs."""
    
    print("=" * 70)
    print("🔍 URL DISCOVERY TOOL FOR BLOG RESTORATION")
    print("=" * 70)
    print()
    
    print("Step 1: Search Google for cached pages")
    print("-" * 70)
    print("Search query: site:alexeyvishnevsky.com")
    print("URL: https://www.google.com/search?q=site:alexeyvishnevsky.com")
    print()
    
    print("Step 2: Check Internet Archive (Wayback Machine)")
    print("-" * 70)
    print("URL: https://web.archive.org/web/*/alexeyvishnevsky.com")
    print()
    
    print("Step 3: Try common blog URLs")
    print("-" * 70)
    
    common_urls = [
        "https://alexeyvishnevsky.com/",
        "https://alexeyvishnevsky.com/index.html",
        "https://alexeyvishnevsky.com/about",
        "https://alexeyvishnevsky.com/about.html",
        "https://alexeyvishnevsky.com/blog",
        "https://alexeyvishnevsky.com/blog.html",
        "https://alexeyvishnevsky.com/posts",
        "https://alexeyvishnevsky.com/archive",
        "https://alexeyvishnevsky.com/contact",
        "https://alexeyvishnevsky.com/contact.html",
    ]
    
    print("\nTry accessing these common URLs through Google Cache:")
    print()
    for url in common_urls:
        cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
        print(f"  {url}")
        print(f"  Cache: {cache_url}")
        print()
    
    print("Step 4: Create your URL list")
    print("-" * 70)
    print("After finding URLs, add them to fetch_cached_pages.py")
    print()
    
    print("Example:")
    print("""
urls_to_fetch = [
    'https://alexeyvishnevsky.com/',
    'https://alexeyvishnevsky.com/about',
    'https://alexeyvishnevsky.com/posts/my-first-post',
    'https://alexeyvishnevsky.com/posts/another-post',
    # Add more URLs here
]
    """)
    
    print()
    print("Step 5: Check for sitemap")
    print("-" * 70)
    print("Try these sitemap URLs:")
    sitemap_urls = [
        "https://alexeyvishnevsky.com/sitemap.xml",
        "https://alexeyvishnevsky.com/sitemap_index.xml",
        "https://alexeyvishnevsky.com/robots.txt",
    ]
    for url in sitemap_urls:
        print(f"  {url}")
        print(f"  Cache: https://webcache.googleusercontent.com/search?q=cache:{url}")
        print()
    
    print("=" * 70)
    print("💡 TIP: Create a file 'urls.txt' with one URL per line")
    print("=" * 70)
    print()

def create_url_template():
    """Create a template file for URLs."""
    
    template = """# Blog URLs to Restore
# Add one URL per line (remove # to uncomment)

# Homepage
https://alexeyvishnevsky.com/

# About page
# https://alexeyvishnevsky.com/about

# Blog posts (add your actual post URLs)
# https://alexeyvishnevsky.com/posts/post-title-1
# https://alexeyvishnevsky.com/posts/post-title-2
# https://alexeyvishnevsky.com/posts/post-title-3

# Archive/Category pages
# https://alexeyvishnevsky.com/archive
# https://alexeyvishnevsky.com/categories/tech

# Contact page
# https://alexeyvishnevsky.com/contact
"""
    
    with open('urls.txt', 'w') as f:
        f.write(template)
    
    print("✅ Created urls.txt template")
    print("📝 Edit this file and add your blog URLs")
    print()

def read_urls_from_file(filename='urls.txt'):
    """Read URLs from a file."""
    
    if not os.path.exists(filename):
        print(f"❌ File {filename} not found")
        return []
    
    urls = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                urls.append(line)
    
    return urls

def generate_fetch_script(urls):
    """Generate the URL list for fetch_cached_pages.py"""
    
    print("Copy this to fetch_cached_pages.py:")
    print("-" * 70)
    print("urls_to_fetch = [")
    for url in urls:
        print(f"    '{url}',")
    print("]")
    print("-" * 70)

def main():
    """Main function."""
    
    print_instructions()
    
    print("Options:")
    print("1) Create urls.txt template")
    print("2) Generate fetch script from urls.txt")
    print("3) Open Google search for your site")
    print("4) Exit")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == '1':
        create_url_template()
    elif choice == '2':
        urls = read_urls_from_file()
        if urls:
            print(f"\n✅ Found {len(urls)} URLs")
            generate_fetch_script(urls)
        else:
            print("❌ No URLs found. Create and edit urls.txt first.")
    elif choice == '3':
        import webbrowser
        webbrowser.open("https://www.google.com/search?q=site:alexeyvishnevsky.com")
        print("✅ Opened Google search in browser")
    elif choice == '4':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
