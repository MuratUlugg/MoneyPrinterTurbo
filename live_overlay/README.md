# Hediye Arenası — TikTok canlı yayın bağış animasyonları

İzleyicilerin hediye (bağış) göndererek katıldığı, yayına overlay olarak eklenen, Türk düğünü ve kültürü temalı beş etkileşimli **3B** animasyon. Sahneler Three.js ile gerçek zamanlı çizilir: ışık, gölge, yüzlü ve kıyafetli insan modelleri, jokeyli atlar.

## Düğün salonu

Halay ve takı töreni aynı salonda geçer: parke pist, sahnede balon takının altında gelinle damat, pankart, düğün pastası, avizeler, ışık dizileri ve pistin çevresinde örtülü masalar.

- **Masaya oturma:** yorum yazan, beğenen ya da takip eden her izleyici, profil fotoğrafıyla bir masaya oturur. Hediye göndermese de düğündedir.
- **Piste çıkma:** hediye gönderen masadan kalkar, halaya girer.
- **Alkış:** büyük hediyelerde ve kazanma anlarında masadakiler alkışlar; halay sürerken damat sahneden tempo tutar.
- Salon boş görünmesin diye birkaç adsız konuk baştan oturur (`konuk` ayarı); izleyiciler geldikçe yerlerini onlara bırakırlar. Bunların adı, fotoğrafı ya da hediyesi yoktur.
- Sahnedeki pankarta çiftin adı yazılabilir: `/overlay?cift=Ayşe+%26+Mehmet`.

### Kalabalık yayınlar

Salon yüzlerce kişilik yayına göre kuruludur:

- **Masalar:** 16 masa, 128 sandalye. Yorum yazan, beğenen ya da takip eden herkes sırayla oturur.
- **Ayaktakiler:** masalar dolunca gelenler duvar diplerinde ayakta durur (88 kişi). O da dolunca en uzun süredir oturan yerini yeni gelene bırakır; yerini bırakan sayaçta kalır.
- **Halay:** en çok hediye gönderen 14 kişi ön sırada, yüzleri ve kıyafetleriyle görünür; sonraki 48 kişi arkada üç sıra hâlinde aynı adımı atar. Ekranda "Halayda 70 kişi · ön sıraya geçmek için 💎 34" yazar: arkadaki, öndekini geçince yer değiştirir.
- **Sayaç:** "Düğünde 330 misafir" yayına katılan herkesi sayar.
- **Çizim:** kalabalık basit figürlerle ve tek seferde çizilir, bu yüzden 300 kişi de 30 kişi kadar hızlıdır. Kamera bir misafire dönünce o kişi ve yanındakiler birkaç saniyeliğine ayrıntılı (yüzlü, kıyafetli) modele çevrilir.

### Kamera

Kamera yukarıdan bakmaz; salondaki bir kameraman gibi çalışır.

- **Geniş plan:** halay, pistin kenarından ve göz hizasına yakın bir yükseklikten, herkes kadrajda olacak uzaklıktan çekilir. Daire büyüdükçe kamera geri çekilir.
- **Yakın plan:** biri hediye gönderince, yorum yazınca ya da takip edince kamera o kişiye üçüncü şahıs yakın planla döner (pistteyse halaycıya, masadaysa masasına), altta adı ve ne yaptığı yazar, birkaç saniye sonra geniş plana geri çekilir.
- **Öncelik:** hediye her zaman yorumdan önce gelir; beğeniler yalnızca ortalık sakinken kamerayı çevirir. Art arda gelen olaylar görüntüyü sürekli bölmesin diye araya kısa bekleme konur.
- **Ortaya çıkan** kişi oynadığı sürece kadrajda kalır.
- **Takı töreninde** kamera önce altını gönderen misafirin masasına döner, altın oradan havalanır, kamera gelinle damada geri döner.
- **At yarışında** yayın kamerası hediye gönderenin atına yaklaşır; **halatta** çeken kişiye.

At yarışında da tribün ve seyirciler vardır.

| Mod | Anahtar | Nasıl oynanır |
| --- | --- | --- |
| **Düğün Halayı** | `halay` | Hediye gönderen, ortasında davul zurna çalan dairesel halaya girer. En çok gönderen mendili sallayan halay başı olur. Tek seferde 100+ jeton gönderen ortaya çıkar, üstüne para saçılır. Coşku çubuğu dolunca halay başı ilan edilir. |
| **At Yarışı** | `race` | Her izleyicinin bir atı olur, her jeton atı ileri taşır. Finişe ilk gelen kazanır. |
| **Takı Töreni** | `taki` | Hediyeler altın olup gelinle damada takılır: çeyrek, yarım, tam altın, bilezik, beşi bir yerde. Takı hedefi dolunca en cömert misafir ilan edilir. |
| **Çay mı Kahve mi?** | `tug` | İzleyici yoruma `çay` ya da `kahve` (veya `1` / `2`) yazar, hediyesiyle halatı kendi tarafına çeker. Seçmeyen zayıf takıma düşer. |
| **Karpuz Patlatma** | `karpuz` | Her hediye karpuza bir lastik takar. Patlama sınırı gizlidir; patlatan kazanır. |

