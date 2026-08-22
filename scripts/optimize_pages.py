#!/usr/bin/env python3
"""
SciMSPT Performance Optimization Script v1.0
============================================
Updates all HTML files with:
1. Critical CSS inlining
2. Font optimization (font-display: swap, preload)
3. Resource hints (dns-prefetch, preconnect)
4. Service worker registration
5. Performance monitoring script
6. Image lazy loading attributes
7. Defer non-critical JavaScript

Usage: python3 optimize_pages.py [--dry-run]
"""

import os
import re
import glob
from pathlib import Path
from typing import List, Tuple, Optional
import argparse

class PageOptimizer:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.critical_css_path = self.base_dir / "css" / "critical.css"
        self.critical_css = self.load_critical_css()
        
    def load_critical_css(self) -> str:
        """Load critical CSS file"""
        if self.critical_css_path.exists():
            return self.critical_css_path.read_text()
        return ""
    
    def get_html_files(self) -> List[Path]:
        """Get all HTML files to optimize"""
        # Skip backup files and special directories
        exclude_patterns = [
            '*.backup.html',
            '*.phase*.html',
            'portfolio-shorts/*',
            'shorts/*',
            'video-clips/*',
            'assets/slides/*'
        ]
        
        html_files = []
        for pattern in ['*.html', '**/*.html']:
            for f in self.base_dir.glob(pattern):
                # Skip excluded patterns
                skip = False
                for excl in exclude_patterns:
                    if f.match(excl) or any(part.startswith('.') for part in f.parts):
                        skip = True
                        break
                
                if not skip and f.is_file():
                    html_files.append(f)
        
        return sorted(set(html_files))
    
    def optimize_page(self, filepath: Path, dry_run: bool = False) -> Tuple[bool, str]:
        """Optimize a single HTML page"""
        content = filepath.read_text(encoding='utf-8')
        original = content
        
        try:
            # 1. Add Critical CSS in <head>
            content = self.add_critical_css(content)
            
            # 2. Optimize font loading
            content = self.optimize_fonts(content)
            
            # 3. Add resource hints
            content = self.add_resource_hints(content)
            
            # 4. Add service worker registration
            content = self.add_service_worker(content)
            
            # 5. Add performance script
            content = self.add_performance_script(content)
            
            # 6. Optimize images for lazy loading
            content = self.optimize_images(content)
            
            # 7. Defer non-critical scripts
            content = self.defer_scripts(content)
            
            changes_made = content != original
            
            if changes_made and not dry_run:
                filepath.write_text(content, encoding='utf-8')
                
            return changes_made, "Optimized" if changes_made else "No changes needed"
            
        except Exception as e:
            print(f"  ❌ Error optimizing {filepath.name}: {e}")
            return False, f"Error: {e}"
    
    def add_critical_css(self, content: str) -> str:
        """Add critical CSS inline in <head>"""
        if not self.critical_css:
            return content
            
        critical_style = f'''<style>
/* Critical CSS - Inlined for performance */
{self.critical_css}
</style>'''
        
        # Insert after <head> or after <meta charset>
        if '<style>' not in content[:1000]:  # Check if already has inline style
            if '<head>' in content:
                content = content.replace('<head>', f'<head>\n{critical_style}', 1)
            elif '<meta charset' in content:
                # Find end of first meta tag and insert after
                meta_end = content.find('>') + 1
                content = content[:meta_end] + '\n' + critical_style + content[meta_end:]
        
        return content
    
    def optimize_fonts(self, content: str) -> str:
        """Optimize Google Fonts loading with display=swap"""
        # Add display=swap to existing Google Fonts URLs
        old_font_pattern = r'fonts\.googleapis\.com/css2\?([^"]+)'
        new_font_url = r'fonts.googleapis.com/css2?\1&display=swap'
        content = re.sub(old_font_pattern, new_font_url, content)
        
        # Add preload for critical fonts
        preload_links = '''<!-- Critical Font Preloads -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap">'''
        
        if '<!-- Critical Font Preloads -->' not in content:
            if '<link rel="stylesheet" href="https://fonts.googleapis.com' in content:
                content = content.replace(
                    '<link rel="stylesheet" href="https://fonts.googleapis.com',
                    f'{preload_links}\n<link rel="stylesheet" href="https://fonts.googleapis.com',
                    1
                )
        
        return content
    
    def add_resource_hints(self, content: str) -> str:
        """Add DNS prefetch and preconnect hints"""
        hints = '''<!-- Resource Hints -->
<link rel="dns-prefetch" href="//fonts.googleapis.com">
<link rel="dns-prefetch" href="//fonts.gstatic.com">
<link rel="dns-prefetch" href="//www.googletagmanager.com">
<meta name="theme-color" content="#00E5FF">'''
        
        if '<!-- Resource Hints -->' not in content:
            if '<meta charset' in content:
                meta_pos = content.find('<meta charset')
                # Find closing > of this or next meta tag
                close_pos = content.find('>', meta_pos) + 1
                content = content[:close_pos] + '\n' + hints + content[close_pos:]
        
        return content
    
    def add_service_worker(self, content: str) -> str:
        """Add service worker registration"""
        sw_code = '''<!-- Service Worker Registration -->
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(reg => console.log('✅ SW registered:', reg.scope))
      .catch(err => console.warn('⚠️ SW registration failed:', err));
  });
}
</script>'''
        
        if ('serviceWorker' not in content and 
            '<!-- Service Worker Registration -->' not in content):
            # Add before </body>
            content = content.replace('</body>', f'{sw_code}\n</body>')
        
        return content
    
    def add_performance_script(self, content: str) -> str:
        """Add performance optimization script"""
        perf_script = '''<!-- Performance Optimizer -->
<script src="js/performance.js" defer></script>'''
        
        if 'performance.js' not in content:
            # Add before other scripts or before </body>
            if '</body>' in content:
                content = content.replace('</body>', f'{perf_script}\n</body>')
        
        return content
    
    def optimize_images(self, content: str) -> str:
        """Add lazy loading to images"""
        # Add loading="lazy" to images without it (skip above-fold images)
        # Images below first 500 chars are likely below fold
        lines = content.split('\n')
        modified_lines = []
        line_count = len(lines)
        
        for i, line in enumerate(lines):
            # Check if this is an img tag
            if '<img' in line and 'loading=' not in line:
                # Determine if likely above fold (first few images)
                img_count_before = sum(1 for l in modified_lines if '<img' in l)
                
                # Don't lazy-load hero/important images (first 2-3 images)
                if img_count_before >= 2:
                    # Add lazy loading
                    line = line.replace('<img', '<img loading="lazy" decoding="async"', 1)
                else:
                    # Eager load important images
                    if 'decoding=' not in line:
                        line = line.replace('<img', '<img loading="eager" decoding="async"', 1)
            
            modified_lines.append(line)
        
        return '\n'.join(modified_lines)
    
    def defer_scripts(self, content: str) -> str:
        """Add defer/async to scripts that don't have it"""
        # Patterns of scripts that should be deferred
        defer_patterns = [
            'global-components.js',
            'analytics',
            'tracking'
        ]
        
        for pattern in defer_patterns:
            if pattern in content:
                # Find script tags with this source but no async/defer
                regex = rf'(<script\s+src="[^"]*{pattern}[^"]*")(\s*>)'
                replacement = r'\1 defer\2'
                content = re.sub(regex, replacement, content, flags=re.IGNORECASE)
        
        return content


def main():
    parser = argparse.ArgumentParser(description='Optimize SciMSPT pages for performance')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    parser.add_argument('--path', default='.', help='Base directory path')
    args = parser.parse_args()
    
    optimizer = PageOptimizer(args.path)
    html_files = optimizer.get_html_files()
    
    print(f"🚀 SciMSPT Page Optimizer")
    print(f"📁 Base directory: {args.path}")
    print(f"📄 Found {len(html_files)} HTML files to optimize\n")
    
    optimized_count = 0
    skipped_count = 0
    
    for filepath in html_files:
        changed, message = optimizer.optimize_page(filepath, args.dry_run)
        status = "✅" if changed else "⏭️"
        mode = "[DRY RUN] " if args.dry_run else ""
        print(f"{status} {mode}{filepath.name}: {message}")
        
        if changed:
            optimized_count += 1
        else:
            skipped_count += 1
    
    print(f"\n{'='*50}")
    print(f"📊 Summary:")
    print(f"   ✅ Optimized: {optimized_count} files")
    print(f"   ⏭️ Skipped: {skipped_count} files")
    print(f"   📁 Total: {len(html_files)} files")
    
    if args.dry_run:
        print("\n💡 Run without --dry-run to apply changes")


if __name__ == "__main__":
    main()
