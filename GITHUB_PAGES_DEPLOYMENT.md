# GitHub Pages Deployment Guide

## Overview
This guide will help you deploy the restored **alexeyvishnevsky.com** blog to GitHub Pages.

## Prerequisites
- GitHub account
- Git installed on your machine
- Content in `restored-blog-clean/` directory

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `alexeyvishnevsky-blog` (or `yourusername.github.io` for user site)
3. Set to **Public**
4. Do NOT initialize with README
5. Click "Create repository"

## Step 2: Initialize Git Repository

```bash
cd restored-blog-clean/
git init
git add .
git commit -m "Initial commit: Restored blog from Wayback Machine"
```

## Step 3: Connect to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/alexeyvishnevsky-blog.git
git push -u origin main
```

## Step 4: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under "Source":
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**

Your site will be available at: `https://YOUR_USERNAME.github.io/alexeyvishnevsky-blog/`

## Step 5: Custom Domain (Optional)

To use **alexeyvishnevsky.com**:

### A. Add CNAME file

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

### C. Enable in GitHub Settings

1. Go to repository Settings → Pages
2. Under "Custom domain", enter: `alexeyvishnevsky.com`
3. Click Save
4. Wait for DNS check (green checkmark)
5. Enable "Enforce HTTPS"

## Step 6: Fix Internal Links (if using custom domain)

If links don't work correctly, you may need to update the base URL. Create a script:

```bash
# Update all internal links for GitHub Pages subdirectory deployment
find . -name "*.html" -type f -exec sed -i '' 's|href="/|href="/alexeyvishnevsky-blog/|g' {} +
find . -name "*.html" -type f -exec sed -i '' 's|src="/|src="/alexeyvishnevsky-blog/|g' {} +

git add .
git commit -m "Fix internal links for GitHub Pages"
git push
```

**Skip this step if using custom domain!**

## Deployment Checklist

- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] GitHub Pages enabled
- [ ] Site accessible at GitHub URL
- [ ] Custom domain configured (optional)
- [ ] HTTPS enabled
- [ ] All pages render correctly
- [ ] CSS styling applied
- [ ] Internal links working
- [ ] Images loading (if any)

## Troubleshooting

### Pages not loading
- Check that `main` branch is selected in Settings → Pages
- Ensure `index.html` exists in root directory
- Wait 1-2 minutes after pushing changes

### CSS not loading
- Check browser console (F12) for errors
- Verify `css/main.css` exists
- Check CSS paths in HTML files are relative

### 404 errors on internal links
- If using subdirectory deployment, update links with repository name prefix
- If using custom domain, links should be root-relative

### Custom domain not working
- Verify DNS records are correct
- Wait 24-48 hours for DNS propagation
- Check CNAME file is in repository root
- Ensure custom domain is set in GitHub Settings

## Maintenance

### Adding New Content
```bash
# Edit files
git add .
git commit -m "Update content"
git push
```

Changes appear on GitHub Pages within 1-2 minutes.

### Updating Styles
Edit `css/main.css`, then:
```bash
git add css/main.css
git commit -m "Update styles"
git push
```

## Site Structure

```
restored-blog-clean/
├── index.html          # Homepage
├── about/              # About page
├── blog/               # Blog index
├── 2013-2018/          # Blog posts by year
├── category/           # Category archives
├── tag/                # Tag archives  
├── author/             # Author page
└── css/
    └── main.css        # Main stylesheet
```

## Additional Features

### Analytics (Optional)
Add Google Analytics by inserting tracking code in all HTML files before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Search (Optional)
Consider adding:
- Google Custom Search
- Algolia DocSearch
- Lunr.js for static search

## Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Custom Domain Setup](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [GitHub Pages Troubleshooting](https://docs.github.com/en/pages/getting-started-with-github-pages/troubleshooting-404-errors-for-github-pages-sites)

## Success!

Your restored blog is now live on the internet! 🎉

Visit: `https://YOUR_USERNAME.github.io/alexeyvishnevsky-blog/`
Or: `https://alexeyvishnevsky.com` (if custom domain configured)
