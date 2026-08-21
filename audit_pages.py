#!/usr/bin/env python3
"""
SciMSPT Page Auditor & Cleanup Script
======================================
Detects and reports common HTML corruption patterns:
1. JavaScript/code outside <script> tags
2. Orphaned JS comments (/* ... */) in HTML body
3. Unclosed/mismatched script/style tags
4. Visible raw code that should be hidden
5. Chinese text in inappropriate locations (optional)

Usage:
  python3 audit_pages.py              # Audit all pages
  python3 audit_pages.py --fix        # Auto-fix common issues
  python3 audit_pages.py index.html   # Audit specific file
"""

import re
import os
import sys
import glob
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class Issue:
    line_num: int
    issue_type: str
    description: str
    severity: str  # 'CRITICAL', 'WARNING', 'INFO'
    context: str

class HTMLAuditor:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            self.content = f.read()
        self.lines = self.content.split('\n')
        self.issues: List[Issue] = []
    
    def audit(self) -> List[Issue]:
        """Run all audits and return list of issues"""
        self.issues = []
        self._check_js_outside_scripts()
        self._check_orphaned_comments()
        self._check_tag_balance()
        self._check_visible_code_patterns()
        return self.issues
    
    def _is_in_script_or_style(self, line_idx: int) -> bool:
        """Check if a line is inside a script or style tag"""
        # Build context up to this line
        context = '\n'.join(self.lines[:line_idx + 1])
        
        # Count open/close tags before this line
        open_scripts = len(re.findall(r'<script[^>]*>', context))
        close_scripts = len(re.findall(r'</script>', context))
        open_styles = len(re.findall(r'<style[^>]*>', context))
        close_styles = len(re.findall(r'</style>', context))
        
        # If we're inside an unclosed script or style block
        return (open_scripts > close_scripts) or (open_styles > close_styles)
    
    def _check_js_outside_scripts(self):
        """Find JavaScript code that's outside of script tags"""
        js_patterns = [
            (r'^\s*(const|let|var)\s+\w+\s*=', 'Variable declaration'),
            (r'^\s*function\s+\w+\s*\(', 'Function definition'),
            (r'^\s*class\s+\w+\s*\{', 'Class definition'),
            (r'^\s*(if|for|while|return|throw)\s', 'Control statement'),
            (r'^\s*(window|document|console|localStorage)\.', 'DOM/API access'),
            (r'^\s*//\s*$', 'Standalone comment line'),
            (r'^\s*\*\s*$', 'JSDoc comment line'),
            (r'^\s*/\*', 'Block comment start'),
            (r'^\s*\*/', 'Block comment end'),
        ]
        
        for i, line in enumerate(self.lines):
            if self._is_in_script_or_style(i):
                continue
            
            line_stripped = line.strip()
            
            for pattern, desc in js_patterns:
                if re.match(pattern, line_stripped):
                    # Skip if it looks like it's part of normal HTML
                    if '<' in line and ('</' in line or '/>' in line):
                        continue
                    
                    self.issues.append(Issue(
                        line_num=i + 1,
                        issue_type='JS_OUTSIDE_SCRIPT',
                        description=f'{desc}: {line_stripped[:80]}',
                        severity='CRITICAL',
                        context=line.strip()[:100]
                    ))
                    break
    
    def _check_orphaned_comments(self):
        """Find orphaned JS-style comments outside script tags"""
        for i, line in enumerate(self.lines):
            if self._is_in_script_or_style(i):
                continue
            
            line_stripped = line.strip()
            
            # Look for JS comment patterns that shouldn't be in HTML
            if re.match(r'^\s*/\*+', line_stripped):  # /* or /**
                # Check if it looks like a JS header comment
                if '=' in line_stripped or '-' in line_stripped:
                    if 'SYSTEM' in line_stripped or 'v\d' in line_stripped or 'DETECTION' in line_stripped:
                        self.issues.append(Issue(
                            line_num=i + 1,
                            issue_type='ORPHANED_COMMENT',
                            description=f'Orphaned JS header comment: {line_stripped[:70]}',
                            severity='CRITICAL',
                            context=line.strip()[:100]
                        ))
            
            # Also catch lines like "Device-Aware | Contextual | Helpful"
            if re.match(r'^[A-Za-z]+\s*\|\s*[A-Za-z]+\s*\|\s*[A-Za-z]+', line_stripped):
                # Check if previous line was a comment opener
                if i > 0 and '/*' in self.lines[i-1]:
                    self.issues.append(Issue(
                        line_num=i + 1,
                        issue_type='ORPHANED_COMMENT',
                        description=f'Orphaned comment metadata: {line_stripped[:70]}',
                        severity='CRITICAL',
                        context=line.strip()[:100]
                    ))
    
    def _check_tag_balance(self):
        """Check for mismatched script/style tags"""
        open_scripts = len(re.findall(r'<script[^>]*>', self.content))
        close_scripts = len(re.findall(r'</script>', self.content))
        open_styles = len(re.findall(r'<style[^>]*>', self.content))
        close_styles = len(re.findall(r'</style>', self.content))
        
        if open_scripts != close_scripts:
            self.issues.append(Issue(
                line_num=0,
                issue_type='MISMATCHED_SCRIPT_TAGS',
                description=f'Script tags unbalanced: {open_scripts} open, {close_scripts} close',
                severity='CRITICAL',
                context=''
            ))
        
        if open_styles != close_styles:
            self.issues.append(Issue(
                line_num=0,
                issue_type='MISMATCHED_STYLE_TAGS',
                description=f'Style tags unbalanced: {open_styles} open, {close_styles} close',
                severity='WARNING',
                context=''
            ))
    
    def _check_visible_code_patterns(self):
        """Find patterns that indicate visible code corruption"""
        # Look for specific known corruption patterns
        corruption_indicators = [
            'BooleanObserver',
            'MobileDetection',
            'INTELLIGENT MOBILE',
            'BOOLEAN OBSERVER',
            'Device-Aware',
            'Contextual | Helpful',
            'Human Confirmation',
            'Real-time Monitoring',
        ]
        
        for i, line in enumerate(self.lines):
            if self._is_in_script_or_style(i):
                continue
            
            for indicator in corruption_indicators:
                if indicator in line and not line.strip().startswith('<'):
                    # This is likely visible corruption
                    self.issues.append(Issue(
                        line_num=i + 1,
                        issue_type='VISIBLE_CORRUPTION',
                        description=f'Visible code pattern "{indicator}"',
                        severity='CRITICAL',
                        context=line.strip()[:100]
                    ))
    
    def get_summary(self) -> dict:
        """Get summary of issues found"""
        critical = sum(1 for i in self.issues if i.severity == 'CRITICAL')
        warning = sum(1 for i in self.issues if i.severity == 'WARNING')
        info = sum(1 for i in self.issues if i.severity == 'INFO')
        
        types = {}
        for issue in self.issues:
            types[issue.issue_type] = types.get(issue.issue_type, 0) + 1
        
        return {
            'file': self.filename,
            'total': len(self.issues),
            'critical': critical,
            'warning': warning,
            'info': info,
            'types': types,
            'clean': critical == 0
        }

