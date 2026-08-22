#!/usr/bin/env python3
"""
Fix skeleton loader blocking issue on all HTML pages
Adds critical CSS to hide skeleton loaders immediately
"""

import os
import re
from pathlib import Path

def fix_skeleton_loader(filepath):
    """Add CSS to hide skeleton loader immediately"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already fixed
        if 'CRITICAL FIX: Hide skeleton loader' in content:
            return False  # Already fixed
        
        # Find the first <style> tag and add fix after it
        fix_css = """
    /* CRITICAL FIX: Hide skeleton loader immediately to prevent blocking */
    .skeleton-loader, #skeletonLoader {
      display: none !important;
      opacity: 0 !important;
      visibility: hidden !important;
      pointer-events: none !important;
      position: fixed !important;
      z-index: -9999 !important;
    }
    
    /* Ensure body and content are visible */
    body {
      opacity: 1 !important;
      visibility: visible !important;
    }
"""
        
        # Insert after <style> tag
        if '<style>' in content:
            # Only add if not already present in this file
            content = content.replace('<style>', f'<style>{fix_css}', 1)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    base_dir = Path('/home/z/my-project/Demo2SciMSPT')
    
    # Find all HTML files with skeleton loaders
    html_files = []
    for pattern in ['*.html', '**/*.html']:
        for f in base_dir.glob(pattern):
            if f.is_file() and 'skeleton-loader' in f.read_text(encoding='utf-8', errors='ignore'):
                html_files.append(f)
    
    print(f"Found {len(html_files)} files with skeleton loaders")
    
    fixed_count = 0
    for filepath in html_files:
        if fix_skeleton_loader(filepath):
            print(f"✅ Fixed: {filepath.name}")
            fixed_count += 1
        else:
            print(f"⏭️ Already fixed or no style tag: {filepath.name}")
    
    print(f"\n✅ Fixed {fixed_count} files")

if __name__ == "__main__":
    main()
