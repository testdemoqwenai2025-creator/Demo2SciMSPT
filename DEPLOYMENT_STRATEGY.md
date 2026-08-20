# SciMSPT Deployment Strategy
## Repository Structure & Deployment Guide

**Version:** 1.0  
**Date:** August 20, 2025  
**Status:** Production Ready

---

## 🏗️ Repository Architecture

### Overview

SciMSPT uses a **dual-repository strategy** to balance code privacy with public demonstration:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRIVATE REPOSITORY                        │
│              github.com/[org]/SciMSPT                        │
│                                                             │
│  Contains:                                                  │
│  ✓ All source code (HTML, CSS, JS)                         │
│  ✓ Assessment documents                                     │
│  ✓ Investor materials (CONFIDENTIAL)                       │
│  ✓ Video generation scripts                                 │
│  ✓ Configuration files                                      │
│  ✓ Worklogs & internal documentation                         │
│                                                             │
│  Access: Founders + authorized contributors only            │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Sync (manual/automated)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PUBLIC REPOSITORY                         │
│           github.com/[org]/DemoSciMSPT                      │
│                                                             │
│  Contains:                                                  │
│  ✓ Preview-optimized HTML files only                        │
│  ✓ Minimal assets (images, icons)                           │
│  ✓ README with demo instructions                            │
│  ✓ GitHub Pages deployment config                            │
│                                                             │
│  Access: PUBLIC — anyone can view, fork, star               │
│  Purpose: Investor demos, client previews, recruitment      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 File Classification Guide

### PRIVATE (Main SciMSPT Repo Only)

These files **NEVER** go to public DemoSciMSPT:

```
📁 assessments/
   ├── SCIMSPT_COMPREHENSIVE_ASSESSMENT.md        # Business strategy details
   ├── SCIMSPT_CHALLENGING_SCENARIOS.md           # Risk analysis
   ├── SCIMSPT_INTEGRATION_OPPORTUNITIES.md       # Partnership strategy
   ├── SCIMSPT_PLATFORM_EVOLUTION_STRATEGY.md     # Roadmap details
   ├── SCIMSPT_LETTER_TEMPLATES.md                # Client letter templates
   ├── SCIMSPT_QUANTUM_NICHE_ASSESSMENT.md        # Quantum strategy
   ├── SCIMSPT_QUANTUM_SCENARIOS.md               # Quantum scenarios
   └── SCIMSPT_WORKER_DEPLOYMENT_GUIDE.md         # Internal ops

📁 investor-materials/
   ├── INVESTOR_PITCH_DECK_CUSTOMIZED.md          # Meeting preparation kit
   └── EXECUTIVE_SUMMARY_ONE_PAGER.md             # Financial details

📁 video-clips/
   ├── scripts/                                  # Generation scripts
   ├── audio/                                    # Raw audio files
   ├── temp/                                     # Temporary files
   └── phase3/premium/                           # Premium assets

📄 Configuration Files
   ├── api-config.txt                            # API keys/tokens
   ├── deployment.txt                            # Deploy credentials
   └── version.txt                               # Internal versioning

📄 Backup Files
   └── *.phase1.backup                           # Development backups
```

### PUBLIC (Both Repositories)

These files **CAN** be in DemoSciMSPT for previews:

```
📄 Core Application Pages
   ├── index.html                                # Landing page
   ├── platform.html                             # Platform overview
   ├── startups.html                             # Startup showcase
   ├── research.html                             # Research portal
   ├── quantum.html                              # ⭐ NEW: Quantum page
   ├── dashboard.html                             # Dashboard
   ├── documentation.html                        # Documentation
   ├── about.html                                # About page
   └── studio.html                               # Studio/workspace

📁 Public Assets
   ├── assets/images/                            # Hero images, thumbnails
   ├── assets/icons/                             # UI icons
   ├── charts/                                   # Visualization charts
   └── portfolio-shorts/                         # Portfolio previews

📁 Preview Content
   ├── shorts/                                   # Short-form content
   └── slides.html                               # Slide presentations
```

---

## 🚀 Deployment Procedures

### A. Initial Setup (One-Time)

#### Step 1: Configure Private Repository

```bash
# Navigate to main SciMSPT directory
cd /home/z/my-project/SciMSPT

# Ensure remote is correctly set to private repo
git remote set-url origin https://github.com/[YOUR_ORG]/SciMSPT.git

# Verify repository is private (GitHub CLI required)
# Or manually check: Settings → General → Danger Zone → Change visibility → Private

# Create .gitignore updates if needed
cat >> .gitignore << 'EOF'

# Investor Materials - CONFIDENTIAL
investor-materials/

# Sensitive Configurations
api-config.txt
deployment.txt

# Video Generation Assets (large files)
video-clips/audio/
video-clips/temp/
video-clips/phase3/premium/

# Backup Files
*.phase1.backup
startups-enhancement.html
test-features.html

# OS Files
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local
EOF
```

