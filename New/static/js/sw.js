// Novaryo Service Worker for Progressive Web App
// Version 1.0.0

const CACHE_NAME = 'novaryo-v1';
const STATIC_CACHE = 'novaryo-static-v1';
const DYNAMIC_CACHE = 'novaryo-dynamic-v1';
const API_CACHE = 'novaryo-api-v1';

// Static assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/static/manifest.json',
  '/loyalty/',
  '/hotels/',
  '/flights/',
  // Add critical routes
  '/offline.html'
];

// API endpoints to cache
const API_ENDPOINTS = [
  '/api/loyalty/tiers/public/',
  '/api/loyalty/rewards/public/',
  '/api/loyalty/promotions/public/'
];

// Network-first strategy URLs (always try network first)
const NETWORK_FIRST_URLS = [
  '/api/loyalty/memberships/',
  '/api/loyalty/transactions/',
  '/api/bookings/',
  '/admin/'
];

// Cache-first strategy URLs (serve from cache if available)
const CACHE_FIRST_URLS = [
  '/static/',
  '/media/',
  'https://cdn.jsdelivr.net/',
  'https://cdnjs.cloudflare.com/'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE).then(cache => {
      console.log('Service Worker: Caching static assets');
      return cache.addAll(STATIC_ASSETS);
    }).then(() => {
      console.log('Service Worker: Static assets cached');
      return self.skipWaiting(); // Activate immediately
    }).catch(error => {
      console.error('Service Worker: Installation failed', error);
    })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(cacheName => {
            // Remove old caches that don't match current version
            return cacheName !== STATIC_CACHE && 
                   cacheName !== DYNAMIC_CACHE && 
                   cacheName !== API_CACHE;
          })
          .map(cacheName => {
            console.log('Service Worker: Deleting old cache', cacheName);
            return caches.delete(cacheName);
          })
      );
    }).then(() => {
      console.log('Service Worker: Activated');
      return self.clients.claim(); // Take control immediately
    })
  );
});

// Fetch event - handle network requests
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip Chrome extensions and other protocols
  if (!request.url.startsWith('http')) {
    return;
  }
  
  // Handle different caching strategies
  if (isStaticAsset(request.url)) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
  } else if (isAPIRequest(request.url)) {
    event.respondWith(networkFirstWithCache(request, API_CACHE));
  } else if (isNetworkFirstURL(request.url)) {
    event.respondWith(networkFirst(request));
  } else if (isCacheFirstURL(request.url)) {
    event.respondWith(cacheFirst(request, DYNAMIC_CACHE));
  } else {
    // Default: network first with dynamic caching
    event.respondWith(networkFirstWithCache(request, DYNAMIC_CACHE));
  }
});

// Background sync for offline actions
self.addEventListener('sync', event => {
  console.log('Service Worker: Background sync triggered', event.tag);
  
  if (event.tag === 'loyalty-points-sync') {
    event.waitUntil(syncLoyaltyPoints());
  } else if (event.tag === 'offline-bookings-sync') {
    event.waitUntil(syncOfflineBookings());
  }
});

// Push notification handler
self.addEventListener('push', event => {
  console.log('Service Worker: Push notification received');
  
  const options = {
    body: 'You have a new update!',
    icon: '/static/images/icons/icon-192x192.png',
    badge: '/static/images/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'View Details',
        icon: '/static/images/icons/checkmark.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/images/icons/xmark.png'
      }
    ]
  };
  
  if (event.data) {
    const data = event.data.json();
    options.body = data.body || options.body;
    options.title = data.title || 'Novaryo';
  }
  
  event.waitUntil(
    self.registration.showNotification('Novaryo', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', event => {
  console.log('Service Worker: Notification clicked');
  
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/loyalty/')
    );
  } else if (event.action === 'close') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Message handler for client communication
self.addEventListener('message', event => {
  console.log('Service Worker: Message received', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  } else if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  } else if (event.data && event.data.type === 'CLEAR_CACHE') {
    clearAllCaches().then(() => {
      event.ports[0].postMessage({ success: true });
    });
  }
});

