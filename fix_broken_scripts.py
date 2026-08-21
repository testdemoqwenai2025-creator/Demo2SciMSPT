#!/usr/bin/env python3
"""
Fix Broken Script Tags
======================
Removes erroneously placed </script><script> tag pairs that split 
JavaScript code mid-block, causing visible text corruption.
"""

import re
import os

def fix_broken_scripts(filepath):
    """Fix files with broken script tag placement"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    fixes = 0
    
    # Track if we're in a script block that shouldn't be closed yet
    in_js_block = False
    brace_depth = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Detect start of actual JS code (not just a script tag)
        if not in_js_block and re.match(r'^\s*(const|let|var|function|class|if|for|while|return|//|/\*)', stripped):
            # Check if we need to open a script tag
            if not fixed_lines or not fixed_lines[-1].strip().endswith('<script>'):
                # Check previous non-empty line
                prev_idx = len(fixed_lines) - 1
                while prev_idx >= 0 and not fixed_lines[prev_idx].strip():
                    prev_idx -= 1
                
                if prev_idx >= 0 and not fixed_lines[prev_idx].strip().endswith('<script>'):
                    fixed_lines.append('<script>')
                    fixes += 1
            
            in_js_block = True
        
        # Skip standalone </script> or <script> tags that are breaking JS flow
        if stripped == '</script>' and in_js_block:
            # Check if next lines continue the JS code
            if i + 1 < len(lines):
                next_stripped = lines[i + 1].strip()
                # If next line looks like continued JS, skip this </script>
                if (next_stripped and 
                    not next_stripped.startswith('<') and
                    not next_stripped.startswith('//') and
                    (re.match(r'^[\s\w"\'\:.,(){}\[\];]', next_stripped) or
                     next_stripped.startswith('message:') or
                     next_stripped.startswith('action:') or
                     next_stripped.startswith('icon:') or
                     next_stripped.startswith('buttonText:'))):
                    print(f"   Skipping erroneous </script> at line {i+1}")
                    i += 1
                    continue
        
        if stripped == '<script>' and in_js_block:
            # Check if this is an erroneous mid-block script tag
            prev_non_empty_idx = len(fixed_lines) - 1
            while prev_non_empty_idx >= 0 and not fixed_lines[prev_non_empty_idx].strip():
                prev_non_empty_idx -= 1
            
            if prev_non_empty_idx >= 0:
                prev_line = fixed_lines[prev_non_empty_idx].strip()
                # If previous line looks like unfinished JS, skip this <script>
                if (prev_line.endswith('{') or 
                    prev_line.endswith(',') or 
                    prev_line.endswith('(') or
                    prev_line.endswith('return') or
                    prev_line.startswith('//')):
                    print(f"   Skipping erroneous <script> at line {i+1}")
                    i += 1
                    continue
        
        # Track brace depth to know when JS block truly ends
        if in_js_block:
            brace_depth += line.count('{') - line.count('}')
            
            # Check for legitimate end of JS block
            if stripped == '}' and brace_depth <= 0:
                # Look ahead to see if we should close the script
                if i + 1 < len(lines) and not lines[i + 1].strip().startswith(('<', '//', '/*', '}')):
                    fixed_lines.append(line)
                    fixed_lines.append('</script>')
                    fixes += 1
                    in_js_block = False
                    brace_depth = 0
                    i += 1
                    continue
                elif stripped == '}' and brace_depth <= 0:
                    # End of function/object but more JS might follow
                    pass
        
        fixed_lines.append(line)
        i += 1
    
    # Close any remaining open script
    if in_js_block:
        fixed_lines.append('</script>')
        fixes += 1
    
    if fixes > 0:
        new_content = '\n'.join(fixed_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Fixed {filepath}: {fixes} script tag corrections")
        return True
    else:
        print(f"ℹ️  No fixes needed for {filepath}")
        return False

if __name__ == '__main__':
    import sys
    
    filepath = sys.argv[1] if len(sys.argv) > 1 else '/home/z/my-project/SciMSPT/research.html'
    fix_broken_scripts(filepath)
