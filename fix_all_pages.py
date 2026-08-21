#!/usr/bin/env python3
"""
SciMSPT Auto-Fix Script
=======================
Automatically fixes common HTML corruption patterns:
1. JavaScript code outside <script> tags - wraps it properly
2. Orphaned JS comments - removes them
3. Missing script tags before JS code blocks

This script is designed to be safe - it only adds <script> tags where
JavaScript code is clearly detected outside of script contexts.
"""

import re
import os
import glob
from pathlib import Path

def find_script_boundaries(lines):
    """
    Returns a set of line indices that are inside script/style tags.
    """
    in_script = False
    in_style = False
    script_lines = set()
    
    for i, line in enumerate(lines):
        # Check for script tags
        if re.search(r'<script[^>]*>', line) and not re.search(r'</script>', line):
            in_script = True
        if '</script>' in line:
            # Mark this line as still in script (it contains the close tag)
            script_lines.add(i)
            in_script = False
            continue
        
        # Check for style tags  
        if re.search(r'<style[^>]*>', line) and not re.search(r'</style>', line):
            in_style = True
        if '</style>' in line:
            script_lines.add(i)
            in_style = False
            continue
        
        if in_script or in_style:
            script_lines.add(i)
    
    return script_lines

def is_javascript_line(line):
    """Check if a line looks like JavaScript code"""
    stripped = line.strip()
    
    # Skip empty lines and pure HTML
    if not stripped:
        return False
    if stripped.startswith('<') and not stripped.startswith('/*') and not stripped.startswith('//'):
        return False
    
    # Patterns that indicate JavaScript
    js_patterns = [
        r'^const\s+\w+\s*=', r'^let\s+\w+\s*=', r'^var\s+\w+\s*=',
        r'^function\s+\w+\s*\(', r'^\w+\s*\([^)]*\)\s*\{',  # Arrow functions or calls
        r'^class\s+\w+', r'^if\s*\(', r'^for\s*\(', r'^while\s*\(',
        r'^return\s+', r'^throw\s+',
        r'^console\.', r'^window\.', r'^document\.', r'^localStorage\.',
        r'^navigator\.', r'^setTimeout', r'^setInterval',
        r'^//\s*',  # Line comment
        r'^/\*\*',  # JSDoc start
        r'^/\*',    # Block comment start
        r'^\*',     # JSDoc continuation
        r'\*/$',    # Block comment end
        r'^this\.', r'^new\s+\w+',
        r'^import\s+', r'^export\s+',
        r'^async\s+function', r'^await\s+',
        r'^catch\s*\(', r'^try\s*\{',
        r'^switch\s*\(', r'^case\s+',
        r'^default\s*:',
        r'^else\s*if|^else\s*\{|^else\s*$',
    ]
    
    for pattern in js_patterns:
        if re.match(pattern, stripped):
            return True
    
    return False

def is_js_header_comment(lines, start_idx):
    """Check if this looks like an orphaned JS header comment block"""
    # Look for patterns like:
    # /* ============================================
    #    SYSTEM NAME v4.0
    #    Description
    # ============================================ */
    
    block_text = '\n'.join(lines[start_idx:min(start_idx + 5, len(lines))])
    
    indicators = [
        r'SYSTEM\s+v?\d',
        r'DETECTION\s+SYSTEM',
        r'OBSERVER\s+SYSTEM',
        r'Device-Aware',
        r'Contextual.*Helpful',
        r'Human Confirmation',
        r'Real-time Monitoring',
        r'INTELLIGENT\s+MOBILE',
        r'BOOLEAN\s+OBSERVER',
    ]
    
    for indicator in indicators:
        if re.search(indicator, block_text, re.IGNORECASE):
            return True
    
    return False