#### Step 2: Configure Public Demo Repository

```bash
# Navigate to DemoSciMSPT directory
cd /home/z/my-project/DemoSciMSPT

# Ensure remote points to public repo
git remote set-url origin https://github.com/[YOUR_ORG]/DemoSciMSPT.git

# Verify repository is PUBLIC
# Settings → General → Danger Zone → Change visibility → Public

# Create demo-specific README
cat > README.md << 'EOF'
# SciMSPT — Live Preview Demo

Welcome to the **SciMSPT Quantum** public demonstration site.

## 🚀 Quick Start

1. **Open `index.html`** in your browser to see the main landing page
2. **Navigate to `quantum.html`** to explore our quantum chemistry simulation workspace
3. **Try the interactive IDE** — write quantum algorithms directly in your browser
4. **Explore platform integrations** — IBM Qiskit, Google Cirq, Microsoft Azure Quantum, and more

## 📱 Responsive Design

This demo is fully mobile-responsive. Try it on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Tablets (iPad, Android tablets)
- Mobile phones (iPhone, Android phones)

## 🔬 Key Features Demonstrated

- ✅ Unified quantum platform interface (6+ vendors)
- ✅ Browser-based IDE workspace
- ✅ Pre-built chemistry simulation templates
- ✅ Freemium pricing model visualization
- ✅ Boolean Observer Interface (Human-as-Observer paradigm)
- ✅ Mobile-first responsive design
- ✅ PWA capabilities (installable)

## 🌐 Technology Stack

- Pure HTML5, CSS3, JavaScript (no framework dependencies)
- Google Fonts (Playfair Display, Inter, JetBrains Mono, Orbitron)
- Material Icons Round (Google)
- Mobile-responsive with progressive enhancement

## 📞 Contact

For partnership inquiries, investment opportunities, or enterprise demos:

📧 **Email:** contact@scimspt.com  
💼 **LinkedIn:** [Company Page]  
🌐 **Website:** www.scimspt.com  

---

*This is a demonstration preview of the SciMSPT Quantum platform. For full access to production features, API integration, or enterprise deployment, please contact our team.*

**Version:** 1.0.0 (Quantum Launch)  
**Last Updated:** August 2025
EOF
```

### B. Regular Sync Workflow

#### Option 1: Manual Sync (Recommended Initially)

```bash
#!/bin/bash
# sync-to-demo.sh — Sync approved files to public demo repository

set -e  # Exit on error

SOURCE_DIR="/home/z/my-project/SciMSPT"
DEMO_DIR="/home/z/my-project/DemoSciMSPT"

echo "🔄 Starting sync from SciMSPT to DemoSciMSPT..."

# Define files/directories to sync
SYNC_ITEMS=(
    "index.html"
    "platform.html"
    "startups.html"
    "research.html"
    "quantum.html"          # ⭐ NEW
    "dashboard.html"
    "documentation.html"
    "about.html"
    "studio.html"
    "slides.html"
    "assets/images/"
    "assets/icons/"
    "charts/"
    "portfolio-shorts/"
    "shorts/"
    "README.md"
)

# Sync each item
for item in "${SYNC_ITEMS[@]}"; do
    if [ -e "$SOURCE_DIR/$item" ]; then
        echo "  ✓ Syncing: $item"
        rsync -av --delete "$SOURCE_DIR/$item" "$DEMO_DIR/$item"
    else
        echo "  ⚠ Not found: $item (skipping)"
    fi
done

echo ""
echo "✅ Sync complete!"
echo ""
echo "Next steps:"
echo "  cd $DEMO_DIR"
echo "  git add -A"
echo '  git commit -m "Update demo preview - [date]"'
echo "  git push origin main"
```

#### Option 2: Automated Sync (Advanced)

Create a GitHub Action in the private repo that automatically pushes to public demo:

