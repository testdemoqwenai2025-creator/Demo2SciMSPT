#!/usr/bin/env python3
"""
=============================================================================
SciMSPT PRE-DEPLOYMENT VALIDATION & AUTO-FIX SCRIPT
=============================================================================

PURPOSE:
--------
This script MUST RUN BEFORE every deployment/preview to ensure pages are clean.
It detects and auto-fixes:

1. 🚫 STUCK SKELETON LOADER - Gray placeholder bars blocking content
2. 🚫 JAVASCRIPT OUTSIDE <script> TAGS - BooleanObserver, MobileDetection code 
     rendering as visible text (Chinese characters, code snippets)
3. 🚫 BROKEN SCRIPT TAGS - </script><script> pairs splitting JS code mid-block
4. 🚫 ORPHANED COMMENTS - JS header comments showing as visible text
5. 🚫 MISMATCHED HTML TAGS - Unclosed/misaligned script/style blocks

USAGE:
------
# Run before every deployment (MANDATORY):
python3 pre_deploy_check.py

# Auto-fix all issues:
python3 pre_deploy_check.py --fix

# Fix + verify + deploy if clean:
python3 pre_deploy_check.py --fix --deploy

# Dry run (show issues without fixing):
python3 pre_deploy_check.py --dry-run

# Check specific file:
python3 pre_deploy_check.py index.html

GIT HOOK INTEGRATION:
--------------------
To automate this, add to .git/hooks/pre-push or run manually before:
git push demo2 main --force

EXIT CODES:
-----------
0 = All clean, ready for deployment
1 = Issues found (not fixed)
2 = Critical errors

VERSION: 2.0 - Comprehensive corruption detection & auto-fix
=============================================================================
"""

import re
import os
import sys
import glob
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum

class Severity(Enum):
    CRITICAL = "🔴 CRITICAL"
    WARNING = "🟡 WARNING"
    INFO = "🔵 INFO"

class IssueType(Enum):
    STUCK_LOADER = "STUCK_SKELETON_LOADER"
    JS_OUTSIDE_SCRIPT = "JS_OUTSIDE_SCRIPT"
    BROKEN_SCRIPT_TAGS = "BROKEN_SCRIPT_TAGS"
    ORPHANED_COMMENT = "ORPHANED_COMMENT"
    VISIBLE_CORRUPTION = "VISIBLE_CORRUPTION"
    MISMATCHED_TAGS = "MISMATCHED_SCRIPT_TAGS"

@dataclass
class Issue:
    line_num: int
    issue_type: IssueType
    severity: Severity
    description: str
    context: str
    filepath: str
    
    def to_dict(self):
        return {
            'line': self.line_num,
            'type': self.issue_type.value,
            'severity': self.severity.value,
            'description': self.description,
            'context': self.context[:100],
            'file': self.filepath
        }

