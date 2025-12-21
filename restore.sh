#!/bin/bash

# Blog Restoration Helper Script
# This script helps automate the blog restoration process

set -e

DOMAIN="alexeyvishnevsky.com"
WORKSPACE="/Users/manun/workspace/restore-blog"
OUTPUT_DIR="$WORKSPACE/restored-blog"

echo "🔧 Blog Restoration Helper"
echo "=========================="
echo ""

# Create workspace
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "📋 Checking dependencies..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command_exists git; then
    echo "❌ Git is not installed"
    exit 1
fi

echo "✅ All required tools are installed"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install requests beautifulsoup4 lxml --quiet
echo "✅ Python dependencies installed"
echo ""

# Menu
echo "What would you like to do?"
echo ""
echo "1) Find cached pages (opens Google search)"
echo "2) Fetch cached pages using Python script"
echo "3) Create GitHub repository (opens GitHub)"
echo "4) Deploy to GitHub Pages"
echo "5) View restoration guide"
echo "6) Exit"
echo ""

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "🔍 Opening Google to search for cached pages..."
        echo "Search for: site:$DOMAIN"
        open "https://www.google.com/search?q=site:$DOMAIN"
        echo ""
        echo "Also checking Internet Archive..."
        open "https://web.archive.org/web/*/$DOMAIN"
        ;;
    2)
        echo ""
        echo "📥 Running cache fetcher..."
        if [ -f "fetch_cached_pages.py" ]; then
            python3 fetch_cached_pages.py
        else
            echo "❌ fetch_cached_pages.py not found!"
            echo "Please make sure you're in the correct directory."
        fi
        ;;
    3)
        echo ""
        echo "🌐 Opening GitHub to create repository..."
        echo ""
        echo "Create a repository named: alexeyvishnevsky.github.io"
        echo "(or any name for a project site)"
        open "https://github.com/new"
        echo ""
        read -p "Press Enter once you've created the repository..."
        echo ""
        read -p "Enter your GitHub username: " github_user
        read -p "Enter repository name (default: alexeyvishnevsky.github.io): " repo_name
        repo_name=${repo_name:-alexeyvishnevsky.github.io}
        
        echo ""
        echo "📥 Cloning repository..."
        cd /Users/manun/workspace
        git clone "https://github.com/$github_user/$repo_name.git"
        echo "✅ Repository cloned to: /Users/manun/workspace/$repo_name"
        ;;
    4)
        echo ""
        read -p "Enter your GitHub repository path (e.g., /Users/manun/workspace/alexeyvishnevsky.github.io): " repo_path
        
        if [ ! -d "$repo_path" ]; then
            echo "❌ Repository path not found!"
            exit 1
        fi
        
        if [ ! -d "$OUTPUT_DIR" ]; then
            echo "❌ No restored content found! Please run option 2 first."
            exit 1
        fi
        
        echo "📦 Copying restored content..."
        cp -r "$OUTPUT_DIR"/* "$repo_path/"
        
        echo "📝 Committing and pushing..."
        cd "$repo_path"
        git add .
        git commit -m "Restore blog from Google Cache - $(date +%Y-%m-%d)"
        git push origin main
        
        echo ""
        echo "✅ Blog deployed!"
        echo "🌐 Your site will be available at:"
        echo "   https://$(basename "$repo_path")/"
        ;;
    5)
        echo ""
        if [ -f "RESTORATION_GUIDE.md" ]; then
            cat RESTORATION_GUIDE.md
        else
            echo "Guide not found!"
        fi
        ;;
    6)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice!"
        exit 1
        ;;
esac

echo ""
echo "✨ Done!"