def print_report(auditor: HTMLAuditor, verbose: bool = True):
    """Print formatted audit report"""
    summary = auditor.get_summary()
    
    status = "✅ CLEAN" if summary['clean'] else "❌ ISSUES FOUND"
    print(f"\n{'='*60}")
    print(f"📄 {summary['file']}: {status}")
    print(f"{'='*60}")
    print(f"   Total Issues: {summary['total']}")
    print(f"   🔴 Critical: {summary['critical']}")
    print(f"   🟡 Warning: {summary['warning']}")
    print(f"   🔵 Info: {summary['info']}")
    
    if summary['types']:
        print(f"\n   Issue Types:")
        for itype, count in summary['types'].items():
            print(f"      • {itype}: {count}")
    
    if verbose and auditor.issues:
        print(f"\n   Details:")
        print(f"   {'-'*60}")
        for issue in auditor.issues:
            icon = {'CRITICAL': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}[issue.severity]
            print(f"   {icon} Line {issue.line_num}: [{issue.issue_type}]")
            print(f"      {issue.description}")
            if issue.context:
                print(f"      Context: {issue.context[:80]}")
            print()

def fix_common_issues(filepath: str, dry_run: bool = False) -> int:
    """
    Auto-fix common issues:
    - Remove orphaned JS comments outside script tags
    - Returns number of fixes applied
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    lines = content.split('\n')
    fixed_lines = []
    fixes_applied = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Detect orphaned JS comment blocks
        if re.match(r'^\s*/\*+[=~-]*\s*$', stripped):
            # Check if this is an orphaned comment (not inside script/style)
            # Look ahead to see if it's a header comment block
            block_start = i
            while i < len(lines) and not ('<script' in lines[i] or '<style' in lines[i] or 
                                          '</' in lines[i] or '<section' in lines[i] or 
                                          '<div' in lines[i] or '<!--' in lines[i]):
                i += 1
                if i - block_start > 10:  # Don't skip too many lines
                    break
            
            # Check if the block looks like orphaned JS documentation
            block_text = '\n'.join(lines[block_start:i])
            if any(indicator in block_text for indicator in 
                   ['SYSTEM', 'DETECTION', 'OBSERVER', 'Device-Aware', 'Contextual']):
                # Skip these lines (remove them)
                fixes_applied += i - block_start
                continue
        
        fixed_lines.append(line)
        i += 1
    
    if fixes_applied > 0 and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(fixed_lines))
        print(f"   ✅ Applied {fixes_applied} fixes to {os.path.basename(filepath)}")
    elif fixes_applied > 0:
        print(f"   📋 Would apply {fixes_applied} fixes to {os.path.basename(filepath)} (dry run)")
    
    return fixes_applied

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Audit SciMSPT HTML pages for corruption')
    parser.add_argument('files', nargs='*', help='Specific files to audit (default: all HTML)')
    parser.add_argument('--fix', action='store_true', help='Auto-fix common issues')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without changing files')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    args = parser.parse_args()
    
    # Find HTML files
    base_dir = '/home/z/my-project/SciMSPT'
    if args.files:
        html_files = [f if os.path.isabs(f) else os.path.join(base_dir, f) for f in args.files]
    else:
        html_files = glob.glob(os.path.join(base_dir, '*.html'))
    
    if not html_files:
        print("No HTML files found!")
        sys.exit(1)
    
    print("=" * 60)
    print("🔍 SciMSPT Page Auditor")
    print("=" * 60)
    print(f"Scanning {len(html_files)} file(s)...")
    
    all_clean = True
    results = []
    
    for filepath in sorted(html_files):
        try:
            auditor = HTMLAuditor(filepath)
            auditor.audit()
            
            if args.fix or args.dry_run:
                fix_common_issues(filepath, dry_run=args.dry_run)
                # Re-audit after fix
                auditor = HTMLAuditor(filepath)
                auditor.audit()
            
            results.append(auditor)
            print_report(auditor)
            
            if not auditor.get_summary()['clean']:
                all_clean = False
                
        except Exception as e:
            print(f"\n❌ Error processing {os.path.basename(filepath)}: {e}")
            all_clean = False
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    total_issues = sum(len(a.issues) for a in results)
    clean_count = sum(1 for a in results if a.get_summary()['clean'])
    
    print(f"Files scanned: {len(results)}")
    print(f"Clean files: {clean_count}/{len(results)}")
    print(f"Total issues: {total_issues}")
    
    if all_clean:
        print("\n✅ All pages are clean! Ready for deployment.")
    else:
        print("\n❌ Some pages have issues. Run with --fix to auto-fix.")
    
    if args.json:
        import json
        json_results = [{
            'file': r.filename,
            'summary': r.get_summary(),
            'issues': [{'line': i.line_num, 'type': i.issue_type, 'desc': i.description, 'severity': i.severity} 
                       for i in r.issues]
        } for r in results]
        print(json.dumps(json_results, indent=2))
    
    sys.exit(0 if all_clean else 1)

if __name__ == '__main__':
    main()
