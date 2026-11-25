# İş listesi

Ralph döngüsü bu dosyayı her turda okur ve günceller (`RALPH.md`).

## Açık

- [ ] Kalabalık halayda yakın planda öndeki halaycıların sırtı araya giriyor; kamera açısı kişiyi net görecek şekilde seçilmeli.
- [ ] Halay adımı tek bir basit tekme; gerçek halay figürü (üç adım, çök-kalk, omuz silkme) yok.
- [ ] Takı töreninde gelin hiç hareket etmiyor; en azından nefes, baş ve gövde salınımı daha canlı olmalı.
- [ ] At yarışında atlar aynı ilerlemedeyken üst üste biniyor, etiketler okunmuyor.
- [ ] Yer volkanları ve üçüncü çelenk ekran görüntüsünde hiç doğrulanmadı.
- [ ] Menü kartlarındaki "gerçek hediye adı + ikon" yolu test hediyelerinde ikon olmadığı için hiç görülmedi; `smoke.js` ikonlu bir test hediyesi göndermeli.
- [ ] `smoke.js` yalnızca "hata yok, kazanan var" diyor: masaya oturma, ortaya çıkma, davulcuya bahşiş, ad denetimi, ayar kaydı ve otomatik program için kontrol yok.
- [ ] Panelde ayar kaydederken bir alan geçersizse kullanıcıya hangisi olduğu söylenmiyor (sunucu sessizce sınırlıyor).
- [ ] Karpuz, halat ve at yarışı düğün salonunun dışında ayrı dünyalarda; salonla ortak bir görsel dil (aynı HUD dışında) yok.
- [ ] Ses efektleri kod olarak var ama hiç dinlenmedi; davul deseni düz "dum-tek".
- [ ] Overlay tek dosyada 1.100+ satır; mantık (kombo, seviye, yönetmen) için tarayıcısız birim testi yok.
- [ ] `on_event` kullanımı FastAPI'de kullanımdan kalkıyor (testlerde uyarı veriyor); `lifespan`'e geçilmeli.

## Kullanıcıda (döngü çözemez)

- Gerçek TikTok yayınıyla deneme: kare hızı, hediye sayımı, telefonda yerleşim.
- Model lisansları (README'deki tablo).
- Sesli anons: test ortamı seslendirme servisine ulaşamıyor.
- İmza servisinin koşulları ve gerekirse anahtar.
- Ürün kararı: "düğün yayını" mı, "oyun paketi" mi; karpuzdaki şans unsuru.
- Daha fazla yüz / hareketli gelin / yüksek poligonlu at: yeni model gerekir.

## Bitenler

- Kalıcı yayın defteri, rapor, ayar paneli, otomatik program, ad denetimi, otomatik kalite, yerel kütüphane, başlatma betikleri (QA: 8 birim testi + elle yenileme denemesi).
- Otomatik QA kapısı (`qa/run.sh`): 5 mod, kazanma akışı, yenilemeden sonra geri yükleme, panel.
- Bağlantı göstergesi: sunucu ya da TikTok bağlantısı yokken overlay'in sol üstünde küçük nokta, `?kilavuz=1` iken yazı; panel sunucuya ulaşamazsa uyarır (QA: duman testi TikTok'suz durumda göstergenin `tiktok` dediğini kontrol ediyor; sunucu kopması elle denenmedi).
