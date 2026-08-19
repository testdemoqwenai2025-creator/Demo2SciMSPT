# SciMSPT — Scientific Management System for Paper Transformation

[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue?logo=github)](https://testdemoqwenai2025-creator.github.io/SciMSPT/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Production](https://img.shields.io/badge/Status-Production-brightgreen)]()

## 🚀 Overview

**SciMSPT** transforms peer-reviewed scientific publications into investment-ready startup opportunities. Our proprietary pipeline analyzes **264+ ScienceDaily articles weekly** across **4 research axes** to identify **7 high-potential venture concepts**.

### The Pipeline
```
Research → Analysis → Venture
```

1. **ScienceDaily RSS Feeds** - Automated ingestion of 264+ articles/week
2. **AI-Powered Analysis** - Domain classification, venture scoring, TAM estimation
3. **7 Fundable Startups** - Complete investment theses with NPV/IRR analysis

## 🌐 Live Demo

**URL**: [https://testdemoqwenai2025-creator.github.io/SciMSPT/](https://testdemoqwenai2025-creator.github.io/SciMSPT/)

## 📁 Repository Structure

```
SciMSPT/
├── index.html              # Landing page (hero, pipeline, breakthroughs)
├── dashboard.html          # Real-time metrics & system health
├── research.html           # Research trends & weekly digests
├── startups.html           # 7 Startup portfolio with papers
├── about.html              # Methodology & team info
├── slides.html             # Presentation slides viewer
│
├── Skills.md               # Platform capabilities documentation
├── worklog.md              # Development log & session history
├── roadmap.md              # Product roadmap & milestones
├── README.md               # This file
│
├── Scripts/                # Automation scripts
│   └── (coming soon)
│
├── shorts/                 # Research Short documents (7 domains)
│   ├── SD-M-01.html        # Quantum Magnons breakthrough
│   ├── SD-M-02.html        # Quantum-Classical Hybrid algorithms
│   ├── SD-P-05.html        # Tandem Solar Cell materials
│   ├── SD-P-07.html        # Protein Engineering advances
│   ├── SD-S-04.html        # 2nm CMOS Process breakthrough
│   ├── SD-T-03.html        # Neural Temporal Foundation models
│   └── SD-T-06.html        # Time Series forecasting
│
├── portfolio-shorts/       # Individual startup deep-dives
│   ├── index.html          # Portfolio overview
│   ├── P3.html             # Startup details
│   ├── P5.html
│   ├── P9.html
│   ├── P11.html
│   ├── P12.html
│   ├── P-ai-materials.html
│   └── P-cmos-2nm.html
│
├── data/                   # Static JSON data
│   └── weekly_digest/      # Weekly parsed content
│
├── assets/                 # Static assets
│   ├── icons/              # Platform icons
│   ├── images/             # Thumbnails & graphics
│   ├── mandalas/           # Scientific mandala art
│   ├── reports/            # PDF reports bundle
│   └── slides/             # HTML presentation slides
│
├── .gitignore              # Git ignore rules
└── .nojekyll               # Disable Jekyll processing
```

## 🎨 Design System

### Color Palette
| Variable | Value | Usage |
|----------|-------|-------|
| Background | `#0a1628` | Dark mode background |
| Accent | `#4da8da` | Primary accent (Crystal Blue) |
| Accent Glow | `#2d7ab3` | Hover states |
| Primary Text | `#e8f0f8` | Main text color |
| Muted Text | `#7a9bb8` | Secondary text |
| Research Highlight | `#00E5FF` | "Research" text (Quantum Cyan) |
| Papers Highlight | `#c084fc` | "Papers" text (Purple) |

### Typography
- **Headings**: Playfair Display (serif)
- **Body**: Inter (sans-serif)
- **Code/Data**: JetBrains Mono (monospace)

### Features
- ✅ Dark/Light theme toggle with persistence
- ✅ Glass-morphism UI with backdrop-filter blur
- ✅ Animated scientific visualizations (DNA helix, protein structure)
- ✅ Responsive design (mobile-first)
- ✅ GDPR-compliant cookie consent
- ✅ OAuth integration (GitHub, LinkedIn, Twitter, Google)

## 🔬 Research Domains

| Domain | Code | Focus Area |
|--------|------|------------|
| Quantum Computing | SD-M | Physics breakthroughs |
| Mathematics | SD-M | Optimization algorithms |
| Materials Science | SD-P | Photovoltaics, perovskites |
| Biotechnology | SD-P | Protein design, folding |
| Semiconductors | SD-S | CMOS, 2nm process |
| Time Series | SD-T | Neural forecasting models |

## 📊 Key Metrics

- **7 Startups** generated per week
- **264+ Papers** analyzed weekly
- **49 Papers** average per startup thesis
- **$18B+** average Total Addressable Market
- **6 Domains** covered across sciences

## 🛠️ Tech Stack

### Frontend
- HTML5 / CSS3 (Custom Properties)
- Vanilla JavaScript (no framework dependencies)
- Google Fonts + Material Icons
- SVG animations with CSS keyframes

### Backend (Planned)
- Cloudflare Workers (API endpoints)
- GitHub Actions (weekly automation)
- RSS feed parsing (ScienceDaily, arXiv)
- OAI-PMH synchronization

### Data Sources
| Source | Type | Update Frequency |
|--------|------|------------------|
| ScienceDaily | RSS | Daily |
| arXiv | API/OAI-PMH | Hourly |
| bioRxiv/medRxiv | API | Daily |
| chemRxiv | API | Weekly |

## 🚀 Getting Started

### Prerequisites
- Git (for cloning)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Optional: Node.js (for local development server)

### Local Development

```bash
# Clone the repository
git clone https://github.com/testdemoqwenai2025-creator/SciMSPT.git
cd SciMSPT

# Open in browser (simplest method)
open index.html
# or on Linux:
xdg-open index.html

# Or use a local server (recommended)
npx serve .
# or
python3 -m http.server 8000
```

### Deployment to GitHub Pages

This repository is configured for automatic GitHub Pages deployment:

1. Push changes to `main` branch
2. GitHub Actions builds and deploys automatically
3. Site available at: `https://<username>.github.io/SciMSPT/`

## 📝 Documentation

- **[Skills.md](./Skills.md)** - Full platform capabilities and technical specs
- **[worklog.md](./worklog.md)** - Development history and session logs
- **[roadmap.md](./roadmap.md)** - Product roadmap and future plans

## 🔐 Authentication

OAuth providers are configured but require credentials:

1. **GitHub OAuth** - Primary authentication method
2. **LinkedIn OAuth** - Professional profile import
3. **Twitter/X OAuth** - Identity verification
4. **Google OAuth** - SSO integration

See `Skills.md` for environment variable configuration.

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Use 2 spaces for indentation
- Follow BEM naming for CSS classes
- Write semantic HTML5
- Comment complex JavaScript logic

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ScienceDaily** - For providing excellent science news aggregation
- **arXiv** - For open-access preprint hosting
- **bioRxiv/medRxiv** - For biology preprint infrastructure
- **Cloudflare** - For Workers platform (planned backend)
- **Google Fonts** - For Playfair Display, Inter, JetBrains Mono

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/testdemoqwenai2025-creator/SciMSPT/issues)
- **Discussions**: [GitHub Discussions](https://github.com/testdemoqwenai2025-creator/SciMSPT/discussions)
- **Email**: contact@scimspt.research (placeholder)

---

<div align="center">

**Built with ❤️ for the research community**

*From Papers to Ventures*

*Last Updated: Week 34, 2026*

</div>
