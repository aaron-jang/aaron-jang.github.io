/* 디즈니 어드벤처 가이드 서비스 워커: 모든 언어 페이지와 자원을 미리 저장해 오프라인에서도 열림 */
const VERSION = "da23e0afad";
const CACHE = "da-guide-" + VERSION;
const PRECACHE = ["/disney-adventure-decks/", "/disney-adventure-decks/ko/", "/disney-adventure-decks/en/", "/disney-adventure-decks/ja/", "/disney-adventure-decks/zh-cn/", "/disney-adventure-decks/zh-tw/", "/disney-adventure-decks/assets/style.css", "/disney-adventure-decks/assets/app.js", "/disney-adventure-decks/manifest.webmanifest", "/disney-adventure-decks/assets/icon-192.png", "/disney-adventure-decks/assets/icon-512.png"];
const BASE = "/disney-adventure-decks";
const FONT_HOSTS = ["cdn.jsdelivr.net"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("da-guide-") && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request; if (req.method !== "GET") return;
  const url = new URL(req.url);
  const inScope = url.origin === location.origin && url.pathname.startsWith(BASE + "/");
  const isFont = FONT_HOSTS.includes(url.hostname);
  if (!inScope && !isFont) return;
  if (req.mode === "navigate" || req.destination === "document") {
    /* 페이지: 네트워크 우선(최신 내용), 실패 시 캐시 */
    e.respondWith(fetch(req).then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); return r; })
      .catch(() => caches.match(req, {ignoreSearch: true}).then(r => r || caches.match(BASE + "/ko/"))));
    return;
  }
  /* 자원·폰트: 캐시 우선, 백그라운드 갱신 */
  e.respondWith(caches.match(req).then(cached => {
    const fresh = fetch(req).then(r => { if (r.ok || r.type === "opaque") { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); } return r; }).catch(() => cached);
    return cached || fresh;
  }));
});
