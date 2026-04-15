# microGPT Lab

Andrej Karpathy'nin sıfırdan yazdığı [microGPT](https://github.com/karpathy/microGPT) uygulaması üzerine Türkçe isim üretimi odaklı laboratuvar çalışması.

Kod; öz-farklılaşma (autograd), transformer mimarisi, Adam optimizörü ve karakter düzeyinde tokenizasyonu **harici kütüphane kullanmadan** gerçekleştirmektedir.

---

## Dosya Yapısı

```
microgpt-lab/
├── README.md               # Bu dosya
├── microgpt.py             # Orijinal tek-dosya microGPT uygulaması
├── isimler.txt             # 2.446 Türkçe isim — eğitim veri seti
│
├── lab1.pdf                # Lab 1 — soru kağıdı
├── lab1-cevap/             # Lab 1 — cevap dosyaları
│   ├── train.py            # Model eğitim scripti
│   ├── test.py             # Çıkarım scripti (temperature=0.5)
│   └── test_temperature.py # Temperature karşılaştırma scripti
│
├── lab2.pdf                # Lab 2 — soru kağıdı
├── lab2-cevap.zip          # Lab 2 — cevap anahtarı (şifreli)
└── microgpt_ablasyon.py    # Lab 2 — Attention vs. MLP ablasyon deneyi
```

---

## Şifreli Cevap Dosyaları

`lab1-cevap.zip` ve `lab2-cevap.zip` şifreli arşivlerdir.  
Şifre [YouTube kanalımda](https://www.youtube.com/@kemalbicakci) verilecektir.

---

## Lab 1 — Modüler Mimari ve Temperature

### Alıştırma 1: Token Analizi
`isimler.txt` dosyasındaki Türkçe isimler kullanılarak kaç farklı token (karakter) bulunduğunu hesaplayın.

### Alıştırma 2: Modüler Yapı
Orijinal tek-dosya kodu `train.py` + `test.py` olarak ikiye ayırın. Model ağırlıklarını `pickle` ile kaydedin ve yükleyin.

```bash
cd lab1-cevap
python train.py                                # modeli eğit, model.pkl kaydeder
python test.py                                 # 20 isim üret (temperature=0.5)
python test_temperature.py --temperature 0.1   # deterministik
python test_temperature.py --temperature 2.0   # yaratıcı
```

### Alıştırma 3: Temperature Parametresi
`--temperature` komut satırı argümanını ekleyerek farklı yaratıcılık seviyelerinde isim üretimi yapın.  
`0.1` (deterministik) → `2.0` (çeşitli) arasında karşılaştırın.

---

## Lab 2 — Attention Mekanizmasının Önemi

Bu laboratuvarda attention mekanizmasının önemi **ablasyon deneyi** ile gösterilmektedir:  
attention bloğu, eşit parametreli bir MLP ile değiştirilir ve iki model karşılaştırılır.

### Deney Tasarımı

| | Attention Modeli | MLP-Only Modeli |
|---|---|---|
| Bağlam erişimi | Tüm önceki tokenlar (Q×K^T) | Yalnızca mevcut token |
| Attention bloğu | Wq, Wk, Wv, Wo: 4×(16×16) = 1.024 param | ctx_fc1 + ctx_fc2: (16×32)+(32×16) = 1.024 param |
| **Toplam parametre** | **~4.192** | **~4.192** |

İki model **tam olarak eşit sayıda parametreye** sahiptir — fark kapasiteden değil, mimarinin yapısından kaynaklanır.

### Sentetik Görev

Her dizi sabit uzunlukta (7 karakter) ve şu kurala göre oluşturulur:

```
'a' + [rastgele filler] + 'a'   →  örnek: "abcdfea"
'z' + [rastgele filler] + 'z'   →  örnek: "zxmkpqz"
```

Son anchor'ı tahmin etmek için **ilk karakteri hatırlamak** gerekir. Attention bunu yapabilir, MLP yapamaz.

### Çalıştırma

```bash
python microgpt_ablasyon.py
```

### Beklenen Sonuçlar

| Metrik | Attention | MLP-Only |
|---|---|---|
| KEY pozisyon kaybı (son 500 adım) | ~0.002 | ~0.711 ≈ log(2) |
| Doğruluk (100 yeni örnek) | %100 | ~%42 |

### Attention Kafası Uzmanlaşması

Eğitim sonunda `pid=6` (son filler pozisyonu) için attention ağırlıkları incelendiğinde **Kafa 3'ün tamamen anchor dedektörüne dönüştüğü** görülür:

```
Dizi: 'zlhihe'  (anchor='z')
  pos:     BOS     z     l     h     i     h     e
kafa 1:   0.05  0.25  0.38  0.05  0.08  0.05  0.13
kafa 2:   0.02  0.04  0.35  0.12  0.30  0.12  0.05
kafa 3:   0.00  0.95  0.05  0.00  0.00  0.00  0.00   ← uzmanlaşmış
kafa 4:   0.07  0.27  0.15  0.14  0.12  0.14  0.12
  ort:    0.04  0.38  0.23  0.08  0.13  0.08  0.07   ← pid=1 en yüksek
```

---

## Gereksinimler

Python 3.x — ek kütüphane gerekmez.

---

## Kaynak

- [microGPT — Andrej Karpathy](https://github.com/karpathy/microGPT)
