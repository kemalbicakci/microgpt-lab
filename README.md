# microGPT Lab

Andrej Karpathy'nin sıfırdan yazdığı [microGPT](https://github.com/karpathy/microGPT) uygulaması üzerine Türkçe isim üretimi odaklı laboratuvar çalışması.

Kod; öz-farklılaşma (autograd), transformer mimarisi, Adam optimizörü ve karakter düzeyinde tokenizasyonu **harici kütüphane kullanmadan** gerçekleştirmektedir.

---

## Dosya Yapısı

```
microgpt-lab/
├── README.md            # Bu dosya
├── microgpt.py          # Orijinal tek-dosya microGPT uygulaması
├── isimler.txt          # 2 446 Türkçe isim — eğitim veri seti
├── lab1.pdf             # Lab 1 görevleri ve sorular
└── lab1-cevap/
    ├── lab1-cevaplar.pdf    # Cevap anahtarı
    ├── model.pkl            # Eğitilmiş model ağırlıkları
    ├── train.py             # Modeli eğitir → model.pkl kaydeder
    ├── test.py              # model.pkl yükler, isim üretir
    └── test_temperature.py  # --temperature argümanıyla isim üretir
```

---

## Lab 1 — Alıştırmalar

### Alıştırma 1: Token Analizi
`isimler.txt` dosyasındaki Türkçe isimler kullanılarak kaç farklı token (karakter) bulunduğu hesaplanır.

```
vocab_size: 31   # 30 benzersiz karakter + 1 BOS tokeni
```

### Alıştırma 2: Modüler Yapı

Orijinal tek-dosya kod eğitim ve test olmak üzere ikiye ayrılır. Model ağırlıkları `pickle` ile kaydedilip yüklenir.

```bash
# Eğit ve kaydet
python lab1-cevap/train.py

# Yükle ve üret
python lab1-cevap/test.py
```

### Alıştırma 3: Temperature Parametresi

`--temperature` argümanıyla farklı yaratıcılık seviyelerinde isim üretimi yapılır.

```bash
python lab1-cevap/test_temperature.py --temperature 0.1   # tekrarlayan
python lab1-cevap/test_temperature.py --temperature 0.5   # dengeli
python lab1-cevap/test_temperature.py --temperature 1.0   # çeşitli
python lab1-cevap/test_temperature.py --temperature 2.0   # rastgele
```

| Temperature | Davranış |
|---|---|
| 0.1 | Aynı isimler tekrarlar, minimum çeşitlilik |
| 0.5 | Türkçe isim kalıplarına uyan dengeli çıktı |
| 1.0 | Daha çeşitli, bazıları gerçek dışı kombinasyonlar |
| 2.0 | Anlamsız karakter dizileri |

---

## Gereksinimler

Python 3.x — ek kütüphane gerekmez.

---

## Kaynak

- [microGPT — Andrej Karpathy](https://github.com/karpathy/microGPT)