## Hediye göndermeyi teşvik eden mekanikler

Hepsi gerçek hediyelere dayanır; sahte bağışçı, sahte geri sayım ya da şans oyunu yoktur.

- **Hediye menüsü:** başlığın altında, ne gönderirsen ekranda ne olacağını yazan kartlar döner (örneğin "🌹 1+ kalk, halaya gir", "💎 100+ ortaya çık, para saçılsın"). İzleyici neyin karşılığında ne alacağını üç saniyede anlar.
- **Düşük giriş eşiği:** yorum yazan masaya oturur, tek bir Gül gönderen piste çıkar; kamera ona döner, adı alt bantta yazar.
- **Kademeli ödüller (halay):** 30+ jeton davulcuya bahşiştir (kasketine para iliştirilir, tempo coşar, kamera davulcuya döner); 50+ **oyun havasını değiştirir** (çiftetelli → horon → zeybek sırayla; 25 saniye sürer, sonra halaya dönülür; sahnenin üstünde "HORON · Ayşe açtırdı · 20 sn" yazar; her oyunun adımı ve kol duruşu ayrıdır); 100+ ortaya çıkarır ve üstüne para saçılır; 500+ sahnenin önünde yer volkanlarını ateşler.
- **Çelenkler:** yayının en cömert üç ismi adına sahnenin önünde, üzerinde adları ve jeton sayıları yazan çelenkler durur. Sıra değiştikçe çelenk de el değiştirir.
- **Seviye rozetleri:** yayın boyunca toplam hediyeye göre Bronz (10), Gümüş (100), Altın (500), Elmas (2000). Her hediye bildiriminde bir sonraki seviyeye kalan miktar yazar.
- **Liderlik rekabeti:** en çok destekleyen üç kişi hep ekrandadır; altında sıradaki kişinin bir üst sıraya çıkması için gereken net miktar döner. Liderlik el değiştirince "liderliği kaptı, geri almak için X" bildirimi çıkar.
- **Kombo:** 8 saniye içinde art arda gelen hediyeler oyundaki etkiyi %10'ar artırır (en çok 2 kat). Bir kişinin hediyesi başkalarını da hemen göndermeye çeker.
- **Büyük hediye gösterisi:** tek seferde 100+ jeton gönderenin adı ve fotoğrafı birkaç saniye sahnenin üstünü kaplar; 1000+ için "efsane" sürümü.
- **Yayın hedefi:** herkesin katkısıyla dolan ortak çubuk; dolunca kutlanır ve hedef ikiye katlanır.
- **Kalıcı tanınma:** her turun kazananı "son şampiyon" olarak ekranda kalır.

Her modda ayrıca hediye bildirimi, beğeni kalpleri ve takip bildirimi görünür.

## Kurulum

**Kolay yol:** `live_overlay/baslat.bat` (Windows) ya da `live_overlay/baslat.sh` (macOS / Linux) dosyasını çalıştırın. İlk seferde gerekenleri kurar, sonra kontrol panelini tarayıcıda açar. Bilgisayarda Python 3.11 ya da üstü kurulu olmalıdır.

**Elle:**

```bash
pip install -r live_overlay/requirements.txt
python -m live_overlay.server --user tiktok_kullanici_adin
```

- Kontrol paneli: <http://127.0.0.1:8765/>
- Overlay: <http://127.0.0.1:8765/overlay>

`--user` vermeden de başlatıp kullanıcı adını panelden girebilirsiniz. Yayın kapalıysa sunucu 15 saniyede bir yeniden dener ve yayın açılınca kendiliğinden bağlanır.

## Yayına ekleme

- **OBS**: Kaynak ekle → Tarayıcı → adres `http://127.0.0.1:8765/overlay`, genişlik 1080, yükseklik 1920. Tarayıcı kaynağında donanım hızlandırma açık olmalı.
- **TikTok Live Studio**: Kaynak ekle → Bağlantı → aynı adres.

Zemin şeffaftır, kamera görüntüsünün üstüne oturur. Yerleşimi kontrol etmek için adrese `?kilavuz=1` ekleyin: TikTok arayüzünün yaklaşık olarak kapladığı yerler kırmızı gösterilir.

## Kontrol paneli