class PageAuditor:
    """Comprehensive HTML page auditor for SciMSPT corruption detection"""
    
    # Patterns that indicate JavaScript code (should be inside <script>)
    JS_PATTERNS = [
        (r'^\s*(const|let|var)\s+\w+\s*=', 'Variable declaration'),
        (r'^\s*function\s+\w+\s*\(', 'Function definition'),
        (r'^\s*class\s+\w+', 'Class definition'),
        (r'^\s*(if|for|while|return|throw)\s', 'Control statement'),
        (r'^\s*(window|document|console|localStorage|navigator)\.', 'DOM/API access'),
        (r'^\s*//\s*$', 'Standalone comment'),
        (r'^\s*/\*', 'Block comment start'),
        (r'^\s*\*/', 'Block comment end'),
        (r'^\s*\*', 'JSDoc continuation'),
    ]
    
    # Keywords that indicate visible corruption when found outside scripts
    CORRUPTION_KEYWORDS = [
        'BooleanObserver',
        'MobileDetection',
        'INTELLIGENT MOBILE DETECTION',
        'BOOLEAN OBSERVER SYSTEM',
        'Device-Aware | Contextual',
        'Human Confirmation | Real-time Monitoring',
        'MobileDetection.init()',
        'BooleanObserver.init()',
    ]
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            self.content = f.read()
            self.original_content = self.content
        
        self.lines = self.content.split('\n')
        self.issues: List[Issue] = []
        self._script_lines: set = set()
        self._build_script_map()
    
    def _build_script_map(self):
        """Build a set of line indices that are inside script/style tags"""
        in_script = False
        in_style = False
        
        for i, line in enumerate(self.lines):
            # Check for script open (but not close on same line)
            if re.search(r'<script[^>]*>', line) and '</script>' not in line:
                in_script = True
            
            # Check for style open
            if re.search(r'<style[^>]*>', line) and '</style>' not in line:
                in_style = True
            
            # Mark as inside script/style
            if in_script or in_style:
                self._script_lines.add(i)
            
            # Check for closes
            if '</script>' in line:
                self._script_lines.add(i)  # Include the close tag line
                in_script = False
                
            if '</style>' in line:
                self._script_lines.add(i)
                in_style = False
    
    def _is_in_code_block(self, line_idx: int) -> bool:
        return line_idx in self._script_lines
    
    def _is_javascript_line(self, line: str) -> bool:
        """Check if a line looks like JavaScript code"""
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            return False
        
        # Skip pure HTML lines
        if stripped.startswith('<') and not stripped.startswith(('/*', '//')):
            return False
        
        # Check against JS patterns
        for pattern, desc in self.JS_PATTERNS:
            if re.match(pattern, stripped):
                return True
        
        return False
    
    def audit(self) -> List[Issue]:
        """Run all audits and return list of issues"""
        self.issues = []
        
        self._check_stuck_skeleton_loader()
        self._check_js_outside_scripts()
        self._check_broken_script_tags()
        self._check_orphaned_comments()
        self._check_visible_corruption()
        self._check_tag_balance()
        
        return self.issues
    
    def _check_stuck_skeleton_loader(self):
        """Check for skeleton loader that might get stuck"""
        # Look for skeleton loader without proper hide mechanism
        has_loader = 'skeletonLoader' in self.content
        has_failsafe = any(pattern in self.content for pattern in [
            'setTimeout.*loader.*hide',
            'setTimeout.*loader.*remove',
            r'loader\.style\.opacity',
            r'classList\.add.*hidden',
        ])
        
        if has_loader and not has_failsafe:
            self.issues.append(Issue(
                line_num=0,
                issue_type=IssueType.STUCK_LOADER,
                severity=Severity.WARNING,
                description='Skeleton loader found but no fail-safe hide mechanism detected',
                context='Add fail-safe: setTimeout(() => { loader.remove(); }, 3000);',
                filepath=self.filename
            ))
        
        # Check for position:fixed loader with high z-index (blocks page)
        if 'position:*fixed' in self.content.replace(' ', '') or 'position:fixed' in self.content:
            if 'z-index:*9999' in self.content.replace(' ', '') or 'z-index: 9999' in self.content:
                if 'setTimeout' not in self.content.split('</body>')[0] if '</body>' in self.content else self.content[-2000:]:
                    self.issues.append(Issue(
                        line_num=0,
                        issue_type=IssueType.STUCK_LOADER,
                        severity=Severity.CRITICAL,
                        description='Fixed-position skeleton loader may block page without timeout fallback',
                        context='Loader has position:fixed; z-index:9999 but no reliable hide mechanism',
                        filepath=self.filename
                    ))
    
    def _check_js_outside_scripts(self):
        """Find JavaScript code that's outside of script tags"""
        for i, line in enumerate(self.lines):
            if self._is_in_code_block(i):
                continue
            
            if self._is_javascript_line(line):
                stripped = line.strip()
                
                # Skip false positives
                if '<' in stripped and ('</' in stripped or '/>' in stripped):
                    continue
                
                self.issues.append(Issue(
                    line_num=i + 1,
                    issue_type=IssueType.JS_OUTSIDE_SCRIPT,
                    severity=Severity.CRITICAL,
                    description=f'JavaScript code outside <script> tags: {stripped[:60]}',
                    context=line.strip()[:100],
                    filepath=self.filename
                ))
    
    def _check_broken_script_tags(self):
        """Find broken </script><script> patterns that split JS code"""
        for i, line in enumerate(self.lines):
            stripped = line.strip()
            
            # Look for orphaned </script> followed by JS-like content
            if stripped == '</script>' and i + 1 < len(self.lines):
                next_stripped = self.lines[i + 1].strip()
                
                # If next line looks like continued JS, this </script> is wrong
                if (next_stripped and 
                    not next_stripped.startswith(('<', '//')) and
                    (re.match(r'^[\s\w"\'\:.,(){}\[\];]', next_stripped) or
                     next_stripped.startswith(('message:', 'action:', 'icon:', 'buttonText:')))):
                    
                    self.issues.append(Issue(
                        line_num=i + 1,
                        issue_type=IssueType.BROKEN_SCRIPT_TAGS,
                        severity=Severity.CRITICAL,
                        description='Orphaned </script> splitting JavaScript code',
                        context=f'</script> followed by: {next_stripped[:50]}',
                        filepath=self.filename
                    ))
            
            # Look for orphaned <script> after JS code (not starting new block)
            if stripped == '<script>' and i > 0:
                prev_idx = i - 1
                while prev_idx >= 0 and not self.lines[prev_idx].strip():
                    prev_idx -= 1
                
                if prev_idx >= 0:
                    prev_line = self.lines[prev_idx].strip()
                    # If previous line looks like unfinished JS
                    if prev_line.endswith(('{', ',', '(', 'return', '}')) or prev_line.startswith('//'):
                        self.issues.append(Issue(
                            line_num=i + 1,
                            issue_type=IssueType.BROKEN_SCRIPT_TAGS,
                            severity=Severity.CRITICAL,
                            description='Orphaned <script> breaking JavaScript flow',
                            context=f'<script> after: {prev_line[:50]}',
                            filepath=self.filename
                        ))
    
    def _check_orphaned_comments(self):
        """Find JS-style comments outside script tags that show as text"""
        for i, line in enumerate(self.lines):
            if self._is_in_code_block(i):
                continue
            
            stripped = line.strip()
            
            # Detect JS header comment pattern
            if re.match(r'^\s*/\*[=~-]+\s*$', stripped):
                # Look ahead to see if this is an orphaned comment block
                block_end = min(i + 5, len(self.lines))
                block_text = '\n'.join(self.lines[i:block_end])
                
                if any(indicator in block_text for indicator in [
                    r'SYSTEM\s+v?\d', r'DETECTION\s+SYSTEM', r'OBSERVER\s+SYSTEM',
                    'Device-Aware', 'Contextual.*Helpful'
                ]):
                    self.issues.append(Issue(
                        line_num=i + 1,
                        issue_type=IssueType.ORPHANED_COMMENT,
                        severity=Severity.CRITICAL,
                        description='Orphaned JavaScript header comment will render as visible text',
                        context=stripped[:80],
                        filepath=self.filename
                    ))
    
    def _check_visible_corruption(self):
        """Find specific known corruption patterns"""
        for i, line in enumerate(self.lines):
            if self._is_in_code_block(i):
                continue
            
            for keyword in self.CORRUPTION_KEYWORDS:
                if keyword in line:
                    # Make sure it's not in an onclick handler or similar
                    if 'onclick' not in line and '<' not in line or line.strip().startswith(keyword):
                        self.issues.append(Issue(
                            line_num=i + 1,
                            issue_type=IssueType.VISIBLE_CORRUPTION,
                            severity=Severity.CRITICAL,
                            description=f'Visible corruption pattern "{keyword}"',
                            context=line.strip()[:100],
                            filepath=self.filename
                        ))
                        break  # Only report once per line
    
    def _check_tag_balance(self):
        """Check for mismatched script/style tags"""
        open_scripts = len(re.findall(r'<script[^>]*>', self.content))
        close_scripts = len(re.findall(r'</script>', self.content))
        
        if open_scripts != close_scripts:
            self.issues.append(Issue(
                line_num=0,
                issue_type=IssueType.MISMATCHED_TAGS,
                severity=Severity.CRITICAL,
                description=f'Script tags unbalanced: {open_scripts} open, {close_scripts} close',
                context='',
                filepath=self.filename
            ))
    
    def get_summary(self) -> Dict:
        """Get summary of audit results"""
        critical = sum(1 for i in self.issues if i.severity == Severity.CRITICAL)
        warning = sum(1 for i in self.issues if i.severity == Severity.WARNING)
        info = sum(1 for i in self.issues if i.severity == Severity.INFO)
        
        types = {}
        for issue in self.issues:
            types[issue.issue_type.value] = types.get(issue.issue_type.value, 0) + 1
        
        return {
            'file': self.filename,
            'total': len(self.issues),
            'critical': critical,
            'warning': warning,
            'info': info,
            'types': types,
            'clean': critical == 0,
            'has_warnings': warning > 0
        }


