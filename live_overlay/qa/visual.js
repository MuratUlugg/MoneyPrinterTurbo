// Görsel denetim çekimleri: düğün salonu ve at yarışının belirli anlarını 3B pencere çözünürlüğünde kaydeder.
// Bu dosya karar vermez; görüntülere bir gözün bakması gerekir (RALPH.md, "Görsel denetim").
// Çalıştırma: live_overlay/qa/run.sh <python> gorsel   (çıktı: $QA_OUT/gorsel-*.png)
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = process.env.QA_BASE || 'http://127.0.0.1:8766', OUT = process.env.QA_OUT || '/tmp/hediye-qa';
const api = (path, body) => fetch(BASE + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) }).then(r => r.json());
const NAMES = ['Ayşe', 'Mehmet', 'Zeynep', 'Emre', 'Elif', 'Can', 'Deniz', 'Selin', 'Burak', 'Ece', 'Kerem', 'Melis'];
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('PAGEERR', e.message));
  const gl = async name => { const box = await p.locator('#gl').boundingBox(); await p.screenshot({ path: `${OUT}/gorsel-${name}.png`, clip: box }); console.log('çekildi', name); };
  const full = async name => { await p.screenshot({ path: `${OUT}/gorsel-${name}.png` }); console.log('çekildi', name); };
  const gift = (name, diamonds, count = 1, gift = 'Gül') => api('/api/simulate', { name, gift, diamonds, count });
  const wait = s => p.waitForTimeout(s * 1000);
  await p.goto(`${BASE}/overlay?_hiz=8&halay=100000&taki=100000&goal=100000`); await wait(6);
  await api('/api/reset');

  // ---- HALAY
  await api('/api/mode', { mode: 'halay' }); await wait(6); await gl('halay-0-bos');                       // pist boş: adsız konuklar
  for (const n of ['Hakan', 'Sibel', 'Tolga', 'Derya', 'Okan', 'Pınar']) await api('/api/simulate', { type: 'comment', name: n, text: 'selam' });
  for (const n of NAMES.slice(0, 3)) await gift(n, 1, 2);
  await wait(14); await gl('halay-1-uc-kisi-genis');
  for (const n of NAMES.slice(3, 12)) await gift(n, 1, 2);
  await wait(16); await gl('halay-2-on-iki-kisi-genis'); await full('halay-2-tam-ekran');
  await gift('Emre', 1); await wait(2.4); await gl('halay-3-yakin-halayci');
  await wait(9); await api('/api/simulate', { type: 'comment', name: 'Sibel', text: 'maşallah' }); await wait(2.6); await gl('halay-4-yakin-misafir');
  await wait(8); await gift('Elif', 30, 1, 'Donut'); await wait(2.4); await gl('halay-5-davulcu-bahsis');
  await wait(8); await gift('Selin', 500, 1, 'Aslan'); await wait(1.2); await gl('halay-6-volkan'); await wait(3); await gl('halay-7-ortada');

  // ---- TAKI
  await api('/api/mode', { mode: 'taki' }); await wait(7); await gl('taki-0-cift');
  await gift('Sibel', 30, 2, 'Donut'); await wait(1.3); await gl('taki-1-gonderen-misafir'); await wait(2.2); await gl('taki-2-altin-ucuyor');
  for (const [n, d] of [['Ayşe', 1], ['Mehmet', 10], ['Zeynep', 60], ['Emre', 250], ['Elif', 1200], ['Can', 5], ['Deniz', 20]]) await gift(n, d);
  await wait(16); await gl('taki-3-takilar-takili'); await full('taki-3-tam-ekran');

  // ---- AT YARIŞI
  await api('/api/mode', { mode: 'race' }); await wait(4); await gl('yaris-0-bos');
  for (const n of NAMES.slice(0, 8)) await gift(n, 1, 3);
  await wait(6); await gl('yaris-1-sekiz-at-ayni-hizada');
  for (const [i, n] of NAMES.slice(0, 8).entries()) await gift(n, 300 * (i + 1));
  await wait(7); await gl('yaris-2-dagilmis'); await full('yaris-2-tam-ekran');
  await gift('Ayşe', 10); await wait(2.2); await gl('yaris-3-yakin-at');
  await wait(6); await gift('Selin', 99000, 1, 'Galaksi'); await wait(1.6); await gl('yaris-4-finis');
  await b.close();
})();
