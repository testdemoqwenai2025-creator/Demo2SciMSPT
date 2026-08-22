/**
 * SciMSPT Global Search System v2.0
 * =====================================
 * Features:
 * - ArXiv API Integration
 * - PubMed/NCBI API Integration  
 * - Semantic Search with NLP
 * - Search History (localStorage)
 * - Keyboard Shortcuts (Ctrl+K / Cmd+K)
 * - Inline Results Dropdown
 * - Autocomplete with Real-time Suggestions
 * - Search Filters & Facets
 * - Toast Notifications
 */

class SciMSPTSearchSystem {
  constructor() {
    this.searchInput = null;
    this.searchWrapper = null;
    this.searchSuggestions = null;
    this.searchHistory = [];
    this.isSearching = false;
    this.debounceTimer = null;
    this.apiEndpoints = {
      arxiv: 'http://export.arxiv.org/api/query?search_query=all:',
      pubmed: 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=',
      pubmedFetch: 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=json&id='
    };
    
    this.init();
  }

  init() {
    this.loadSearchHistory();
    this.setupGlobalSearchListener();
    this.setupKeyboardShortcuts();
    this.createSearchOverlay();
    this.createToastContainer();
    console.log('🔍 SciMSPT Search System initialized');
  }

  // ============================================
  // SEARCH HISTORY MANAGEMENT
  // ============================================

  loadSearchHistory() {
    try {
      const saved = localStorage.getItem('scimspt-search-history');
      this.searchHistory = saved ? JSON.parse(saved) : [];
    } catch (e) {
      this.searchHistory = [];
    }
  }

  saveSearchHistory(query) {
    if (!query || query.trim().length < 2) return;
    
    // Remove if already exists (move to top)
    this.searchHistory = this.searchHistory.filter(h => h !== query);
    
    // Add to beginning
    this.searchHistory.unshift(query.trim());
    
    // Keep only last 20 searches
    this.searchHistory = this.searchHistory.slice(0, 20);
    
    // Save to localStorage
    try {
      localStorage.setItem('scimspt-search-history', JSON.stringify(this.searchHistory));
    } catch (e) {
      console.warn('Could not save search history:', e);
    }
  }

  getRecentSearches(limit = 5) {
    return this.searchHistory.slice(0, limit);
  }

  clearSearchHistory() {
    this.searchHistory = [];
    localStorage.removeItem('scimspt-search-history');
    this.showToast('Search history cleared', 'info');
  }

  // ============================================
  // ARXIV API INTEGRATION
  // ============================================