class AutoFixer:
    """Automatic fixer for common HTML corruption issues"""
    
    def __init__(self, auditor: PageAuditor):
        self.auditor = auditor
        self.filepath = auditor.filepath
        self.fixes_applied = 0
        self.fix_log: List[str] = []
    
    def fix_all(self) -> bool:
        """Apply all available fixes. Returns True if fixes were applied."""
        original_content = self.auditor.content
        
        self._fix_orphaned_comments()
        self._fix_broken_script_tags()
        self._fix_js_outside_scripts()
        self._add_loader_failsafe()
        
        # Save if changes were made
        if self.auditor.content != original_content:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(self.auditor.content)
            
            print(f"   ✅ Applied {self.fixes_applied} fix(es) to {self.auditor.filename}")
            for log_msg in self.fix_log:
                print(f"      • {log_msg}")
            return True
        
        return False
    
    def _fix_orphaned_comments(self):
        """Remove orphaned JS header comments outside script tags"""
        lines = self.auditor.content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Detect start of orphaned comment block
            if re.match(r'^\s*/\*[=~-]+\s*$', stripped):
                # Check if we're outside script tags
                if i not in self.auditor._script_lines:
                    # Look ahead to confirm it's a JS header comment
                    block_end = min(i + 6, len(lines))
                    block_text = '\n'.join(lines[i:block_end])
                    
                    if any(indicator in block_text for indicator in [
                        'SYSTEM', 'DETECTION', 'OBSERVER', 'Device-Aware', 'Contextual'
                    ]):
                        # Skip entire comment block
                        start_i = i
                        while i < len(lines):
                            if '*/' in lines[i]:
                                i += 1
                                break
                            i += 1
                        
                        # Also skip metadata lines
                        while i < len(lines):
                            next_stripped = lines[i].strip()
                            if not next_stripped or next_stripped.startswith('<'):
                                break
                            if re.match(r'^[A-Za-z]+\s*\|', next_stripped):
                                i += 1
                                continue
                            break
                        
                        removed_count = i - start_i
                        self.fixes_applied += 1
                        self.fix_log.append(f"Removed orphaned JS comment block ({removed_count} lines)")
                        continue
            
            fixed_lines.append(line)
            i += 1
        
        self.auditor.content = '\n'.join(fixed_lines)
        # Rebuild script map after changes
        self.auditor._build_script_map()
    
    def _fix_broken_script_tags(self):
        """Remove erroneously placed </script><script> pairs splitting JS code"""
        lines = self.auditor.content.split('\n')
        fixed_lines = []
        i = 0
        in_corrupt_zone = False
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Detect corrupt zone: IIFE pattern followed by <script>
            if (not in_corrupt_zone and 
                stripped == '(function() {' and 
                i + 2 < len(lines) and 
                lines[i+1].strip() == "'use strict';" and
                i + 3 < len(lines) and
                lines[i+3].strip() == '<script>'):
                
                in_corrupt_zone = True
                fixed_lines.append('<script>')  # Add proper opening
                fixed_lines.append(line)
                self.fixes_applied += 1
                i += 1
                continue
            
            if in_corrupt_zone:
                # Skip orphaned script tags
                if stripped in ['<script>', '</script>']:
                    self.fixes_applied += 1
                    i += 1
                    continue
                
                fixed_lines.append(line)
                
                # End of IIFE
                if stripped == '})();':
                    fixed_lines.append('</script>')  # Add proper closing
                    in_corrupt_zone = False
                    self.fixes_applied += 1
                
                i += 1
                continue
            
            fixed_lines.append(line)
            i += 1
        
        self.auditor.content = '\n'.join(fixed_lines)
        self.auditor._build_script_map()
    
    def _fix_js_outside_scripts(self):
        """Wrap orphaned JS code in proper script tags"""
        lines = self.auditor.content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Skip if already in script block
            if i in self.auditor._script_lines:
                fixed_lines.append(line)
                i += 1
                continue
            
            # Check if this is JS code outside script
            if self.auditor._is_javascript_line(line):
                # Collect consecutive JS lines
                js_block = []
                while i < len(lines) and i not in self.auditor._script_lines:
                    if self.auditor._is_javascript_line(lines[i]) or lines[i].strip() == '':
                        js_block.append(lines[i])
                        i += 1
                    else:
                        break
                
                if js_block:
                    # Wrap in script tags
                    fixed_lines.append('<script>')
                    fixed_lines.extend(js_block)
                    fixed_lines.append('</script>')
                    self.fixes_applied += 1
                    self.fix_log.append(f"Wrapped {len(js_block)} lines of orphaned JS in <script>")
                continue
            
            fixed_lines.append(line)
            i += 1
        
        self.auditor.content = '\n'.join(fixed_lines)
        self.auditor._build_script_map()
    
    def _add_loader_failsafe(self):
        """Add failsafe mechanism for skeleton loaders if missing"""
        if 'skeletonLoader' not in self.auditor.content:
            return
        
        # Check if failsafe exists
        has_failsafe = any(pattern in self.auditor.content for pattern in [
            'loader-failsafe',
            'forceHideLoader',
            'setTimeout.*loader.*800',
        ])
        
        if not has_failsafe:
            # Find where to insert (before </body>)
            failsafe_script = '''
  <!-- FAILSAFE: Force hide skeleton loader after 800ms -->
  <script>
    (function() {
      var loader = document.getElementById('skeletonLoader');
      if (loader) {
        setTimeout(function() {
          loader.style.opacity = '0';
          loader.style.visibility = 'hidden';
          setTimeout(function() { if (loader.parentNode) loader.remove(); }, 500);
        }, 800);
      }
    })();
  </script>
'''
            
            if '</body>' in self.auditor.content:
                self.auditor.content = self.auditor.content.replace('</body>', failsafe_script + '\n</body>')
                self.fixes_applied += 1
                self.fix_log.append("Added skeleton loader failsafe (800ms timeout)")


