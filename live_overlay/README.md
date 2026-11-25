# Hediye Arenası — TikTok canlı yayın bağış animasyonları

İzleyicilerin hediye (bağış) göndererek katıldığı, yayına overlay olarak eklenen beş etkileşimli animasyon.

| Mod | Nasıl oynanır |
| --- | --- |
| **Yarış** | Hediye gönderen yarışa girer, her jeton ileri taşır. Finişe ilk ulaşan kazanır. |
| **Boss Savaşı** | Her hediye canavara hasar verir. Canavar yenilince en çok vuran MVP olur, seviye artar. |
| **Halat Çekme** | İzleyici yoruma `kırmızı` ya da `mavi` (veya `1` / `2`) yazar, hediyesiyle takımını çeker. Seçmeyen zayıf takıma düşer. |
| **Balon** | Her hediye balonu şişirir. Patlama sınırı gizlidir; patlatan kazanır. |
| **Şans Çarkı** | Hediye gönderen çarka girer, jetonu kadar dilim alır. Süre bitince çark döner. |

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

Adrese parametre ekleyin, örnek: `/overlay?goal=500&round=60`

| Parametre | Varsayılan | Anlamı |
| --- | --- | --- |
| `goal` | 300 | Yarışta finiş için gereken jeton |
| `bossHp` | 500 | 1. seviye canavarın canı (her seviye %50 artar) |
| `tug` | 300 | Halatı kazanmak için gereken jeton farkı |
| `round` | 45 | Çark turunun süresi (saniye) |
| `balloonMin` / `balloonMax` | 120 / 450 | Balonun patlayabileceği jeton aralığı |
| `mode` | — | Overlay'i tek moda sabitler (`race`, `boss`, `tug`, `balloon`, `wheel`) |

## Bilmeniz gerekenler

- TikTok bağlantısı resmî olmayan [TikTokLive](https://github.com/isaackogan/TikTokLive) kütüphanesiyle kurulur. TikTok tarafındaki değişiklikler bağlantıyı geçici olarak bozabilir; böyle bir durumda kütüphaneyi güncelleyin.
- Sunucu yalnızca kendi bilgisayarınızdan erişilecek şekilde (`127.0.0.1`) açılır ve panelde parola yoktur. `--host 0.0.0.0` ile ağa açarsanız ağdaki herkes modu değiştirebilir ve test olayı gönderebilir.
- Çekiliş/ödül vaat eden modları (Çark, Balon) kullanırken TikTok'un canlı yayın ve hediye kurallarına uyduğunuzdan emin olun.
