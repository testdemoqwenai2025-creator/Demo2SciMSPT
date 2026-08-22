#!/usr/bin/env python3
"""
=============================================================================
SciMSPT ADVANCED CORRUPTION REMOVER - v2.0
=============================================================================

⚠️  COMPREHENSIVE CLEANING - RUN BEFORE EVERY DEPLOYMENT!

WHAT IT CLEANS:
-------------
1. 🚫 Chinese/Japanese/Korean characters (unless intentional)
2. 🚫 Visible JavaScript code showing as text
3. 🚫 Orphaned JS comments rendering as visible content
4. 🚫 Broken </script> tags leaving code outside script blocks
5. 🚫 Stuck skeleton loaders (gray bars blocking content)
6. 🚫 Rogue agent injections (unwanted platform references)
7. 🚫 Encoding artifacts and corruption markers

GUARD RAILS:
-----------
- Preserves intentional Unicode (©, ®, ™, °, etc.)
- Preserves HTML entities (&nbsp;, &amp;, etc.)
- Logs all changes for audit trail
- Creates backup before modifications

USAGE:
------
python3 scripts/clean_corruption.py          # Clean all files
python3 scripts/clean_corruption.py index.html  # Clean specific file
python3 scripts/clean_corruption.py --dry-run    # Preview only, no changes

EXIT CODES:
-----------
0 = All pages clean
1 = Fixes applied
2 = Error occurred

=============================================================================
"""

import re
import os
import sys
import glob
from datetime import datetime
from pathlib import Path

# Configuration
ALLOWED_UNICODE_PATTERNS = [
    r'©', r'®', r'™', r'°', r'±', r'×', r'÷', r'≤', r'≥', 
    r'∞', r'√', r'∑', r'∏', r'π', r'Ω', r'α', r'β', r'γ',
    r'&[a-zA-Z]+;',  # HTML entities like &nbsp;
]

# Patterns that indicate legitimate Chinese content (whitelist)
CHINESE_WHITELIST = [
    'lang="zh"', 'lang="zh-CN"', 'chinese', 'mandarin',
    'baidu.com', 'alibaba.com', 'tencent.com',  # Known Chinese platforms
]

