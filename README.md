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
└── lab1-cevap.zip       # Cevap dosyaları (şifreli)
```

---

## Cevap Dosyaları

`lab1-cevap.zip` şifreli bir arşivdir. Şifre [YouTube kanalımda](https://www.youtube.com/@kemalbicakci) verilecektir.

---

## Lab 1 — Alıştırmalar

### Alıştırma 1: Token Analizi
`isimler.txt` dosyasındaki Türkçe isimler kullanılarak kaç farklı token (karakter) bulunduğunu hesaplayın.

### Alıştırma 2: Modüler Yapı

Orijinal tek-dosya kodu eğitim ve test olmak üzere ikiye ayırın. Model ağırlıklarını `pickle` ile kaydedin ve yükleyin.

### Alıştırma 3: Temperature Parametresi

`--temperature` komut satırı argümanını ekleyerek farklı yaratıcılık seviyelerinde isim üretimi yapın. Farklı temperature değerlerinin (0.1, 0.5, 1.0, 2.0) çıktıyı nasıl etkilediğini gözlemleyin.

---

## Gereksinimler

Python 3.x — ek kütüphane gerekmez.

---

## Kaynak

- [microGPT — Andrej Karpathy](https://github.com/karpathy/microGPT)
