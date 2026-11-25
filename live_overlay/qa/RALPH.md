# Ralph döngüsü: Hediye Arenası'nı her turda bir adım iyileştir

Bu dosya döngünün her turunda baştan okunur. Tek bir turda **tek bir iş** bitirilir; iş bitmeden yenisine geçilmez.

## Tur

1. **ANALİZ.** `live_overlay/qa/BACKLOG.md` dosyasını oku. Açık işlerden en değerlisini seç (sıra: yayında para kaybettiren hata → geliri artıran → görsel kalite → kod sağlığı). Liste boşsa ya da yalnızca "kullanıcıda" işleri kaldıysa ürün sahibi gözüyle yeniden denetle: son QA ekran görüntülerine tek tek bak, kodu oku, yeni bulguları listeye yaz.
2. **KODLA.** Seçtiğin işi yap. Küçük ve geri alınabilir tut; ilgisiz yeri elleme. Yalnızca `live_overlay/` ve `test/services/test_live_overlay.py` değişir.
3. **QA.** `live_overlay/qa/run.sh <python>` çalıştır. Kapı: birim testleri + duman testi geçmeli. Yeni davranış için kontrol yoksa önce kontrolü ekle (birim testi ya da `smoke.js`). Ekran görüntülerine gözle bak: kayma, üst üste binme, boş sahne, okunmayan yazı var mı?
4. **KALİTE KONTROL.** `git diff`'i oku. Sor: Geriye dönük bir şey bozuldu mu? Yayında çökerse ne olur? Yorumlar nedenini anlatıyor mu? README güncel mi?
5. **KAYDET.** QA geçtiyse commit + push. Geçmediyse düzelt; iki denemede düzelmezse değişikliği geri al ve işi listeye "denendi, şu yüzden olmadı" notuyla yaz.
6. **LİSTEYİ GÜNCELLE.** Biten işi "Bitenler"e taşı (bir satır: ne değişti, nasıl doğrulandı). Yolda gördüğün yeni sorunları "Açık" bölümüne ekle.

## Değişmez kurallar

- QA kırmızıyken push yok. Testi susturmak, atlamak ya da beklentiyi gevşetmek çözüm değildir.
- İzleyiciyi yanıltan hiçbir şey eklenmez: sahte bağışçı, sahte geri sayım, sahte "az kaldı", ödüllü şans oyunu yok. Ekrandaki her 💎 gerçek jetondur.
- Lisansı belirsiz yeni model ya da görsel eklenmez; eklenirse README'deki lisans tablosuna kaynağıyla yazılır.
- Doğrulanamayan şey "yapıldı" diye yazılmaz. Göremediysen "gözle doğrulanmadı" de.

## Durma koşulu

Şunlardan biri olunca döngüyü bitir ve kullanıcıya kısa bir özet yaz (ne bitti, ne kaldı, neden kaldı):

- Art arda iki turda, "küçük rötuş"un üstünde bir iş bulunamadı.
- Açık kalan işlerin hepsi kullanıcıya bağlı (gerçek yayın denemesi, lisans, model, ürün kararı).
- Aynı iş iki turda da QA'dan geçemedi ve geri alındı: dur, nedenini yaz.
