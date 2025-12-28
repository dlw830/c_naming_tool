// Service Worker - 提供离线支持

const CACHE_NAME = 'c-naming-tool-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/app.js',
    '/variable',
    '/translator',
    '/pointer',
    '/function'
];

// 安装Service Worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('缓存已打开');
                return cache.addAll(urlsToCache);
            })
            .catch((error) => {
                console.log('缓存失败:', error);
            })
    );
});

// 激活Service Worker
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('删除旧缓存:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// 拦截请求
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // 缓存命中，返回缓存
                if (response) {
                    return response;
                }

                // 缓存未命中，发起网络请求
                return fetch(event.request).then((response) => {
                    // 检查是否是有效响应
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }

                    // 克隆响应
                    const responseToCache = response.clone();

                    // 缓存新请求的响应
                    caches.open(CACHE_NAME)
                        .then((cache) => {
                            cache.put(event.request, responseToCache);
                        });

                    return response;
                }).catch(() => {
                    // 网络请求失败，返回离线页面
                    return caches.match('/');
                });
            })
    );
});
