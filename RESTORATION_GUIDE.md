# Blog Recovery & GitHub Pages Restoration Guide

This guide will help you restore your blog **alexeyvishnevsky.com** from Google Cache and deploy it as a GitHub Pages website.

## Table of Contents
1. [Finding Cached Pages](#finding-cached-pages)
2. [Fetching Content](#fetching-content)
3. [Setting Up GitHub Pages](#setting-up-github-pages)
4. [Deploying Your Blog](#deploying-your-blog)
5. [Custom Domain Setup](#custom-domain-setup)

---

## Step 1: Finding Cached Pages

### Method A: Google Search Console

Search Google for your cached pages:

```
site:alexeyvishnevsky.com
```

Or for specific cached pages:

```
cache:alexeyvishnevsky.com
```

### Method B: Direct Cache URLs

Access cached pages directly:

```
https://webcache.googleusercontent.com/search?q=cache:alexeyvishnevsky.com
```

### Method C: Internet Archive (Wayback Machine)

Check if your site was archived:

```
https://web.archive.org/web/*/alexeyvishnevsky.com
```

---

## Step 2: Fetching Content

### Option 1: Automated Python Script

We've created a Python script to automate fetching:

```bash
cd /Users/manun/workspace/restore-blog
python3 fetch_cached_pages.py
```

**Before running:**
1. Install dependencies: `pip3 install requests beautifulsoup4`
2. Edit `fetch_cached_pages.py` and add all your blog URLs to the `urls_to_fetch` list

### Option 2: Manual Fetching

1. **Open each cached page in your browser:**
   - Search: `cache:alexeyvishnevsky.com/your-post-title`
   
2. **Save the page:**
   - Press `Cmd+S` (Mac) or `Ctrl+S` (Windows)
   - Choose "Webpage, Complete" to save HTML + assets
   
3. **Clean up the HTML:**
   - Remove Google cache headers/banners
   - Fix broken links
   - Update asset paths

### Option 3: Use Wayback Machine Downloader

```bash
# Install wayback-machine-downloader
gem install wayback_machine_downloader

# Download all snapshots
wayback_machine_downloader alexeyvishnevsky.com
```

---

## Step 3: Setting Up GitHub Pages

### Create a GitHub Repository

1. **Go to GitHub**: https://github.com/new

2. **Create repository:**
   - Name: `alexeyvishnevsky.github.io` (for user site)
   - OR: `blog` (for project site)
   - Make it **Public**
   - Don't initialize with README (we'll add files)

3. **Clone the repository:**
   ```bash
   cd /Users/manun/workspace
   git clone https://github.com/YOUR_USERNAME/alexeyvishnevsky.github.io.git
   cd alexeyvishnevsky.github.io
   ```

### Initialize GitHub Pages

GitHub Pages will automatically serve content from:
- `main` or `master` branch (root or `/docs` folder)
- `gh-pages` branch

---

## Step 4: Deploying Your Blog

### Basic Structure

Create this structure in your repository:

```
alexeyvishnevsky.github.io/
├── index.html          # Homepage
├── about.html          # About page
├── posts/              # Blog posts
│   ├── post-1.html
│   ├── post-2.html
│   └── ...
├── assets/             # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── CNAME              # For custom domain (optional)
└── README.md          # Repository info
```

### Deploy Steps

```bash
# Navigate to your repository
cd /Users/manun/workspace/alexeyvishnevsky.github.io

# Copy your restored blog files
cp -r /Users/manun/workspace/restore-blog/restored-blog/* .

# Add all files
git add .

# Commit
git commit -m "Initial blog restoration from Google Cache"

# Push to GitHub
git push origin main
```

### Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select `main` branch
4. Click **Save**
5. Your site will be live at: `https://YOUR_USERNAME.github.io/`

---

## Step 5: Custom Domain Setup

To use your original domain `alexeyvishnevsky.com`:

### A. Create CNAME File

```bash
echo "alexeyvishnevsky.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push
```

### B. Configure DNS

Add these DNS records at your domain registrar:

**For apex domain (alexeyvishnevsky.com):**

```
Type: A
Name: @
Value: 185.199.108.153

Type: A
Name: @
Value: 185.199.109.153

Type: A
Name: @
Value: 185.199.110.153

Type: A
Name: @
Value: 185.199.111.153
```

**For www subdomain:**

```
Type: CNAME
Name: www
Value: YOUR_USERNAME.github.io
```

### C. Enable HTTPS

1. Go to GitHub Settings → Pages
2. Check **Enforce HTTPS**
3. Wait for SSL certificate (can take 24 hours)

---

## Step 6: Finding All Your Blog URLs

### Method 1: Google Search

```
site:alexeyvishnevsky.com
```

Copy all URLs from search results.

### Method 2: Google Search Console

If you had access:
1. Go to: https://search.google.com/search-console
2. Check **Coverage** or **Index** reports
3. Export all indexed URLs

### Method 3: Sitemap

Check if Google cached your sitemap:

```
cache:alexeyvishnevsky.com/sitemap.xml
```

---

## Additional Scripts & Tools

### Script: Find All Cached URLs

```bash
#!/bin/bash
# save as: find_cached_urls.sh

DOMAIN="alexeyvishnevsky.com"

echo "Searching for cached pages..."
echo "Please manually search Google for: site:$DOMAIN"
echo "Then use the Python script to fetch them."
```

### Script: Clean HTML Files

```python
# clean_html.py - Remove Google cache artifacts

import os
import glob
from bs4 import BeautifulSoup

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Remove Google cache elements
    for elem in soup.select('[style*="background"]'):
        elem.decompose()
    
    # Save cleaned version
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

for html_file in glob.glob('restored-blog/**/*.html', recursive=True):
    print(f"Cleaning {html_file}")
    clean_file(html_file)
```

---

## Troubleshooting

### Issue: Can't Find Cached Pages

**Solutions:**
- Try different search terms: `site:alexeyvishnevsky.com blog post title`
- Use Internet Archive: https://web.archive.org
- Check if you have local backups
- Ask search engines: Bing, DuckDuckGo may have cached versions

### Issue: Broken Links/Images

**Solutions:**
- Update all internal links to relative paths
- Re-download images from cache
- Use `sed` to batch update links:
  ```bash
  sed -i 's/http:\/\/alexeyvishnevsky.com/./g' *.html
  ```

### Issue: GitHub Pages Not Working

**Solutions:**
- Check repository is public
- Verify GitHub Pages is enabled in Settings
- Check `index.html` exists in root
- Wait 5-10 minutes for deployment
- Check GitHub Actions tab for build errors

---

## Quick Start Commands

```bash
# 1. Create workspace
mkdir -p /Users/manun/workspace/restore-blog
cd /Users/manun/workspace/restore-blog

# 2. Install dependencies
pip3 install requests beautifulsoup4 lxml

# 3. Run fetcher (after editing URLs)
python3 fetch_cached_pages.py

# 4. Create GitHub repo and clone
# (Do this on GitHub.com first)
cd /Users/manun/workspace
git clone https://github.com/YOUR_USERNAME/alexeyvishnevsky.github.io.git

# 5. Copy restored content
cp -r restore-blog/restored-blog/* alexeyvishnevsky.github.io/

# 6. Deploy
cd alexeyvishnevsky.github.io
git add .
git commit -m "Restore blog from cache"
git push origin main
```

---

## Resources

- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **Wayback Machine**: https://web.archive.org
- **Google Cache Checker**: http://cachedview.com/
- **Custom Domains**: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

---

## Next Steps

1. ✅ Find all cached URLs (use Google search: `site:alexeyvishnevsky.com`)
2. ✅ Run `fetch_cached_pages.py` with your URLs
3. ✅ Create GitHub repository
4. ✅ Copy restored files to repository
5. ✅ Push to GitHub
6. ✅ Configure custom domain (optional)
7. ✅ Set up HTTPS

Good luck with your blog restoration! 🚀