- **Sahne:** bölümü değiştirir. “Bu turu baştan başlat” sıralamaya dokunmaz; “Yayını bitir, yenisini başlat” raporu arşivler ve ekranı sıfırlar.
- **Düğün programı:** bölümleri verdiğiniz sürelerle sırayla kendiliğinden değiştirir (örneğin 10 dk halay, 6 dk takı töreni). Ekranda “Sıradaki: Takı Töreni · 2:15” yazar.
- **Ayarlar:** tüm eşikler, yayın hedefi, pankart yazısı, ses, kalite. Kaydedince overlay kendiliğinden yenilenir.
- **Overlay durumu:** overlay'in saniyede kaç kare çizdiğini ve hangi kalitede çalıştığını gösterir.
- **Yayın raporu:** toplam jeton, hediye gönderen sayısı, kişi başı ortalama, dakika dakika jeton grafiği, bölümlere göre dağılım, en cömertler, CSV indirme.
- **Tüm zamanlar:** biten yayınların toplamı.

## Güvenilirlik

- **Hiçbir şey kaybolmaz.** Hediyelerin asıl kaydı sunucudadır ve birkaç saniyede bir diske yazılır (`live_overlay/data/`). OBS kaynağı yenilense, overlay çökse ya da sunucu yeniden başlasa bile sıralama, seviyeler, çelenkler ve yayın hedefi geri gelir. Yarım kalan tur (örneğin yarışın o anki durumu) baştan başlar.
- **Otomatik kalite.** Kare hızı saniyede 22'nin altına düşerse overlay kendini kademe kademe kısar: önce gölgeler, sonra çözünürlük, en son kalabalık. Panelden “hep yüksek” ya da “düşük” de seçilebilir.
- **Kalabalık yayın.** Salonda 216 kişilik yer vardır ve kalabalık tek seferde çizilir; aynı anda en çok 10 misafir ayrıntılı modelle gösterilir. İzleyici listesi uzun yayında kendini temizler.
- **İnternetsiz kütüphane.** Three.js yerel kopyadan yüklenir (`static/vendor/`).
- **Ad denetimi.** Küfür, bağlantı ya da telefon numarası içeren adlar ekranda “Misafir” olur. Kendi yasak kelimelerinizi ve adı gizlenecek kullanıcıları panelden ekleyin.
- **Bağlantı sınırı.** TikTok bağlantısı üçüncü taraf bir imza servisinden geçer ve yoğun kullanımda sınıra takılabilir. Anahtarınız varsa sunucuyu başlatmadan önce `TIKTOK_SIGN_API_KEY` ortam değişkenine girin.

## Ses

- **Efektler** (panelde “Davul, altın ve alkış sesi”): davul vuruşu, altın şıngırtısı, alkış. Müzik içermez; müziği yayında siz çalarsınız.
- **Sesli anons** (panelde “Hediyeleri sesli oku”): belirlediğiniz jetonun üstündeki hediyeleri Türkçe okur (“Ayşe, üç tane Gül gönderdi”). `edge-tts` paketi ve internet gerekir; ses dosyaları `data/tts/` klasöründe önbelleğe alınır.

## İlk yayından önce: deneme yayını listesi

1. Sunucuyu başlatın, paneli açın, overlay'i OBS'e ekleyin.
2. Panelden test hediyeleri gönderin; “Overlay durumu” satırında kare hızına bakın. 40 ve üstü iyi, 24'ün altı takılır.
3. Adrese `?kilavuz=1` ekleyip önemli yazıların kırmızı bölgelerin dışında kaldığını kontrol edin; telefonda kendi yayınınızı izleyerek doğrulayın.
4. Kısa, özel bir deneme yayını açın; bir arkadaşınız 1 jetonluk bir hediye ve bir seri hediye göndersin. Ekrandaki ve rapordaki sayının TikTok'taki ile aynı olduğunu doğrulayın.
5. Yayın sırasında OBS kaynağını bir kez yenileyin; sıralamanın geri geldiğini görün.
6. “Yayını bitir, yenisini başlat” ile deneme verisini temizleyin.

## Yayından önce deneme (TikTok'suz)

Paneldeki “Test olayı gönder” bölümü overlay'e sahte hediye, beğeni, takip, paylaşım ve yorum yollar; TikTok'a hiçbir şey gitmez. Sunucusuz hızlı bir bakış için `/overlay?demo=1` adresi rastgele izleyicilerle kendi kendine oynar (bunu yayında kullanmayın).

## Ayarlar

Ayarların hepsi panelden yapılır. Aynı adlar adres çubuğundan da verilebilir ve panel ayarının üstüne yazar, örnek: `/overlay?goal=500&halay=600`

