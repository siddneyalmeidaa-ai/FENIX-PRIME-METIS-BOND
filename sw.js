const CACHE_NAME = 'fenix-prime-v362-cache';
const assets = [
  './',
  './index.html',
  './manifest.json',
  './logo.png',
  './tridente.svg'
];

// INSTALAÇÃO: SALVA O ESSENCIAL
self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(assets))
  );
});

// ATIVAÇÃO: LIMPA O CACHE VELHO (V27 E OUTROS)
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    })
  );
});

// ESTRATÉGIA: BUSCA NA REDE, SE FALHAR, USA O CACHE
self.addEventListener('fetch', (e) => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
}
                     );
