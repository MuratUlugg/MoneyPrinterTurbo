# Hediye Arenası — TikTok canlı yayın bağış animasyonları

İzleyicilerin hediye (bağış) göndererek katıldığı, yayına overlay olarak eklenen, Türk düğünü ve kültürü temalı beş etkileşimli **3B** animasyon. Sahneler Three.js ile gerçek zamanlı çizilir: ışık, gölge, yüzlü ve kıyafetli insan modelleri, jokeyli atlar.

| Mod | Anahtar | Nasıl oynanır |
| --- | --- | --- |
| **Düğün Halayı** | `halay` | Hediye gönderen davul zurna eşliğinde halaya girer. En çok gönderen mendili sallayan halay başı olur. Coşku çubuğu dolunca halay başı ilan edilir. |
| **At Yarışı** | `race` | Her izleyicinin bir atı olur, her jeton atı ileri taşır. Finişe ilk gelen kazanır. |
| **Takı Töreni** | `taki` | Hediyeler altın olup gelinle damada takılır: çeyrek, yarım, tam altın, bilezik, beşi bir yerde. Takı hedefi dolunca en cömert misafir ilan edilir. |
| **Çay mı Kahve mi?** | `tug` | İzleyici yoruma `çay` ya da `kahve` (veya `1` / `2`) yazar, hediyesiyle halatı kendi tarafına çeker. Seçmeyen zayıf takıma düşer. |
| **Karpuz Patlatma** | `karpuz` | Her hediye karpuza bir lastik takar. Patlama sınırı gizlidir; patlatan kazanır. |

Her modda ayrıca hediye bildirimi, beğeni kalpleri, takip bildirimi ve en çok destekleyen üç kişi görünür.

## Kurulum

```bash
pip install -r live_overlay/requirements.txt   # fastapi ve uvicorn ana projeyle gelir
python -m live_overlay.server --user tiktok_kullanici_adin
```

- Kontrol paneli: <http://127.0.0.1:8765/>
- Overlay: <http://127.0.0.1:8765/overlay>

`--user` vermeden de başlatıp kullanıcı adını panelden girebilirsiniz. Yayın kapalıysa sunucu 15 saniyede bir yeniden dener ve yayın açılınca kendiliğinden bağlanır.

## Yayına ekleme

- **OBS**: Kaynak ekle → Tarayıcı → adres `http://127.0.0.1:8765/overlay`, genişlik 1080, yükseklik 1920.
- **TikTok Live Studio**: Kaynak ekle → Bağlantı → aynı adres.

Zemin şeffaftır, kamera görüntüsünün üstüne oturur. Üstteki ve alttaki boşluklar TikTok arayüzü (profil, sohbet) için bırakılmıştır.

## Yayından önce deneme

Paneldeki “Test olayı gönder” bölümü overlay'e sahte hediye, beğeni, takip ve yorum yollar; TikTok'a hiçbir şey gitmez. Sunucusuz hızlı bir bakış için `/overlay?demo=1` adresi rastgele izleyicilerle kendi kendine oynar (bunu yayında kullanmayın).

## Ayarlar

Adrese parametre ekleyin, örnek: `/overlay?goal=500&halay=600`

| Parametre | Varsayılan | Anlamı |
| --- | --- | --- |
| `goal` | 300 | At yarışında finiş için gereken jeton |
| `halay` | 400 | Halayda coşkuyu doldurmak için gereken jeton |
| `taki` | 500 | İlk düğünün takı hedefi (her düğünde %50 artar) |
| `tug` | 300 | Halatı kazanmak için gereken jeton farkı |
| `karpuzMin` / `karpuzMax` | 120 / 450 | Karpuzun patlayabileceği jeton aralığı |
| `mode` | — | Overlay'i tek moda sabitler (tablodaki anahtarlardan biri) |

## 3B modeller

Modeller `static/models/` klasöründedir ve hepsi [three.js örnek deposundan](https://github.com/mrdoob/three.js/tree/dev/examples/models) alınmıştır:

- `Groom.glb`: takım elbiseli, papyonlu, yüzlü erkek (Ready Player Me avatarı). Damat, halaycılar, davulcu, zurnacı, halat takımları ve jokeyler bu modelden üretilir; ceket ve pantolon rengi kişiye göre değişir, jokeylere kask takılır.
- `Bride.glb`: yüzlü kadın modeli (three.js `female02`). Elbisesi beyaza çevrilmiş, üzerine uzun etek, duvak ve buket eklenmiştir. İskeleti yoktur, yerinde durur.
- `Horse.glb`: dörtnala koşan at (Mirada, ro.me).

Bilinen sınırlar: halaycıların hepsi aynı erkek modelidir (yalnızca kıyafet rengi ve başının üstündeki profil fotoğrafı farklıdır), at modeli düşük poligonludur. Ticari yayında kullanmadan önce modellerin kullanım koşullarını kontrol edin. Kendi modelinizi kullanmak için aynı kemik adlarına (`Hips`, `Spine`, `LeftArm`, `LeftUpLeg`…) sahip bir `.glb` dosyasını `Groom.glb` yerine koyun.

Three.js kütüphanesi CDN'den yüklenir, bu yüzden overlay'in açıldığı bilgisayarda internet gerekir. OBS tarayıcı kaynağında donanım hızlandırma açık olmalıdır.

## Bilmeniz gerekenler

- TikTok bağlantısı resmî olmayan [TikTokLive](https://github.com/isaackogan/TikTokLive) kütüphanesiyle kurulur. TikTok tarafındaki değişiklikler bağlantıyı geçici olarak bozabilir; böyle bir durumda kütüphaneyi güncelleyin.
- Sunucu yalnızca kendi bilgisayarınızdan erişilecek şekilde (`127.0.0.1`) açılır ve panelde parola yoktur. `--host 0.0.0.0` ile ağa açarsanız ağdaki herkes modu değiştirebilir ve test olayı gönderebilir.
- Çekiliş/ödül vaat eden modları (örneğin Karpuz Patlatma) kullanırken TikTok'un canlı yayın ve hediye kurallarına uyduğunuzdan emin olun.
