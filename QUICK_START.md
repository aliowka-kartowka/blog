# 🔧 Blog Restoration - Quick Reference

## 📋 What I've Set Up For You

I've created a complete toolkit in `/Users/manun/workspace/restore-blog/` to help you restore your blog **alexeyvishnevsky.com** from Google Cache and deploy it to GitHub Pages.

## 📁 Files Created

```
/Users/manun/workspace/restore-blog/
├── README.md                    # Project overview
├── RESTORATION_GUIDE.md         # Complete step-by-step guide
├── fetch_cached_pages.py        # Automated cache fetcher
├── find_urls.py                 # URL discovery tool
├── restore.sh                   # Interactive helper script
└── requirements.txt             # Python dependencies
```

## 🚀 Quick Start (3 Methods)

### Method 1: Interactive Script (Recommended)

```bash
cd /Users/manun/workspace/restore-blog
./restore.sh
```

This will guide you through the entire process interactively.

### Method 2: Manual Step-by-Step

```bash
# 1. Navigate to restoration workspace
cd /Users/manun/workspace/restore-blog

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Find your cached pages (browser windows will open)
python3 find_urls.py

# 4. Edit fetch_cached_pages.py and add your URLs
# Add all discovered URLs to the urls_to_fetch list

# 5. Fetch the cached content
python3 fetch_cached_pages.py

# 6. Review fetched content
ls -la restored-blog/

# 7. Create GitHub repository
# Go to: https://github.com/new
# Name: alexeyvishnevsky.github.io

# 8. Clone and deploy
cd /Users/manun/workspace
git clone https://github.com/YOUR_USERNAME/alexeyvishnevsky.github.io.git
cd alexeyvishnevsky.github.io
cp -r /Users/manun/workspace/restore-blog/restored-blog/* .
git add .
git commit -m "Restore blog from Google Cache"
git push origin main
```

### Method 3: Use Internet Archive Downloader

```bash
# Install wayback-machine-downloader
gem install wayback_machine_downloader

# Download all archived pages
cd /Users/manun/workspace
wayback_machine_downloader alexeyvishnevsky.com

# This will create a folder with all archived pages
```

## 🔍 Finding Your Cached Pages

I've already opened two browser tabs for you:

1. **Google Search**: `site:alexeyvishnevsky.com`
   - Shows all indexed pages from your blog
   - Click on any result, then click "Cached" to view

2. **Internet Archive**: Historical snapshots
   - Browse calendar to find archived versions
   - Download HTML directly from timeline

### Additional Places to Check

- **Google Cache Direct**: `https://webcache.googleusercontent.com/search?q=cache:alexeyvishnevsky.com`
- **Bing Cache**: Search `site:alexeyvishnevsky.com` on Bing
- **Your Browser History**: If you visited your blog recently
- **Local Backups**: Check if you have any local copies

## 📝 Step-by-Step Process

### 1. Discovery Phase
- [ ] Find all blog URLs using Google search
- [ ] Check Internet Archive for snapshots
- [ ] Make list of all pages you want to restore

### 2. Content Retrieval
- [ ] Edit `fetch_cached_pages.py` with your URLs
- [ ] Run the fetcher: `python3 fetch_cached_pages.py`
- [ ] Verify content in `restored-blog/` folder

### 3. GitHub Setup
- [ ] Create repository: `alexeyvishnevsky.github.io`
- [ ] Clone repository locally
- [ ] Copy restored content to repository

### 4. Deployment
- [ ] Commit and push to GitHub
- [ ] Enable GitHub Pages in Settings → Pages
- [ ] Wait 5-10 minutes for deployment

### 5. Custom Domain (Optional)
- [ ] Add CNAME file with your domain
- [ ] Configure DNS records (A records to GitHub IPs)
- [ ] Enable HTTPS in GitHub Settings

## 🛠️ Tools & Scripts Explained

### `fetch_cached_pages.py`
- Automatically fetches pages from Google Cache
- Cleans up Google cache artifacts
- Saves HTML files locally
- **Edit this file** to add your blog URLs

### `find_urls.py`
- Helps discover all your blog URLs
- Creates `urls.txt` template
- Generates URL list for fetcher
- Opens browser to search tools

### `restore.sh`
- Interactive menu system
- Guides through entire process
- Automates common tasks
- Checks dependencies

## 🌐 GitHub Pages Configuration

### Repository Name Options

**Option A: User Site** (Recommended)
```
Repository: alexeyvishnevsky.github.io
URL: https://alexeyvishnevsky.github.io/
Custom domain: alexeyvishnevsky.com
```

**Option B: Project Site**
```
Repository: blog (or any name)
URL: https://YOUR_USERNAME.github.io/blog/
```

### DNS Configuration for Custom Domain

Add these records at your domain registrar:

```
# A Records (apex domain)
Type: A, Host: @, Value: 185.199.108.153
Type: A, Host: @, Value: 185.199.109.153
Type: A, Host: @, Value: 185.199.110.153
Type: A, Host: @, Value: 185.199.111.153

# CNAME Record (www subdomain)
Type: CNAME, Host: www, Value: YOUR_USERNAME.github.io
```

## 📚 Documentation

All detailed documentation is in `RESTORATION_GUIDE.md`:
```bash
cat /Users/manun/workspace/restore-blog/RESTORATION_GUIDE.md
```

Or open in VS Code:
```bash
code /Users/manun/workspace/restore-blog/RESTORATION_GUIDE.md
```

## 🎯 Next Actions

**Immediate Next Steps:**

1. **Browse the opened tabs** to find your cached pages
2. **Make a list** of all URLs you find
3. **Run the URL finder**:
   ```bash
   cd /Users/manun/workspace/restore-blog
   python3 find_urls.py
   # Choose option 1 to create urls.txt template
   ```
4. **Edit urls.txt** and add all your blog URLs
5. **Run the interactive script**:
   ```bash
   ./restore.sh
   # Choose option 2 to fetch cached pages
   ```

## 💡 Pro Tips

1. **Start with homepage**: Always fetch the homepage first to understand structure
2. **Check robots.txt**: May contain sitemap URL
3. **Look for patterns**: Blog posts often follow pattern like `/posts/title-here`
4. **Archive.org is gold**: Often has more content than Google Cache
5. **Save everything**: Better to fetch too much than too little

## 🆘 Troubleshooting

**Can't find any cached pages?**
- Try different search engines (Bing, DuckDuckGo)
- Check if you have browser history
- Ask friends if they bookmarked your blog

**Script not working?**
- Check Python version: `python3 --version` (need 3.7+)
- Reinstall dependencies: `pip3 install -r requirements.txt`
- Check permissions: `chmod +x restore.sh`

**GitHub Pages not deploying?**
- Verify repository is public
- Check Settings → Pages is enabled
- Wait 10 minutes and clear browser cache
- Check for `index.html` in repository root

## 📞 Resources

- **Complete Guide**: `RESTORATION_GUIDE.md`
- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **Internet Archive**: https://web.archive.org
- **Google Cache**: Add `cache:` before URL in Google search

---

**Ready to start?** Run this command:

```bash
cd /Users/manun/workspace/restore-blog && ./restore.sh
```

Good luck restoring your blog! 🚀✨
