// Hediye Arenası duman testi: her modu gerçek tarayıcıda açar, olay yollar, kazanma akışını bekler.
// Kapı: tarayıcı hatası yok, her mod 3B sahnesini kuruyor, kazanan ilan ediliyor, yenilemeden sonra sıralama geri geliyor.
// Çalıştırma: live_overlay/qa/run.sh   (çıktı: $QA_OUT altında ekran görüntüleri + sonuc.json)
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = process.env.QA_BASE || 'http://127.0.0.1:8766', OUT = process.env.QA_OUT || '/tmp/hediye-qa';
const api = (path, body, method = 'POST') => fetch(BASE + path, { method, headers: { 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined }).then(r => r.json());
const MODES = ['halay', 'race', 'taki', 'tug', 'karpuz'];
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const fails = [], errs = [], b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 } });
  p.on('console', x => x.type() === 'error' && errs.push(x.text().slice(0, 200)));
  p.on('pageerror', e => errs.push('PAGEERR: ' + e.message));
  const check = (ok, what) => { if (!ok) fails.push(what); console.log((ok ? 'ok   ' : 'FAIL ') + what); };
  // _hiz: ekran kartsız makinede oyun saati geri kalır; test bunu telafi eder. _qa: sahne durumunu window.__qa'ya yazar.
  await p.goto(`${BASE}/overlay?_hiz=8&_qa=1&halay=300`); await p.waitForTimeout(5000);
  await api('/api/reset');
  const q0 = await p.evaluate(() => window.__qa || {});
  for (const m of MODES) {
    await api('/api/mode', { mode: m }); await p.waitForTimeout(1500);
    await api('/api/simulate', { type: 'comment', name: 'Sibel', text: 'kahve' });
    for (const n of ['Mehmet', 'Ayşe', 'Can', 'Elif']) await api('/api/simulate', { name: n, gift: 'Donut', diamonds: 30, count: 2 });
    await p.waitForTimeout(3500); await p.screenshot({ path: `${OUT}/${m}-1-oyun.png` });
    let q = await p.evaluate(() => window.__qa || null);
    check(q && q.mode === m && q.built, `${m}: 3B sahne kuruldu`);
    const before = q ? q.wins : 0;
    await api('/api/simulate', { name: 'Zeynep', gift: 'Galaksi', diamonds: 1000 });
    let won = false; for (let i = 0; i < 14 && !won; i++) { await p.waitForTimeout(1000); q = await p.evaluate(() => window.__qa || null); won = !!(q && q.wins > before && q.champion === 'Zeynep'); }
    await p.screenshot({ path: `${OUT}/${m}-2-kazanan.png` });
    check(won, `${m}: büyük hediyeden sonra kazanan ilan edildi`);
    await p.waitForTimeout(4500);
  }
  check(q0.link === 'tiktok', `bağlantı göstergesi TikTok'a bağlı olmadığını bildiriyor (${q0.link})`);
  // kalıcılık: sayfa yenilenince sıralama defterden geri gelmeli
  await p.reload(); await p.waitForTimeout(7000);
  const q = await p.evaluate(() => window.__qa || null), rep = await api('/api/report', undefined, 'GET');
  check(q && q.top[0] === 'Zeynep' && q.session === rep.total && rep.total > 0, `yenilemeden sonra sıralama ve toplam geri geldi (${q && q.session} = ${rep.total})`);
  check(rep.gifters === 5 && Object.keys(rep.by_mode).length === MODES.length, 'rapor: 5 bağışçı, 5 bölüm');
  await p.screenshot({ path: `${OUT}/son-yenileme.png` });
  // panel
  const c = await b.newPage({ viewport: { width: 1200, height: 1500 } });
  c.on('console', x => x.type() === 'error' && errs.push('panel: ' + x.text().slice(0, 200))); c.on('pageerror', e => errs.push('PANEL: ' + e.message));
  await c.goto(BASE + '/'); await c.waitForTimeout(4000); await c.screenshot({ path: `${OUT}/panel.png` });
  check((await c.textContent('#k-total')).trim() !== '0', 'panel raporu doldu');
  check(errs.length === 0, 'tarayıcı hatası yok' + (errs.length ? ': ' + [...new Set(errs)].join(' | ') : ''));
  fs.writeFileSync(`${OUT}/sonuc.json`, JSON.stringify({ fails, errs: [...new Set(errs)] }, null, 1));
  await b.close();
  console.log(fails.length ? `\nQA BAŞARISIZ: ${fails.length} kontrol` : '\nQA GEÇTİ');
  process.exit(fails.length ? 1 : 0);
})();
