/**
 * SciMSPT Global Components System v4.0 (SAFE VERSION)
 * =====================================================
 * CRITICAL DESIGN PRINCIPLE: This script MUST NEVER block or hide page content.
 * 
 * Features (all optional, non-blocking):
 * - ArXiv/PubMed API Integration with Caching
 * - Global Search with Keyboard Shortcuts (Ctrl+K/Cmd+K)
 * - Search History (localStorage)
 * - Toast Notification System
 * - Google Analytics 4 Integration
 * - Export Features (CSV, JSON, BibTeX)
 * 
 * SAFETY RULES:
 * 1. Never set body opacity/visibility in constructor
 * 2. Never prevent default link behavior
 * 3. Wrap all feature init in try-catch
 * 4. Use setTimeout for non-critical features
 */

class SciMSPTGlobal {
  constructor() {
    this.searchInput = null;
    this.searchWrapper = null;
    this.searchSuggestions = null;
    this.searchOverlay = null;
    this.searchHistory = [];
    this.isSearching = false;
    this.debounceTimer = null;
    this.cache = new Map();
    this.CACHE_TTL = 5 * 60 * 1000;
    this.initialized = false;
    
    this.apiEndpoints = {
      arxiv: 'https://export.arxiv.org/api/query?search_query=all:',
      pubmed: 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=',
      pubmedFetch: 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=json&id='
    };
    
    this.analyticsConfig = {
      ga4MeasurementId: 'G-XXXXXXXXXX',
      enabled: true
    };
    
    // SAFE: Schedule init for later, don't call immediately!
    this.scheduleInit();
  }

  scheduleInit() {
    const initWhenReady = () => {
      if (this.initialized) return;
      try {
        this.init();
        this.initialized = true;
        console.log('✅ SciMSPT v4.0 initialized');
      } catch (error) {
        console.error('❌ Init error (non-fatal):', error);
      }
    };

    if (document.readyState === 'complete') {
      setTimeout(initWhenReady, 0);
    } else {
      document.addEventListener('DOMContentLoaded', () => setTimeout(initWhenReady, 0));
    }
    
    window.addEventListener('load', () => {
      if (!this.initialized) setTimeout(initWhenReady, 100);
    });
  }

  init() {
    this.loadSearchHistory();
    this.safeExecute('Search', () => this.setupGlobalSearch());
    this.safeExecute('Keyboard', () => this.setupKeyboardShortcuts());
    this.safeExecute('Overlay', () => this.createSearchOverlay());
    this.safeExecute('Toast', () => this.createToastContainer());
    this.safeExecute('Analytics', () => this.setupAnalytics());
  }

  safeExecute(name, fn) {
    try { fn(); } catch (e) { console.warn(`⚠️ ${name} failed:`, e.message); }
  }

  // ============================================
  // SEARCH HISTORY
  // ============================================

  loadSearchHistory() {
    try {
      const saved = localStorage.getItem('scimspt_search_history');
      if (saved) this.searchHistory = JSON.parse(saved);
    } catch (e) { this.searchHistory = []; }
  }

  saveSearchHistory() {
    try {
      localStorage.setItem('scimspt_search_history', JSON.stringify(this.searchHistory.slice(0, 50)));
    } catch (e) {}
  }

  addToHistory(query) {
    if (!query || !query.trim()) return;
    this.searchHistory = this.searchHistory.filter(h => h.toLowerCase() !== query.toLowerCase());
    this.searchHistory.unshift(query.trim());
    this.saveSearchHistory();
  }

  // ============================================
  // GLOBAL SEARCH
  // ============================================

