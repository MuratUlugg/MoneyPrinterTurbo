# Ralph döngüsü: Hediye Arenası'nı her turda bir adım iyileştir

Bu dosya döngünün her turunda baştan okunur. Tek bir turda **tek bir iş** bitirilir; iş bitmeden yenisine geçilmez.

## Kapsam

Yalnızca **düğün** (salon, halay, takı töreni) ve **at yarışı**. Halat ve karpuz bölümlerine, kod düzenine ve belgelere bu aşamada dokunulmaz; bunlar listede "Sonraya" bölümünde bekler. Tek istisna: kapsamdaki bir işin bozduğu şeyi onarmak.

**Aşama: yeni özellikler.** Her turda "Açık: özellik" bölümünün en üstündeki iş yapılır. Özellik bitmiş sayılmaz, ta ki: (1) görüntüde çalıştığı görülene, (2) `smoke.js` ya da birim testinde bir kontrolü olana, (3) `visual.js`'te en az bir çekimi olana, (4) README'de ve panelde (ayarı varsa) yeri olana kadar. Yeni özelliğin getirdiği görsel kusur aynı turda düzeltilir; ekranda görünen kusur yine her şeyden önce gelir.

## Tur

1. **ANALİZ.** `live_overlay/qa/BACKLOG.md` dosyasını oku. Önceki turun özelliği görsel kusur bıraktıysa önce onu düzelt. Yoksa "Açık: özellik" bölümünün en üstündeki işi seç; o bölüm boşsa "Açık: görsel", sonra "Açık: diğer". Hepsi boşsa görsel denetimi (aşağıda) baştan yap ve bulguları listeye yaz.
2. **KODLA.** Seçtiğin işi yap. Küçük ve geri alınabilir tut; ilgisiz yeri elleme. Yalnızca `live_overlay/` ve `test/services/test_live_overlay.py` değişir.
3. **QA.** `live_overlay/qa/run.sh <python>` çalıştır. Kapı: birim testleri + duman testi geçmeli. Yeni davranış için kontrol yoksa önce kontrolü ekle (birim testi ya da `smoke.js`). Sonra **görsel denetimi** yap (aşağıda): değiştirdiğin sahnenin önceki ve sonraki görüntüsünü yan yana koyup bak. "QA geçti" görsel olarak iyi demek değildir.
4. **KALİTE KONTROL.** `git diff`'i oku. Sor: Geriye dönük bir şey bozuldu mu? Yayında çökerse ne olur? Yorumlar nedenini anlatıyor mu? README güncel mi?
5. **KAYDET.** QA geçtiyse commit + push. Geçmediyse düzelt; iki denemede düzelmezse değişikliği geri al ve işi listeye "denendi, şu yüzden olmadı" notuyla yaz.
6. **LİSTEYİ GÜNCELLE.** Biten işi "Bitenler"e taşı (bir satır: ne değişti, nasıl doğrulandı). Yolda gördüğün yeni sorunları "Açık" bölümüne ekle.

## Görsel denetim

`live_overlay/qa/run.sh <python> gorsel` düğün ve yarışın belirli anlarını 3B pencere çözünürlüğünde çeker (`$QA_OUT/gorsel-*.png`). Görüntüleri **küçültmeden ya da en çok dörtlü sayfalar hâlinde** aç ve her birine şu sorularla bak:

- **Okunabilirlik:** adlar ve etiketler üst üste biniyor mu, çubukların ya da başka yazıların üstüne taşıyor mu?
- **Kadraj:** asıl konu (halaycıların yüzü, gelin-damat, öndeki at) görünüyor mu, yoksa sırt, boş zemin ya da duvar mı görüyoruz? Biri kadrajı kapatıyor mu?
- **Kişiler:** duruş doğal mı (kollar, bacaklar, oturuş, binicilik)? Biri bir şeyin içinden geçiyor mu, havada mı duruyor?
- **Nesneler:** ölçek doğru mu, bir şey başka bir şeyin içine gömülmüş mü, düz renkli leke gibi duran var mı?
- **Işık ve renk:** sahne soluk, düz ya da patlamış mı? Zemin, duvar ve kişiler birbirinden ayrışıyor mu?
- **Çeşitlilik:** aynı görünen kişiler ya da atlar yan yana mı?
- **An yakalandı mı:** çekimin adı "yakın plan" ama görüntü geniş plansa bu da bir bulgudur (ya kamera ya çekim betiği bozuk).

Bir görüntüde kusur gördüysen ve o turun işi değilse listeye yaz; "sonra bakarım" diye geçme.

## Değişmez kurallar

- QA kırmızıyken push yok. Testi susturmak, atlamak ya da beklentiyi gevşetmek çözüm değildir.
- İzleyiciyi yanıltan hiçbir şey eklenmez: sahte bağışçı, sahte geri sayım, sahte "az kaldı", ödüllü şans oyunu yok. Ekrandaki her 💎 gerçek jetondur.
- Lisansı belirsiz yeni model ya da görsel eklenmez; eklenirse README'deki lisans tablosuna kaynağıyla yazılır.
- Çekim betiği bir görüntüyü yeniden üretmediyse (çıktıda "çekildi <ad>" satırı yoksa) o görüntü eskidir; ona bakıp karar verilmez. Uzun tek satırlık koda `//` yorumu eklenmez (satırın devamını yutar); `/* */` kullanılır.
- Doğrulanamayan şey "yapıldı" diye yazılmaz. Göremediysen "gözle doğrulanmadı" de.

## Durma koşulu

Şunlardan biri olunca döngüyü bitir ve kullanıcıya kısa bir özet yaz (ne bitti, ne kaldı, neden kaldı):

- "Açık: özellik" dahil bütün "Açık" bölümleri boş ve art arda iki turda görsel denetim "küçük rötuş"un üstünde bir kusur bulamadı.
- Açık kalan işlerin hepsi kullanıcıya bağlı (gerçek yayın denemesi, lisans, model, ürün kararı).
- Aynı iş iki turda da QA'dan geçemedi ve geri alındı: dur, nedenini yaz.
