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
  const qa = () => p.evaluate(() => window.__qa || {});
  // Çekimden önce oyun saati dondurulur: ekran görüntüsü almak saniyeler sürebilir ve o sırada an kaçmasın.
  const freeze = async on => { await p.evaluate(v => { window.__qaPause = v; }, on); if (on) { const f0 = (await qa()).frame; for (let i = 0; i < 80 && (await qa()).frame < f0 + 2; i++) await p.waitForTimeout(200); } };
  const snap = async (name, clip) => { await freeze(true); const q = await qa(); await p.screenshot({ path: `${OUT}/gorsel-${name}.png`, clip }); await freeze(false); console.log('çekildi', name, '| yakın plan:', q.focus || 'yok'); };
  let box = null; // her çekimde yeniden sormak yavaş makinede anı kaçırtıyor
  const gl = async name => snap(name, box || (box = await p.locator('#gl').boundingBox()));
  const full = async name => snap(name);
  const gift = (name, diamonds, count = 1, gift = 'Gül') => api('/api/simulate', { name, gift, diamonds, count });
  // Ekran kartsız makinede oyun saati gerçek saatten yavaş akar; bu yüzden gerçek saniye değil OYUN saniyesi beklenir.
  const wait = async s => { const t0 = (await qa()).T || 0; for (let i = 0; i < 400; i++) { await p.waitForTimeout(250); if (((await qa()).T || 0) - t0 >= s) return; } };
  const only = process.env.QA_ONLY; // yalnızca bir bölümü çekmek için: halay | taki | race | kalabalik (kalabalık yalnızca istenince çekilir)
  await p.goto(`${BASE}/overlay?_hiz=8&_qa=1&halay=100000&taki=100000&goal=20000`); await p.waitForTimeout(6000);
  await api('/api/reset');

  // ---- HALAY
  if (!only || only === 'halay') {
  await api('/api/mode', { mode: 'halay' }); await wait(3); await gl('halay-0-bos');                       // pist boş: adsız konuklar
  for (const n of ['Hakan', 'Sibel', 'Tolga', 'Derya', 'Okan', 'Pınar']) await api('/api/simulate', { type: 'comment', name: n, text: 'selam' });
  for (const n of NAMES.slice(0, 3)) await gift(n, 1, 2);
  await wait(5); await gl('halay-1-uc-kisi-genis');
  for (const n of NAMES.slice(3, 12)) await gift(n, 1, 2);
  await wait(6); await gl('halay-2-on-iki-kisi-genis'); await full('halay-2-tam-ekran');
  /* el ve ayak denetimi: sıranın ortasına yakından bak, adım döngüsünün dört vuruşunu ayrı ayrı çek */
  const cam = c => p.evaluate(v => { window.__qaCam = v; }, c);
  await cam([0, 1.05, -.9, 0, .9, -2.6]); await wait(.3); await gl('halay-8-eller-yakin');
  await cam([0, .9, 2.6, 0, .75, -2.4]);
  for (let k = 0; k < 4; k++) { await p.evaluate(v => { window.__qaStopAt = v; }, k); for (let i = 0; i < 120 && !(await p.evaluate(() => window.__qaPause)); i++) await p.waitForTimeout(150); await gl('halay-9-adim-' + k); } /* her vuruş tam ortasında dondurulup çekilir */
  await cam(null);
  await wait(1); await gift('Emre', 1); await wait(.5); await gl('halay-3-yakin-halayci');
  await wait(6); await api('/api/simulate', { type: 'comment', name: 'Sibel', text: 'maşallah' }); await wait(.5); await gl('halay-4-yakin-misafir');
  await wait(6); await gift('Elif', 30, 1, 'Donut'); await wait(.5); await gl('halay-5-davulcu-bahsis');
  await wait(6); await gift('Selin', 500, 1, 'Aslan'); await wait(.4); await gl('halay-6-volkan'); await full('halay-6-tam-ekran'); await wait(1.5); await gl('halay-7-ortada');
  /* oyun havası: 50 jetonluk hediye sıradaki oyunu açtırır (çiftetelli → horon → zeybek; Selin'in 500'lük hediyesi de bir oyun açtığı için sıra oradan devam eder); kamera hediyeyi atandan geniş plana dönünce çekilir */
  await wait(10); await gift('Deniz', 50, 1, 'Şapka'); await wait(5); await gl('halay-10-oyun-a'); await full('halay-10-tam-ekran');
  await gift('Can', 50, 1, 'Şapka'); await wait(5); await gl('halay-10-oyun-b');
  await gift('Burak', 50, 1, 'Şapka'); await wait(5); await gl('halay-10-oyun-c'); await wait(1.2); await gl('halay-10-oyun-c2');

  }
  // ---- KALABALIK: 260 yorumcu + 70 hediye gönderen (yaklaşık 500 kişilik bir yayının etkileşen kısmı)
  if (only === 'kalabalik') {
  await api('/api/mode', { mode: 'halay' }); await wait(2);
  for (let i = 0; i < 260; i++) await api('/api/simulate', { type: 'comment', name: 'Misafir' + i, text: 'selam' });
  for (let i = 0; i < 70; i++) await gift('Halayci' + i, 1, 1 + (i * 7) % 40);
  await wait(6); await gl('kalabalik-0-halay-genis'); await full('kalabalik-0-tam-ekran'); console.log('durum', JSON.stringify(await qa()));
  await p.evaluate(v => { window.__qaCam = v; }, [0, 6.5, 9.5, 0, .8, -2.5]); await wait(.3); await gl('kalabalik-1-ustten-salon');
  await p.evaluate(v => { window.__qaCam = v; }, null);
  await p.evaluate(v => { window.__qaCam = v; }, [-7.4, 1.5, -2.8, -9.2, 1.05, -2.8]); await wait(.3); await gl('kalabalik-4-masa-yakin'); await p.evaluate(v => { window.__qaCam = v; }, null);
  await api('/api/simulate', { type: 'comment', name: 'Misafir200', text: 'maşallah' }); await wait(.6); await gl('kalabalik-2-yakin-misafir');
  await wait(6); await api('/api/mode', { mode: 'taki' }); await wait(3); await gl('kalabalik-3-taki');
  }
  // ---- TAKI
  if (!only || only === 'balon') { /* yorum balonu: masadaki misafirin yakın planında, geniş planda ve halaycının başında */
    await api('/api/mode', { mode: 'halay' }); await wait(2); for (const n of NAMES.slice(0, 4)) await gift(n, 2); await wait(6);
    await api('/api/simulate', { type: 'comment', name: 'Sibel', text: 'maşallah çok güzel düğün olmuş' }); await wait(.7); await gl('balon-0-yakin-misafir');
    await wait(2.6); await gl('balon-1-genis');
    await wait(4); await api('/api/simulate', { type: 'comment', name: 'Ayşe', text: 'Allah bir yastıkta kocatsın, darısı bekarların başına inşallah' }); await wait(.7); await gl('balon-2-halayci-uzun'); await wait(2.6); await full('balon-3-tam-ekran');
  }
  if (only === 'poz') { /* duruş laboratuvarı: QA_POZ='[[oyun,[kaldırma,salınım,öne,x,y,z]],...]' ile serbest oyunların kol duruşu tek oturumda denenir */
    await api('/api/mode', { mode: 'halay' }); await wait(2); for (const n of NAMES.slice(0, 5)) await gift(n, 2); await wait(5);
    let cur = 0; for (const [i, [st, k]] of JSON.parse(process.env.QA_POZ || '[]').entries()) {
      while (cur !== st) { await gift('Deniz', 50, 1, 'Şapka'); await wait(4.5); cur = cur % 3 + 1; }
      await p.evaluate(([st, k]) => { window.__kol[st].splice(0, 6, ...k); }, [st, k]); await wait(.4); await gl(`poz-${i}-oyun${st}`); console.log('poz', i, JSON.stringify(k)); }
  }
  if (!only || only === 'taki') {
  await api('/api/mode', { mode: 'taki' }); await wait(3); await gl('taki-0-cift');
  await gift('Sibel', 30, 2, 'Donut'); await wait(.3); await gl('taki-1-gonderen-misafir'); await wait(.9); await gl('taki-2-altin-ucuyor');
  for (const [n, d] of [['Ayşe', 1], ['Mehmet', 10], ['Zeynep', 60], ['Emre', 250], ['Elif', 1200], ['Can', 5], ['Deniz', 20], ['Selin', 1], ['Burak', 12], ['Ece', 55], ['Kerem', 3], ['Melis', 70]]) await gift(n, d);
  await wait(9); // büyük hediye bandı kalksın, takılar kurdeleye otursun
  await gl('taki-3-takilar-takili'); await full('taki-3-tam-ekran');

  }
  // ---- AT YARIŞI
  if (!only || only === 'race') {
  await api('/api/mode', { mode: 'race' }); await wait(2); await gl('yaris-0-bos');
  for (const n of NAMES.slice(0, 8)) await gift(n, 1, 3);
  await wait(4); await gl('yaris-1-sekiz-at-ayni-hizada');
  for (const [i, n] of NAMES.slice(0, 8).entries()) await gift(n, 700 * (i + 1)); // finiş 20.000, kombo en çok 2 kat: en öndeki 11.200'de kalır, yarış bitmez
  await wait(4); await gl('yaris-2-dagilmis'); await full('yaris-2-tam-ekran');
  await wait(3); await gift('Ayşe', 10); await wait(.5); await gl('yaris-3-yakin-at');
  await wait(4); await gift('Selin', 40000, 1, 'Galaksi'); await wait(1.5); /* kazanan takın altından geçerken */ await gl('yaris-4-finis');
  }
  await b.close();
})();
