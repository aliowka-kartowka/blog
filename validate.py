#!/usr/bin/env python3
"""
Validate the restored blog is ready for deployment
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"  {status} {description}")
    return exists

def check_directory_has_files(dirpath, pattern, min_count, description):
    """Check if directory has minimum number of files"""
    if not os.path.exists(dirpath):
        print(f"  ✗ {description} - Directory not found")
        return False
    
    count = sum(1 for root, dirs, files in os.walk(dirpath) 
                for f in files if f.endswith(pattern))
    
    passed = count >= min_count
    status = "✓" if passed else "✗"
    print(f"  {status} {description} ({count} files)")
    return passed

def validate_html_has_css(filepath):
    """Check if HTML file has CSS link"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            has_css = 'css/main.css' in content or '../css/main.css' in content
            has_wayback = 'archive.org' in content
            return has_css, not has_wayback
    except:
        return False, False

print("="*60)
print("  BLOG RESTORATION VALIDATION")
print("="*60)
print()

all_checks_passed = True

# 1. Check directory structure
print("1. Directory Structure:")
checks = [
    check_file_exists('restored-blog-clean/', 'Main directory'),
    check_file_exists('restored-blog-clean/css/', 'CSS directory'),
    check_file_exists('restored-blog-clean/index.html', 'Homepage'),
    check_file_exists('restored-blog-clean/about/index.html', 'About page'),
]
all_checks_passed = all_checks_passed and all(checks)
print()

# 2. Check CSS
print("2. CSS Files:")
checks = [
    check_file_exists('restored-blog-clean/css/main.css', 'Main stylesheet'),
]

# Check CSS file size
if os.path.exists('restored-blog-clean/css/main.css'):
    size = os.path.getsize('restored-blog-clean/css/main.css')
    size_ok = size > 10000  # At least 10KB
    status = "✓" if size_ok else "✗"
    print(f"  {status} CSS file size: {size:,} bytes")
    checks.append(size_ok)

all_checks_passed = all_checks_passed and all(checks)
print()

# 3. Check HTML files
print("3. HTML Content:")
checks = [
    check_directory_has_files('restored-blog-clean/', '.html', 40, 'HTML pages'),
]
all_checks_passed = all_checks_passed and all(checks)
print()

# 4. Validate HTML cleanup
print("4. HTML File Validation:")
test_files = [
    'restored-blog-clean/index.html',
    'restored-blog-clean/about/index.html',
]

for filepath in test_files:
    if os.path.exists(filepath):
        has_css, no_wayback = validate_html_has_css(filepath)
        
        rel_path = filepath.replace('restored-blog-clean/', '')
        
        if has_css:
            print(f"  ✓ {rel_path} - Has CSS link")
        else:
            print(f"  ✗ {rel_path} - Missing CSS link")
            all_checks_passed = False
        
        if no_wayback:
            print(f"  ✓ {rel_path} - No Wayback artifacts")
        else:
            print(f"  ⚠ {rel_path} - Still has Wayback references")
            # Not critical, just warning

print()

# 5. Check blog posts
print("5. Blog Posts:")
post_dirs = []
for year in ['2013', '2014', '2015', '2017', '2018']:
    year_path = f'restored-blog-clean/{year}'
    if os.path.exists(year_path):
        for root, dirs, files in os.walk(year_path):
            if 'index.html' in files:
                post_dirs.append(root)

print(f"  ✓ Found {len(post_dirs)} blog post pages")
all_checks_passed = all_checks_passed and len(post_dirs) >= 10
print()

# 6. Check documentation
print("6. Documentation:")
checks = [
    check_file_exists('GITHUB_PAGES_DEPLOYMENT.md', 'Deployment guide'),
    check_file_exists('FINAL_SUMMARY.md', 'Final summary'),
    check_file_exists('RESTORATION_SUMMARY.md', 'Restoration summary'),
]
all_checks_passed = all_checks_passed and all(checks)
print()

# Final result
print("="*60)
if all_checks_passed:
    print("  ✅ ALL CHECKS PASSED!")
    print("  🚀 Site is ready for deployment!")
else:
    print("  ⚠️  SOME CHECKS FAILED")
    print("  Please review the issues above")

print("="*60)
print()

# Deployment reminder
if all_checks_passed:
    print("Next steps:")
    print("  1. Preview locally: ./preview.sh")
    print("  2. Deploy to GitHub: See GITHUB_PAGES_DEPLOYMENT.md")
    print()

sys.exit(0 if all_checks_passed else 1)
