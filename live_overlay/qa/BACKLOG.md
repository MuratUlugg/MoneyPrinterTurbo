# İş listesi

Ralph döngüsü bu dosyayı her turda okur ve günceller (`RALPH.md`). Kapsam: düğün (salon, halay, takı) ve at yarışı.

## Açık: görsel

İlk görsel denetimde (20 çekim) bulunanlar, göze batma sırasıyla.

### Halay
- [ ] Halaycıların kolları dümdüz yana açık (T duruşu gibi); el ele / omuz omuza tutuş yok, dirsek kırılmıyor.
- [ ] Hanımların hepsi aynı çizme ve aynı saç kesimiyle; yalnızca renk değişiyor.
- [ ] Yer volkanları 500 jetonluk hediyede kadrajda yok: kamera ortaya çıkana dönüyor, volkanlar sahnenin önünde arkada kalıyor. Ya volkanlar pistin çevresine alınmalı ya kamera önce geniş planda kalmalı.
- [ ] **Kasket başın üstünde havada duruyor**, altı kel; şapka başa oturmalı, altından saç görünmeli.
- [ ] Halay başının mendili yakın planda kocaman, dümdüz beyaz bir levha.
- [ ] Yakın planda salonun duvarı bitiyor, arkası kapkara boşluk (sol üst).
- [ ] Büyük hediye bandı, ortaya çıkan kişinin başını kapatıyor.
- [ ] Davulcu yakın planında komşu halaycıların kolları kadraja giriyor, davul görüntünün üçte birini kaplıyor.

### Takı töreni
- [ ] **Arka plan soluk ve boş**: bej perde, üstünde balon takının lekeli gölgesi, düz sarı sahne zemini. Balon takı, pankart ve çiçekler kadraja girmiyor.
- [ ] Damat kolları sarkık, dimdik duruyor; gelin hiç kıpırdamıyor. İkisi birbirine dönük, el ele ya da kol kola durmalı.
- [ ] En cömertler listesi çiftin ayaklarını ve gelinliğin eteğini kapatıyor.

### At yarışı
- [ ] **Jokey atın boynuna yatmış, bacakları yere sarkıyor**; eyerde oturmuyor ve ata göre fazla büyük.
- [ ] Finiş anı (takın altından geçiş) hâlâ görüntülenemedi: çekim hep kutlama kartına denk geliyor.
- [ ] Yakın at planında öndeki kulvardaki at kadrajın altını kaplayabiliyor.
- [ ] Yarışta büyük hediye bandı en uzak kulvarlardaki atları ve etiketleri kapatıyor.
- [ ] Atların hepsi aynı kahverengi; don rengi çeşitliliği görünmüyor.
- [ ] Tribün soluk pastel kutular ve beyaz toplar; seyirci gibi durmuyor. Gökyüzü neredeyse görünmüyor.
- [ ] Pist dokusu iri kareli gürültü.

### Genel
- [ ] Takı kurdelesi koyu kırmızı verildiği hâlde ekranda pembeye yakın çıkıyor: pozlama / ton eşlemesi renkleri açıyor (aşağıdaki "soluk" maddesiyle aynı kök).
- [ ] Sahneler soluk ve düz: ortam ışığı fazla, kontrast az; kişiler zeminden ve duvardan ayrışmıyor.

## Açık: diğer

- [ ] `smoke.js`: masaya oturma, ortaya çıkma, davulcuya bahşiş, ad denetimi, ayar kaydı ve otomatik program için kontrol yok.

## Sonraya (kapsam dışı)

- Halat (Çay mı Kahve mi) ve karpuz bölümleri: görsel dil, duruşlar, politika riski.
- Ses efektlerinin dinlenerek ayarlanması, davul deseni.
- Panelde geçersiz alan uyarısı.
- Overlay'in parçalara bölünmesi, tarayıcısız birim testleri, `lifespan`'e geçiş.

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
- Görsel denetim çekimleri (`qa/visual.js`, 20 an) ve ilk denetim: 20 görsel kusur listeye yazıldı.
- Bağlantı göstergesi: sunucu ya da TikTok bağlantısı yokken overlay'in sol üstünde küçük nokta, `?kilavuz=1` iken yazı; panel sunucuya ulaşamazsa uyarır (QA: duman testi TikTok'suz durumda göstergenin `tiktok` dediğini kontrol ediyor; sunucu kopması elle denenmedi).
- Halay kameraya açık yay (at nalı) oldu: geniş planda herkesin yüzü, ortada davul zurna görünüyor; ortaya çıkan kişinin önü açık (görsel: `halay-2`, `halay-7` önce/sonra karşılaştırıldı).
- Halay ad etiketleri üç kata kaydırılıyor, 12 kişide de okunuyor (görsel: `halay-2`).
- Çekim betiği anı donduruyor ve oyun saatine göre bekliyor: yakın planların beşi de yakalandı; kamera odağının halayda, masada, davulcuda ve takıda çalıştığı görüldü.
- Takılar: göğse gömülü sarı lekeler yerine, çiftin göğsündeki ucu çatallı kırmızı kurdeleye üçer üçer dizilen, değerine göre boyu değişen fiyonklu altınlar; iki kurdele dengeli doluyor (görsel: `taki-3` önce/sonra; QA geçti).
- At yarışı kadrajı: kulvarlar genişledi, kamera yükseltildi; sekiz at ayrı ayrı görünüyor, her atın adı kendi kulvarında atın arkasında okunuyor (görsel: `yaris-1`, `yaris-2` önce/sonra; QA geçti).
