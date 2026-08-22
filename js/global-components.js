/**
 * SciMSPT Global Components System v3.0
 * =======================================
 * Comprehensive feature suite:
 * - ArXiv/PubMed API Integration with Caching
 * - Semantic Search with NLP Enhancement
 * - Search History (localStorage + Cross-device sync)
 * - Keyboard Shortcuts (Ctrl+K / Cmd+K)
 * - Inline Results Dropdown (no page nav)
 * - Autocomplete with Real-time Suggestions
 * - Toast Notification System
 * - Google Analytics 4 Integration
 * - Page Transitions & Scroll Animations
 * - Skeleton Screen Loading States
 * - Export Features (CSV, JSON, BibTeX)
 * - Performance Monitoring
 */

class SciMSPTGlobal {
  constructor() {
    // Core state
    this.searchInput = null;
    this.searchWrapper = null;
    this.searchSuggestions = null;
    this.searchOverlay = null;
    this.searchHistory = [];
    this.isSearching = false;
    this.debounceTimer = null;
    this.cache = new Map();
    this.CACHE_TTL = 5 * 60 * 1000; // 5 minutes
    
    // API Endpoints with CORS proxies if needed
    this.apiEndpoints = {
      arxiv: 'https://export.arxiv.org/api/query?search_query=all:',
      pubmed: 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=',
      pubmedFetch: 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=json&id=',
      cacheApi: '/api/cache' // Server-side caching endpoint
    };
    
    // Analytics configuration
    this.analyticsConfig = {
      ga4MeasurementId: 'G-XXXXXXXXXX', // Replace with actual GA4 ID
      plausibleDomain: window.location.hostname,
      enabled: true
    };
    
    // Initialize all systems
    this.init();
  }

  // ============================================
  // INITIALIZATION
  // ============================================

  init() {
    this.loadSearchHistory();
    this.setupGlobalSearchListener();
    this.setupKeyboardShortcuts();
    this.createSearchOverlay();
    this.createToastContainer();
    this.setupAnalytics();
    this.setupPageTransitions();
    this.setupScrollAnimations();
    this.observePerformance();
    
    console.log('🚀 SciMSPT Global Components v3.0 initialized');
  }

  // ============================================
  // SEARCH HISTORY MANAGEMENT
  // ============================================

  loadSearchHistory() {
    try {
      const saved = localStorage.getItem('scimspt-search-history');
      this.searchHistory = saved ? JSON.parse(saved) : [];
      
      // Load from cloud if user is logged in
      if (this.isUserLoggedIn()) {
        this.syncSearchHistoryFromCloud();
      }
    } catch (e) {
      this.searchHistory = [];
    }
  }

  saveSearchHistory(query) {
    if (!query || query.trim().length < 2) return;
    
    // Remove if already exists (move to top)
    this.searchHistory = this.searchHistory.filter(h => h !== query);
    
    // Add to beginning
    this.searchHistory.unshift({
      query: query.trim(),
      timestamp: Date.now(),
      resultCount: 0
    });
    
    // Keep only last 50 searches
    this.searchHistory = this.searchHistory.slice(0, 50);
    
    // Save to localStorage
    try {
      localStorage.setItem('scimspt-search-history', JSON.stringify(this.searchHistory));
      
      // Sync to cloud if user is logged in
      if (this.isUserLoggedIn()) {
        this.syncSearchHistoryToCloud();
      }
    } catch (e) {
      console.warn('Could not save search history:', e);
    }
  }

  getRecentSearches(limit = 5) {
    return this.searchHistory.slice(0, limit).map(h => 
      typeof h === 'string' ? h : h.query
    );
  }

  clearSearchHistory() {
    this.searchHistory = [];
    localStorage.removeItem('scimspt-search-history');
    this.showToast('Search history cleared', 'info');
    
    // Clear from cloud too
    if (this.isUserLoggedIn()) {
      fetch('/api/search-history', { method: 'DELETE' });
    }
  }

  isUserLoggedIn() {
    return localStorage.getItem('scimspt-user-token') !== null;
  }

  async syncSearchHistoryFromCloud() {
    try {
      const token = localStorage.getItem('scimspt-user-token');
      const response = await fetch('/api/search-history', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const cloudHistory = await response.json();
        // Merge histories (cloud takes precedence for duplicates)
        const merged = [...cloudHistory, ...this.searchHistory]
          .filter((v, i, a) => a.findIndex(t => 
            (typeof t === 'string' ? t : t.query) === (typeof v === 'string' ? v : v.query)
          ) === i)
          .slice(0, 50);
        
        this.searchHistory = merged;
        localStorage.setItem('scimspt-search-history', JSON.stringify(merged));
      }
    } catch (e) {
      console.warn('Could not sync search history from cloud:', e);
    }
  }

