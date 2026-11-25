# İş listesi

Ralph döngüsü bu dosyayı her turda okur ve günceller (`RALPH.md`). Kapsam: düğün (salon, halay, takı) ve at yarışı.

## Açık: görsel

İlk görsel denetimde (20 çekim) bulunanlar, göze batma sırasıyla.

### Halay
- [ ] **Geniş planda halaycıların çoğunun sırtı görünüyor.** Tam daire göz hizasından çekilince kameraya yakın yarı sırtını dönüyor, yüzler ve ortadaki davul zurna kapanıyor. Halay kameraya açık bir yay (at nalı) olmalı: herkesin yüzü görünsün, ortası boş kalsın.
- [ ] **Adlar üst üste biniyor, okunmuyor** ("KerEceMelis"). 8+ kişide etiketler çakışıyor; çakışanlar kaydırılmalı ya da yalnızca fotoğraf kalmalı.
- [ ] **Ortaya çıkan kişinin önünü bir halaycının sırtı kapatıyor**; kadrajın yarısı pembe bir tişört sırtı.
- [ ] Halaycıların kolları dümdüz yana açık (T duruşu gibi); el ele / omuz omuza tutuş yok, dirsek kırılmıyor.
- [ ] Hanımların hepsi aynı çizme ve aynı saç kesimiyle; yalnızca renk değişiyor.
- [ ] Çekim betiği yakın plan anlarını (halaycı, misafir, davulcuya bahşiş, yer volkanı) yakalayamadı: hepsi geniş plan çıktı. Ya kamera odağı çalışmıyor ya betiğin zamanlaması yanlış; ikisi de doğrulanmalı.
- [ ] Yer volkanları hâlâ hiçbir görüntüde görülmedi.

### Takı töreni
- [ ] **Altınlar düz sarı leke gibi**: çok büyük, yarısı göğse gömülü, hilal şeklinde kesiliyor, altın gibi parlamıyor. Küçük, parlak, kırmızı kurdeleye asılı altın gibi görünmeli.
- [ ] **Arka plan soluk ve boş**: bej perde, üstünde balon takının lekeli gölgesi, düz sarı sahne zemini. Balon takı, pankart ve çiçekler kadraja girmiyor.
- [ ] Damat kolları sarkık, dimdik duruyor; gelin hiç kıpırdamıyor. İkisi birbirine dönük, el ele ya da kol kola durmalı.
- [ ] En cömertler listesi çiftin ayaklarını ve gelinliğin eteğini kapatıyor.
- [ ] "Altını gönderen misafire dön" çekimi misafiri değil çifti gösterdi: kamera odağı takıda çalışmıyor olabilir.

### At yarışı
- [ ] **Atlar üst üste yığılıyor**: sekiz at çapraz tek bir küme hâlinde, kulvarlar ayırt edilmiyor.
- [ ] **Adlar birbirinin ve üstteki çubuğun üstüne biniyor.**
- [ ] **Jokey atın boynuna yatmış, bacakları yere sarkıyor**; eyerde oturmuyor ve ata göre fazla büyük.
- [ ] Atların hepsi aynı kahverengi; don rengi çeşitliliği görünmüyor.
- [ ] Tribün soluk pastel kutular ve beyaz toplar; seyirci gibi durmuyor. Gökyüzü neredeyse görünmüyor.
- [ ] Pist dokusu iri kareli gürültü.
- [ ] Çekim betiğinde "dağılmış" sahnesi dağılmadı (finiş hedefi çok yüksek verildi); betik düzeltilmeli. Finiş anı henüz incelenmedi.

### Genel
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