```yaml
# .github/workflows/sync-demo.yml (in PRIVATE SciMSPT repo)
name: Sync to Demo Repository

on:
  push:
    branches: [main]
    paths:
      - 'index.html'
      - 'platform.html'
      - 'quantum.html'
      - '**/*.html'  # Trigger on any HTML change

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout private repo
        uses: actions/checkout@v3
        with:
          path: scimspt-private
      
      - name: Checkout public demo repo
        uses: actions/checkout@v3
        with:
          path: scimspt-demo
          repository: [YOUR_ORG]/DemoSciMSPT
          token: ${{ secrets.DEMO_SYNC_TOKEN }}
      
      - name: Sync approved files
        run: |
          # Copy only approved files
          cp scimspt-private/index.html scimspt-demo/
          cp scimspt-private/platform.html scimspt-demo/
          cp scimspt-private/quantum.html scimspt-demo/
          # ... other approved files ...
          
      - name: Commit and push to demo
        run: |
          cd scimspt-demo
          git config user.name "SciMSPT Bot"
          git config user.email "bot@scimspt.com"
          git add -A
          git diff --cached --quiet || git commit -m "Auto-sync from main repo $(date +%Y-%m-%d)"
          git push origin main
```

### C. GitHub Pages Setup (For Demo Site)

#### Enable GitHub Pages on DemoSciMSPT:

1. Go to **DemoSciMSPT** repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select:
   - **Branch:** `main`
   - **Folder:** `/ (root)`
4. Click **Save**

Your demo will be live at: `https://[YOUR_ORG].github.io/DemoSciMSPT/`

#### Custom Domain (Optional):

1. Add CNAME file to DemoSciMSPT root:
   ```
   demo.scimspt.com
   ```

2. Configure DNS:
   - Record Type: `CNAME`
   - Name: `demo`
   - Value: `[YOUR_ORG].github.io`
   - TTL: 3600

3. Enable custom domain in GitHub Pages settings

---

## 🔒 Security Best Practices

### Private Repository Protection

✅ **DO:**
- Enable branch protection rules for `main` branch
- Require pull requests for all changes
- Use two-person review rule for sensitive files
- Enable dependency scanning (GitHub Advanced Security)
- Rotate access tokens every 90 days
- Maintain audit log of all access

❌ **DON'T:**
- Commit API keys, passwords, or tokens
- Add sensitive documents to public repo accidentally
- Share repository invites broadly
- Disable commit history (contains sensitive info in history)

### Public Demo Repository Guidelines

✅ **Safe to Include:**
- Frontend HTML/CSS/JavaScript only
- Static images and assets
- Generic configuration examples
- Public-facing documentation

❌ **Never Include:**
- Backend API endpoints
- Database connection strings
- Authentication logic
- Business intelligence data
- Internal roadmaps or financials
- Investor materials

---

## 📊 Deployment Checklist

### Before Every Push to Private Repo:

- [ ] All changes tested locally
- [ ] No sensitive data in committed files
- [ ] `.gitignore` properly configured
- [ ] Commit messages are clear and descriptive
- [ ] Large files (videos, audio) handled via Git LFS or separate storage
- [ ] Team members notified of significant changes

### Before Every Sync to Public Demo:

- [ ] Review files being synced against classification guide
- [ ] Test demo site loads correctly in browser
- [ ] Check mobile responsiveness on real device (or dev tools)
- [ ] Verify no console errors in browser dev tools
- [ ] Confirm all links work (no broken internal links)
- [ ] Update README.md if new features added
- [ ] Test quantum.html specifically (new page)

### Monthly Maintenance:

- [ ] Review and rotate access tokens/credentials
- [ ] Audit repository access (remove former team members)
- [ ] Check for stale branches (delete if >90 days old)
- [ ] Update dependencies if applicable
- [ ] Review GitHub Actions workflows
- [ ] Backup critical data externally
- [ ] Test restore procedures

---

## 🆘 Troubleshooting

### Common Issues

**Issue:** "Push rejected — repository visibility conflict"  
**Fix:** Ensure you're pushing to correct remote; check `git remote -v`

**Issue:** "File too large for GitHub" (>100MB)  
**Fix:** Use Git LFS for large files, or store in external cloud (S3, GCS)

**Issue:** "Demo site not updating after push"  
**Fix:** Check GitHub Pages build logs; ensure HTML validates; clear browser cache

**Issue:** "Sensitive file accidentally pushed to public repo"  
**Fix:** 
1. Immediately remove file from public repo
2. Use `git filter-branch` or BFG Repo Cleaner to remove from history
3. Force push to clean history
4. Rotate any compromised credentials
5. Document incident for future prevention

**Issue:** "Sync script missing new files"  
**Fix:** Update `sync-to-demo.sh` SYNC_ITEMS array when adding new public files

---

## 📞 Support Contacts

For deployment issues:
- **Technical Lead:** [Name] ([email])
- **DevOps Contact:** [Name] ([email])
- **Emergency:** [Slack channel] / [phone number]

---

**Document Status:** PRODUCTION READY  
**Last Updated:** August 20, 2025  
**Owner:** DevOps Team / Founders

*Follow this guide strictly to maintain security while enabling public demonstrations.*
