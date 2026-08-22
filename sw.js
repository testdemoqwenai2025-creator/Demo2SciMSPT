/**
 * SciMSPT Service Worker v2.0
 * ===========================
 * Advanced caching strategy for GitHub Pages
 * 
 * Strategies:
 * - Cache First: Static assets (CSS, JS, fonts, images)
 * - Network First: API calls (ArXiv, PubMed)
 * - Stale While Revalidate: HTML pages
 * - Offline Fallback: Custom offline page
 */

const CACHE_VERSION = 'v2.0.0';
const STATIC_CACHE = `scimspt-static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `scimspt-dynamic-${CACHE_VERSION}`;
const API_CACHE = `scimspt-api-${CACHE_VERSION}`;

// Cache TTL (in seconds)
const CACHE_TTL = {
  static: 30 * 24 * 60 * 30,    // 30 days for static assets
  dynamic: 24 * 60 * 60,        // 1 day for pages
  api: 5 * 60                    // 5 minutes for API responses
};

// Files to cache immediately on install
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/offline.html',
  '/css/critical.css',
  '/css/design-system.css',
  '/css/global-components.css',
  '/js/global-components.js',
  '/manifest.json'
];

// API endpoints to cache with network-first strategy
const API_PATTERNS = [
  /export\.arxiv\.org/,
  /eutils\.ncbi\.nlm\.nih\.gov/,
  /api\//
];

// Static asset patterns (cache-first)
const STATIC_PATTERNS = [
  /\.css$/,
  /\.js$/,
  /\.woff2?$/,
  /\.ttf$/,
  /\.otf$/,
  /\.svg$/,
  /\.png$/,
  /\.jpg$/,
  /\.jpeg$/,
  /\.webp$/,
  /\.gif$/,
  /\.ico$/
];

// ============================================
// INSTALL EVENT
// ============================================

self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...', CACHE_VERSION);
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('[SW] Pre-caching static assets');
        return cache.addAll(PRECACHE_URLS).catch(err => {
          console.warn('[SW] Some assets failed to precache:', err);
          // Continue even if some fail (GitHub Pages might not have all)
          return Promise.resolve();
        });
      })
      .then(() => self.skipWaiting())
  );
});

// ============================================
// ACTIVATE EVENT
// ============================================

self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...', CACHE_VERSION);
  
  event.waitUntil(
    caches.keys()
      .then(keys => {
        return Promise.all(
          keys
            .filter(key => key.startsWith('scimspt-') && !key.includes(CACHE_VERSION))
            .map(key => {
              console.log('[SW] Deleting old cache:', key);
              return caches.delete(key);
            })
        );
      })
      .then(() => self.clients.claim())
  );
});

// ============================================
// FETCH EVENT (Main caching logic)
// ============================================

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') return;
  
  // Skip chrome-extension and other non-http requests
  if (!url.protocol.startsWith('http')) return;
  
  // Determine strategy based on request type
  if (isAPIRequest(url)) {
    event.respondWith(networkFirst(request, API_CACHE));
  } else if (isStaticAsset(url.pathname)) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
  } else if (isHTMLRequest(url)) {
    event.respondWith(staleWhileRevalidate(request, DYNAMIC_CACHE));
  } else {
    // Default: network first, fallback to cache
    event.respondWith(networkFirst(request, DYNAMIC_CACHE));
  }
});

// ============================================
// CACHING STRATEGIES
// ============================================

/**
 * Cache First Strategy
 * Best for: Static assets that rarely change
 */
async function cacheFirst(request, cacheName) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    // Check if cache is still valid
    if (!isCacheExpired(cachedResponse, CACHE_TTL.static)) {
      return cachedResponse;
    }
  }
  
  try {
    const networkResponse = await fetch(request);
    
    // Only cache successful responses
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    // Return cached version even if expired when offline
    return cachedResponse || getOfflineFallback();
  }
}

/**
 * Network First Strategy
 * Best for: API calls, dynamic content
 */
async function networkFirst(request, cacheName) {
  const cachedResponse = await caches.match(request);
  
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    // Return cached response or error fallback
    return cachedResponse || getOfflineFallback();
  }
}

/**
 * Stale While Revalidate Strategy
 * Best for: HTML pages, resources that update occasionally
 */
async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cachedResponse = await cache.match(request);
  
  // Fetch in background to update cache
  const fetchPromise = fetch(request)
    .then(networkResponse => {
      if (networkResponse.ok) {
        cache.put(request, networkResponse.clone());
      }
      return networkResponse;
    })
    .catch(() => {}); // Ignore network errors
  
  // Return cached version immediately (or wait for network)
  return cachedResponse || fetchPromise || getOfflineFallback();
}

// ============================================
// HELPER FUNCTIONS
// ============================================

function isAPIRequest(url) {
  return API_PATTERNS.some(pattern => pattern.test(url.href));
}

function isStaticAsset(pathname) {
  return STATIC_PATTERNS.some(pattern => pattern.test(pathname));
}

function isHTMLRequest(url) {
  return url.pathname.endsWith('.html') || 
         url.pathname.endsWith('/') ||
         !url.pathname.includes('.');
}

function isCacheExpired(response, ttlSeconds) {
  const dateHeader = response.headers.get('date');
  if (!dateHeader) return false; // Assume valid if no date header
  
  const fetchedDate = new Date(dateHeader).getTime();
  const now = Date.now();
  const ageSeconds = (now - fetchedDate) / 1000;
  
  return ageSeconds > ttlSeconds;
}

async function getOfflineFallback() {
  const cache = await caches.open(STATIC_CACHE);
  const offlinePage = await cache.match('/offline.html');
  
  if (offlinePage) return offlinePage;
  
  // Return a basic offline response
  return new Response(
    `<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Offline - SciMSPT</title>
      <style>
        body { font-family: system-ui; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background: #0a1628; color: #e8f4fc; text-align: center; padding: 20px; }
        h1 { font-size: 2em; margin-bottom: 10px; color: #00E5FF; }
        p { color: #64748b; }
        button { margin-top: 20px; padding: 12px 24px; background: #00E5FF; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; }
      </style>
    </head>
    <body>
      <div>
        <h1>You're Offline</h1>
        <p>Please check your internet connection and try again.</p>
        <button onclick="window.location.reload()">Retry</button>
      </div>
    </body>
    </html>`,
    {
      status: 503,
      statusText: 'Service Unavailable',
      headers: new Headers({ 'Content-Type': 'text/html' })
    }
  );
}

// ============================================
// BACKGROUND SYNC
// ============================================

self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'sync-search-history') {
    event.waitUntil(syncSearchHistory());
  }
  
  if (event.tag === 'sync-analytics') {
    event.waitUntil(syncAnalyticsData());
  }
});

async function syncSearchHistory() {
  // Sync search history to server when back online
  try {
    // Implementation depends on backend
    console.log('[SW] Search history synced');
  } catch (error) {
    console.error('[SW] Failed to sync history:', error);
  }
}

async function syncAnalyticsData() {
  // Queue analytics events for later sending
  try {
    console.log('[SW] Analytics data synced');
  } catch (error) {
    console.error('[SW] Failed to sync analytics:', error);
  }
}

// ============================================
// PUSH NOTIFICATIONS (Future)
// ============================================

self.addEventListener('push', (event) => {
  console.log('[SW] Push received:', event);
  
  let data = {
    title: 'SciMSPT',
    body: 'New research papers available!',
    icon: '/assets/icon-192.svg'
  };
  
  if (event.data) {
    try {
      data = event.data.json();
    } catch (e) {
      data.body = event.data.text();
    }
  }
  
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: data.icon,
      badge: '/assets/icon-192.svg',
      data: { url: data.url || '/' },
      actions: [
        { action: 'view', title: 'View' },
        { action: 'dismiss', title: 'Dismiss' }
      ]
    })
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'dismiss') return;
  
  const url = event.notification.data?.url || '/';
  
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then(clientList => {
      // Focus existing window if open
      for (const client of clientList) {
        if (client.url === url && 'focus' in client) {
          return client.focus();
        }
      }
      // Open new window
      if (clients.openWindow) {
        return clients.openWindow(url);
      }
    })
  );
});

// ============================================
// MESSAGE HANDLING
// ============================================

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    caches.keys().then(keys => {
      keys.forEach(key => caches.delete(key));
    });
  }
});

console.log('[SW] Service worker loaded:', CACHE_VERSION);