  setupGlobalSearch() {
    const initSearch = () => {
      this.searchInput = document.querySelector('#globalSearchInput') ||
                         document.querySelector('.search-input') ||
                         document.querySelector('input[type="search"]');
      if (!this.searchInput) return;
      
      this.searchWrapper = this.searchInput.closest('.search-wrapper') || this.searchInput.parentElement;
      this.setupAutocomplete();
      
      const form = this.searchInput.closest('form');
      if (form) form.addEventListener('submit', (e) => this.handleSearch(e));
    };

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initSearch);
    } else {
      initSearch();
    }
  }

  setupAutocomplete() {
    if (!this.searchInput) return;
    
    this.searchSuggestions = document.createElement('div');
    this.searchSuggestions.id = 'globalSearchSuggestions';
    this.searchSuggestions.className = 'search-suggestions';
    
    if (this.searchWrapper) {
      this.searchWrapper.style.position = 'relative';
      this.searchWrapper.appendChild(this.searchSuggestions);
    }

    this.searchInput.addEventListener('input', (e) => {
      this.debounce(() => this.showSuggestions(e.target.value), 300);
    });

    this.searchInput.addEventListener('focus', () => {
      if (this.searchInput.value.length > 1) this.showSuggestions(this.searchInput.value);
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.search-wrapper')) this.hideSuggestions();
    });
  }

  showSuggestions(query) {
    if (!this.searchSuggestions || query.length < 2) { this.hideSuggestions(); return; }
    
    const matches = this.searchHistory
      .filter(h => h.toLowerCase().includes(query.toLowerCase()))
      .slice(0, 5);
    
    if (matches.length === 0) { this.hideSuggestions(); return; }

    this.searchSuggestions.innerHTML = matches.map(s => `
      <div class="suggestion-item" data-query="${this.escapeHtml(s)}">
        <span class="material-icons-round">history</span>
        <span>${this.escapeHtml(s)}</span>
      </div>
    `).join('');
    
    this.searchSuggestions.classList.add('visible');

    this.searchSuggestions.querySelectorAll('.suggestion-item').forEach(item => {
      item.addEventListener('click', () => {
        if (this.searchInput) this.searchInput.value = item.dataset.query;
        this.hideSuggestions();
        this.doSearch(item.dataset.query);
      });
    });
  }

  hideSuggestions() {
    if (this.searchSuggestions) this.searchSuggestions.classList.remove('visible');
  }

  handleSearch(e) {
    e.preventDefault();
    const query = this.searchInput ? this.searchInput.value : '';
    if (query.trim()) {
      this.addToHistory(query);
      this.doSearch(query);
    }
  }

  doSearch(query) {
    if (window.location.pathname.includes('search.html') || window.location.pathname.includes('results')) {
      window.dispatchEvent(new CustomEvent('scimspt:search', { detail: { query } }));
    } else {
      window.location.href = `search.html?q=${encodeURIComponent(query)}`;
    }
  }

  // ============================================
  // KEYBOARD SHORTCUTS
  // ============================================

  setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.toggleOverlay();
      }
      if (e.key === 'Escape') this.closeOverlay();
    });
  }

  // ============================================
  // SEARCH OVERLAY (Cmd+K)
  // ============================================

  createSearchOverlay() {
    if (document.getElementById('scimspt-search-overlay')) return;

    const overlay = document.createElement('div');
    overlay.id = 'scimspt-search-overlay';
    overlay.className = 'search-overlay';
    overlay.innerHTML = `
      <div class="search-overlay-content">
        <div class="search-overlay-header">
          <span class="material-icons-round">search</span>
          <input type="text" placeholder="Search papers, topics..." id="overlayInput" autofocus>
          <kbd>ESC</kbd>
        </div>
        <div class="search-overlay-results" id="overlayResults">
          <div class="search-overlay-empty">
            <span class="material-icons-round">science</span>
            <p>Start typing to search...</p>
          </div>
        </div>
        <div class="overlay-footer">
          <span><kbd>↑↓</kbd> Navigate</span>
          <span><kbd>Enter</kbd> Select</span>
          <span><kbd>Esc</kbd> Close</span>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) this.closeOverlay();
    });

    const input = document.getElementById('overlayInput');
    if (input) {
      input.addEventListener('input', (e) => this.debounce(() => this.overlaySearch(e.target.value), 200));
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const first = overlay.querySelector('.overlay-result-item');
          if (first) first.click();
        }
      });
    }
  }

  toggleOverlay() {
    const overlay = document.getElementById('scimspt-search-overlay');
    if (!overlay) return;

    if (overlay.classList.contains('active')) {
      this.closeOverlay();
    } else {
      overlay.classList.add('active');
      const input = document.getElementById('overlayInput');
      if (input) setTimeout(() => input.focus(), 100);
      this.showRecentSearches();
    }
  }

  closeOverlay() {
    const overlay = document.getElementById('scimspt-search-overlay');
    if (overlay) overlay.classList.remove('active');
  }

  showRecentSearches() {
    const container = document.getElementById('overlayResults');
    if (!container) return;

    if (this.searchHistory.length === 0) {
      container.innerHTML = `<div class="search-overlay-empty"><span class="material-icons-round">history</span><p>No recent searches</p></div>`;
      return;
    }

    container.innerHTML = `
      <div class="overlay-section-title">Recent Searches</div>
      ${this.searchHistory.slice(0, 8).map(h => `
        <div class="overlay-result-item" data-query="${this.escapeHtml(h)}">
          <span class="material-icons-round">history</span>
          <span>${this.escapeHtml(h)}</span>
          <span class="overlay-arrow">→</span>
        </div>
      `).join('')}
    `;

    container.querySelectorAll('.overlay-result-item').forEach(item => {
      item.addEventListener('click', () => {
        this.addToHistory(item.dataset.query);
        this.closeOverlay();
        this.doSearch(item.dataset.query);
      });
    });
  }

  async overlaySearch(query) {
    const container = document.getElementById('overlayResults');
    if (!container) return;

    if (query.length < 2) { this.showRecentSearches(); return; }

    container.innerHTML = `<div class="search-overlay-loading"><div class="spinner"></div><p>Searching...</p></div>`;

    try {
      const results = await this.searchArXiv(query);
      
      if (results.length === 0) {
        container.innerHTML = `<div class="search-overlay-empty"><span class="material-icons-round">search_off</span><p>No results for "${this.escapeHtml(query)}"</p></div>`;
        return;
      }

      container.innerHTML = `
        <div class="overlay-section-title">ArXiv Results</div>
        ${results.slice(0, 8).map(r => `
          <div class="overlay-result-item" data-url="${r.url || '#'}">
            <span class="material-icons-round">article</span>
            <div class="overlay-result-content">
              <div class="overlay-result-title">${this.escapeHtml(r.title)}</div>
              <div class="overlay-result-meta">${r.authors ? this.escapeHtml(r.authors.substring(0, 60)) : ''}</div>
            </div>
            <span class="overlay-arrow">→</span>
          </div>
        `).join('')}
      `;

      container.querySelectorAll('.overlay-result-item[data-url]').forEach(item => {
        item.addEventListener('click', () => {
          if (item.dataset.url && item.dataset.url !== '#') window.open(item.dataset.url, '_blank');
        });
      });
    } catch (error) {
      container.innerHTML = `<div class="search-overlay-empty"><span class="material-icons-round">error</span><p>Search error. Try again.</p></div>`;
    }
  }

  // ============================================
  // API: ARXIV SEARCH
  // ============================================

  async searchArXiv(query) {
    const cacheKey = `arxiv:${query}`;
    const cached = this.getCache(cacheKey);
    if (cached) return cached;

    try {
      const response = await fetch(`${this.apiEndpoints.arxiv}${encodeURIComponent(query)}&max_results=10`);
      const text = await response.text();
      const results = this.parseArXivXML(text);
      this.setCache(cacheKey, results);
      return results;
    } catch (error) {
      console.error('ArXiv search error:', error);
      return [];
    }
  }

  parseArXivXML(xmlText) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(xmlText, 'text/xml');
    const entries = doc.querySelectorAll('entry');
    const results = [];

    entries.forEach(entry => {
      const title = entry.querySelector('title')?.textContent?.trim() || 'Untitled';
      const url = entry.querySelector('id')?.textContent?.trim() || '#';
      
      const authorEls = entry.querySelectorAll('author name');
      const authors = Array.from(authorEls).map(a => a.textContent.trim()).join(', ');
      
      const summary = entry.querySelector('summary')?.textContent?.trim() || '';
      const published = entry.querySelector('published')?.textContent?.split('T')[0] || '';

      results.push({ title, url, authors, summary, published, source: 'arxiv' });
    });

    return results;
  }

  // ============================================
  // API: PUBMED SEARCH
  // ============================================

  async searchPubMed(query) {
    const cacheKey = `pubmed:${query}`;
    const cached = this.getCache(cacheKey);
    if (cached) return cached;

    try {
      const searchResponse = await fetch(`${this.apiEndpoints.pubmed}${encodeURIComponent(query)}&retmax=10`);
      const searchText = await searchResponse.text();
      const idMatch = searchText.match(/<Id>(\d+)<\/Id>/g);
      
      if (!idMatch || idMatch.length === 0) return [];

      const ids = idMatch.map(m => m.match(/<Id>(\d+)<\/Id>/)[1]).join(',');
      const fetchResponse = await fetch(`${this.apiEndpoints.pubmedFetch}${ids}`);
      const fetchData = await fetchResponse.json();
      const results = this.parsePubMedJSON(fetchData);
      
      this.setCache(cacheKey, results);
      return results;
    } catch (error) {
      console.error('PubMed search error:', error);
      return [];
    }
  }

  parsePubMedJSON(data) {
    const results = [];
    const articles = data.resultlist?.result || [];
    
    (Array.isArray(articles) ? articles : [articles]).forEach(article => {
      results.push({
        title: article.title || 'Untitled',
        authors: Array.isArray(article.authors?.author) 
          ? article.authors.author.map(a => a.name).join(', ') 
          : '',
        url: article.elocationid ? `https://pubmed.ncbi.nlm.nih.gov/${article.uid}/` : '#',
        source: 'pubmed'
      });
    });

    return results;
  }

  // ============================================
  // CACHING SYSTEM
  // ============================================

  getCache(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    if (Date.now() - item.timestamp > this.CACHE_TTL) {
      this.cache.delete(key);
      return null;
    }
    return item.data;
  }

  setCache(key, data) {
    this.cache.set(key, { data, timestamp: Date.now() });
  }

  // ============================================
  // TOAST NOTIFICATIONS
  // ============================================

  createToastContainer() {
    if (document.getElementById('scimspt-toast-container')) return;
    
    const container = document.createElement('div');
    container.id = 'scimspt-toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('scimspt-toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icons = { success: 'check_circle', error: 'error', warning: 'warning', info: 'info' };
    toast.innerHTML = `
      <span class="material-icons-round">${icons[type] || 'info'}</span>
      <span class="toast-message">${this.escapeHtml(message)}</span>
      <button class="toast-close"><span class="material-icons-round">close</span></button>
    `;

    container.appendChild(toast);
    
    // Trigger animation
    requestAnimationFrame(() => toast.classList.add('show'));

    // Close button
    toast.querySelector('.toast-close').addEventListener('click', () => this.dismissToast(toast));
    
    // Auto dismiss
    if (duration > 0) {
      setTimeout(() => this.dismissToast(toast), duration);
    }

    return toast;
  }

  dismissToast(toast) {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }

  // ============================================
  // ANALYTICS (GA4)
  // ============================================

  setupAnalytics() {
    // Only setup if gtag is available
    if (typeof gtag === 'function') {
      this.trackPageView(window.location.pathname);
    }
  }

  trackPageView(path) {
    if (typeof gtag === 'function') {
      try {
        gtag('event', 'page_view', { page_path: path });
      } catch (e) {}
    }
  }

  trackEvent(action, params = {}) {
    if (typeof gtag === 'function') {
      try {
        gtag('event', action, params);
      } catch (e) {}
    }
  }

  // ============================================
  // EXPORT FEATURES
  // ============================================

  exportToCSV(data, filename = 'export.csv') {
    if (!data || !data.length) return;
    
    const headers = Object.keys(data[0]);
    const csvContent = [
      headers.join(','),
      ...data.map(row => headers.map(h => `"${(row[h] + '').replace(/"/g, '""')}"`).join(','))
    ].join('\n');

    this.downloadFile(csvContent, filename, 'text/csv');
    this.showToast('Exported to CSV', 'success');
  }

  exportToJSON(data, filename = 'export.json') {
    const jsonContent = JSON.stringify(data, null, 2);
    this.downloadFile(jsonContent, filename, 'application/json');
    this.showToast('Exported to JSON', 'success');
  }

  exportToBibTeX(papers, filename = 'references.bib') {
    if (!papers || !papers.length) return;
    
    const bibtex = papers.map((paper, i) => {
      const key = paper.title ? paper.title.substring(0, 20).replace(/\s+/g, '').toLowerCase() : `paper${i}`;
      return `@article{${key},
  title={${paper.title}},
  author={${paper.authors || 'Unknown'}},
  year={new Date().getFullYear()}
}`;
    }).join('\n\n');

    this.downloadFile(bibtex, filename, 'application/x-bibtex');
    this.showToast('Exported to BibTeX', 'success');
  }

  downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // ============================================
  // UTILITY FUNCTIONS
  // ============================================

  debounce(fn, delay) {
    clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(fn, delay);
  }

  escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  throttle(fn, limit) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        fn.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }
}

// ============================================
// GLOBAL INITIALIZATION (SAFE)
// ============================================

let scimspt;

// Initialize when DOM is ready - but NEVER block rendering
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    scimspt = new SciMSPTGlobal();
    window.scimspt = scimspt;
  });
} else {
  scimspt = new SciMSPTGlobal();
  window.scimspt = scimspt;
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SciMSPTGlobal;
}
