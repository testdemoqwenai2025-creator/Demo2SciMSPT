/**
 * SciMSPT Performance Optimizer v1.0
 * ===================================
 * Comprehensive performance utilities:
 * - Image lazy loading with intersection observer
 * - Font loading optimization
 * - Resource preloading hints
 * - Performance monitoring
 * - Background sync manager
 */

class SciMSPTPerformance {
  constructor() {
    this.observers = [];
    this.metrics = {};
    this.init();
  }

  init() {
    // Run optimizations when DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setupOptimizations());
    } else {
      this.setupOptimizations();
    }
  }

  setupOptimizations() {
    this.setupImageLazyLoading();
    this.setupFontPreloading();
    this.setupResourceHints();
    this.startPerformanceMonitoring();
    this.setupBackgroundSync();
    
    console.log('⚡ SciMSPT Performance Optimizer initialized');
  }

  // ============================================
  // IMAGE LAZY LOADING
  // ============================================

  setupImageLazyLoading() {
    // Use native lazy loading where supported, fallback to IntersectionObserver
    const images = document.querySelectorAll('img[data-src], img[loading="lazy"]');
    
    if ('loading' in HTMLImageElement.prototype) {
      // Native lazy loading supported
      images.forEach(img => {
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
        }
      });
    } else {
      // Fallback: Intersection Observer
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            
            if (img.dataset.src) {
              img.src = img.dataset.src;
              img.removeAttribute('data-src');
            }
            
            img.classList.add('loaded');
            observer.unobserve(img);
          }
        });
      }, {
        rootMargin: '200px 0px', // Start loading before visible
        threshold: 0.01
      });

      images.forEach(img => imageObserver.observe(img));
      this.observers.push(imageObserver);
    }

    // Background image lazy loading
    const bgImages = document.querySelectorAll('[data-bg-src]');
    const bgObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          el.style.backgroundImage = `url(${el.dataset.bgSrc})`;
          el.removeAttribute('data-bg-src');
          observer.unobserve(el);
        }
      });
    }, { rootMargin: '100px' });

    bgImages.forEach(el => bgObserver.observe(el));
    this.observers.push(bgObserver);
  }

  // ============================================
  // FONT OPTIMIZATION
  // ============================================

  setupFontPreloading() {
    // Critical fonts to preload
    const criticalFonts = [
      { url: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap', type: 'style' },
      { url: 'https://fonts.googleapis.com/icon?family=Material+Icons+Round', type: 'style' }
    ];

    // Add preload links for fonts
    criticalFonts.forEach(font => {
      if (!document.querySelector(`link[href="${font.url}"]`)) {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = font.type === 'style' ? 'style' : 'font';
        if (font.type === 'font') link.crossOrigin = 'anonymous';
        link.href = font.url;
        
        // Insert before first stylesheet
        const firstStyle = document.querySelector('link[rel="stylesheet"]');
        if (firstStyle) {
          firstStyle.parentNode.insertBefore(link, firstStyle);
        } else {
          document.head.appendChild(link);
        }
      }
    });

    // Optimize existing font loads with font-display: swap
    this.optimizeFontDisplay();
  }

  optimizeFontDisplay() {
    // Inject CSS for font-display: swap on Google Fonts
    const style = document.createElement('style');
    style.textContent = `
      @font-face {
        font-family: 'Inter';
        font-display: swap;
      }
      @font-face {
        font-family: 'Playfair Display';
        font-display: swap;
      }
      @font-face {
        font-family: 'JetBrains Mono';
        font-display: swap;
      }
      @font-face {
        font-family: 'Orbitron';
        font-display: swap;
      }
      @font-face {
        font-family: 'Material Icons Round';
        font-display: swap;
      }
      
      /* Critical font loading optimization */
      body {
        /* Prevent invisible text during font load */
        font-display: swap;
      }
    `;
    document.head.appendChild(style);
  }

  // ============================================
  // RESOURCE HINTS
  // ============================================

  setupResourceHints() {
    // DNS prefetch for external domains
    const domains = [
      'fonts.googleapis.com',
      'fonts.gstatic.com',
      'www.googletagmanager.com',
      'analytics.us.umami.is',
      'export.arxiv.org',
      'eutils.ncbi.nlm.nih.gov'
    ];

    domains.forEach(domain => {
      if (!document.querySelector(`link[rel="dns-prefetch"][href*="${domain}"]`)) {
        const link = document.createElement('link');
        link.rel = 'dns-prefetch';
        link.href = `//${domain}`;
        document.head.appendChild(link);
      }

      // Preconnect for critical domains
      if (['fonts.googleapis.com', 'fonts.gstatic.com'].includes(domain)) {
        if (!document.querySelector(`link[rel="preconnect"][href*="${domain}"]`)) {
          const link = document.createElement('link');
          link.rel = 'preconnect';
          link.href = `https://${domain}`;
          if (domain === 'fonts.gstatic.com') link.crossOrigin = 'anonymous';
          document.head.appendChild(link);
        }
      }
    });
  }

  // ============================================
  // PERFORMANCE MONITORING
  // ============================================

  startPerformanceMonitoring() {
    // Wait for page to fully load
    window.addEventListener('load', () => {
      setTimeout(() => this.collectMetrics(), 0);
    });
  }

  collectMetrics() {
    const navigation = performance.getEntriesByType('navigation')[0];
    const paint = performance.getEntriesByType('paint');
    
    this.metrics = {
      // Core Web Vitals
      fcp: this.getMetric(paint, 'first-contentful-paint'),
      lcp: this.getLCP(),
      fid: this.getFID(),
      cls: this.getCLS(),
      
      // Navigation timing
      domContentLoaded: navigation?.domContentLoadedEventEnd - navigation?.startTime,
      loadComplete: navigation?.loadEventEnd - navigation?.startTime,
      domInteractive: navigation?.domInteractive - navigation?.startTime,
      
      // Resource counts
      resourceCount: performance.getEntriesByType('resource').length,
      
      // Cache status
      isOffline: !navigator.onLine,
      serviceWorkerReady: !!navigator.serviceWorker?.controller
    };

    // Log metrics for debugging
    console.table(this.metrics);

    // Send to analytics if available
    this.reportMetrics();

    // Store for later analysis
    localStorage.setItem('scimspt_perf_metrics', JSON.stringify({
      ...this.metrics,
      timestamp: Date.now(),
      url: window.location.pathname
    }));
  }

  getMetric(entries, name) {
    const entry = entries.find(e => e.name === name);
    return entry ? Math.round(entry.startTime) : null;
  }

  getLCP() {
    return new Promise(resolve => {
      new PerformanceObserver(list => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        resolve(Math.round(lastEntry.startTime));
      }).observe({ type: 'largest-contentful-paint', buffered: true });
    });
  }

  getFID() {
    return new Promise(resolve => {
      new PerformanceObserver(list => {
        const entry = list.getEntries()[0];
        resolve(entry ? Math.round(entry.processingStart - entry.startTime) : null);
      }).observe({ type: 'first-input', buffered: true });
      });
  }

  getCLS() {
    let clsValue = 0;
    new PerformanceObserver(list => {
      list.getEntries().forEach(entry => {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
        }
      });
    }).observe({ type: 'layout-shift', buffered: true });
    return clsValue.toFixed(3);
  }

  reportMetrics() {
    // Send to GA4 if available
    if (typeof gtag === 'function') {
      gtag('event', 'web_vitals', {
        fcp: this.metrics.fcp,
        lcp: this.metrics.lcp,
        fid: this.metrics.fid,
        cls: this.metrics.cls
      });
    }

    // Send custom event
    window.dispatchEvent(new CustomEvent('scimspt:metrics', { detail: this.metrics }));
  }

  // ============================================
  // BACKGROUND SYNC MANAGER
  // ============================================

  setupBackgroundSync() {
    // Register sync events when service worker is ready
    if ('serviceWorker' in navigator && 'sync' in registration) {
      navigator.serviceWorker.ready.then(registration => {
        this.syncManager = registration.sync;
      });
    }
  }

  async queueSync(tag) {
    try {
      if (this.syncManager) {
        await this.syncManager.register(tag);
        return true;
      }
    } catch (error) {
      console.warn('Background sync not available:', error);
    }
    return false;
  }

  async saveForLater(key, data) {
    // Save data to IndexedDB for later sync
    try {
      const db = await this.openSyncDB();
      const tx = db.transaction(['pending'], 'readwrite');
      const store = tx.objectStore('pending');
      await store.put({ key, data, timestamp: Date.now() });
      return true;
    } catch (error) {
      console.error('Failed to save for later:', error);
      return false;
    }
  }

  openSyncDB() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('SciMSPTSyncDB', 1);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
      
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('pending')) {
          db.createObjectStore('pending', { keyPath: 'key' });
        }
      };
    });
  }

  // ============================================
  // UTILITY FUNCTIONS
  // ============================================

  // Preload a specific URL
  preload(url, as = 'fetch') {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = as;
    link.href = url;
    document.head.appendChild(link);
  }

  // Prefetch a page for likely navigation
  prefetch(url) {
    const link = document.createElement('link');
    link.rel = 'prefetch';
    link.href = url;
    document.head.appendChild(link);
  }

  // Check if user prefers reduced motion
  prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  // Check connection speed
  getConnectionInfo() {
    const connection = navigator.connection || 
                       navigator.mozConnection || 
                       navigator.webkitConnection;
    
    if (!connection) return null;
    
    return {
      effectiveType: connection.effectiveType,
      downlink: connection.downlink,
      rtt: connection.rtt,
      saveData: connection.saveData
    };
  }

  // Optimize based on connection
  adaptToConnection() {
    const conn = this.getConnectionInfo();
    
    if (!conn) return;

    // Reduce image quality on slow connections
    if (conn.saveData || ['slow-2g', '2g'].includes(conn.effectiveType)) {
      document.documentElement.setAttribute('data-connection', 'slow');
      this.disableHeavyFeatures();
    } else if (['3g'].includes(conn.effectiveType)) {
      document.documentElement.setAttribute('data-connection', 'medium');
    } else {
      document.documentElement.setAttribute('data-connection', 'fast');
    }
  }

  disableHeavyFeatures() {
    // Disable animations
    document.documentElement.style.setProperty('--animation-duration', '0s');
    
    // Lower image quality
    document.querySelectorAll('img').forEach(img => {
      if (img.src.includes('?')) {
        img.src += '&quality=low';
      }
    });
    
    // Hide decorative elements
    document.querySelectorAll('.decorative, .parallax-bg').forEach(el => {
      el.style.display = 'none';
    });
  }

  // Cleanup observers when no longer needed
  destroy() {
    this.observers.forEach(observer => observer.disconnect());
    this.observers = [];
  }
}

// Initialize performance optimizer
window.scimsptPerf = new SciMSPTPerformance();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SciMSPTPerformance;
}
