# SciMSPT Product Roadmap

## Vision Statement
Transform how scientific research becomes venture capital opportunities by automating the journey from peer-reviewed papers to fundable startups.

---

## Current Phase: Foundation (Q3 2026)

### ✅ Completed
- [x] Platform landing page with dark/light theme
- [x] Core pages (Dashboard, Research, Startups, About)
- [x] 7 Research Shorts (one per domain)
- [x] 7 Startup cards with investment theses
- [x] Scientific visualizations (DNA, Protein SVG)
- [x] Navigation ribbon and floating nav
- [x] OAuth UI (GitHub, LinkedIn, Twitter, Google)
- [x] GDPR consent management
- [x] Repository organization (Skills.md, worklog, roadmap)

### 🔄 In Progress
- [ ] Pipeline section (Research → Analysis → Venture visualization)
- [ ] Paper search with filters (domain/year/venue)
- [ ] User bookmarks system
- [ ] Comment system infrastructure

### 📋 Planned This Sprint
- [ ] ScienceDaily RSS integration
- [ ] bioRxiv/medRxiv API connection
- [ ] arXiv OAI-PMH sync setup
- [ ] Dark mode accessibility improvements
- [ ] Card layout centering fixes

---

## Phase 2: Intelligence (Q4 2026)

### AI & Automation
- [ ] **Weekly Auto-Parsing Pipeline**
  - GitHub Actions workflow for ScienceDaily
  - Automated categorization using NLP
  - Breakthrough scoring algorithm
  - Weekly digest email generation

- [ ] **Enhanced Analysis Engine**
  - Domain-specific ML models
  - Citation impact scoring
  - Researcher network mapping
  - Patent potential indicator

### Data Expansion
- [ ] **Preprint Integration**
  - Real-time arXiv feed (cs.AI, q-bio.*)
  - bioRxiv/medRxiv health preprints
  - chemRxiv materials science
  - Automated relevance filtering

- [ ] **API Layer**
  - Public API for research data
  - Rate limiting and caching
  - API key management
  - Developer documentation

### User Features
- [ ] **Search & Discovery**
  - Full-text paper search
  - Faceted filters (domain, year, venue, citations)
  - Saved searches
  - Search alerts

- [ ] **Personalization**
  - User profiles
  - Interest-based recommendations
  - Reading history
  - Custom digests

---

## Phase 3: Community (Q1 2027)

### Social Features
- [ ] **Comment System** (Worker Backend)
  - Per-paper discussions
  - Startup feedback threads
  - Expert Q&A
  - Moderation tools

- [ ] **Collaboration**
  - Shared bookmark collections
  - Team workspaces
  - Annotation tools
  - Export to PDF/Notion

### Authentication & Security
- [ ] **Full OAuth Implementation**
  - GitHub OAuth (complete flow)
  - LinkedIn professional profile import
  - Twitter/X identity verification
  - Google SSO integration

- [ ] **Access Control**
  - Free tier (limited features)
  - Pro tier ($19/mo) - full access
  - Enterprise tier (custom) - API + data
  - Academic discounts

---

## Phase 4: Venture Tools (Q2 2027)

### Studio IDE Development
- [ ] **Interactive Workspace**
  - Paper analysis dashboard
  - Code generation from findings
  - Data visualization builder
  - Collaborative editing

- [ ] **Venture Analysis Suite**
  - NPV/IRR calculators
  - Monte Carlo simulations
  - Market sizing tools
  - Competitive landscape mapper

### Reporting & Export
- [ ] **Professional Reports**
  - Auto-generated startup briefs
  - Investment memo templates
  - Due diligence checklists
  - Board presentation decks

- [ ] **Data Export**
  - CSV/JSON bulk export
  - API webhooks
  - Zapier integration
  - Slack/Teams notifications

---

## Phase 5: Ecosystem (Q3-Q4 2027)

### Platform Expansion
- [ ] **Mobile Applications**
  - iOS native app
  - Android native app
  - Progressive Web App (PWA)
  - Offline reading mode

- [ ] **Marketplace**
  - Researcher-investor matching
  - Startup incubator listings
  - Grant opportunity aggregator
  - Conference event calendar

### Advanced Features
- [ ] **AI Assistant**
  - Natural language queries
  - Paper summarization
  - Hypothesis generation
  - Trend prediction