// Caching strategies
async function cacheFirst(request, cacheName) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      console.log('Service Worker: Serving from cache', request.url);
      return cachedResponse;
    }
    
    // Not in cache, fetch from network
    const networkResponse = await fetch(request);
    
    // Cache the response for next time
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.error('Service Worker: Cache first failed', error);
    return getOfflinePage();
  }
}

async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request);
    return networkResponse;
  } catch (error) {
    console.log('Service Worker: Network failed, trying cache', request.url);
    const cachedResponse = await caches.match(request);
    return cachedResponse || getOfflinePage();
  }
}

async function networkFirstWithCache(request, cacheName) {
  try {
    const networkResponse = await fetch(request);
    
    // Cache successful responses
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('Service Worker: Network failed, trying cache', request.url);
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // For API requests, return a meaningful offline response
    if (isAPIRequest(request.url)) {
      return new Response(JSON.stringify({
        error: 'Offline',
        message: 'This request is not available offline'
      }), {
        status: 503,
        statusText: 'Service Unavailable',
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return getOfflinePage();
  }
}

// Helper functions
function isStaticAsset(url) {
  return STATIC_ASSETS.some(asset => url.includes(asset)) ||
         url.includes('/static/') ||
         url.includes('.css') ||
         url.includes('.js') ||
         url.includes('.png') ||
         url.includes('.jpg') ||
         url.includes('.svg');
}

function isAPIRequest(url) {
  return url.includes('/api/');
}

function isNetworkFirstURL(url) {
  return NETWORK_FIRST_URLS.some(pattern => url.includes(pattern));
}

function isCacheFirstURL(url) {
  return CACHE_FIRST_URLS.some(pattern => url.includes(pattern));
}

async function getOfflinePage() {
  try {
    const cache = await caches.open(STATIC_CACHE);
    const offlinePage = await cache.match('/offline.html');
    return offlinePage || new Response('You are offline', {
      status: 503,
      statusText: 'Service Unavailable'
    });
  } catch {
    return new Response('You are offline', {
      status: 503,
      statusText: 'Service Unavailable'
    });
  }
}

async function clearAllCaches() {
  const cacheNames = await caches.keys();
  return Promise.all(
    cacheNames.map(cacheName => caches.delete(cacheName))
  );
}

// Background sync functions
async function syncLoyaltyPoints() {
  try {
    console.log('Service Worker: Syncing loyalty points...');
    
    // Get offline points data from IndexedDB
    const offlineData = await getOfflineLoyaltyData();
    
    if (offlineData.length > 0) {
      // Sync each offline transaction
      for (const data of offlineData) {
        await fetch('/api/loyalty/transactions/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${data.token}`
          },
          body: JSON.stringify(data.transaction)
        });
      }
      
      // Clear offline data after successful sync
      await clearOfflineLoyaltyData();
      console.log('Service Worker: Loyalty points synced successfully');
    }
  } catch (error) {
    console.error('Service Worker: Loyalty points sync failed', error);
  }
}

async function syncOfflineBookings() {
  try {
    console.log('Service Worker: Syncing offline bookings...');
    
    // Implementation for offline booking sync
    // This would integrate with your booking system
    
  } catch (error) {
    console.error('Service Worker: Offline bookings sync failed', error);
  }
}

// IndexedDB helpers (simplified implementation)
async function getOfflineLoyaltyData() {
  // In a real implementation, this would use IndexedDB
  return [];
}

async function clearOfflineLoyaltyData() {
  // In a real implementation, this would clear IndexedDB
  return Promise.resolve();
}

// Log service worker lifecycle
console.log('Service Worker: Script loaded');

// Handle unhandled promise rejections
self.addEventListener('unhandledrejection', event => {
  console.error('Service Worker: Unhandled promise rejection', event.reason);
  event.preventDefault();
});

// Periodic background sync (if supported)
if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
  // Register for background sync when SW is ready
  self.addEventListener('sync', event => {
    if (event.tag === 'periodic-loyalty-sync') {
      event.waitUntil(periodicLoyaltySync());
    }
  });
}

async function periodicLoyaltySync() {
  try {
    // Fetch latest loyalty data
    await fetch('/api/loyalty/memberships/my_membership/');
    console.log('Service Worker: Periodic loyalty sync completed');
  } catch (error) {
    console.error('Service Worker: Periodic loyalty sync failed', error);
  }
}