  async syncSearchHistoryToCloud() {
    try {
      const token = localStorage.getItem('scimspt-user-token');
      await fetch('/api/search-history', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(this.searchHistory)
      });
    } catch (e) {
      console.warn('Could not sync search history to cloud:', e);
    }
  }

  // ============================================
  // SERVER-SIDE CACHING LAYER
  // ============================================

  getCacheKey(url, params) {
    return `${url}:${JSON.stringify(params)}`;
  }

  async getCachedData(key) {
    // Check memory cache first
    if (this.cache.has(key)) {
      const cached = this.cache.get(key);
      if (Date.now() - cached.timestamp < this.CACHE_TTL) {
        console.log('✅ Cache hit (memory):', key);
        return cached.data;
      }
      this.cache.delete(key);
    }
    
    // Check server-side cache
    try {
      const response = await fetch(`${this.apiEndpoints.cacheApi}?key=${encodeURIComponent(key)}`);
      if (response.ok) {
        const { data, timestamp } = await response.json();
        if (Date.now() - timestamp < this.CACHE_TTL) {
          console.log('✅ Cache hit (server):', key);
          this.cache.set(key, { data, timestamp: Date.now() });
          return data;
        }
      }
    } catch (e) {
      console.warn('Server cache check failed:', e);
    }
    
    return null;
  }

  async setCachedData(key, data) {
    // Set in memory cache
    this.cache.set(key, { data, timestamp: Date.now() });
    
    // Set in server-side cache
    try {
      await fetch(this.apiEndpoints.cacheApi, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key, data, timestamp: Date.now() })
      });
    } catch (e) {
      console.warn('Server cache set failed:', e);
    }
  }

  // ============================================
  // ARXIV API INTEGRATION (with caching)
  // ============================================

  async searchArXiv(query, maxResults = 10) {
    const cacheKey = this.getCacheKey('arxiv', { query, maxResults });
    
    // Try cache first
    const cached = await this.getCachedData(cacheKey);
    if (cached) {
      this.trackEvent('search_cache_hit', { source: 'arxiv' });
      return cached;
    }
    
    try {
      const encodedQuery = encodeURIComponent(query);
      const url = `${this.apiEndpoints.arxiv}${encodedQuery}&start=0&max_results=${maxResults}&sortBy=submittedDate&sortOrder=descending`;
      
      const response = await fetch(url);
      const text = await response.text();
      
      // Parse XML response
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(text, 'text/xml');
      
      const entries = xmlDoc.getElementsByTagName('entry');
      const results = [];
      
      for (let entry of entries) {
        const title = entry.getElementsByTagName('title')[0]?.textContent || '';
        const summary = entry.getElementsByTagName('summary')[0]?.textContent || '';
        const id = entry.getElementsByTagName('id')[0]?.textContent || '';
        const published = entry.getElementsByTagName('published')[0]?.textContent || '';
        const updated = entry.getElementsByTagName('updated')[0]?.textContent || '';
        const authors = Array.from(entry.getElementsByTagName('author')).map(a => 
          a.getElementsByTagName('name')[0]?.textContent || ''
        );
        
        // Extract categories
        const categories = Array.from(entry.getElementsByTagName('category')).map(c => 
          c.getAttribute('term') || ''
        ).filter(Boolean);
        
        // Get PDF link
        const links = Array.from(entry.getElementsByTagName('link'));
        const pdfLink = links.find(l => l.getAttribute('title') === 'pdf')?.getAttribute('href') || '';
        
        results.push({
          id: id.split('/').pop() || id,
          title: title.replace(/\n/g, ' ').trim(),
          summary: summary.replace(/\n/g, ' ').trim().substring(0, 400) + '...',
          authors,
          published: new Date(published).toLocaleDateString(),
          updated: new Date(updated).toLocaleDateString(),
          categories,
          source: 'arxiv',
          url: id,
          pdfUrl: pdfLink,
          type: 'paper',
          year: new Date(published).getFullYear()
        });
      }
      
      const result = { success: true, results, source: 'ArXiv', total: results.length };
      
      // Cache the result
      await this.setCachedData(cacheKey, result);
      
      return result;
      
    } catch (error) {
      console.error('ArXiv search error:', error);
      return { success: false, error: error.message, results: [] };
    }
  }

  // ============================================
  // PUBMED API INTEGRATION (with caching)
  // ============================================

  async searchPubMed(query, maxResults = 10) {
    const cacheKey = this.getCacheKey('pubmed', { query, maxResults });
    
    // Try cache first
    const cached = await this.getCachedData(cacheKey);
    if (cached) {
      this.trackEvent('search_cache_hit', { source: 'pubmed' });
      return cached;
    }
    
    try {
      const encodedQuery = encodeURIComponent(query);
      const searchUrl = `${this.apiEndpoints.pubmed}${encodedQuery}&retmax=${maxResults}&retmode=json&sort=relevance`;
      
      const searchResponse = await fetch(searchUrl);
      const searchData = await searchResponse.json();
      
      const ids = searchData.esearchresult?.idlist || [];
      const totalCount = parseInt(searchData.esearchresult?.count || 0);
      
      if (ids.length === 0) {
        const result = { success: true, results: [], source: 'PubMed', total: 0 };
        await this.setCachedData(cacheKey, result);
        return result;
      }
      
      // Fetch details for each paper
      const fetchUrl = `${this.apiEndpoints.pubmedFetch}${ids.join(',')}`;
      const fetchResponse = await fetch(fetchUrl);
      const fetchData = await fetchResponse.json();
      
      const results = (fetchData.result || []).filter(key => key !== 'uids').map(key => {
        const article = fetchData.result[key];
        return {
          id: article.pmid || key,
          title: article.title || '',
          summary: (article.abstract || '').replace(/[\n\r]+/g, ' ').trim().substring(0, 400) + '...',
          authors: article.authors?.map(a => a.name || '') || [],
          published: article.pubdate || '',
          categories: [article.source || 'Journal Article'],
          journal: article.journal || '',
          source: 'pubmed',
          url: `https://pubmed.ncbi.nlm.nih.gov/${article.pmid}/`,
          doi: article.doi ? `https://doi.org/${article.doi}` : '',
          type: 'paper',
          year: article.pubdate ? parseInt(article.pubdate.split(' ')[0]) : null
        };
      });
      
      const result = { success: true, results, source: 'PubMed', total: totalCount };
      
      // Cache the result
      await this.setCachedData(cacheKey, result);
      
      return result;
      
    } catch (error) {
      console.error('PubMed search error:', error);
      return { success: false, error: error.message, results: [] };
    }
  }

  // ============================================
  // SEMANTIC SEARCH (NLP-Enhanced)
  // ============================================

  enhanceQueryWithNLP(query) {
    let enhanced = query.trim();
    
    // Expand common abbreviations
    const expansions = {
      'ml': 'machine learning',
      'dl': 'deep learning',
      'nlp': 'natural language processing',
      'ai': 'artificial intelligence',
      'cv': 'computer vision',
      'rl': 'reinforcement learning',
      'llm': 'large language model',
      'gpt': 'generative pre-trained transformer',
      'quantum': 'quantum computing',
      'crispr': 'gene editing CRISPR'
    };
    
    Object.keys(expansions).forEach(abbr => {
      const regex = new RegExp(`\\b${abbr}\\b`, 'gi');
      enhanced = enhanced.replace(regex, `(${abbr} OR ${expansions[abbr]})`);
    });
    
    // Add field-specific terms based on context
    const fieldTerms = {
      physics: ['quantum mechanics', 'particle physics', 'theoretical physics'],
      biology: ['molecular biology', 'genomics', 'biochemistry'],
      medicine: ['clinical trial', 'treatment', 'therapy'],
      cs: ['algorithm', 'computing', 'programming']
    };
    
    return enhanced;
  }

  async semanticSearch(query, options = {}) {
    const startTime = performance.now();
    const enhancedQuery = this.enhanceQueryWithNLP(query);
    
    this.trackEvent('semantic_search_initiated', { 
      original_query: query,
      enhanced_query: enhancedQuery 
    });
    
    // Search multiple sources in parallel
    const [arxivResults, pubmedResults] = await Promise.allSettled([
      this.searchArXiv(enhancedQuery, options.maxResults || 10),
      this.searchPubMed(enhancedQuery, options.maxResults || 10)
    ]);
    
    const arxivData = arxivResults.status === 'fulfilled' ? arxivResults.value : { results: [] };
    const pubmedData = pubmedResults.status === 'fulfilled' ? pubmedResults.value : { results: [] };
    
    // Combine and rank results by relevance
    const allResults = [
      ...(arxivData.results || []).map(r => ({ ...r, relevanceScore: this.calculateRelevance(r, query) })),
      ...(pubmedData.results || []).map(r => ({ ...r, relevanceScore: this.calculateRelevance(r, query) }))
    ];
    
    // Sort by relevance score
    allResults.sort((a, b) => b.relevanceScore - a.relevanceScore);
    
    // Apply filters if provided
    let filteredResults = allResults;
    if (options.filters) {
      filteredResults = this.applyFilters(allResults, options.filters);
    }
    
    const duration = performance.now() - startTime;
    
    const result = {
      success: true,
      results: filteredResults.slice(0, options.limit || 20),
      sources: {
        arxiv: arxivData,
        pubmed: pubmedData
      },
      metadata: {
        originalQuery: query,
        enhancedQuery,
        totalResults: allResults.length,
        duration: Math.round(duration),
        timestamp: Date.now()
      }
    };
    
    // Save to search history
    this.saveSearchHistory(query);
    
    // Track performance
    this.trackEvent('search_completed', {
      result_count: result.results.length,
      duration_ms: Math.round(duration),
      sources: ['arxiv', 'pubmed'].filter(s => result.sources[s].results.length > 0)
    });
    
    return result;
  }

  calculateRelevance(result, query) {
    let score = 0;
    const queryTerms = query.toLowerCase().split(/\s+/);
    const title = (result.title || '').toLowerCase();
    const summary = (result.summary || '').toLowerCase();
    
    // Title matches are worth more
    queryTerms.forEach(term => {
      if (title.includes(term)) score += 10;
      if (summary.includes(term)) score += 2;
    });
    
    // Boost recent papers
    if (result.year && result.year >= 2023) score += 5;
    
    // Category matching
    if (result.categories) {
      result.categories.forEach(cat => {
        if (queryTerms.some(term => cat.toLowerCase().includes(term))) {
          score += 3;
        }
      });
    }
    
    return score;
  }

  applyFilters(results, filters) {
    let filtered = [...results];
    
    if (filters.year) {
      const [minYear, maxYear] = filters.year;
      filtered = filtered.filter(r => r.year >= minYear && r.year <= maxYear);
    }
    
    if (filters.source && filters.source.length > 0) {
      filtered = filtered.filter(r => filters.source.includes(r.source));
    }
    
    if (filters.type && filters.type.length > 0) {
      filtered = filtered.filter(r => filters.type.includes(r.type));
    }
    
    if (filters.categories && filters.categories.length > 0) {
      filtered = filtered.filter(r => 
        r.categories.some(c => filters.categories.some(fc => c.toLowerCase().includes(fc.toLowerCase())))
      );
    }
    
    return filtered;
  }

  // ============================================
  // SEARCH UI COMPONENTS
  // ============================================

  setupGlobalSearchListener() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.initSearchUI());
    } else {
      this.initSearchUI();
    }
  }

  initSearchUI() {
    this.searchInput = document.getElementById('globalSearchInput');
    this.searchWrapper = document.getElementById('globalSearchWrapper');
    this.searchSuggestions = document.getElementById('globalSearchSuggestions');
    
    if (!this.searchInput) return;
    
    // Input event listener with debounce
    this.searchInput.addEventListener('input', (e) => {
      this.handleSearchInput(e.target.value);
    });
    
    // Focus events
    this.searchInput.addEventListener('focus', () => {
      this.showSuggestions();
    });
    
    // Click outside to close
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.search-wrapper')) {
        this.hideSuggestions();
      }
    });
    
    // Form submit
    const form = this.searchInput.closest('form');
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.performSearch(this.searchInput.value);
      });
    }
  }

  handleSearchInput(value) {
    // Debounce input
    clearTimeout(this.debounceTimer);
    
    if (value.length < 2) {
      this.showRecentSearches();
      return;
    }
    
    this.debounceTimer = setTimeout(() => {
      this.showAutocompleteSuggestions(value);
    }, 300);
  }

  showRecentSearches() {
    if (!this.searchSuggestions) return;
    
    const recent = this.getRecentSearches(5);
    
    if (recent.length === 0) {
      this.searchSuggestions.innerHTML = `
        <div class="suggestion-empty">
          <span class="material-icons-round">history</span>
          <p>No recent searches</p>
        </div>
      `;
      return;
    }
    
    this.searchSuggestions.innerHTML = `
      <div class="suggestion-header">
        <span>Recent Searches</span>
        <button onclick="window.scimspt.clearSearchHistory()" class="clear-history-btn">
          <span class="material-icons-round">delete_outline</span> Clear
        </button>
      </div>
      ${recent.map(item => `
        <div class="suggestion-item" onclick="window.scimspt.performSearch('${item.replace(/'/g, "\\'")}')">
          <span class="material-icons-round">history</span>
          <span>${this.escapeHtml(item)}</span>
        </div>
      `).join('')}
    `;
    
    this.showSuggestions();
  }

  async showAutocompleteSuggestions(query) {
    if (!this.searchSuggestions) return;
    
    this.searchSuggestions.innerHTML = `
      <div class="suggestion-loading">
        <div class="skeleton-loader"></div>
        <div class="skeleton-loader"></div>
        <div class="skeleton-loader"></div>
      </div>
    `;
    this.showSuggestions();
    
    try {
      // Quick search for autocomplete (fewer results, faster)
      const results = await this.semanticSearch(query, { maxResults: 5, limit: 5 });
      
      if (results.results.length === 0) {
        this.searchSuggestions.innerHTML = `
          <div class="suggestion-empty">
            <span class="material-icons-round">search_off</span>
            <p>No results found for "${this.escapeHtml(query)}"</p>
            <p class="suggestion-hint">Try different keywords or check spelling</p>
          </div>
        `;
        return;
      }
      
      this.searchSuggestions.innerHTML = `
        <div class="suggestion-header">
          <span>Suggestions</span>
          <span class="result-count">${results.metadata.totalResults}+ results</span>
        </div>
        ${results.results.map(result => `
          <div class="suggestion-item" onclick="window.scimspt.selectResult('${result.id}', '${result.source}')">
            <span class="material-icons-round">${result.source === 'arxiv' ? 'article' : 'biotech'}</span>
            <div class="suggestion-content">
              <div class="suggestion-title">${this.escapeHtml(result.title.substring(0, 80))}</div>
              <div class="suggestion-meta">
                ${result.authors.slice(0, 2).join(', ')} • ${result.published}
              </div>
            </div>
            <span class="source-badge ${result.source}">${result.source}</span>
          </div>
        `).join('')}
        <div class="suggestion-footer">
          <button onclick="window.scimspt.performSearch('${query.replace(/'/g, "\\'")}')" class="view-all-btn">
            View all results →
          </button>
        </div>
      `;
      
    } catch (error) {
      console.error('Autocomplete error:', error);
      this.searchSuggestions.innerHTML = `
        <div class="suggestion-error">
          <span class="material-icons-round">error_outline</span>
          <p>Error loading suggestions</p>
        </div>
      `;
    }
  }

  selectResult(id, source) {
    this.trackEvent('result_selected', { id, source });
    // Navigate to result detail or open URL
    const result = this.findResultById(id, source);
    if (result && result.url) {
      window.open(result.url, '_blank');
    }
    this.hideSuggestions();
  }

  findResultById(id, source) {
    // This would typically be stored from last search
    return null;
  }

  performSearch(query) {
    if (!query || query.trim().length < 2) {
      this.showToast('Please enter at least 2 characters to search', 'warning');
      return;
    }
    
    this.trackEvent('search_performed', { query });
    
    // Show loading state
    this.showSearchLoading();
    
    // Perform semantic search
    this.semanticSearch(query).then(results => {
      this.hideSearchLoading();
      this.displaySearchResults(results);
      this.hideSuggestions();
      
      // Update URL without reload
      const url = new URL(window.location);
      url.searchParams.set('q', query);
      window.history.pushState({}, '', url);
      
    }).catch(error => {
      this.hideSearchLoading();
      this.showToast('Search failed. Please try again.', 'error');
      console.error('Search error:', error);
    });
  }

  displaySearchResults(results) {
    // If on search results page, update the results container
    const resultsContainer = document.getElementById('searchResultsContainer');
    if (resultsContainer) {
      this.renderResultsInContainer(resultsContainer, results);
      return;
    }
    
    // Otherwise, redirect to search results page with data
    const searchData = btoa(JSON.stringify(results));
    window.location.href = `search-results.html?data=${encodeURIComponent(searchData)}`;
  }

  renderResultsInContainer(container, results) {
    container.innerHTML = `
      <div class="results-header">
        <h2>Search Results</h2>
        <div class="results-meta">
          <span>${results.results.length} results found</span>
          <span>in ${Math.round(results.metadata.duration)}ms</span>
        </div>
      </div>
      
      <div class="results-filters">
        <button class="filter-btn active" data-filter="all">All</button>
        <button class="filter-btn" data-filter="arxiv">ArXiv (${results.sources.arxiv.results.length})</button>
        <button class="filter-btn" data-filter="pubmed">PubMed (${results.sources.pubmed.results.length})</button>
        <select class="sort-select" id="sortSelect">
          <option value="relevance">Relevance</option>
          <option value="date">Date (Newest)</option>
          <option value="citations">Citations</option>
        </select>
        <div class="export-buttons">
          <button onclick="window.scimspt.exportResults('csv')" class="export-btn">
            <span class="material-icons-round">download</span> CSV
          </button>
          <button onclick="window.scimspt.exportResults('json')" class="export-btn">
            <span class="material-icons-round">code</span> JSON
          </button>
          <button onclick="window.scimspt.exportResults('bibtex')" class="export-btn">
            <span class="material-icons-round">book</span> BibTeX
          </button>
        </div>
      </div>
      
      <div class="results-list">
        ${results.results.map((result, index) => `
          <div class="result-card" data-source="${result.source}" style="animation-delay: ${index * 0.05}s">
            <div class="result-header">
              <span class="source-badge ${result.source}">${result.source.toUpperCase()}</span>
              <span class="result-date">${result.published}</span>
            </div>
            <h3 class="result-title">
              <a href="${result.url}" target="_blank" rel="noopener">${this.escapeHtml(result.title)}</a>
            </h3>
            <div class="result-authors">${result.authors.join(', ')}</div>
            <p class="result-summary">${this.escapeHtml(result.summary)}</p>
            <div class="result-categories">
              ${result.categories.slice(0, 3).map(cat => `<span class="category-tag">${cat}</span>`).join('')}
            </div>
            <div class="result-actions">
              ${result.pdfUrl ? `<a href="${result.pdfUrl}" target="_blank" class="action-link"><span class="material-icons-round">picture_as_pdf</span> PDF</a>` : ''}
              <a href="${result.url}" target="_blank" rel="noopener" class="action-link"><span class="material-icons-round">open_in_new</span> View</a>
              <button onclick="window.scimspt.saveResult('${result.id}')" class="action-link"><span class="material-icons-round">bookmark_border</span> Save</button>
            </div>
          </div>
        `).join('')}
      </div>
    `;
    
    // Store current results for export
    this.currentResults = results;
    
    // Setup filter buttons
    container.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        this.filterResults(e.target.dataset.filter);
      });
    });
  }

  filterResults(filter) {
    const cards = document.querySelectorAll('.result-card');
    cards.forEach(card => {
      if (filter === 'all' || card.dataset.source === filter) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  }

  // ============================================
  // EXPORT FEATURES
  // ============================================

  exportResults(format) {
    if (!this.currentResults || !this.currentResults.results.length) {
      this.showToast('No results to export', 'warning');
      return;
    }
    
    this.trackEvent('results_exported', { format });
    
    let content, filename, type;
    
    switch (format) {
      case 'csv':
        content = this.exportAsCSV();
        filename = `scimspt-search-${Date.now()}.csv`;
        type = 'text/csv';
        break;
      case 'json':
        content = JSON.stringify(this.currentResults.results, null, 2);
        filename = `scimspt-search-${Date.now()}.json`;
        type = 'application/json';
        break;
      case 'bibtex':
        content = this.exportAsBibTeX();
        filename = `scimspt-search-${Date.now()}.bib`;
        type = 'text/plain';
        break;
      default:
        return;
    }
    
    // Download file
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    this.showToast(`Exported as ${format.toUpperCase()}`, 'success');
  }

  exportAsCSV() {
    const headers = ['Title', 'Authors', 'Source', 'Published', 'Categories', 'URL'];
    const rows = this.currentResults.results.map(r => [
      `"${r.title.replace(/"/g, '""')}"`,
      `"${r.authors.join('; ')}"`,
      r.source,
      r.published,
      `"${r.categories.join('; ')}"`,
      r.url
    ]);
    
    return [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  }

  exportAsBibTeX() {
    return this.currentResults.results.map(r => {
      const key = r.authors[0]?.split(' ')[0]?.toLowerCase() + r.year + r.id?.slice(-4) || `entry${r.id}`;
      return `@article{${key},
  title = {${r.title}},
  author = {${r.authors.join(' and ')}},
  journal = {${r.categories[0] || 'Unknown'}},
  year = {${r.year || r.published}},
  url = {${r.url}}
}`;
    }).join('\n\n');
  }

  saveResult(id) {
    // Get saved papers from localStorage
    let savedPapers = [];
    try {
      savedPapers = JSON.parse(localStorage.getItem('scimspt-saved-papers') || '[]');
    } catch (e) {}
    
    const paper = this.currentResults.results.find(r => r.id === id);
    if (paper && !savedPapers.find(p => p.id === id)) {
      savedPapers.unshift(paper);
      localStorage.setItem('scimspt-saved-papers', JSON.stringify(savedPapers));
      this.showToast('Paper saved to library', 'success');
      this.trackEvent('paper_saved', { id });
    } else if (savedPapers.find(p => p.id === id)) {
      this.showToast('Paper already saved', 'info');
    }
  }

  // ============================================
  // KEYBOARD SHORTCUTS
  // ============================================

  setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ctrl+K / Cmd+K to open search
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.openSearchOverlay();
        return;
      }
      
      // Escape to close overlay/suggestions
      if (e.key === 'Escape') {
        this.closeSearchOverlay();
        this.hideSuggestions();
        return;
      }
      
      // Navigate suggestions with arrow keys
      if (this.searchSuggestions && this.searchSuggestions.classList.contains('visible')) {
        this.handleSuggestionNavigation(e);
      }
    });
  }

  handleSuggestionNavigation(e) {
    const items = this.searchSuggestions.querySelectorAll('.suggestion-item:not([disabled])');
    const currentIndex = Array.from(items).findIndex(item => item.classList.contains('focused'));
    
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (currentIndex < items.length - 1) {
          items[currentIndex]?.classList.remove('focused');
          items[currentIndex + 1]?.classList.add('focused');
          items[currentIndex + 1]?.scrollIntoView({ block: 'nearest' });
        }
        break;
        
      case 'ArrowUp':
        e.preventDefault();
        if (currentIndex > 0) {
          items[currentIndex]?.classList.remove('focused');
          items[currentIndex - 1]?.classList.add('focused');
          items[currentIndex - 1]?.scrollIntoView({ block: 'nearest' });
        }
        break;
        
      case 'Enter':
        e.preventDefault();
        if (currentIndex >= 0) {
          items[currentIndex].click();
        }
        break;
    }
  }

  createSearchOverlay() {
    // Create overlay element
    this.searchOverlay = document.createElement('div');
    this.searchOverlay.className = 'search-overlay';
    this.searchOverlay.id = 'searchOverlay';
    this.searchOverlay.innerHTML = `
      <div class="search-overlay-content">
        <div class="search-overlay-header">
          <span class="material-icons-round">search</span>
          <input type="text" 
                 id="overlaySearchInput" 
                 placeholder="Search research papers, startups, quantum algorithms..." 
                 autofocus
          >
          <kbd>ESC</kbd>
        </div>
        <div class="search-overlay-results" id="overlaySearchResults">
          <div class="search-overlay-empty">
            <span class="material-icons-round">travel_explore</span>
            <p>Start typing to search across ArXiv & PubMed</p>
            <div class="search-shortcuts-hint">
              <span><kbd>↑↓</kbd> Navigate</span>
              <span><kbd>↵</kbd> Select</span>
              <span><kbd>esc</kbd> Close</span>
            </div>
          </div>
        </div>
        <div class="search-overlay-filters">
          <button class="overlay-filter active" data-source="all">All Sources</button>
          <button class="overlay-filter" data-source="arxiv">ArXiv</button>
          <button class="overlay-filter" data-source="pubmed">PubMed</button>
        </div>
      </div>
    `;
    
    document.body.appendChild(this.searchOverlay);
    
    // Setup overlay events
    const overlayInput = document.getElementById('overlaySearchInput');
    overlayInput?.addEventListener('input', (e) => {
      this.handleOverlaySearch(e.target.value);
    });
    
    overlayInput?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        this.performSearch(overlayInput.value);
        this.closeSearchOverlay();
      }
    });
    
    // Close on backdrop click
    this.searchOverlay.addEventListener('click', (e) => {
      if (e.target === this.searchOverlay) {
        this.closeSearchOverlay();
      }
    });
    
    // Filter buttons
    this.searchOverlay.querySelectorAll('.overlay-filter').forEach(btn => {
      btn.addEventListener('click', () => {
        this.searchOverlay.querySelectorAll('.overlay-filter').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.overlayFilter = btn.dataset.source;
        if (overlayInput?.value) {
          this.handleOverlaySearch(overlayInput.value);
        }
      });
    });
  }

  openSearchOverlay() {
    this.searchOverlay?.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    const input = document.getElementById('overlaySearchInput');
    input?.focus();
    
    this.trackEvent('search_overlay_opened');
  }

  closeSearchOverlay() {
    this.searchOverlay?.classList.remove('active');
    document.body.style.overflow = '';
  }

  async handleOverlaySearch(query) {
    const resultsContainer = document.getElementById('overlaySearchResults');
    
    if (query.length < 2) {
      resultsContainer.innerHTML = `
        <div class="search-overlay-empty">
          <span class="material-icons-round">travel_explore</span>
          <p>Start typing to search across ArXiv & PubMed</p>
        </div>
      `;
      return;
    }
    
    // Show skeleton loading
    resultsContainer.innerHTML = this.generateSkeletonLoader(5);
    
    const filter = this.overlayFilter || 'all';
    const options = { maxResults: 10, limit: 10 };
    
    if (filter !== 'all') {
      options.filters = { source: [filter] };
    }
    
    try {
      const results = await this.semanticSearch(query, options);
      
      if (results.results.length === 0) {
        resultsContainer.innerHTML = `
          <div class="search-overlay-empty">
            <span class="material-icons-round">search_off</span>
            <p>No results found for "${this.escapeHtml(query)}"</p>
          </div>
        `;
        return;
      }
      
      resultsContainer.innerHTML = `
        <div class="overlay-results-list">
          ${results.results.map(result => `
            <div class="overlay-result-item" onclick="window.scimspt.selectResult('${result.id}', '${result.source}'); window.scimspt.closeSearchOverlay();">
              <span class="material-icons-round overlay-icon">${result.source === 'arxiv' ? 'article' : 'biotech'}</span>
              <div class="overlay-result-content">
                <h4>${this.escapeHtml(result.title)}</h4>
                <p>${result.authors.slice(0, 2).join(', ')} • ${result.published}</p>
              </div>
              <span class="overlay-arrow">→</span>
            </div>
          `).join('')}
        </div>
        <div class="overlay-footer">
          <button onclick="window.scimspt.performSearch('${query.replace(/'/g, "\\'")}'); window.scimspt.closeSearchOverlay();" class="view-all-overlay-btn">
            View all ${results.metadata.totalResults}+ results →
          </button>
        </div>
      `;
      
    } catch (error) {
      resultsContainer.innerHTML = `
        <div class="search-overlay-empty error">
          <span class="material-icons-round">error_outline</span>
          <p>Search error. Please try again.</p>
        </div>
      `;
    }
  }

  // ============================================
  // TOAST NOTIFICATION SYSTEM
  // ============================================

  createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    container.id = 'toastContainer';
    document.body.appendChild(container);
  }

  showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icons = {
      success: 'check_circle',
      error: 'error',
      warning: 'warning',
      info: 'info'
    };
    
    toast.innerHTML = `
      <span class="material-icons-round toast-icon">${icons[type] || icons.info}</span>
      <span class="toast-message">${this.escapeHtml(message)}</span>
      <button class="toast-close" onclick="this.parentElement.remove()">
        <span class="material-icons-round">close</span>
      </button>
    `;
    
    container.appendChild(toast);
    
    // Trigger animation
    requestAnimationFrame(() => {
      toast.classList.add('show');
    });
    
    // Auto-remove
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, duration);
    
    return toast;
  }

  // ============================================
  // GOOGLE ANALYTICS 4 INTEGRATION
  // ============================================

  setupAnalytics() {
    // Don't load analytics in development or if disabled
    if (localhost || !this.analyticsConfig.enabled) {
      console.log('📊 Analytics disabled in development');
      return;
    }
    
    // Load GA4 script
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${this.analyticsConfig.ga4MeasurementId}`;
    document.head.appendChild(script);
    
    // Initialize gtag
    window.dataLayer = window.dataLayer || [];
    function gtag(...args) {
      window.dataLayer.push(args);
    }
    window.gtag = gtag;
    
    gtag('js', new Date());
    gtag('config', this.analyticsConfig.ga4MeasurementId, {
      send_page_view: true,
      custom_map: {
        custom_parameter_1: 'search_query',
        custom_parameter_2: 'result_count'
      }
    });
    
    console.log('📊 Google Analytics 4 initialized');
  }

  trackEvent(eventName, parameters = {}) {
    // Send to GA4
    if (window.gtag) {
      window.gtag('event', eventName, parameters);
    }
    
    // Send to Plausible if available
    if (window.plausible) {
      window.plausible(eventName, { props: parameters });
    }
    
    // Log in development
    if (localhost) {
      console.log(`📊 Event: ${eventName}`, parameters);
    }
  }

  trackPageView(pagePath) {
    if (window.gtag) {
      window.gtag('config', this.analyticsConfig.ga4MeasurementId, {
        page_path: pagePath
      });
    }
  }

  // ============================================
  // PAGE TRANSITIONS
  // ============================================

  setupPageTransitions() {
    // Add transition class to body for entry animations only
    // NOTE: Click interception DISABLED for static sites (GitHub Pages compatibility)
    // Page transitions via AJAX break static hosting - using normal navigation instead
    document.body.classList.add('page-transitions-enabled');
    
    // Handle popstate (back/forward) - just track, don't intercept
    window.addEventListener('popstate', () => {
      this.trackPageView(window.location.pathname);
    });
    
    // Initial page view
    this.trackPageView(window.location.pathname);
    
    console.log('📄 Page transitions: Entry animations enabled (click interception disabled for static hosting)');
  }

  async transitionToPage(url) {
    // Show exit animation
    document.body.classList.add('page-exiting');
    
    this.trackEvent('page_transition_start', { destination: url });
    
    try {
      // Preload page
      const response = await fetch(url);
      const html = await response.text();
      
      // Parse new page
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      
      // Update content after exit animation completes
      setTimeout(() => {
        // Update page content
        document.documentElement.innerHTML = doc.documentElement.innerHTML;
        document.body.classList.remove('page-exiting');
        document.body.classList.add('page-entering');
        
        // Reinitialize components
        this.init();
        
        // Update URL
        window.history.pushState({}, '', url);
        
        // Remove entering class after animation
        setTimeout(() => {
          document.body.classList.remove('page-entering');
        }, 300);
        
        // Scroll to top
        window.scrollTo(0, 0);
        
      }, 300);
      
    } catch (error) {
      console.error('Page transition error:', error);
      // Fallback to normal navigation
      window.location.href = url;
    }
  }

  // ============================================
  // SCROLL ANIMATIONS (Intersection Observer)
  // ============================================

  setupScrollAnimations() {
    // Create observer for fade-in-up animations
    const fadeObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          
          // Optional: unobserve after animation
          if (entry.target.dataset.once !== 'false') {
            fadeObserver.unobserve(entry.target);
          }
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe elements with animate-on-scroll class
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    animateElements.forEach(el => fadeObserver.observe(el));
    
    // Create observer for parallax effects
    this.setupParallaxObserver();
    
    // Create observer for count-up animations
    this.setupCountUpObserver();
  }

  setupParallaxObserver() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    if (parallaxElements.length === 0) return;
    
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      
      parallaxElements.forEach(el => {
        const speed = parseFloat(el.dataset.parallax) || 0.5;
        const yPos = -(scrollY * speed);
        el.style.transform = `translateY(${yPos}px)`;
      });
    }, { passive: true });
  }

  setupCountUpObserver() {
    const countElements = document.querySelectorAll('[data-count-up]');
    
    const countObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateCountUp(entry.target);
          countObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    
    countElements.forEach(el => countObserver.observe(el));
  }

  animateCountUp(element) {
    const target = parseInt(element.dataset.countUp);
    const duration = parseInt(element.dataset.countDuration) || 2000;
    const start = 0;
    const startTime = performance.now();
    
    const updateCount = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function (ease-out)
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(start + (target - start) * eased);
      
      element.textContent = current.toLocaleString();
      
      if (progress < 1) {
        requestAnimationFrame(updateCount);
      }
    };
    
    requestAnimationFrame(updateCount);
  }

  // ============================================
  // SKELETON LOADING STATES
  // ============================================

  generateSkeletonLoader(count = 3) {
    return Array(count).fill(0).map((_, i) => `
      <div class="skeleton-card" style="--delay: ${i * 0.1}s">
        <div class="skeleton-line skeleton-title"></div>
        <div class="skeleton-line skeleton-text"></div>
        <div class="skeleton-line skeleton-text short"></div>
        <div class="skeleton-tags">
          <div class="skeleton-tag"></div>
          <div class="skeleton-tag"></div>
        </div>
      </div>
    `).join('');
  }

  showSkeletonLoader(container, count = 3) {
    container.innerHTML = this.generateSkeletonLoader(count);
  }

  showSearchLoading() {
    const btn = document.querySelector('.search-btn');
    if (btn) {
      btn.classList.add('loading');
      btn.disabled = true;
      btn.innerHTML = '<div class="spinner"></div>';
    }
  }

  hideSearchLoading() {
    const btn = document.querySelector('.search-btn');
    if (btn) {
      btn.classList.remove('loading');
      btn.disabled = false;
      btn.innerHTML = '<span class="material-icons-round">search</span> AI Search';
    }
  }

  // ============================================
  // PERFORMANCE MONITORING
  // ============================================

  observePerformance() {
    // Log Core Web Vitals
    if ('PerformanceObserver' in window) {
      // Largest Contentful Paint
      try {
        const lcpObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          console.log(`📈 LCP: ${lastEntry.startTime.toFixed(0)}ms`);
          this.trackEvent('web_vital_lcp', { value: Math.round(lastEntry.startTime) });
        });
        lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true });
      } catch (e) {}
      
      // First Input Delay
      try {
        const fidObserver = new PerformanceObserver((list) => {
          const entry = list.getEntries()[0];
          console.log(`📈 FID: ${entry.processingStart - entry.startTime.toFixed(0)}ms`);
          this.trackEvent('web_vital_fid', { value: Math.round(entry.processingStart - entry.startTime) });
        });
        fidObserver.observe({ type: 'first-input', buffered: true });
      } catch (e) {}
      
      // Cumulative Layout Shift
      try {
        const clsObserver = new PerformanceObserver((list) => {
          let clsValue = 0;
          list.getEntries().forEach(entry => {
            clsValue += entry.value;
          });
          console.log(`📈 CLS: ${clsValue.toFixed(3)}`);
          this.trackEvent('web_vital_cls', { value: clsValue.toFixed(3) });
        });
        clsObserver.observe({ type: 'layout-shift', buffered: true });
      } catch (e) {}
    }
  }

  // ============================================
  // UTILITY FUNCTIONS
  // ============================================

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  showSuggestions() {
    this.searchSuggestions?.classList.add('visible');
  }

  hideSuggestions() {
    this.searchSuggestions?.classList.remove('visible');
  }

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  throttle(func, limit) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }
}

// ============================================
// GLOBAL INITIALIZATION
// ============================================

// Detect localhost for development mode
const localhost = location.hostname === 'localhost' || 
                  location.hostname === '127.0.0.1' ||
                  location.hostname === '';

// Initialize when DOM is ready
let scimspt;
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
