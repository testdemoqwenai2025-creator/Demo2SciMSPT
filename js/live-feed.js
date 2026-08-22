/**
 * SciMSPT Live Research Feed v1.0
 * ==================================
 * Real-time research paper updates from ArXiv & PubMed
 * Features:
 * - WebSocket/polling connection to ArXiv API
 * - New paper notifications
 * - Topic-based filtering
 * - Background sync for offline support
 */

class SciMSPTLiveFeed {
  constructor(options = {}) {
    // Configuration
    this.config = {
      updateInterval: options.updateInterval || 5 * 60 * 1000, // 5 minutes
      maxItems: options.maxItems || 20,
      topics: options.topics || [
        'quantum computing',
        'machine learning',
        'molecular simulation',
        'materials science',
        'biotechnology',
        'neural networks'
      ],
      enableNotifications: options.enableNotifications !== false,
      autoStart: options.autoStart !== false,
      ...options
    };
    
    // State
    this.feedContainer = null;
    this.papers = [];
    this.lastUpdate = null;
    this.isRunning = false;
    this.updateTimer = null;
    this.observer = null;
    
    // Initialize
    if (this.config.autoStart) {
      this.init();
    }
  }

  async init() {
    console.log('📡 Initializing Live Research Feed...');
    
    // Setup UI
    this.createFeedContainer();
    
    // Request notification permission
    if (this.config.enableNotifications && 'Notification' in window) {
      const permission = await Notification.requestPermission();
      this.notificationsEnabled = permission === 'granted';
    }
    
    // Load cached papers
    this.loadCachedPapers();
    
    // Start feed
    if (this.config.autoStart) {
      this.start();
    }
    
    console.log('✅ Live Research Feed initialized');
  }

  createFeedContainer() {
    // Check if container already exists
    this.feedContainer = document.getElementById('scimspt-live-feed');
    
    if (!this.feedContainer) {
      this.feedContainer = document.createElement('div');
      this.feedContainer.id = 'scimspt-live-feed';
      this.feedContainer.className = 'live-feed-container';
      
      this.feedContainer.innerHTML = `
        <div class="live-feed-header">
          <div class="live-feed-title">
            <span class="live-indicator"></span>
            <h3>Live Research Feed</h3>
          </div>
          <div class="live-feed-controls">
            <button class="feed-btn topic-filter" aria-label="Filter by topic" title="Filter Topics">
              <span class="material-icons-round">filter_list</span>
            </button>
            <button class="feed-btn refresh-btn" aria-label="Refresh feed" title="Refresh Now">
              <span class="material-icons-round">refresh</span>
            </button>
            <button class="feed-btn pause-btn" aria-label="Pause feed" title="Pause Updates">
              <span class="material-icons-round">pause</span>
            </button>
          </div>
        </div>
        
        <div class="live-feed-topics" id="feedTopics"></div>
        
        <div class="live-feed-content" id="feedContent">
          <div class="live-feed-loading">
            <div class="spinner"></div>
            <p>Loading latest research...</p>
          </div>
        </div>
        
        <div class="live-feed-footer">
          <span class="last-update" id="lastUpdate">Last update: Never</span>
          <span class="paper-count" id="paperCount">0 papers</span>
        </div>
        
        <!-- Topic Filter Dropdown -->
        <div class="topic-dropdown" id="topicDropdown" hidden>
          <h4>Filter by Topics</h4>
          <div class="topic-list" id="topicList"></div>
        </div>
      `;
      
      // Add styles if not present
      if (!document.getElementById('live-feed-styles')) {
        this.injectStyles();
      }
      
      // Append to page or return for manual placement
      if (document.body) {
        document.body.appendChild(this.feedContainer);
      }
    }
    
    // Setup event listeners
    this.setupEventListeners();
  }

