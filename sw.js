const CACHE_NAME = 'supremacia-v27-cache';
const assets = [
  '/FENIX-PRIME-METIS-BOND/',
  '/FENIX-PRIME-METIS-BOND/index.html',
  '/FENIX-PRIME-METIS-BOND/manifest.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(assets)));
});

self.addEventListener('fetch', (e) => {
  e.respondWith(caches.match(e.request).then((res) => res || fetch(e.request)));
})
  ;