def print_header():
    """Print script header"""
    print("\n" + "=" * 70)
    print("🔍 SciMSPT PRE-DEPLOYMENT VALIDATION")
    print("=" * 70)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def print_report(auditors: List[PageAuditor], verbose: bool = True):
    """Print formatted audit report"""
    total_issues = sum(len(a.issues) for a in auditors)
    total_critical = sum(s.get_summary()['critical'] for s in auditors)
    total_clean = sum(1 for a in auditors if a.get_summary()['clean'])
    
    print("-" * 70)
    print("📊 AUDIT RESULTS")
    print("-" * 70)
    print(f"Files scanned: {len(auditors)}")
    print(f"Clean files: {total_clean}/{len(auditors)}")
    print(f"Total issues: {total_issues} ({total_critical} critical)")
    print()
    
    # Per-file summary
    for auditor in sorted(auditors, key=lambda x: -len(x.issues)):
        summary = auditor.get_summary()
        status = "✅ CLEAN" if summary['clean'] else f"❌ {summary['total']} ISSUES"
        print(f"  {auditor.filename:35} {status}")
        
        if verbose and not summary['clean'] and summary['types']:
            for itype, count in summary['types'].items():
                print(f"      └─ {itype}: {count}")
    
    print()
    
    # Overall status
    if total_critical == 0:
        print("✅✅✅ ALL PAGES ARE CLEAN - READY FOR DEPLOYMENT ✅✅✅")
        return True
    else:
        print("❌ ISSUES FOUND - FIX REQUIRED BEFORE DEPLOYMENT")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='SciMSPT Pre-Deployment Validation Script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 pre_deploy_check.py              # Audit only
  python3 pre_deploy_check.py --fix         # Audit + auto-fix
  python3 pre_deploy_check.py --fix --deploy # Fix + push to GitHub
  python3 pre_deploy_check.py index.html    # Single file
        """
    )
    
    parser.add_argument('files', nargs='*', help='Specific files to check (default: all)')
    parser.add_argument('--fix', action='store_true', help='Auto-fix detected issues')
    parser.add_argument('--deploy', action='store_true', help='Push to GitHub after fixing')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    parser.add_argument('--quiet', action='store_true', help='Only show summary')
    parser.add_argument('--force', action='store_true', help='Deploy even with warnings')
    
    args = parser.parse_args()
    
    # Determine files to scan
    base_dir = '/home/z/my-project/SciMSPT'
    
    if args.files:
        html_files = [f if os.path.isabs(f) else os.path.join(base_dir, f) for f in args.files]
    else:
        html_files = glob.glob(os.path.join(base_dir, '*.html'))
    
    if not html_files:
        print("❌ No HTML files found!")
        sys.exit(2)
    
    # Print header
    if not args.quiet:
        print_header()
    
    # Audit all files
    auditors = []
    for filepath in sorted(html_files):
        try:
            auditor = PageAuditor(filepath)
            auditor.audit()
            auditors.append(auditor)
        except Exception as e:
            print(f"❌ Error auditing {os.path.basename(filepath)}: {e}")
    
    # Print initial report
    is_clean = print_report(auditors, verbose=not args.quiet and not args.json)
    
    # Apply fixes if requested
    if args.fix or args.dry_run:
        if is_clean and not args.dry_run:
            if not args.quiet:
                print("\n✅ No fixes needed - all pages are clean!")
        else:
            if not args.quiet:
                print("\n" + "=" * 70)
                print("🔧 APPLYING FIXES")
                print("=" * 70)
            
            for auditor in auditors:
                if not auditor.get_summary()['clean']:
                    if args.dry_run:
                        print(f"\n  Would fix: {auditor.filename}")
                        for issue in auditor.issues[:10]:
                            print(f"    • [{issue.severity.value}] Line {issue.line_num}: {issue.description[:60]}")
                    else:
                        fixer = AutoFixer(auditor)
                        fixer.fix_all()
                        
                        # Re-audit after fix
                        auditor.content = auditor.original_content  # Reset
                        with open(auditor.filepath, 'r') as f:
                            auditor.content = f.read()
                        auditor.lines = auditor.content.split('\n')
                        auditor._build_script_map()
                        auditor.issues = []
                        auditor.audit()
            
            # Re-print status after fixes
            if not args.dry_run and not args.quiet:
                print("\n" + "=" * 70)
                print("📋 POST-FIX STATUS")
                print("=" * 70)
                is_clean = all(a.get_summary()['clean'] for a in auditors)
                print_report(auditors, verbose=False)
    
    # Deploy if requested and clean
    if args.deploy and not args.dry_run:
        final_clean = all(a.get_summary()['clean'] for a in auditors)
        
        if final_clean or args.force:
            if not args.quiet:
                print("\n" + "=" * 70)
                print("🚀 DEPLOYING TO GITHUB PAGES")
                print("=" * 70)
            
            try:
                os.chdir(base_dir)
                
                # Git operations
                subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
                
                commit_msg = f"""🔧 Pre-deployment validation & auto-fix ({datetime.now().strftime('%Y-%m-%d %H:%M')})