  injectStyles() {
    const style = document.createElement('style');
    style.id = 'live-feed-styles';
    style.textContent = `
      /* Live Research Feed Styles */
      .live-feed-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 380px;
        max-height: 500px;
        background: var(--bg-glass, rgba(10, 22, 40, 0.95));
        backdrop-filter: blur(16px);
        border: 1px solid var(--border-subtle, rgba(0, 229, 255, 0.15));
        border-radius: var(--radius-xl, 16px);
        box-shadow: 
          0 25px 50px rgba(0, 0, 0, 0.5),
          var(--glow-primary, 0 0 30px rgba(0, 229, 255, 0.1));
        z-index: 9000;
        display: flex;
        flex-direction: column;
        font-family: var(--font-body, 'Inter', sans-serif);
        opacity: 1 !important;
        visibility: visible !important;
        transform: translateY(0);
        transition: transform 0.3s ease, opacity 0.3s ease;
      }
      
      .live-feed-container.collapsed {
        transform: translateY(calc(100% - 50px));
      }
      
      .live-feed-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 16px;
        border-bottom: 1px solid var(--border-subtle, rgba(0, 229, 255, 0.1));
      }
      
      .live-feed-title {
        display: flex;
        align-items: center;
        gap: 10px;
      }
      
      .live-feed-title h3 {
        margin: 0;
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary, #e8f4fc);
      }
      
      .live-indicator {
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        animation: pulse-dot 2s ease-in-out infinite;
      }
      
      @keyframes pulse-dot {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        50% { opacity: 0.8; box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
      }
      
      .live-feed-controls {
        display: flex;
        gap: 4px;
      }
      
      .feed-btn {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: transparent;
        border: none;
        border-radius: var(--radius-md, 8px);
        color: var(--text-muted, #64748b);
        cursor: pointer;
        transition: all 0.2s ease;
      }
      
      .feed-btn:hover {
        background: var(--accent-primary-muted, rgba(0, 229, 255, 0.15));
        color: var(--accent-primary, #00E5FF);
      }
      
      .feed-btn .material-icons-round { font-size: 18px; }
      
      .live-feed-topics {
        display: flex;
        gap: 6px;
        padding: 8px 16px;
        overflow-x: auto;
        scrollbar-width: none;
      }
      
      .live-feed-topics::-webkit-scrollbar { display: none; }
      
      .topic-chip {
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 600;
        white-space: nowrap;
        background: var(--accent-primary-muted, rgba(0, 229, 255, 0.15));
        color: var(--accent-primary, #00E5FF);
        border-radius: var(--radius-full, 9999px);
        cursor: pointer;
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }
      
      .topic-chip:hover,
      .topic-chip.active {
        background: var(--accent-primary, #00E5FF);
        color: var(--bg-primary, #0a1628);
      }
      
      .live-feed-content {
        flex: 1;
        overflow-y: auto;
        padding: 8px;
      }
      
      /* Paper Item */
      .paper-item {
        padding: 12px;
        margin-bottom: 8px;
        background: var(--bg-secondary, rgba(17, 29, 50, 0.8));
        border: 1px solid var(--border-subtle, rgba(0, 229, 255, 0.08));
        border-radius: var(--radius-lg, 12px);
        cursor: pointer;
        transition: all 0.2s ease;
        opacity: 1 !important;
        visibility: visible !important;
      }
      
      .paper-item:hover {
        border-color: var(--accent-primary, #00E5FF);
        transform: translateX(-4px);
      }
      
      .paper-item.new {
        border-left: 3px solid var(--accent-primary, #00E5FF);
        animation: slide-in-right 0.3s ease-out;
      }
      
      @keyframes slide-in-right {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
      }
      
      .paper-item-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        gap: 8px;
        margin-bottom: 6px;
      }
      
      .paper-item-title {
        font-size: 13px;
        font-weight: 600;
        color: var(--text-primary, #e8f4fc);
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      
      .paper-item-source {
        font-size: 10px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        text-transform: uppercase;
        flex-shrink: 0;
      }
      
      .source-arxiv { background: #B31B1B; color: white; }
      .source-pubmed { background: #006699; color: white; }
      
      .paper-item-meta {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 11px;
        color: var(--text-muted, #64748b);
      }
      
      .paper-item-authors {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      
      .paper-item-time {
        flex-shrink: 0;
      }
      
      .paper-item-topics {
        display: flex;
        gap: 4px;
        margin-top: 8px;
        flex-wrap: wrap;
      }
      
      .paper-topic-tag {
        font-size: 10px;
        padding: 2px 6px;
        background: rgba(167, 139, 250, 0.15);
        color: var(--accent-secondary, #a78bfa);
        border-radius: 4px;
      }
      
      /* Loading State */
      .live-feed-loading {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 20px;
        color: var(--text-muted, #64748b);
      }
      
      .spinner {
        width: 24px;
        height: 24px;
        border: 2px solid var(--border-default, rgba(148, 163, 184, 0.2));
        border-top-color: var(--accent-primary, #00E5FF);
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-bottom: 12px;
      }
      
      @keyframes spin { to { transform: rotate(360deg); } }
      
      /* Footer */
      .live-feed-footer {
        display: flex;
        justify-content: space-between;
        padding: 8px 16px;
        border-top: 1px solid var(--border-subtle, rgba(0, 229, 255, 0.1));
        font-size: 11px;
        color: var(--text-muted, #64748b);
      }
      
      /* Topic Dropdown */
      .topic-dropdown {
        position: absolute;
        bottom: 100%;
        right: 0;
        width: 280px;
        background: var(--bg-glass-heavy, rgba(10, 20, 35, 0.98));
        border: 1px solid var(--border-default, rgba(148, 163, 184, 0.2));
        border-radius: var(--radius-lg, 12px);
        padding: 16px;
        margin-bottom: 8px;
        box-shadow: var(--shadow-xl, 0 20px 40px rgba(0, 0, 0, 0.5));
      }
      
      .topic-dropdown h4 {
        margin: 0 0 12px;
        font-size: 13px;
        color: var(--text-primary, #e8f4fc);
      }
      
      .topic-list {
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      
      .topic-option {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px;
        border-radius: var(--radius-md, 8px);
        cursor: pointer;
        transition: background 0.2s ease;
      }
      
      .topic-option:hover {
        background: var(--accent-primary-muted, rgba(0, 229, 255, 0.1));
      }
      
      .topic-option input[type="checkbox"] {
        accent-color: var(--accent-primary, #00E5FF);
      }
      
      .topic-option label {
        font-size: 13px;
        color: var(--text-secondary, #94a3b8);
        cursor: pointer;
        flex: 1;
      }
      
      /* Responsive */
      @media (max-width: 480px) {
        .live-feed-container {
          left: 10px;
          right: 10px;
          width: auto;
          bottom: 10px;
          max-height: 400px;
        }
      }
    `;
    document.head.appendChild(style);
  }