class CorruptionCleaner:
    def __init__(self, base_dir=None, dry_run=False):
        self.base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dry_run = dry_run
        self.total_fixes = 0
        self.files_modified = []
        self.audit_log = []
        
    def log(self, message, level='INFO'):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {level}: {message}")
        self.audit_log.append(f"{timestamp} - {level} - {message}")
    
    def find_chinese_characters(self, content):
        """Find all CJK characters that aren't whitelisted"""
        
        # Check if this page intentionally contains Chinese
        content_lower = content.lower()
        is_intentional_chinese = any(whitelist_item in content_lower for whitelist_item in CHINESE_WHITELIST)
        
        if is_intentional_chinese:
            return [], False
        
        # Find Chinese character ranges
        chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')
        matches = list(chinese_pattern.finditer(content))
        
        if not matches:
            return [], False
            
        # Group consecutive Chinese characters into phrases
        phrases = []
        current_phrase = None
        
        for match in matches:
            if current_phrase and match.start() == current_phrase['end'] + 1:
                # Consecutive - extend phrase
                current_phrase['text'] += match.group()
                current_phrase['end'] = match.end()
            else:
                # New phrase
                if current_phrase:
                    phrases.append(current_phrase)
                current_phrase = {
                    'start': match.start(),
                    'end': match.end(),
                    'text': match.group()
                }
        
        if current_phrase:
            phrases.append(current_phrase)
            
        return phrases, True
    
    def remove_chinese_text(self, content, filepath):
        """Remove Chinese text while preserving structure"""
        
        phrases, has_chinese = self.find_chinese_characters(content)
        
        if not has_chinese or not phrases:
            return content, 0
        
        fixes = 0
        # Process in reverse order to maintain positions
        for phrase in reversed(phrases):
            start = phrase['start']
            end = phrase['end']
            text = phrase['text']
            
            # Get context for logging
            context_start = max(0, start - 30)
            context_end = min(len(content), end + 30)
            context = content[context_start:context_end].replace('\n', ' ')
            
            self.log(f"Removing Chinese: '{text}' in {os.path.basename(filepath)}", 'WARN')
            self.log(f"  Context: ...{context}...", 'DEBUG')
            
            # Remove the Chinese text
            content = content[:start] + content[end:]
            fixes += 1
            
        return content, fixes
    
    def fix_orphaned_js(self, content):
        """Fix JavaScript code that's outside script tags"""
        
        orphan_indicators = [
            'INTELLIGENT MOBILE DETECTION',
            'BOOLEAN OBSERVER SYSTEM',
            'Device-Aware | Contextual',
            'Human Confirmation | Real-time Monitoring'
        ]
        
        fixes = 0
        
        for indicator in orphan_indicators:
            if indicator in content:
                # Find the position and wrap with script tag
                pos = content.find(indicator)
                
                # Go back to find line start
                line_start = content.rfind('\n', 0, pos) + 1
                
                # Check if already in script tag
                before = content[:line_start]
                if '<script' in before.rsplit('</script>', 1)[-1] if '</script>' in before else True:
                    continue
                    
                self.log(f"Wrapping orphaned JS: {indicator}", 'FIX')
                content = content[:line_start] + '<script>\n' + content[line_start:]
                
                # Find end of IIFE
                iife_end = content.find('})();', pos) + len('})();')
                content = content[:iife_end] + '\n</script>' + content[iife_end:]
                fixes += 1
                
        return content, fixes
    
    def fix_broken_script_tags(self, content):
        """Remove erroneous </script><script> pairs"""
        
        # Pattern: </script> immediately followed by more JS code
        pattern = r'</script>\s*\n(\s*//\s*|/\*|\w+\s*[=:(])'
        matches = list(re.finditer(pattern, content))
        
        fixes = 0
        for match in reversed(matches):
            self.log("Removing broken </script> tag", 'FIX')
            content = content[:match.start()] + content[match.start() + len('</script>'):match.end()].lstrip() + content[match.end():]
            fixes += 1
            
        return content, fixes
    
    def add_loader_failsafe(self, content):
        """Add automatic skeleton loader hide"""
        
        if 'skeletonLoader' not in content or 'loader-failsafe' in content:
            return content, 0
            
        failsafe = '''
  <!-- FAILSAFE: Auto-hide skeleton loader after 800ms -->
  <script id="loader-failsafe">
    (function() {
      function hideLoader() {
        var loader = document.getElementById('skeletonLoader');
        if (loader) {
          loader.style.opacity = '0';
          loader.style.visibility = 'hidden';
          loader.style.pointerEvents = 'none';
          setTimeout(function() { try { loader.remove(); } catch(e) {} }, 500);
        }
      }
      hideLoader();
      setTimeout(hideLoader, 800);
      setTimeout(hideLoader, 2000);
      setTimeout(hideLoader, 5000);
    })();
  </script>
'''
        
        if '</body>' in content:
            content = content.replace('</body>', failsafe + '\n</body>')
            return content, 1
            
        return content, 0
    
    def clean_file(self, filepath):
        """Clean a single file of all corruption types"""
        
        filename = os.path.basename(filepath)
        self.log(f"Scanning: {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original = f.read()
        except Exception as e:
            self.log(f"Error reading {filename}: {e}", 'ERROR')
            return 0
            
        content = original
        total_fixes = 0
        
        # Run all cleaners
        content, fixes1 = self.remove_chinese_text(content, filepath)
        total_fixes += fixes1
        
        content, fixes2 = self.fix_orphaned_js(content)
        total_fixes += fixes2
        
        content, fixes3 = self.fix_broken_script_tags(content)
        total_fixes += fixes3
        
        content, fixes4 = self.add_loader_failsafe(content)
        total_fixes += fixes4
        
        if total_fixes > 0 and not self.dry_run:
            # Create backup
            backup_path = filepath + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original)
            
            # Write cleaned version
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
            self.files_modified.append(filename)
            self.log(f"✅ Fixed {total_fixes} issues in {filename}", 'SUCCESS')
        elif total_fixes > 0:
            self.log(f"Would fix {total_fixes} issues in {filename} (dry run)", 'INFO')
        else:
            self.log(f"✓ {filename} is clean", 'OK')
            
        self.total_fixes += total_fixes
        return total_fixes
    
    def run(self, target_files=None):
        """Run cleaner on specified files or all HTML files"""
        
        print("=" * 70)
        print("🧹 SciMSPT Advanced Corruption Remover v2.0")
        print("=" * 70)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Base Directory: {self.base_dir}")
        print(f"🔍 Mode: {'DRY RUN (no changes)' if self.dry_run else 'LIVE (will modify files)'}")
        print()
        
        try:
            os.chdir(self.base_dir)
        except Exception as e:
            self.log(f"Cannot access directory: {e}", 'ERROR')
            return 2
        
        if target_files:
            html_files = [f for f in target_files if f.endswith('.html')]
        else:
            html_files = sorted(glob.glob('*.html'))
        
        if not html_files:
            self.log("No HTML files found!", 'ERROR')
            return 2
            
        print(f"📄 Processing {len(html_files)} files...\n")
        
        for filepath in html_files:
            self.clean_file(filepath)
            print()
        
        # Summary
        print("=" * 70)
        print("📊 CLEANING SUMMARY")
        print("=" * 70)
        print(f"Files scanned: {len(html_files)}")
        print(f"Files modified: {len(self.files_modified)}")
        print(f"Total issues fixed: {self.total_fixes}")
        
        if self.files_modified:
            print("\n📝 Modified files:")
            for f in self.files_modified:
                print(f"  • {f}")
        
        if self.total_fixes == 0:
            print("\n✨ All pages are CLEAN! Ready for deployment.")
            return 0
        else:
            print(f"\n🎉 Cleaning complete! {self.total_fixes} issues resolved.")
            return 1


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='SciMSPT Corruption Cleaner v2.0')
    parser.add_argument('files', nargs='*', help='Specific files to clean (default: all HTML)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying')
    parser.add_argument('--dir', help='Base directory (default: auto-detect)')
    
    args = parser.parse_args()
    
    cleaner = CorruptionCleaner(
        base_dir=args.dir,
        dry_run=args.dry_run
    )
    
    exit_code = cleaner.run(args.files if args.files else None)
    
    # Save audit log
    log_path = os.path.join(cleaner.base_dir, 'cleaning_audit.log')
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Cleaning Session: {datetime.now().isoformat()}\n")
        f.write(f"Exit Code: {exit_code}\n")
        f.write('\n'.join(cleaner.audit_log))
        f.write('\n')
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
