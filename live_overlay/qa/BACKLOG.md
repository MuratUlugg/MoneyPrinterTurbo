# İş listesi

Ralph döngüsü bu dosyayı her turda okur ve günceller (`RALPH.md`). Kapsam: düğün (salon, halay, takı) ve at yarışı.

## Açık: görsel

İlk görsel denetimde (20 çekim) bulunanlar, göze batma sırasıyla.

### Halay
- [ ] Hanımların hepsi aynı çizme ve aynı saç kesimiyle; yalnızca renk değişiyor.
- [ ] Davulcu yakın planında komşu halaycıların kolları kadraja giriyor, davul görüntünün üçte birini kaplıyor.

### Takı töreni
- [ ] Gelinle damat el ele ya da kol kola değil; gelinin kolları hiç oynamıyor (iskeletsiz model).
- [ ] Takı yokken kurdeleler göğüste boş kırmızı dikdörtgen gibi duruyor; ilk takıya kadar gizlenebilir ya da daha ince olabilir.

### At yarışı
- [ ] Yakın at planında öndeki kulvardaki at kadrajın altını kaplayabiliyor.
- [ ] Tribün soluk pastel kutular ve beyaz toplar; seyirci gibi durmuyor. Gökyüzü neredeyse görünmüyor.

### Genel

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
- Jokey artık eyerde: dizler yukarıda atı kavrıyor, gövde öne eğik, kollar dizginlere uzanıyor, ata göre boyu küçüldü (görsel: `yaris-3` önce/sonra; QA geçti).
- At donları: doru, al, kır, yağız, kula, beyaz, koyu doru ve bej; yele ve kuyruk ayrı renkte, pistteki atlar birbirinden farklı (görsel: `yaris-1`, `yaris-3` önce/sonra; QA geçti).
- Renk uzayı: malzeme renkleri doğrusal uzaya çevriliyor; kıyafetler, halı, pist ve atlar artık pastel değil doygun, kurdele kırmızı (görsel: halay, takı ve yarışın önce/sonra karşılaştırması; QA geçti).
- Takı kadrajı: geniş açıyla balon takı çifti çerçeveliyor, sahne kırmızı halılı, en cömertler tek satırda ve çiftin ayaklarını kapatmıyor (görsel: `taki-3` önce/sonra; QA geçti).
- Çiftin duruşu: damat geline dönük, kolları dirsekten kırık ve rahat; gelin hafifçe salınıp nefes alıyor; ikisi birbirine yaklaştı; balonların perdedeki lekeli gölgesi kalktı (görsel: `taki-0` önce/sonra; QA geçti).
- Halay yakın planı: salon kapalı kutu oldu (ön duvar, tavan), arkada karanlık boşluk yok; kasketin altında saç var ve başa oturuyor; mendil küçük, kırmızı kenarlı ve kıvrımlı (görsel: `halay-3` önce/sonra; QA geçti).
- Halay figürü: eller aşağıda ve dirsekler kırık (el ele tutuş), iki vuruşta çök-kalk, omuz silkme; kollar artık T duruşunda değil (görsel: `halay-2` önce/sonra; hareketin kendisi yalnızca durağan karelerde görüldü, videoyla doğrulanmadı; QA geçti).
- Pist: iri kareli gürültü yerine ince taneli kum, tırmık izleri ve kulvar çizgileri (görsel: `yaris-1`, `yaris-3` önce/sonra; QA geçti).
- Büyük hediye bandı sahnenin üstünden başlık bölgesine taşındı; yarışta atları, halayda ortaya çıkanı kapatmıyor. Sol kenarda kesilen at adı fotoğrafın sağına yazılıyor (görsel: `yaris-2-tam-ekran` önce/sonra, `halay-6-tam-ekran`; QA geçti).
- Yer volkanları: pistin arka kenarına ve sahnenin iki yanına taşındı, kıvılcımlar yumuşak parlak nokta oldu ve sayısı kare hızından bağımsız; ortaya çıkanın arkasında ilk kez görüntülendi (görsel: `halay-6`, `halay-7`; QA geçti).
- Finiş çekimi: kazanan belli olunca kamera takın önüne geçip atların çizgiye gelişini karşıdan gösteriyor, alt bantta "finişe geliyor"; kutlama kartı ondan sonra çıkıyor (görsel: `yaris-4`, ilk kez yakalandı; QA geçti).
