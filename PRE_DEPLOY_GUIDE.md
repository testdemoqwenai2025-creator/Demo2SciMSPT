# SciMSPT Pre-Deployment Validation Script
## 🛡️ Quality Control for Clean Page Deployment

### 📋 WHAT THIS SCRIPT DOES

**Location:** `/home/z/my-project/SciMSPT/pre_deploy_check.py`

This script **MUST RUN BEFORE EVERY DEPLOYMENT** to ensure pages are clean and professional.

### ✅ ISSUES IT DETECTS & FIXES AUTOMATICALLY:

| Issue Type | Description | Auto-Fix |
|------------|-------------|----------|
| 🔴 **STUCK SKELETON LOADER** | Gray placeholder bars blocking content, page appears "loading" forever | Adds 800ms timeout failsafe |
| 🔴 **JS OUTSIDE SCRIPT TAGS** | BooleanObserver/MobileDetection code rendering as visible text (Chinese characters, code) | Wraps in proper `<script>` tags |
| 🔴 **BROKEN SCRIPT TAGS** | `</script><script>` pairs splitting JavaScript mid-execution | Removes orphaned tags |
| 🔴 **ORPHANED COMMENTS** | JS header comments (`/* SYSTEM v4.0 */`) showing as visible text | Removes orphaned blocks |
| 🔴 **VISIBLE CORRUPTION** | Known corruption patterns like `MobileDetection.init()` appearing on page | Fixes source issue |
| 🟡 **MISMATCHED TAGS** | Unclosed `<script>` or `<style>` tags breaking page structure | Balances tags |

---

## 🚀 HOW TO USE (MANDATORY WORKFLOW)

### Option 1: Quick Check (Before Preview)
```bash
cd /home/z/my-project/SciMSPT
python3 pre_deploy_check.py
```
**Output:** Shows which pages have issues (does not modify files)

### Option 2: Fix + Verify (Before Client Demo)
```bash
cd /home/z/my-project/SciMSPT
python3 pre_deploy_check.py --fix
```
**Output:** Automatically fixes all issues, then re-verifies everything is clean

### Option 3: Full Deploy Pipeline (Recommended)
```bash
cd /home/z/my-project/SciMSPT
python3 pre_deploy_check.py --fix --deploy
```
**Output:** 
1. Audits all 21 HTML files
2. Auto-fixes any issues found
3. Re-verifies all pages are clean
4. Commits changes with descriptive message
5. Pushes to GitHub Pages (demo2 remote)
6. Reports success/failure

### Option 4: Dry Run (See What Would Be Fixed)
```bash
python3 pre_deploy_check.py --dry-run
```
**Output:** Shows issues without modifying any files

### Option 5: Single File Check
```bash
python3 pre_deploy_check.py index.html
python3 pre_deploy_check.py research.html
```

---

## 📊 EXAMPLE OUTPUT

```
======================================================================
🔍 SciMSPT PRE-DEPLOYMENT VALIDATION
======================================================================
⏰ Timestamp: 2026-08-22 10:30:00

----------------------------------------------------------------------
📊 AUDIT RESULTS
----------------------------------------------------------------------
Files scanned: 21
Clean files: 21/21
Total issues: 0 (0 critical)

  about.html                          ✅ CLEAN
  dashboard.html                      ✅ CLEAN
  index.html                          ✅ CLEAN
  platform.html                       ✅ CLEAN
  research.html                       ✅ CLEAN
  ... (all 21 files)

✅✅✅ ALL PAGES ARE CLEAN - READY FOR DEPLOYMENT ✅✅✅
```

---

## ⚠️ WHEN TO RUN THIS SCRIPT

**ALWAYS run before:**
- [x] Sending preview links to clients/stakeholders
- [x] Pushing to GitHub Pages (demo2 remote)
- [x] Any demo or presentation
- [x] After making HTML/JS changes
- [x] After merging branches

**Run frequency:** Every single time you deploy or share a link.

---

## 🔧 TROUBLESHOOTING

### If script shows issues after fixing:
```bash
# Run multiple times - some fixes reveal other issues
python3 pre_deploy_check.py --fix
python3 pre_deploy_check.py --fix   # Run again until clean
```

### If specific file keeps failing:
```bash
# Check that one file in detail
python3 pre_deploy_check.py problematic_file.html --fix
```

### If you need to force deploy despite warnings:
```bash
python3 pre_deploy_check.py --deploy --force
```
*(Not recommended - only if you've manually verified)*

---

## 📁 FILES CREATED IN THIS PROJECT

| File | Purpose |
|------|---------|
| `pre_deploy_check.py` | **MAIN SCRIPT** - Run this before every deployment |
| `audit_pages.py` | Detailed audit tool (used by main script) |
| `fix_all_pages.py` | Bulk fix tool (legacy, kept for reference) |
| `fix_broken_scripts.py` | Surgical fix for broken script tags |

---

## 🎯 SUCCESS CRITERIA

The script reports **SUCCESS** when:
- ✅ All 21 HTML files pass validation
- ✅ Zero critical issues detected
- ✅ No visible JavaScript code outside `<script>` tags
- ✅ All skeleton loaders have timeout failsafes
- ✅ Script tags are balanced (open = close)

---

## 📞 SUPPORT

If the script detects issues it cannot auto-fix:
1. Note the filename and line numbers from output
2. Manually inspect those lines
3. Ensure JavaScript is inside `<script>...</script>` blocks
4. Re-run the script to verify fix worked

---

**Remember:** This script exists because visible code corruption looks EXTREMELY unprofessional.
Running it takes 5 seconds and saves hours of embarrassment.

**RUN IT EVERY TIME. NO EXCEPTIONS.**

---

*Last updated: 2026-08-22*
*Version: 2.0*