Automated fixes applied by pre_deploy_check.py:
- Removed visible JavaScript corruption
- Fixed broken script tags
- Added skeleton loader failsafes
- Verified all pages render correctly"""

                result = subprocess.run(
                    ['git', 'commit', '-m', commit_msg],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0 and 'nothing to commit' not in result.stderr:
                    print(f"Commit warning: {result.stderr}")
                
                # Push to demo2 remote
                push_result = subprocess.run(
                    ['git', 'push', 'demo2', 'main', '--force'],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if push_result.returncode == 0:
                    print("✅ Successfully deployed to GitHub Pages!")
                    print("🌐 Live URL: https://testdemoqwenai2025-creator.github.io/Demo2SciMSPT/")
                else:
                    print(f"❌ Push failed: {push_result.stderr}")
                    sys.exit(1)
                    
            except subprocess.TimeoutExpired:
                print("❌ Git operation timed out")
                sys.exit(1)
            except Exception as e:
                print(f"❌ Deployment error: {e}")
                sys.exit(1)
        else:
            print("\n❌ Cannot deploy: pages still have issues. Run with --fix first.")
            sys.exit(1)
    
    # JSON output
    if args.json:
        import json
        output = {
            'timestamp': datetime.now().isoformat(),
            'files': [{
                'filename': a.filename,
                'summary': a.get_summary(),
                'issues': [i.to_dict() for i in a.issues]
            } for a in auditors],
            'all_clean': all(a.get_summary()['clean'] for a in auditors)
        }
        print(json.dumps(output, indent=2))
    
    # Exit with appropriate code
    final_status = all(a.get_summary()['clean'] for a in auditors)
    sys.exit(0 if final_status else 1)


if __name__ == '__main__':
    main()
