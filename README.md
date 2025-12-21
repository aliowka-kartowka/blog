# Blog Restoration Project

This directory contains tools and scripts to restore **alexeyvishnevsky.com** from Google Cache and deploy it to GitHub Pages.

## Quick Start

### Option 1: Automated Script

```bash
cd /Users/manun/workspace/restore-blog
chmod +x restore.sh
./restore.sh
```

### Option 2: Manual Steps

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Edit fetch_cached_pages.py with your blog URLs
# Add all URLs you want to recover

# 3. Run the fetcher
python3 fetch_cached_pages.py

# 4. Review fetched content
ls -la restored-blog/

# 5. Create GitHub repository and deploy (see RESTORATION_GUIDE.md)
```

## Files in This Directory

- **RESTORATION_GUIDE.md** - Complete step-by-step guide
- **fetch_cached_pages.py** - Python script to fetch cached pages
- **restore.sh** - Interactive helper script
- **requirements.txt** - Python dependencies

## Finding Your Cached Pages

### Google Search

Search Google for your blog:
```
site:alexeyvishnevsky.com
```

### Direct Cache Access

Access cached pages:
```
https://webcache.googleusercontent.com/search?q=cache:alexeyvishnevsky.com
```

### Internet Archive

Check historical snapshots:
```
https://web.archive.org/web/*/alexeyvishnevsky.com
```

## Next Steps

1. **Find all your blog URLs** - Search Google for `site:alexeyvishnevsky.com`
2. **Edit fetch_cached_pages.py** - Add discovered URLs to the `urls_to_fetch` list
3. **Run the fetcher** - Execute `python3 fetch_cached_pages.py`
4. **Review content** - Check `restored-blog/` directory
5. **Create GitHub repo** - Create `alexeyvishnevsky.github.io` repository
6. **Deploy** - Copy content and push to GitHub

## Need Help?

Read the complete **RESTORATION_GUIDE.md** for detailed instructions.

## Example URL List

Based on common blog structures, you might have URLs like:

- `https://alexeyvishnevsky.com/`
- `https://alexeyvishnevsky.com/about`
- `https://alexeyvishnevsky.com/blog`
- `https://alexeyvishnevsky.com/posts/your-post-title`
- `https://alexeyvishnevsky.com/archive`
- `https://alexeyvishnevsky.com/contact`

Add these to `urls_to_fetch` in the Python script!
