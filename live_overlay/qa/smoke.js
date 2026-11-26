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
    if (m === 'taki') { for (let i = 0; i < 40 && q.seref < 3; i++) { await p.waitForTimeout(700); q = await p.evaluate(() => window.__qa || null); } check(q.seref === 3, `taki: en çok takı takan üç kişi şeref konuğu olarak sahneye çıktı (${q.seref})`); }
    if (m === 'race') { for (let i = 0; i < 12 && q.faz !== 'kos'; i++) { await p.waitForTimeout(700); q = await p.evaluate(() => window.__qa || null); } check(q.faz === 'kos', `race: geri sayımdan sonra kapılar açıldı (${q.faz})`);
      const n0 = q.atlar; await api('/api/simulate', { type: 'comment', name: 'Taraftar', text: '4' }); await p.waitForTimeout(600); await api('/api/simulate', { name: 'Taraftar', gift: 'Gül', diamonds: 5 }); await p.waitForTimeout(600); q = await p.evaluate(() => window.__qa || null);
      check(q.taraftar === 1 && q.atlar === n0, `race: yorumla taraf olundu, taraftarın hediyesi yeni at açmadı (${q.taraftar} taraftar, ${q.atlar}/${n0} at)`); }
    if (m === 'halay') { await api('/api/simulate', { name: 'Can', gift: 'Şapka', diamonds: 50 }); await p.waitForTimeout(800); q = await p.evaluate(() => window.__qa || null);
      check(q && q.oyun && q.oyun !== 'HALAY', `halay: 50 jetonluk hediye oyun havasını değiştirdi (${q && q.oyun})`); }
    if (m === 'halay') { await api('/api/simulate', { type: 'comment', name: 'Sibel', text: 'maşallah çok güzel' }); await api('/api/simulate', { type: 'comment', name: 'Reklamcı', text: 'takipçi için www.ornek.com' }); await p.waitForTimeout(800); q = await p.evaluate(() => window.__qa || null);
      check(q && q.balon === 1, `halay: yorum balonu açıldı, bağlantılı yorum gösterilmedi (${q && q.balon})`); }
    const before = q ? q.wins : 0;
    await api('/api/simulate', { name: 'Zeynep', gift: 'Galaksi', diamonds: 1000 });
    let won = false, sawPodium = false, sawCake = false, sawGroom = false; for (let i = 0; i < 70 && !won; i++) /* kazanan, törenden (pasta, kürsü) sonra ilan edilir; yavaş makinede oyun saati geride kalır */ { await p.waitForTimeout(1000); q = await p.evaluate(() => window.__qa || null); won = !!(q && q.wins > before && q.champion === 'Zeynep'); if (q && q.faz === 'kursu') sawPodium = true; if (q && q.pasta) sawCake = true; if (q && q.damat) sawGroom = true; }
    await p.screenshot({ path: `${OUT}/${m}-2-kazanan.png` });
    check(won, `${m}: büyük hediyeden sonra kazanan ilan edildi`);
    if (m === 'race') { check(sawPodium, 'race: kazanandan önce kürsü töreni yapıldı'); check(q.zafer === 1, `race: kazananın zaferi sayıldı (${q.zafer})`); }
    if (m === 'halay') { check(sawCake, 'halay: coşku dolunca pasta kesme töreni yapıldı'); check(sawGroom, 'halay: büyük hediyede damat sahneden inip ortaya çıkanla oynadı'); }
    await p.waitForTimeout(4500);
  }
  check(q0.link === 'tiktok', `bağlantı göstergesi TikTok'a bağlı olmadığını bildiriyor (${q0.link})`);
  // kalıcılık: sayfa yenilenince sıralama defterden geri gelmeli
  await p.reload(); await p.waitForTimeout(7000);
  const q = await p.evaluate(() => window.__qa || null), rep = await api('/api/report', undefined, 'GET');
  check(q && q.zaferTop === 1, `yenilemeden sonra yarış zaferi sunucudaki defterden geri geldi (${q && q.zaferTop})`);
  check(q && q.top[0] === 'Zeynep' && q.session === rep.total && rep.total > 0, `yenilemeden sonra sıralama ve toplam geri geldi (${q && q.session} = ${rep.total})`);
  check(rep.gifters === 6 && Object.keys(rep.by_mode).length === MODES.length, `rapor: 6 bağışçı (biri taraftar), 5 bölüm (${rep.gifters})`);
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