  setupEventListeners() {
    // Refresh button
    const refreshBtn = this.feedContainer.querySelector('.refresh-btn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => this.fetchNewPapers());
    }
    
    // Pause/Resume button
    const pauseBtn = this.feedContainer.querySelector('.pause-btn');
    if (pauseBtn) {
      pauseBtn.addEventListener('click', () => this.togglePause());
    }
    
    // Topic filter button
    const filterBtn = this.feedContainer.querySelector('.topic-filter');
    const dropdown = this.feedContainer.querySelector('#topicDropdown');
    if (filterBtn && dropdown) {
      filterBtn.addEventListener('click', () => {
        dropdown.hidden = !dropdown.hidden;
      });
    }
    
    // Populate topic list
    this.populateTopicFilters();
  }

  populateTopicFilters() {
    const topicList = this.feedContainer.querySelector('#topicList');
    if (!topicList) return;
    
    topicList.innerHTML = this.config.topics.map(topic => `
      <label class="topic-option">
        <input type="checkbox" value="${topic}" checked data-topic="${topic}">
        <span>${topic}</span>
      </label>
    `).join('');
    
    // Add event listeners
    topicList.querySelectorAll('input').forEach(input => {
      input.addEventListener('change', (e) => {
        if (e.target.checked) {
          if (!this.activeTopics) this.activeTopics = [...this.config.topics];
        } else {
          this.activeTopics = Array.from(topicList.querySelectorAll('input:checked'))
            .map(cb => cb.value);
        }
        this.filterPapersByTopics();
      });
    });
  }