- [ ] **Blockchain Verification**
  - Research provenance tracking
  - Citation integrity
  - Token-based incentives
  - Decentralized review

---

## Technical Milestones

### Infrastructure
| Quarter | Goal | Status |
|---------|------|--------|
| Q3 2026 | GitHub Pages hosting | ✅ Complete |
| Q4 2026 | Cloudflare Worker backend | 📋 Planned |
| Q1 2027 | Database integration | 📋 Planned |
| Q2 2027 | CDN optimization | 📋 Planned |
| Q3 2027 | Multi-region deployment | 📋 Planned |

### Performance Targets
| Metric | Current | Target | Deadline |
|--------|---------|--------|----------|
| Lighthouse Performance | 75 | >90 | Q4 2026 |
| Time to Interactive | 3.5s | <2s | Q1 2027 |
| Bundle Size | 200KB | <100KB | Q2 2027 |
| API Response Time | N/A | <200ms | Q1 2027 |

---

## Data Sources Roadmap

### Current Sources
- ✅ ScienceDaily (RSS feeds)
- ✅ arXiv (query API)
- ✅ Manual curation from journals

### Q4 2026 Additions
- [ ] bioRxiv/medRxiv (health/bio focus)
- [ ] chemRxiv (materials focus)
- [ ] PubMed Central (biomedical)
- [ ] Semantic Scholar (AI search)

### 2027 Expansion
- [ ] IEEE Xplore (engineering)
- [ ] ACM Digital Library (CS)
- [ ] Nature/Springer APIs (premium)
- [ ] Patent databases (USPTO, EPO)

---

## Monetization Strategy

### Free Tier (Always Free)
- Access to weekly digest
- View top 3 startups
- Basic search
- Community forums

### Pro Tier ($19/month)
- Full startup portfolio (7/week)
- Advanced search & filters
- Unlimited bookmarks
- PDF report downloads
- API access (1000 req/day)

### Enterprise Tier (Custom)
- Everything in Pro
- Unlimited API access
- Custom data feeds
- White-label options
- Dedicated support
- SLA guarantees

### Estimated Revenue (Year 1)
| Tier | Users | Price | MRR |
|------|-------|-------|-----|
| Free | 10,000 | $0 | $0 |
| Pro | 500 | $19 | $9,500 |
| Enterprise | 20 | $500 | $10,000 |
| **Total** | **10,520** | - | **$19,500/mo** |

---

## Success Metrics

### Engagement KPIs
- [ ] 10,000 monthly active users (end of Year 1)
- [ ] 25% return visitor rate
- [ ] Average session duration > 5 minutes
- [ ] 100+ comments/day on platform

### Impact KPIs
- [ ] 50+ startups funded through platform
- [ ] $100M+ total funding raised
- [ ] 10+ research institutions partnered
- [ ] Featured in TechCrunch/VentureBeat

### Quality KPIs
- [ ] 95% uptime SLA
- [ ] < 1% error rate on API calls
- [ ] 4.5+ star user rating
- [ ] NPS score > 50

---

## Risk Assessment

### High Risk
- **API Rate Limits**: Mitigation - implement caching, respect rate limits
- **Content Accuracy**: Mitigation - human review + AI validation
- **Compliance (GDPR)**: Mitigation - privacy-by-design, consent management

### Medium Risk
- **Competition**: Mitigation - unique pipeline methodology, first-mover advantage
- **Monetization**: Mitigation - freemium model, enterprise focus
- **Technical Debt**: Mitigation - quarterly refactoring sprints

### Low Risk
- **Platform Dependencies**: GitHub Pages reliable, can migrate to Cloudflare
- **Talent Acquisition**: Remote-first, academic partnerships
- **Market Adoption**: Growing interest in deep tech investing

---

## Governance

### Advisory Board (Planned)
- [ ] Academic: Professor in computational biology
- [ ] VC Partner: Deep tech investor
- [ ] Entrepreneur: Founded research-backed startup
- [ ] Legal: IP/tech transfer expert

### Ethics Guidelines
- No pay-to-play startup listings
- Transparent methodology publication
- Conflict of interest disclosures
- Researcher attribution always included

---

*Roadmap Version: 1.0*  
*Last Updated: 2026-08-20*  
*Next Review: 2026-09-01*