def fix_file(filepath, dry_run=False):
    """Fix a single HTML file. Returns number of fixes applied."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    lines = content.split('\n')
    script_lines = find_script_boundaries(lines)
    
    fixed_lines = []
    i = 0
    fixes_applied = 0
    pending_script_open = False
    
    while i < len(lines):
        line = lines[i]
        
        # If we're already in a script block, keep as-is
        if i in script_lines:
            fixed_lines.append(line)
            i += 1
            continue
        
        # Check if this line is JavaScript outside of script
        if is_javascript_line(line):
            # Start of a new JS block that needs wrapping
            js_block_start = i
            
            # Check if it's an orphaned header comment that should be removed
            if is_js_header_comment(lines, i):
                # Skip the entire comment block
                while i < len(lines):
                    stripped = lines[i].strip()
                    if '*/' in stripped:
                        i += 1
                        break
                    i += 1
                
                # Also skip any metadata lines after the comment
                while i < len(lines):
                    stripped = lines[i].strip()
                    if not stripped or stripped.startswith('<'):
                        break
                    if re.match(r'^[A-Za-z]+\s*\|', stripped):
                        i += 1
                        continue
                    break
                
                fixes_applied += i - js_block_start
                continue
            
            # Collect consecutive JS lines
            js_block_lines = []
            while i < len(lines) and i not in script_lines:
                current_line = lines[i]
                if is_javascript_line(current_line) or current_line.strip() == '' or current_line.strip().startswith('*'):
                    js_block_lines.append(current_line)
                    i += 1
                else:
                    # Check if we should include this non-JS line
                    # (might be part of object literal, etc.)
                    if js_block_lines and i < len(lines) - 1:
                        next_is_js = is_javascript_line(lines[i + 1]) if i + 1 < len(lines) else False
                        if next_is_js or (current_line.strip() and current_line.strip() in ['}', ']', ');', '});']):
                            js_block_lines.append(current_line)
                            i += 1
                            continue
                    break
            
            if js_block_lines:
                # Add script wrapper
                fixed_lines.append('<script>')
                fixed_lines.extend(js_block_lines)
                fixed_lines.append('</script>')
                fixes_applied += 1
            continue
        
        # Regular HTML line
        fixed_lines.append(line)
        i += 1
    
    if fixes_applied > 0 and not dry_run:
        new_content = '\n'.join(fixed_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"   ✅ Fixed {filepath}: {fixes_applied} script block(s) wrapped")
    elif fixes_applied > 0:
        print(f"   📋 Would fix {filepath}: {fixes_applied} script block(s) (dry run)")
    
    return fixes_applied

def verify_fix(filepath):
    """Verify that a file has no more issues"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    script_lines = find_script_boundaries([line.rstrip('\n') for line in lines])
    issues = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        stripped = line.strip()
        
        if i not in script_lines and is_javascript_line(stripped):
            # Double-check it's really an issue
            if '<' not in stripped or ('</' not in stripped and '/>' not in stripped):
                issues.append((line_num, stripped[:60]))
    
    return issues

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Auto-fix SciMSPT HTML corruption')
    parser.add_argument('files', nargs='*', help='Specific files to fix (default: all)')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    parser.add_argument('--verify', action='store_true', help='Verify after fixing')
    args = parser.parse_args()
    
    base_dir = '/home/z/my-project/SciMSPT'
    
    if args.files:
        html_files = [f if os.path.isabs(f) else os.path.join(base_dir, f) for f in args.files]
    else:
        html_files = glob.glob(os.path.join(base_dir, '*.html'))
    
    print("=" * 60)
    print("🔧 SciMSPT Auto-Fix Tool")
    print("=" * 60)
    print(f"Processing {len(html_files)} file(s)...\n")
    
    total_fixes = 0
    fixed_files = []
    
    for filepath in sorted(html_files):
        try:
            fixes = fix_file(filepath, dry_run=args.dry_run)
            if fixes > 0:
                total_fixes += fixes
                fixed_files.append(os.path.basename(filepath))
        except Exception as e:
            print(f"   ❌ Error with {os.path.basename(filepath)}: {e}")
    
    print("\n" + "=" * 60)
    print("📊 RESULTS")
    print("=" * 60)
    print(f"Files processed: {len(html_files)}")
    print(f"Files fixed: {len(fixed_files)}")
    print(f"Total script blocks wrapped: {total_fixes}")
    
    if args.verify and not args.dry_run:
        print("\n🔍 Verifying fixes...")
        all_clean = True
        
        for filepath in sorted(html_files):
            issues = verify_fix(filepath)
            if issues:
                all_clean = False
                print(f"\n   ❌ {os.path.basename(filepath)} still has {len(issues)} issue(s):")
                for line_num, context in issues[:5]:
                    print(f"      Line {line_num}: {context}")
            else:
                print(f"   ✅ {os.path.basename(filepath)}: CLEAN")
        
        if all_clean:
            print("\n✅ All files are clean!")
        else:
            print("\n⚠️ Some files may need manual review")

if __name__ == '__main__':
    main()