  populateTopicChips() {
    const topicsContainer = this.feedContainer.querySelector('#feedTopics');
    if (!topicsContainer) return;
    
    topicsContainer.innerHTML = this.config.topics.slice(0, 5).map(topic => `
      <span class="topic-chip">${topic}</span>
    `).join('');
  }

  // ============================================
  // FEED CONTROL METHODS
  // ============================================

  start() {
    if (this.isRunning) return;
    
    this.isRunning = true;
    console.log('▶️ Live Feed started');
    
    // Initial fetch
    this.fetchNewPapers();
    
    // Set up interval
    this.updateTimer = setInterval(() => {
      this.fetchNewPapers();
    }, this.config.updateInterval);
    
    // Update UI
    const pauseBtn = this.feedContainer.querySelector('.pause-btn');
    if (pauseBtn) {
      pauseBtn.innerHTML = '<span class="material-icons-round">pause</span>';
      pauseBtn.title = 'Pause Updates';
    }
  }

  stop() {
    if (!this.isRunning) return;
    
    this.isRunning = false;
    clearInterval(this.updateTimer);
    this.updateTimer = null;
    
    console.log('⏸️ Live Feed paused');
    
    const pauseBtn = this.feedContainer.querySelector('.pause-btn');
    if (pauseBtn) {
      pauseBtn.innerHTML = '<span class="material-icons-round">play_arrow</span>';
      pauseBtn.title = 'Resume Updates';
    }
  }

  togglePause() {
    if (this.isRunning) {
      this.stop();
    } else {
      this.start();
    }
  }

  // ============================================
  // DATA FETCHING
  // ============================================

  async fetchNewPapers() {
    const contentEl = this.feedContainer.querySelector('#feedContent');
    if (!contentEl) return;
    
    try {
      // Show loading state on first load
      if (this.papers.length === 0) {
        contentEl.innerHTML = `
          <div class="live-feed-loading">
            <div class="spinner"></div>
            <p>Searching ArXiv & PubMed...</p>
          </div>
        `;
      }
      
      // Fetch from multiple sources in parallel
      const [arxivPapers, pubmedPapers] = await Promise.all([
        this.fetchFromArXiv(),
        this.fetchFromPubMed()
      ]);
      
      // Combine and deduplicate
      const newPapers = this.deduplicatePapers([...arxivPapers, ...pubmedPapers]);
      
      // Check for truly new papers (not in current list)
      const existingIds = new Set(this.papers.map(p => p.id));
      const trulyNew = newPapers.filter(p => !existingIds.has(p.id));
      
      // Update papers list
      this.papers = [...newPapers, ...this.papers].slice(0, this.config.maxItems);
      
      // Render papers
      this.renderPapers(trulyNew);
      
      // Notify about new papers
      if (trulyNew.length > 0 && this.notificationsEnabled) {
        this.notifyNewPapers(trulyNew);
      }
      
      // Cache papers
      this.cachePapers();
      
      // Update last update time
      this.lastUpdate = new Date();
      this.updateLastUpdateTime();
      
    } catch (error) {
      console.error('❌ Error fetching papers:', error);
      
      if (this.papers.length === 0) {
        contentEl.innerHTML = `
          <div class="live-feed-loading">
            <span class="material-icons-round" style="font-size: 36px;">error_outline</span>
            <p>Failed to load papers. Retrying...</p>
          </div>
        `;
      }
    }
  }

  async fetchFromArXiv() {
    try {
      // Build query from active topics
      const query = (this.activeTopics || this.config.topics)
        .slice(0, 3)
        .map(t => `all:${encodeURIComponent(t)}`)
        .join('+OR+');
      
      const response = await fetch(
        `https://export.arxiv.org/api/query?search_query=${query}&max_results=10&sortBy=submittedDate&sortOrder=descending`
      );
      
      const text = await response.text();
      return this.parseArXivResponse(text);
    } catch (error) {
      console.warn('ArXiv fetch failed:', error.message);
      return [];
    }
  }

