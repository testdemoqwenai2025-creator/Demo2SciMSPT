/**
 * SciMSPT Service Worker
 * Offline-first PWA support
 */

const CACHE_NAME = 'scimspt-v2.0.0';
const STATIC_CACHE = 'scimspt-static-v2.0';
const DYNAMIC_CACHE = 'scimspt-dynamic-v2.0';

// Assets to pre-cache for offline use
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/platform.html',
  '/dashboard.html',
  '/quantum.html',
  '/pipeline.html',
  '/security.html',
  '/research.html',
  '/monitoring.html',
  '/scaling.html',
  '/infrastructure.html',
  '/about.html',
  '/studio.html',
  '/startups.html',
  '/manifest.json',
  '/assets/og-image.png',
  '/assets/icon-192.png',
  '/assets/icon-512.png',
  // Fonts (CDN - cache with network fallback)
  'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Orbitron:wght@400;700;900&display=swap',
  'https://fonts.googleapis.com/icon?family=Material+Icons+Round'
];

// Install event - precache static assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('[SW] Pre-caching static assets');
        return cache.addAll(PRECACHE_ASSETS).catch(err => {
          console.warn('[SW] Some assets failed to precache:', err);
          // Continue even if some assets fail (external resources may be unavailable during install)
          return Promise.resolve();
        });
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter(name => name !== STATIC_CACHE && name !== DYNAMIC_CACHE)
          .map(name => {
            console.log('[SW] Deleting old cache:', name);
            return caches.delete(name);
          })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - Network first, fallback to cache
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') return;
  
  // Skip external requests (except fonts/icons)
  if (url.origin !== location.origin && !url.hostname.includes('fonts.googleapis.com')) {
    return;
  }
  
  // For navigation requests (HTML pages)
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Cache successful responses
          if (response.ok) {
            const responseClone = response.clone();
            caches.open(DYNAMIC_CACHE).then(cache => cache.put(request, responseClone));
          }
          return response;
        })
        .catch(() => {
          // Fallback to cache or offline page
          return caches.match(request).then(cachedResponse => {
            return cachedResponse || caches.match('/index.html');
          });
        })
    );
    return;
  }
  
  // For static assets (CSS, JS, images) - Cache First
  if (url.pathname.match(/\.(css|js|png|jpg|jpeg|svg|gif|ico|woff2?)$/)) {
    event.respondWith(
      caches.match(request).then(cached => {
        if (cached) {
          // Update cache in background
          fetch(request).then(response => {
            if (response.ok) {
              caches.open(DYNAMIC_CACHE).then(cache => cache.put(request, response));
            }
          }).catch(() => {});
          return cached;
        }
        
        return fetch(request)
          .then(response => {
            if (response.ok) {
              const responseClone = response.clone();
              caches.open(DYNAMIC_CACHE).then(cache => cache.put(request, responseClone));
            }
            return response;
          });
      })
    );
    return;
  }
  
  // Default: Network first for everything else
  event.respondWith(
    fetch(request)
      .then(response => {
        if (response.ok) {
          const responseClone = response.clone();
          caches.open(DYNAMIC_CACHE).then(cache => cache.put(request, responseClone));
        }
        return response;
      })
      .catch(() => caches.match(request))
  );
});

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'sync-quantum-job') {
    event.waitUntil(syncQuantumJob());
  }
  
  if (event.tag === 'sync-pipeline-run') {
    event.waitUntil(syncPipelineRun());
  }
});

// Push notifications (future feature)
self.addEventListener('push', (event) => {
  if (!event.data) return;
  
  const data = event.data.json();
  const options = {
    body: data.body || 'New notification from SciMSPT',
    icon: '/assets/icon-192.png',
    badge: '/assets/icon-192.png',
    vibrate: [100, 50, 100],
    data: data.url || '/',
    actions: [
      { action: 'open', title: 'Open' },
      { action: 'dismiss', title: 'Dismiss' }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title || 'SciMSPT', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'dismiss') return;
  
  event.waitUntil(
    clients.openWindow(event.notification.data || '/')
  );
});

// Helper functions for background sync
async function syncQuantumJob() {
  // TODO: Implement quantum job sync when online
  console.log('[SW] Syncing quantum jobs...');
}

async function syncPipelineRun() {
  // TODO: Implement pipeline run sync when online
  console.log('[SW] Syncing pipeline runs...');
}
