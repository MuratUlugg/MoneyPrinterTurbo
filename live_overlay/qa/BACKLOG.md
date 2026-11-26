# İş listesi

Ralph döngüsü bu dosyayı her turda okur ve günceller (`RALPH.md`). Kapsam: düğün (salon, halay, takı) ve at yarışı.

## Açık: görsel

İlk görsel denetimde (20 çekim) bulunanlar, göze batma sırasıyla.

### Halay

### Takı töreni
- [ ] Gelinle damat el ele ya da kol kola değil; gelinin kolları hiç oynamıyor (iskeletsiz model).

### At yarışı
- [ ] Yakın at planında öndeki kulvardaki at kadrajın altını kaplayabiliyor.

### Genel

### Kalabalık
- [ ] Arka sıraların sol bacak kalkışı kodda var ama görüntüde ayırt edilemedi.
- [ ] 500 kişilik gerçek yük hiç denenmedi: test 330 kişiyle ve saniyede 1 kare çizen ekran kartsız makinede yapıldı.

## Açık: özellik

Kullanıcı isteği: yeni özellikler. Sırayla, turda bir tane. Hepsi düğün ve at yarışı için; hiçbiri sahte bağışçı, sahte geri sayım ya da şans oyunu içermez.

- [ ] **Oyun havası değişimi (düğün).** Belirli tutarın üstündeki hediye oyunu değiştirir: halay → çiftetelli → horon → zeybek. Her oyunun kendi adımı ve kol duruşu var; alt bantta "Ayşe horon açtırdı". Hediye atanın ekranda anında ve herkesçe görülen bir etkisi olur.
- [ ] **Yorum balonu (düğün).** Masadaki misafirin yazdığı yorum kısa süre başının üstünde konuşma balonunda görünür (ad denetiminden geçer). Bedava katılım; salonu canlı gösterir.
- [ ] **Start kapısı ve tur düzeni (yarış).** Boş pist yerine kapıda bekleyen atlar, "3-2-1" ile gerçek start, tur bitince kürsü töreni: ilk üç at, kupa, sahiplerinin adı. Boş pist notunu da kapatır.
- [ ] **Taraftar desteği (yarış).** İzleyici yorumla bir ata taraf olur ("3"); taraftarların beğenisi ve hediyesi o atı da iter, tribünde o atın renginde bayraklar sallanır. Bahis değil: ödül ya da para yok, yalnızca destek.
- [ ] **Pasta kesme (düğün).** Coşku %100 olunca gelin-damat pastayı keser, salon ayağa kalkar, havai fişek; en cömert üç kişinin adı pastanın yanında. Hedefe gerçek hediyelerle ulaşılır.
- [ ] **Şeref masası (düğün).** En cömert üç kişi sahnenin yanındaki süslü masaya oturur, önlerinde ad kartı; sıralama değişince yer değişir.
- [ ] **At adı ve ahır (yarış).** Her izleyicinin atının kalıcı bir adı olur (Şahbatur, Gülbatur…), kazandığı yarışlar sayılır; etikette yıldız olarak görünür.
- [ ] **Damat halaya iniyor (düğün).** Büyük hediyede damat sahneden inip halayın başına geçer, hediyeyi atanla yan yana oynar.

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
- Tribün: yedi sıra, canlı renkli formalar, ten ve saç renkleri, bazıları ayakta; beyaz toplar ve pastel kutular gitti (görsel: `yaris-4` önce/sonra; QA geçti).
- Hanımlarda çeşitlilik: kısa saç, topuz, uzun saç ya da eşarp; dört ayrı çizme rengi (görsel: `halay-2` önce/sonra, `halay-5`'te topuz ve eşarp görüldü; uzun saç görüntüde yakalanmadı; QA geçti).
- Halay mekaniği yeniden yazıldı (kullanıcı geri bildirimi): omuz omuza tek sıra, komşuların elleri aynı noktada buluşuyor (kol omuzdan hedefe nişanlanıyor), herkes aynı anda dört vuruşluk adımı atıyor (sağa adım, sol ayağı çek, çök, sol tekme), sıra adımla birlikte kayıyor; baştaki mendil sallıyor, sondakinin eli belinde; davul zurna sıranın sağında (görsel: `halay-2`, `halay-8` el yakın planı, `halay-9` dört vuruş; QA geçti).
- Ölçek (kullanıcı geri bildirimi): 16 masa × 8 sandalye (128 oturan) + duvar diplerinde 88 ayakta misafir; halayda 14 kişilik ön sıra + 48 kişilik arka sıralar; kalabalık birkaç çizim çağrısıyla çiziliyor, kameranın döndüğü misafir ve komşuları ayrıntılı modele çevriliyor; "Düğünde N misafir" sayacı ve "ön sıraya geçmek için" çağrısı (görsel: `kalabalik-0..3`, 330 kişiyle; QA geçti).
- Kalabalık figürleri: kutu yerine omuzlu gövde, kollar ve ayrı bacaklar; yakın planda odaktaki misafirin komşuları da ayrıntılı modele çevriliyor, alt bantla çakışan yazı gizleniyor (görsel: `kalabalik-0`, `-2`, `-4` önce/sonra; QA geçti).
- Grafik turu (kullanıcı geri bildirimi; sahneler tam çözünürlükte tek tek incelendi): çalgıcıların zombi gibi dümdüz kolları dirsekten kırıldı, zurna inceldi ve ellerde; kasket başa oturdu; halay ve takı kadrajı yaklaştı; misafir sayacı sahnenin ortasından başlığa taşındı; çubukların başındaki yuvarlak leke kalktı; büyük hediyede sahneye saçılan renkli noktalar azaltıldı; yarış etiketleri küçüldü ve atları kapatmıyor; takı sıralaması kenardan taşmıyor (görsel: halay-1, halay-2, taki-3, yaris-2 önce/sonra; QA geçti).
- Takı kurdelesi ilk takıyla beliriyor ve takı sırası arttıkça uzuyor; boşken göğüste kırmızı levha yok (görsel: `taki-0`, `taki-2`, `taki-3`; QA geçti).
- Yakın plan ayrıntıları: sandalyelere ayak eklendi (havada duran levha gibiydi), kasket saçı örtüyor, davul küçüldü ve kadrajı kaplamıyor, bahşiş parası kasketin önüne iliştirildi, topuz küçüldü, kadrajın üstünde kesilen ad etiketi çizilmiyor (görsel: `halay-3`, `halay-5` önce/sonra; QA geçti).
- [not] Kasketin altında şakakta gri saç şeridi görünüyor; davulcunun sol eli davula tam değmiyor.
- Yarış: jokeyin altına eyer ve kendi renginde eyer örtüsü eklendi; yakın planda atın uzağında kalan ad etiketi kaldırıldı (görsel: `yaris-3` önce/sonra; QA geçti). Dizgin iki kez denendi, atın başından ileri taşan çubuklar gibi durduğu için geri alındı: atın başı canlandırma ile oynadığından sabit bir çubuk tutmuyor.
- Halay adımı doğrulandı: çekim betiği her vuruşu tam ortasında donduruyor; sağa adım, çökme ve sol tekme karelerinde herkesin aynı anda aynı hareketi yaptığı görüldü. Eller yaklaştırıldı (omuz aralığı .5), geniş plan soldaki halaycıları kesmiyor ve çalgıcıları da alıyor (görsel: `halay-2`, `halay-9-adim-0/2/3`; QA geçti). Geniş planın son uzaklık ayarı (biraz yaklaştırma) yeniden çekilmedi.
- El tutuşu: halaycıların parmakları kıvrılıyor (açık avuç yerine kavrayan el); el yakın planı için kamera açısı eklendi (görsel: `halay-8`; QA geçti). Komşu eller arasında hâlâ birkaç santimlik boşluk var: iki farklı boydaki modelin eli tam aynı noktaya gelmiyor.
- Takı yakın planı: misafirin yüzünün üstüne binen "ilk takıyı sen tak" yazısı ve küçük fotoğraf yakın planda gizleniyor; gelinin kurdelesi göğsün altından başlıyor ve elbisenin önünde duruyor; en cömertler şeridi içindeki kişi sayısı kadar geniş (görsel: `taki-1`, `taki-3` önce/sonra; QA geçti).
- Sofra: her sandalyenin önünde altın kenarlı tabak, bardak ve kırmızı peçete; masalar boş beyaz yüzey değil (görsel: `taki-1`; QA geçti). QA kapısına overlay betiği için sözdizimi denetimi eklendi: bu turda aynı adı iki kez tanımlayan bir hata sahneyi hiç açtırmadı ve çekimler eskidi; artık ilk adımda yakalanıyor.
- Kalabalık: figürlere yüz eklendi (gözler, gülümseme, yanak), masa çiçeği küçüldü; 8'den fazla halaycı varken etiketler küçük fotoğrafa indi ve adlar ekranı kaplamıyor (görsel: `kalabalik-0`, `kalabalik-4` önce/sonra; QA geçti). Halay başının adının tacın üstüne alınması yeniden çekilmedi.
- Yarış etiketleri: ad ve fotoğraf artık her atın tam üstünde, koyu bir hap içinde; önceden atın gerisinde boşlukta duruyor ve hangi adın hangi ata ait olduğu karışıyordu. İlk denemede etiketler bir arkadaki kulvara kaydı (yüksek noktayı izdüşürmek yüzünden); jokeyin başını izdüşürüp ekranda yukarı kaydırarak düzeltildi (görsel: `yaris-1`, `yaris-2` önce/sonra; QA geçti). Etiketi 12 piksel daha yukarı alan son ayar yeniden çekilmedi.
- Ortada oynayan: kollar dümdüz yana açık (T duruşu) yerine omuz üstünde, dirsekten yukarı kırık ve sırayla kalkıyor. İlk denemede önkol ters yöne kırıldı ve eller öne sarktı; işaret çevrilerek düzeltildi (görsel: `halay-7` üç çekim; QA geçti).
- Bacak yönü hatası bulundu ve düzeltildi: bu modelde uyluk +x ile öne gidiyor; kod tersini varsayıyordu. Sonuç: masadaki ayrıntılı misafirlerin bacakları sandalyenin arkasından geriye uzanıyordu (ayak konumu ölçüldü: -0,5 m; düzeltmeden sonra +0,5 m) ve halay tekmesi arkaya atılıyordu. İkisi de çevrildi; tekme artık kameraya doğru, öne (görsel: yandan oturma çekimi, `halay-9-adim-2/3`; QA geçti).
- Jokeyin bacakları: doğrulanan yön kuralıyla (uyluk öne) yeniden kuruldu, görüntüde ayaklar atın karnından aşağı sarktı; geri alındı. Eski duruş (uyluklar geriye katlı, eyerde diz çökmüş gibi) bilerek bırakıldı ve koda not düşüldü (görsel: `yaris-3` önce/sonra).
- Tam görsel denetim (26 çekim): yalnızca küçük rötuş çıktı. Takıda kamera hedefi alçaltıldı, çiftin ayakları ve gelinliğin eteği sıralama şeridinin üstünde tam görünüyor (görsel: `taki-3`); halayda fotoğraf etiketleri başın biraz üstüne alındı (yeniden çekilmedi). **Durma sayacı: 1/2** (art arda iki denetim yalnızca küçük rötuş bulursa döngü durur).
- Oturan misafirin göğsündeki altın üçgen: sandalye arkalığı omuzdan yüksekti ve yakanın açıklığından görünüyordu (bacak yönü düzeltmesi bunu gidermemişti). Arkalık alçaltıldı, oturan biraz yükseltildi; üçüncü denemede kayboldu (görsel: `halay-4` dört çekim; QA geçti). İkinci denetim gerçek bir kusur bulduğu için **durma sayacı sıfırlandı: 0/2**.
- Alkış duruşu: misafirlerin kolları dümdüz öne uzanıyordu (hortlak gibi); artık dirsekler kırık, eller göğüs önünde. Kalabalık halayda üst üste binip kesilen halay başı adı kaldırıldı, taç kalıyor (görsel: `kalabalik-2` önce/sonra; QA geçti). Gerçek kusur bulundu: durma sayacı 0/2.
- Yarış denetimi (6 çekim, tek tek açıldı): etiketler atların üstünde ve okunuyor, finiş çekimi ve tribün yerinde; yalnızca küçük rötuş çıktı. Eyer örtüsü düz bir levhaydı ve yakın planda atın yanından dışarı taşan tahta gibi duruyordu; artık sırtı saran kavisli bir örtü (görsel: `yaris-3` önce/sonra; QA geçti). Kalan küçük notlar: atın kuyruğu köşeli, uzak kulvarlarda etiketler birbirine yakın. **Durma sayacı: 1/2** (sıradaki tur düğün sahnelerini denetler; orada da yalnızca rötuş çıkarsa döngü durur).
- Düğün denetimi (20 çekim, sekizi tam çözünürlükte tek tek açıldı): halay sırasında sahnedeki damat kolları iki yana açık, kalıp gibi duruyordu (boş pistte ve halayın arkasında görünüyordu); artık tempo tutup alkışlıyor, eller göğüs önünde (görsel: `halay-0` önce/sonra; QA geçti). Gerçek kusur bulundu: **durma sayacı sıfırlandı: 0/2**.
- Kasket ve mendil: kasketin altında saç şakağa ve enseye iniyor, kasket lacivert ve saçtan ayrışıyor (önceden altı kel, kask gibiydi); mendil ince kenarlı ve kıvrımlı bir bez (önceden kalın çerçeveli karton gibiydi). İlk denemede saç kasketin tepesinden taştı, kasket yükseltilerek düzeltildi (görsel: `halay-3` üç çekim, `halay-5`; QA geçti). Kasket hâlâ biraz yüksek ve yuvarlak. Durma sayacı 0/2.
- Halay geniş planı ve bahşiş: kamera uzaklığı gerçek yatay görüş açısına göre hesaplanıyor, 12 halaycı ve iki çalgıcı kenarda kesilmeden görünüyor; bahşiş parası kasketin yanına iliştirildi, davulcunun alnını ve gözlerini kapatmıyor (görsel: `halay-2` önce/sonra, `halay-5` üç çekim; QA geçti). Para biraz havada duruyor gibi; küçük rötuş. Açık görsel iş kalmadı; sıradaki tur baştan tam denetim. Durma sayacı 0/2.
- Tam denetim (26 çekim yeniden alındı; bu turda el yakın planı, tekme adımı, büyük hediye tam ekranı ve iki takı çekimi açıldı, diğerleri son üç turda düzeltmelerden sonra açılmıştı): yalnızca küçük rötuş çıktı. "tam altın taktı!" bildirimi damadın şapkasını kesiyordu; bildirim inceltildi ve şapkanın üstünde bitiyor (görsel: `taki-2` önce/sonra; QA geçti). Bilinen ve kalan: komşu eller arasında birkaç santim boşluk (`halay-8`). **Durma sayacı: 1/2.**
- Kalabalık denetimi (6 çekim, beşi tek tek açıldı): kalabalıkta bir misafire yakın planda, kamerayla misafirin arasında duran başka bir misafirin başı ve şapkası kadrajın ortasını kapatıyordu. Artık kamera hattında kalanlar çekim boyunca gizleniyor, çekim bitince geri geliyor (görsel: `kalabalik-2` önce/sonra; QA geçti; geri gelişleri görüntüyle doğrulanmadı). Gerçek kusur bulundu: **durma sayacı sıfırlandı: 0/2**.
- [not] Masa yakın planında (`kalabalik-4`) kalabalık figürleri oyuncak gibi; bu çekim yalnızca denetim kamerasıyla alınıyor, yayında kamera bir misafire dönünce çevresi ayrıntılı modele çevriliyor. Fesli misafirin alnı açık, saçı yanlarda (`kalabalik-2`).
- Tam denetim (32 çekim yeniden alındı; bu turda yedisi açıldı: masadaki misafir, dört kişilik halay, ortada oynayan, boş pist, takı tam ekranı, kalabalık halay tam ekranı, kalabalıkta misafir yakın planı): yalnızca küçük rötuş çıktı. Sahne çerçevesinin dışına taşan yarım misafir rozeti artık çizilmiyor (QA geçti; yeniden çekilmedi, gözle doğrulanmadı). Kalabalıkta misafir yakın planı ikinci çekimde de açık. **Durma sayacı: 1/2.**
- [not] Boş pist (`yaris-0`) yalnızca kum ve çağrı yazısı; ilk hediye gelene kadar sahne boş. Yayın hedefi çubuğundaki yazı küçük ve çubuğun ucuna sıkışık (`taki-3-tam-ekran`).
- İkinci tam denetim (kalabalık yeniden çekildi; beş çekim açıldı: kalabalık halay tam ekranı, 12 kişilik halay tam ekranı, yarış tam ekranı, finiş, halayın ilk adımı): gerçek kusur çıkmadı, kod değişmedi. Çerçeve dışına taşan yarım rozetin gittiği görüldü (`kalabalik-0-tam-ekran`). Küçük notlar: 12 kişilik geniş planda halaycılar küçük, önde boş pist zemini geniş; uçuşan nota simgesi ara sıra bir halaycının yüzüne denk geliyor; büyük hediyede birkaç kıvılcım noktası sahne çerçevesinin dışına düşüyor. **Durma sayacı: 2/2 — döngü durdu.**