  parseArXivResponse(xmlText) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(xmlText, 'text/xml');
    const entries = doc.querySelectorAll('entry');
    
    return Array.from(entries).map(entry => ({
      id: entry.querySelector('id')?.textContent || '',
      title: entry.querySelector('title')?.textContent?.trim() || '',
      authors: Array.from(entry.querySelectorAll('author name'))
        .map(a => a.textContent.trim())
        .slice(0, 3)
        .join(', ') + (entry.querySelectorAll('author name').length > 3 ? ' et al.' : ''),
      summary: entry.querySelector('summary')?.textContent?.trim()?.substring(0, 200) + '...' || '',
      published: entry.querySelector('published')?.textContent?.split('T')[0] || '',
      source: 'arxiv',
      url: entry.querySelector('id')?.textContent || '#',
      categories: Array.from(entry.querySelectorAll('category'))
        .map(c => c.getAttribute('term') || '')
        .filter(Boolean)
        .slice(0, 3)
    }));
  }

  async fetchFromPubMed() {
    try {
      const query = (this.activeTopics || this.config.topics)
        .slice(0, 2)
        .join(' AND ');
      
      const searchUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${encodeURIComponent(query)}&retmax=5&sort=date&retmode=json`;
      
      const searchResponse = await fetch(searchUrl);
      const searchData = await searchResponse.json();
      
      const ids = searchData.esearchresult?.idlist || [];
      if (ids.length === 0) return [];
      
      const fetchUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=json&id=${ids.join(',')}`;
      const fetchResponse = await fetch(fetchUrl);
      const fetchData = await fetchResponse.json();
      
      return this.parsePubMedResponse(fetchData);
    } catch (error) {
      console.warn('PubMed fetch failed:', error.message);
      return [];
    }
  }

  parsePubMedResponse(data) {
    const articles = data.resultlist?.result || [];
    const results = [];
    
    (Array.isArray(articles) ? articles : [articles]).forEach(article => {
      results.push({
        id: article.uid || `pmid-${Date.now()}-${Math.random()}`,
        title: article.title || 'Untitled',
        authors: Array.isArray(article.authors?.author)
          ? article.authors.author.map(a => a.name).slice(0, 3).join(', ')
          : 'Unknown Authors',
        summary: '',
        published: article.pubdate || new Date().toISOString().split('T')[0],
        source: 'pubmed',
        url: `https://pubmed.ncbi.nlm.nih.gov/${article.uid}/`,
        categories: []
      });
    });
    
    return results;
  }

  deduplicatePapers(papers) {
    const seen = new Set();
    return papers.filter(paper => {
      const key = paper.title.toLowerCase().trim();
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  // ============================================
  // RENDERING
  // ============================================

  renderPapers(newPapers = []) {
    const contentEl = this.feedContainer.querySelector('#feedContent');
    if (!contentEl) return;
    
    contentEl.innerHTML = this.papers.map((paper, index) => `
      <article class="paper-item ${newPapers.find(np => np.id === paper.id) ? 'new' : ''}" 
               data-id="${paper.id}"
               role="article"
               tabindex="0"
               aria-label="${this.escapeHtml(paper.title)}">
        <div class="paper-item-header">
          <h4 class="paper-item-title">${this.escapeHtml(paper.title)}</h4>
          <span class="paper-item-source source-${paper.source}">${paper.source}</span>
        </div>
        <div class="paper-item-meta">
          <span class="paper-item-authors">${this.escapeHtml(paper.authors)}</span>
          <span class="paper-item-time">${this.formatTimeAgo(paper.published)}</span>
        </div>
        ${paper.categories.length ? `
          <div class="paper-item-topics">
            ${paper.categories.slice(0, 2).map(cat => `
              <span class="paper-topic-tag">${cat}</span>
            `).join('')}
          </div>
        ` : ''}
      </article>
    `).join('');
    
    // Add click handlers
    contentEl.querySelectorAll('.paper-item').forEach(item => {
      item.addEventListener('click', () => {
        const paperId = item.dataset.id;
        const paper = this.papers.find(p => p.id === paperId);
        if (paper && paper.url !== '#') {
          window.open(paper.url, '_blank', 'noopener,noreferrer');
        }
      });
      
      item.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          item.click();
        }
      });
    });
    
    // Update count
    const countEl = this.feedContainer.querySelector('#paperCount');
    if (countEl) {
      countEl.textContent = `${this.papers.length} papers`;
    }
    
    // Populate topic chips
    this.populateTopicChips();
  }

  filterPapersByTopics() {
    if (!this.activeTopics || this.activeTopics.length === 0) {
      this.renderPapers();
      return;
    }
    
    // Filter would go here - for now just re-render
    this.renderPapers();
  }

  // ============================================
  // NOTIFICATIONS
  // ============================================

  notifyNewPapers(papers) {
    if (!('Notification' in window) || Notification.permission !== 'granted') return;
    
    // Only notify about first few to avoid spam
    const papersToNotify = papers.slice(0, 3);
    
    papersToNotify.forEach(paper => {
      const notification = new Notification('🔬 New Research Paper', {
        body: paper.title.substring(0, 100) + (paper.title.length > 100 ? '...' : ''),
        icon: '/assets/icon-192.svg',
        badge: '/assets/icon-192.svg',
        tag: paper.id, // Prevent duplicates
        data: { url: paper.url },
        actions: [
          { action: 'view', title: 'View Paper' },
          { action: 'dismiss', title: 'Dismiss' }
        ]
      });
      
      notification.onclick = () => {
        window.focus();
        if (paper.url !== '#') window.open(paper.url, '_blank');
        notification.close();
      };
    });
  }

  // ============================================
  // CACHING & STORAGE
  // ============================================

  cachePapers() {
    try {
      localStorage.setItem('scimspt_live_feed_papers', JSON.stringify({
        papers: this.papers,
        timestamp: Date.now()
      }));
    } catch (e) {
      // Storage full or unavailable
    }
  }

  loadCachedPapers() {
    try {
      const cached = localStorage.getItem('scimspt_live_feed_papers');
      if (cached) {
        const data = JSON.parse(cached);
        // Use cache if less than 30 minutes old
        if (Date.now() - data.timestamp < 30 * 60 * 1000) {
          this.papers = data.papers;
          this.renderPapers();
          this.updateLastUpdateTime(new Date(data.timestamp));
        }
      }
    } catch (e) {
      // No cache available
    }
  }

  // ============================================
  // UTILITY METHODS
  // ============================================

  formatTimeAgo(dateString) {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  }

  updateLastUpdateTime(date = this.lastUpdate) {
    const el = this.feedContainer.querySelector('#lastUpdate');
    if (el && date) {
      el.textContent = `Last update: ${date.toLocaleTimeString()}`;
    }
  }

  escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // ============================================
  // PUBLIC API
  // ============================================

  addTopic(topic) {
    if (!this.config.topics.includes(topic)) {
      this.config.topics.push(topic);
      this.populateTopicFilters();
      this.fetchNewPapers();
    }
  }

  removeTopic(topic) {
    this.config.topics = this.config.topics.filter(t => t !== topic);
    this.populateTopicFilters();
  }

  setTopics(topics) {
    this.config.topics = topics;
    this.populateTopicFilters();
    this.fetchNewPapers();
  }

  getPapers() {
    return this.papers;
  }

  destroy() {
    this.stop();
    if (this.feedContainer && this.feedContainer.parentNode) {
      this.feedContainer.parentNode.removeChild(this.feedContainer);
    }
  }
}

// Export
window.SciMSPTLiveFeed = SciMSPTLiveFeed;

if (typeof module !== 'undefined' && module.exports) {
  module.exports = SciMSPTLiveFeed;
}