| Parametre | Varsayılan | Anlamı |
| --- | --- | --- |
| `goal` | 300 | At yarışında finiş için gereken jeton |
| `halay` | 400 | Halayda coşkuyu doldurmak için gereken jeton |
| `taki` | 500 | İlk düğünün takı hedefi (her düğünde %50 artar) |
| `tug` | 300 | Halatı kazanmak için gereken jeton farkı |
| `karpuzMin` / `karpuzMax` | 120 / 450 | Karpuzun patlayabileceği jeton aralığı |
| `orta` | 100 | Halayda ortaya çıkmak için tek seferde gereken jeton |
| `bahsis` | 30 | Halayda davulcuya bahşiş sayılan tek seferlik jeton |
| `oyun` | 50 | Halayda oyun havasını değiştiren tek seferlik jeton (çiftetelli → horon → zeybek, 25 sn) |
| `buyuk` | 100 | Büyük hediye gösterisini açan tek seferlik jeton (10 katı "efsane") |
| `hedef` | 2000 | Yayın hedefi (toplam jeton) |
| `cift` | MUTLULUKLAR | Sahnedeki pankart yazısı |
| `konuk` | 6 | Baştan oturan adsız konuk sayısı (en çok 16) |
| `ses` | kapalı | Davul vuruşu, altın şıngırtısı ve alkış sesi |
| `kalite` | oto | `oto` takılırsa kendisi kısar, `yuksek` hiç kısmaz, `dusuk` gölgesiz ve düşük çözünürlükle başlar |
| `anons` / `anonsMin` | kapalı / 10 | Sesli anons ve okunacak en küçük hediye |
| `kilavuz` | — | `kilavuz=1` TikTok arayüzünün yaklaşık yerlerini kırmızı gösterir |
| `mode` | — | Overlay'i tek moda sabitler (tablodaki anahtarlardan biri) |

## 3B modeller ve lisans

Modeller `static/models/` klasöründedir:

| Dosya | Ne | Kaynak |
| --- | --- | --- |
| `Groom.glb` | Takım elbiseli, papyonlu bey (damat ve beyefendi misafirler) | three.js örnek deposu (Ready Player Me avatarı) |
| `Woman.glb` | Hanım misafir | `wass08/r3f-virtual-girlfriend-frontend` deposu (Ready Player Me avatarı) |
| `Man.glb` | Genç erkek misafir, jokeyler | `wass08/r3f-lipsync-tutorial` deposu (Ready Player Me avatarı) |
| `Bride.glb` | Gelin: three.js `female02` modeli, elbisesi beyaza çevrildi, etek, duvak ve buket eklendi | three.js örnek deposu |
| `Horse.glb` | Dörtnala koşan at | three.js örnek deposu (Mirada, ro.me) |

**Para kazanmadan önce lisansı çözün.** Bu modeller açık depolardan alınmış örnek dosyalardır; hiçbiri için ticari kullanım izni doğrulanmadı. Ready Player Me avatarlarının ticari kullanımı Ready Player Me'nin kendi koşullarına bağlıdır. Gelir getiren bir yayında kullanmadan önce ya koşulları kendiniz doğrulayın ya da lisansını satın aldığınız / kendi oluşturduğunuz modellerle değiştirin. Değiştirmek kolaydır: aynı kemik adlarına (`Hips`, `Spine`, `LeftArm`, `LeftUpLeg`…) ve `Wolf3D_Outfit_Top` gibi parça adlarına sahip bir `.glb` dosyasını aynı adla klasöre koymak yeterlidir.

Her izleyicinin karakteri kimliğinden türetilir ve hep aynı kalır: üç gövdeden biri (bey, hanım, genç), kıyafet ve elbise rengi, saç rengi, fötr / kasket / fes / saç, hanımlarda kısa saç / topuz / uzun saç / eşarp ve çizme rengi, bıyık, ten rengi, boy ve kilo. Bilinen sınırlar: aynı gövdeyi alan kişilerin yüzü aynıdır, gelin yerinde durur, at modeli düşük poligonludur.

## Bilmeniz gerekenler

- TikTok bağlantısı resmî olmayan [TikTokLive](https://github.com/isaackogan/TikTokLive) kütüphanesiyle kurulur. TikTok tarafındaki değişiklikler bağlantıyı geçici olarak bozabilir; böyle bir durumda kütüphaneyi güncelleyin.
- Sunucu yalnızca kendi bilgisayarınızdan erişilecek şekilde (`127.0.0.1`) açılır ve panelde parola yoktur. `--host 0.0.0.0` ile ağa açarsanız ağdaki herkes modu değiştirebilir ve test olayı gönderebilir.
- Çekiliş/ödül vaat eden modları (örneğin Karpuz Patlatma) kullanırken TikTok'un canlı yayın ve hediye kurallarına uyduğunuzdan emin olun.