  async searchArXiv(query, maxResults = 10) {
    try {
      const encodedQuery = encodeURIComponent(query);
      const url = `${this.apiEndpoints.arxiv}${encodedQuery}&start=0&max_results=${maxResults}`;
      
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
        const authors = Array.from(entry.getElementsByTagName('author')).map(a => 
          a.getElementsByTagName('name')[0]?.textContent || ''
        );
        
        // Extract categories
        const categories = Array.from(entry.getElementsByTagName('category')).map(c => 
          c.getAttribute('term') || ''
        );
        
        results.push({
          id: id.split('/').pop(),
          title: title.replace(/\n/g, ' ').trim(),
          summary: summary.replace(/\n/g, ' ').trim().substring(0, 300) + '...',
          authors,
          published: new Date(published).toLocaleDateString(),
          categories,
          source: 'arxiv',
          url: id,
          type: 'paper'
        });
      }
      
      return { success: true, results, source: 'ArXiv', total: results.length };
      
    } catch (error) {
      console.error('ArXiv search error:', error);
      return { success: false, error: error.message, results: [] };
    }
  }

  // ============================================
  // PUBMED API INTEGRATION
  // ============================================

  async searchPubMed(query, maxResults = 10) {
    try {
      const encodedQuery = encodeURIComponent(query);
      const searchUrl = `${this.apiEndpoints.pubmed}${encodedQuery}&retmax=${maxResults}&retmode=json`;
      
      const searchResponse = await fetch(searchUrl);
      const searchData = await searchResponse.json();
      
      const ids = searchData.esearchresult?.idlist || [];
      
      if (ids.length === 0) {
        return { success: true, results: [], source: 'PubMed', total: 0 };
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
          summary: (article.abstract || '').substring(0, 300) + '...',
          authors: article.authors?.map(a => a.name) || [],
          published: article.pubdate || '',
          categories: [article.source || 'Journal Article'],
          source: 'pubmed',
          url: `https://pubmed.ncbi.nlm.nih.gov/${article.pmid}/`,
          type: 'paper'
        };
      });
      
      return { success: true, results, source: 'PubMed', total: parseInt(searchData.esearchresult?.count || 0) };
      
    } catch (error) {
      console.error('PubMed search error:', error);
      return { success: false, error: error.message, results: [] };
    }
  }

  // ============================================
  // SEMANTIC SEARCH (NLP-Enhanced)
  // ============================================

  async semanticSearch(query) {
    // Enhance query with NLP techniques
    const enhancedQuery = this.enhanceQueryWithNLP(query);
    
    // Search multiple sources in parallel
    const [arxivResults, pubmedResults] = await Promise.allSettled([
      this.searchArXiv(enhancedQuery),
      this.searchPubMed(enhancedQuery)
    ]);
    
    const results = {
      arxiv: arxivResults.status === 'fulfilled' ? arxivResults.value : { results: [] },
      pubmed: pubmedResults.status === 'fulfilled' ? pubmedResults.value : { results: [] },
      allPapers: [],
      suggestions: this.generateSemanticSuggestions(query)
    };
    
    // Combine and rank results
    if (results.arxiv.results) results.allPapers.push(...results.arxiv.results);
    if (results.pubmed.results) results.allPapers.push(...results.pubmed.results);
    
    // Apply relevance ranking
    results.allPapers = this.rankByRelevance(results.allPapers, query);
    
    return results;
  }

  enhanceQueryWithNLP(query) {
    let enhanced = query.toLowerCase().trim();
    
    // Expand common abbreviations
    const expansions = {
      'ai': 'artificial intelligence machine learning',
      'ml': 'machine learning',
      'dl': 'deep learning neural network',
      'nlp': 'natural language processing',
      'cv': 'computer vision image recognition',
      'quantum': 'quantum computing qubit superposition entanglement',
      'genomics': 'genomics dna sequencing bioinformatics',
      'fusion': 'nuclear fusion plasma energy tokamak stellarator'
    };
    
    Object.keys(expansions).forEach(abbr => {
      const regex = new RegExp(`\\b${abbr}\\b`, 'gi');
      if (regex.test(enhanced)) {
        enhanced = enhanced.replace(regex, expansions[abbr]);
      }
    });
    
    // Remove stop words for better matching
    const stopWords = ['the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or'];
    enhanced.split(' ').filter(word => !stopWords.includes(word)).join(' ');
    
    return enhanced;
  }

  generateSemanticSuggestions(query) {
    const suggestions = [
      { text: `${query} research papers`, category: 'Papers' },
      { text: `${query} applications`, category: 'Applications' },
      { text: `${query} breakthrough 2024 2025`, category: 'Recent' },
      { text: `${query} review survey`, category: 'Reviews' },
      { text: `${query} methodology`, category: 'Methods' }
    ];
    
    return suggestions.slice(0, 4);
  }

  rankByRelevance(papers, query) {
    const queryTerms = query.toLowerCase().split(' ');
    
    return papers.map(paper => {
      let score = 0;
      const titleLower = (paper.title || '').toLowerCase();
      const summaryLower = (paper.summary || '').toLowerCase();
      
      // Title matches are worth more
      queryTerms.forEach(term => {
        if (titleLower.includes(term)) score += 10;
        if (summaryLower.includes(term)) score += 3;
      });
      
      // Recent papers get bonus
      if (paper.published && paper.published.includes('2024') || paper.published?.includes('2025')) {
        score += 5;
      }
      
      // Category relevance
      const relevantCategories = ['cs.AI', 'quant-ph', 'stat.ML', 'physics'];
      if (paper.categories?.some(cat => relevantCategories.some(rel => cat.includes(rel)))) {
        score += 2;
      }
      
      return { ...paper, relevanceScore: score };
    }).sort((a, b) => b.relevanceScore - a.relevanceScore);
  }

  // ============================================
  // GLOBAL SEARCH UI COMPONENTS
  // ============================================

  setupGlobalSearchListener() {
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.attachSearchEvents());
    } else {
      this.attachSearchEvents();
    }
  }

  attachSearchEvents() {
    // Find all search inputs on page
    this.searchInputs = document.querySelectorAll('.search-input');
    this.searchWrappers = document.querySelectorAll('.search-wrapper');
    
    this.searchInputs.forEach(input => {
      input.addEventListener('input', (e) => this.handleInputChange(e));
      input.addEventListener('keydown', (e) => this.handleKeyDown(e));
      input.addEventListener('focus', () => this.showSuggestions());
    });
    
    // Close suggestions on outside click
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.search-wrapper')) {
        this.hideAllSuggestions();
      }
    });
  }

  handleInputChange(e) {
    const query = e.target.value;
    
    // Debounce API calls
    clearTimeout(this.debounceTimer);
    
    if (query.length < 2) {
      this.showDefaultSuggestions(e.target);
      return;
    }
    
    this.debounceTimer = setTimeout(async () => {
      await this.performLiveSearch(query);
    }, 300);
  }

  handleKeyDown(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      this.executeFullSearch(e.target.value);
    } else if (e.key === 'Escape') {
      this.hideAllSuggestions();
      e.target.blur();
    } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      this.navigateSuggestions(e.key === 'ArrowDown' ? 1 : -1);
    }
  }

  async performLiveSearch(query) {
    if (!query || query.length < 2) return;
    
    const activeWrapper = document.querySelector('.search-wrapper:focus-within');
    const activeSuggestions = activeWrapper?.querySelector('.search-suggestions');
    
    if (!activeSuggestions) return;
    
    // Show loading state
    activeSuggestions.innerHTML = `
      <div class="suggestion-loading">
        <span class="material-icons-round" style="animation: spin 1s linear infinite;">autorenew</span>
        Searching ArXiv & PubMed...
      </div>
    `;
    activeSuggestions.classList.add('active');
    
    try {
      // Quick search (limited results for dropdown)
      const [arxivResult, pubmedResult] = await Promise.all([
        this.searchArXiv(query, 3),
        this.searchPubMed(query, 3)
      ]);
      
      const papers = [
        ...(arxivResult.results || []),
        ...(pubmedResult.results || [])
      ];
      
      if (papers.length === 0) {
        activeSuggestions.innerHTML = `
          <div class="suggestion-empty">
            <span class="material-icons-round">search_off</span>
            <p>No results found for "${query}"</p>
            <button onclick="window.scimsptSearch.executeFullSearch('${query}')" class="suggestion-action">
              Try broader search
            </button>
          </div>
        `;
        return;
      }
      
      // Render results
      let html = `
        <div class="suggestion-header">
          <span>Found ${papers.length}+ results</span>
          <span style="color: var(--accent-primary); cursor: pointer;" onclick="window.scimsptSearch.executeFullSearch('${query}')">See all →</span>
        </div>
      `;
      
      papers.slice(0, 5).forEach(paper => {
        html += `
          <a href="${paper.url}" target="_blank" class="suggestion-item" onclick="window.scimsptSearch.saveSearchHistory('${query}')">
            <div class="suggestion-icon">
              <span class="material-icons-round">${paper.source === 'arxiv' ? 'description' : 'biotech'}</span>
            </div>
            <div class="suggestion-text">
              <div class="suggestion-title">${this.highlightMatch(paper.title, query)}</div>
              <div class="suggestion-desc">${paper.authors?.slice(0, 2).join(', ') || ''} • ${paper.published}</div>
            </div>
            <span class="suggestion-source ${paper.source}">${paper.source.toUpperCase()}</span>
          </a>
        `;
      });
      
      activeSuggestions.innerHTML = html;
      
    } catch (error) {
      console.error('Live search error:', error);
      activeSuggestions.innerHTML = `
        <div class="suggestion-error">
          <span class="material-icons-round">error_outline</span>
          <p>Search error. Please try again.</p>
        </div>
      `;
    }
  }

  highlightMatch(text, query) {
    if (!text || !query) return text || '';
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }

  showDefaultSuggestions(input) {
    const wrapper = input.closest('.search-wrapper');
    const suggestions = wrapper?.querySelector('.search-suggestions');
    if (!suggestions) return;
    
    const recentSearches = this.getRecentSearches(5);
    
    let html = `
      <div class="suggestion-header">
        <span>Recent Searches</span>
        ${recentSearches.length > 0 ? '<span style="color: var(--accent-primary); cursor: pointer;" onclick="window.scimsptSearch.clearSearchHistory()">Clear</span>' : ''}
      </div>
    `;
    
    if (recentSearches.length > 0) {
      recentSearches.forEach(search => {
        html += `
          <a href="#" class="suggestion-item" onclick="event.preventDefault(); window.scimsptSearch.setSearchQuery('${search}')">
            <div class="suggestion-icon">
              <span class="material-icons-round">history</span>
            </div>
            <div class="suggestion-text">
              <div class="suggestion-title">${search}</div>
              <div class="suggestion-desc">Click to search again</div>
            </div>
          </a>
        `;
      });
    } else {
      html += `
        <div class="suggestion-empty">
          <span class="material-icons-round">search</span>
          <p>No recent searches</p>
        </div>
      `;
    }
    
    // Add popular searches
    html += `
      <div class="suggestion-header" style="margin-top: 12px;">
        <span>Popular Searches</span>
      </div>
      <div class="quick-actions-inline">
        <span class="quick-chip" onclick="window.scimsptSearch.setSearchQuery('Quantum Computing')">Quantum Computing</span>
        <span class="quick-chip" onclick="window.scimsptSearch.setSearchQuery('Machine Learning')">ML/AI</span>
        <span class="quick-chip" onclick="window.scimsptSearch.setSearchQuery('Fusion Energy')">Fusion Energy</span>
        <span class="quick-chip" onclick="window.scimsptSearch.setSearchQuery('Genomics')">Genomics</span>
      </div>
    `;
    
    suggestions.innerHTML = html;
    suggestions.classList.add('active');
  }

  showSuggestions() {
    const activeInput = document.activeElement;
    if (activeInput?.classList.contains('search-input')) {
      this.showDefaultSuggestions(activeInput);
    }
  }

  hideAllSuggestions() {
    document.querySelectorAll('.search-suggestions').forEach(el => {
      el.classList.remove('active');
    });
  }

  navigateSuggestions(direction) {
    // Implementation for keyboard navigation through suggestions
    console.log('Navigate suggestions:', direction);
  }

  setSearchQuery(query) {
    const inputs = document.querySelectorAll('.search-input');
    inputs.forEach(input => {
      input.value = query;
      input.focus();
    });
    this.executeFullSearch(query);
  }

  executeFullSearch(query) {
    if (!query || !query.trim()) {
      this.showToast('Please enter a search term', 'warning');
      return;
    }
    
    this.saveSearchHistory(query);
    this.hideAllSuggestions();
    
    // Show loading state
    this.showToast('Searching databases...', 'info');
    
    // Navigate to search results page or show inline results
    const searchUrl = `search-results.html?q=${encodeURIComponent(query)}`;
    
    // Check if we're on the same page
    if (window.location.pathname.includes('search-results')) {
      this.loadSearchResults(query);
    } else {
      // Smooth transition to results
      document.body.classList.add('page-transitioning');
      setTimeout(() => {
        window.location.href = searchUrl;
      }, 300);
    }
  }

  async loadSearchResults(query) {
    const resultsContainer = document.getElementById('searchResultsContainer');
    if (!resultsContainer) return;
    
    // Show skeleton loading
    resultsContainer.innerHTML = this.generateSkeletonLoader(8);
    
    // Perform comprehensive search
    const results = await this.semanticSearch(query);
    
    // Render results
    setTimeout(() => {
      this.renderSearchResults(results, query);
    }, 800); // Simulate network delay for smooth UX
  }

  renderSearchResults(results, query) {
    const container = document.getElementById('searchResultsContainer');
    if (!container) return;
    
    if (results.allPapers.length === 0) {
      container.innerHTML = `
        <div class="no-results">
          <span class="material-icons-round">search_off</span>
          <h3>No results found for "${query}"</h3>
          <p>Try different keywords or check your spelling</p>
          <div class="suggestions-alt">
            <h4>Suggestions:</h4>
            <ul>
              ${results.suggestions.map(s => `<li><a href="#" onclick="window.scimsptSearch.setSearchQuery('${s.text}')">${s.text}</a></li>`).join('')}
            </ul>
          </div>
        </div>
      `;
      return;
    }
    
    let html = `
      <div class="results-header">
        <h2>Search Results for "${query}"</h2>
        <div class="results-meta">
          <span>${results.allPapers.length} papers found</span>
          <span>•</span>
          <span>${results.arxiv.results?.length || 0} from ArXiv</span>
          <span>•</span>
          <span>${results.pubmed.results?.length || 0} from PubMed</span>
        </div>
      </div>
      
      <div class="filters-sidebar">
        <h3>Filters</h3>
        <div class="filter-group">
          <h4>Source</h4>
          <label><input type="checkbox" checked> ArXiv (${results.arxiv.results?.length || 0})</label>
          <label><input type="checkbox" checked> PubMed (${results.pubmed.results?.length || 0})</label>
        </div>
        <div class="filter-group">
          <h4>Date Range</h4>
          <label><input type="radio" name="date" checked> Any time</label>
          <label><input type="radio" name="date"> Past year</label>
          <label><input type="radio" name="date"> Past month</label>
        </div>
      </div>
      
      <div class="results-list">
    `;
    
    results.allPapers.forEach((paper, index) => {
      html += `
        <article class="result-card" style="animation-delay: ${index * 0.1}s">
          <div class="result-source ${paper.source}">
            <span class="material-icons-round">${paper.source === 'arxiv' ? 'description' : 'biotech'}</span>
            ${paper.source.toUpperCase()}
          </div>
          <h3 class="result-title">
            <a href="${paper.url}" target="_blank" rel="noopener">${paper.title}</a>
          </h3>
          <p class="result-authors">${paper.authors?.join(', ') || 'Unknown Authors'}</p>
          <p class="result-summary">${paper.summary}</p>
          <div class="result-meta">
            <span class="result-date">${paper.published}</span>
            <span class="result-categories">${paper.categories?.slice(0, 3).join(' • ') || ''}</span>
            <span class="relevance-score">Relevance: ${paper.relevanceScore || 'N/A'}</span>
          </div>
          <div class="result-actions">
            <button class="btn-icon" title="Save to library" onclick="window.scimsptSearch.savePaper('${paper.id}')">
              <span class="material-icons-round">bookmark_border</span>
            </button>
            <button class="btn-icon" title="Cite this paper" onclick="window.scimsptSearch.citePaper('${paper.id}')">
              <span class="material-icons-round">format_quote</span>
            </button>
            <button class="btn-icon" title="Share" onclick="window.scimsptSearch.sharePaper('${paper.url}')">
              <span class="material-icons-round">share</span>
            </button>
          </div>
        </article>
      `;
    });
    
    html += '</div>';
    
    container.innerHTML = html;
    
    // Trigger animations
    container.querySelectorAll('.result-card').forEach(card => {
      card.classList.add('animate-in');
    });
  }

  generateSkeletonLoader(count) {
    let html = '<div class="skeleton-grid">';
    for (let i = 0; i < count; i++) {
      html += `
        <div class="skeleton-card">
          <div class="skeleton-line short"></div>
          <div class="skeleton-line long"></div>
          <div class="skeleton-line medium"></div>
          <div class="skeleton-lines">
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line short"></div>
          </div>
        </div>
      `;
    }
    html += '</div>';
    return html;
  }

  // ============================================
  // KEYBOARD SHORTCUTS
  // ============================================

  setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ctrl+K / Cmd+K - Open search
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.openGlobalSearch();
      }
      
      // Escape - Close search overlay
      if (e.key === 'Escape' && this.isOverlayOpen()) {
        this.closeGlobalSearch();
      }
    });
  }

  openGlobalSearch() {
    const overlay = document.getElementById('globalSearchOverlay');
    if (overlay) {
      overlay.classList.add('active');
      const input = overlay.querySelector('.global-search-input');
      if (input) {
        setTimeout(() => input.focus(), 100);
      }
      document.body.style.overflow = 'hidden';
    }
  }

  closeGlobalSearch() {
    const overlay = document.getElementById('globalSearchOverlay');
    if (overlay) {
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  isOverlayOpen() {
    const overlay = document.getElementById('globalSearchOverlay');
    return overlay?.classList.contains('active');
  }

  createSearchOverlay() {
    // Check if overlay already exists
    if (document.getElementById('globalSearchOverlay')) return;
    
    const overlay = document.createElement('div');
    overlay.id = 'globalSearchOverlay';
    overlay.className = 'global-search-overlay';
    overlay.innerHTML = `
      <div class="global-search-modal" onclick="event.stopPropagation()">
        <div class="global-search-header">
          <span class="material-icons-round">search</span>
          <input 
            type="text" 
            class="global-search-input search-input" 
            placeholder="Search ArXiv, PubMed, papers, topics..."
            autocomplete="off"
          >
          <kbd>ESC</kbd>
        </div>
        <div class="global-search-body">
          <div class="search-suggestions global-suggestions">
            <!-- Populated dynamically -->
          </div>
        </div>
        <div class="global-search-footer">
          <span>Powered by ArXiv & PubMed APIs</span>
          <div class="shortcuts-hint">
            <kbd>↑↓</kbd> Navigate
            <kbd>↵</kbd> Select
            <kbd>ESC</kbd> Close
          </div>
        </div>
      </div>
    `;
    
    // Click outside to close
    overlay.addEventListener('click', () => this.closeGlobalSearch());
    
    document.body.appendChild(overlay);
    
    // Attach events to global search input
    const globalInput = overlay.querySelector('.global-search-input');
    if (globalInput) {
      globalInput.addEventListener('input', (e) => this.handleInputChange(e));
      globalInput.addEventListener('keydown', (e) => this.handleKeyDown(e));
      globalInput.addEventListener('focus', () => this.showDefaultSuggestions(globalInput));
    }
  }

  // ============================================
  // TOAST NOTIFICATION SYSTEM
  // ============================================

  createToastContainer() {
    if (document.getElementById('toastContainer')) return;
    
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
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
      <span class="toast-message">${message}</span>
      <button class="toast-close" onclick="this.parentElement.remove()">
        <span class="material-icons-round">close</span>
      </button>
    `;
    
    container.appendChild(toast);
    
    // Trigger animation
    requestAnimationFrame(() => toast.classList.add('show'));
    
    // Auto-remove
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  // ============================================
  // PAPER ACTIONS
  // ============================================

  savePaper(paperId) {
    // Get saved papers from localStorage
    let savedPapers = JSON.parse(localStorage.getItem('scimspt-saved-papers') || '[]');
    
    if (!savedPapers.includes(paperId)) {
      savedPapers.push(paperId);
      localStorage.setItem('scimspt-saved-papers', JSON.stringify(savedPapers));
      this.showToast('Paper saved to library', 'success');
    } else {
      this.showToast('Already in library', 'info');
    }
  }

  citePaper(paperId) {
    // Generate citation (simplified)
    const citation = `[${paperId}] SciMSPT Citation`;
    navigator.clipboard.writeText(citation).then(() => {
      this.showToast('Citation copied to clipboard', 'success');
    }).catch(() => {
      this.showToast('Failed to copy citation', 'error');
    });
  }

  sharePaper(url) {
    if (navigator.share) {
      navigator.share({
        title: 'Check out this paper',
        url: url
      }).catch(() => {});
    } else {
      navigator.clipboard.writeText(url).then(() => {
        this.showToast('Link copied to clipboard', 'success');
      }).catch(() => {
        this.showToast('Failed to copy link', 'error');
      });
    }
  }
}

// Initialize global search system
window.scimsptSearch = new SciMSPTSearchSystem();

// Expose global functions for inline handlers
window.toggleTheme = function() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  html.setAttribute('data-theme', newTheme);
  localStorage.setItem('scimspt-theme', newTheme);
  
  const themeIcon = document.getElementById('themeIcon');
  if (themeIcon) {
    themeIcon.style.transform = 'rotate(360deg) scale(0)';
    setTimeout(() => {
      themeIcon.textContent = newTheme === 'dark' ? 'dark_mode' : 'light_mode';
      themeIcon.style.transform = 'rotate(0deg) scale(1)';
    }, 200);
  }
};

// Initialize theme from localStorage
(function() {
  const savedTheme = localStorage.getItem('scimspt-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  
  const updateIcons = () => {
    document.querySelectorAll('#themeIcon').forEach(icon => {
      icon.textContent = savedTheme === 'dark' ? 'dark_mode' : 'light_mode';
    });
  };
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateIcons);
  } else {
    updateIcons();
  }
})();

console.log('🚀 SciMSPT Global Components Loaded');
