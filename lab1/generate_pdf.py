"""
Lab 1 PDF Generator — iki ayrı dosya üretir:
  lab1.pdf          : görevler + sorular (cevap yok)
  lab1-cevaplar.pdf : tüm soruların cevapları
"""
from fpdf import FPDF
import os

ARIAL      = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL_IT   = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
MONO       = "/System/Library/Fonts/SFNSMono.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))


# ─────────────────────────────────────────────────────────────────────────────
class LabPDF(FPDF):
    def __init__(self, header_label="microGPT Lab Çalışması — Lab 1"):
        super().__init__()
        self._header_label = header_label
        self.add_font("Arial", "",  ARIAL)
        self.add_font("Arial", "B", ARIAL_BOLD)
        self.add_font("Arial", "I", ARIAL_IT)
        self.add_font("Mono",  "",  MONO)

    def header(self):
        self.set_font("Arial", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, self._header_label, align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(180, 180, 180)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 10, f"Sayfa {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)

    # ── Yardımcı metodlar ────────────────────────────────────────────────────

    def cover(self, title, subtitle, note, bar_color=(30, 30, 50)):
        self.set_fill_color(*bar_color)
        self.rect(0, 0, self.w, 55, "F")
        self.set_y(10)
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 24)
        self.cell(0, 12, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 13)
        self.cell(0, 8, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "I", 10)
        self.set_text_color(180, 210, 255)
        self.cell(0, 7, note, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_y(60)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def section_title(self, number, title, color=(40, 80, 140)):
        self.ln(5)
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 12)
        self.cell(0, 9, f"  Alıştırma {number}: {title}", fill=True,
                  new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def page_title(self, text, color=(30, 30, 50)):
        self.set_font("Arial", "B", 13)
        self.set_text_color(*color)
        self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*color)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)
        self.ln(3)

    def sub_title(self, text, color=(40, 80, 140)):
        self.set_font("Arial", "B", 10)
        self.set_text_color(*color)
        self.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)

    def body(self, text, indent=0):
        self.set_font("Arial", "", 10)
        self.set_x(self.l_margin + indent)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def bullet(self, text, indent=5):
        self.set_font("Arial", "", 10)
        self.set_x(self.l_margin + indent)
        self.cell(5, 6, "•")
        self.multi_cell(0, 6, text)

    def numbered(self, number, text, indent=5):
        self.set_font("Arial", "", 10)
        self.set_x(self.l_margin + indent)
        self.cell(8, 6, f"{number}.")
        self.multi_cell(0, 6, text)

    def code_block(self, lines):
        self.set_fill_color(240, 242, 246)
        self.set_draw_color(200, 205, 215)
        self.set_font("Mono", "", 8)
        self.set_text_color(30, 40, 60)
        max_w = self.w - self.l_margin - self.r_margin
        total_h = len(lines) * 5 + 4
        self.ln(1)
        self.rect(self.l_margin, self.get_y(), max_w, total_h, "FD")
        self.set_y(self.get_y() + 2)
        for ln in lines:
            self.set_x(self.l_margin + 3)
            self.cell(max_w - 6, 5, ln, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)

    def info_box(self, title, text, bg=(230, 245, 230), border=(100, 160, 100)):
        self.set_fill_color(*bg)
        self.set_draw_color(*border)
        w = self.w - self.l_margin - self.r_margin
        self.set_font("Arial", "B", 9)
        self.set_x(self.l_margin)
        self.cell(w, 7, f"  {title}", fill=True, border="TLR",
                  new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 9)
        self.set_x(self.l_margin)
        self.multi_cell(w, 5.5, f"  {text}", fill=True, border="BLR")
        self.set_draw_color(0, 0, 0)
        self.ln(2)

    def warning_box(self, title, text):
        self.info_box(title, text, bg=(255, 248, 225), border=(200, 160, 0))

    def question_box(self, questions):
        self.set_fill_color(245, 238, 255)
        self.set_draw_color(120, 80, 180)
        w = self.w - self.l_margin - self.r_margin
        self.set_font("Arial", "B", 9)
        self.set_x(self.l_margin)
        self.cell(w, 7, "  Cevaplamanız Gereken Sorular", fill=True,
                  border="TLR", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 9)
        for i, q in enumerate(questions, 1):
            self.set_x(self.l_margin)
            self.multi_cell(w, 5.5, f"  {i}. {q}", fill=True, border="LR")
        self.set_x(self.l_margin)
        self.cell(w, 2, "", fill=True, border="BLR", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 0, 0)
        self.ln(3)

    def answer_box(self, question, answer_lines, q_number=None):
        """Cevap sayfasında tek bir soru + cevap bloğu."""
        w = self.w - self.l_margin - self.r_margin
        # Soru
        self.set_fill_color(245, 238, 255)
        self.set_draw_color(120, 80, 180)
        self.set_font("Arial", "B", 9)
        label = f"  S{q_number}: " if q_number else "  "
        self.set_x(self.l_margin)
        self.multi_cell(w, 6, f"{label}{question}", fill=True, border="TLR")
        self.set_x(self.l_margin)
        self.cell(w, 1.5, "", fill=True, border="BLR", new_x="LMARGIN", new_y="NEXT")
        # Cevap
        self.set_fill_color(235, 255, 235)
        self.set_draw_color(80, 160, 80)
        self.set_font("Arial", "B", 8)
        self.set_x(self.l_margin)
        self.cell(w, 6, "  Cevap:", fill=True, border="TLR",
                  new_x="LMARGIN", new_y="NEXT")
        self.set_font("Arial", "", 9)
        for line in answer_lines:
            self.set_x(self.l_margin)
            self.multi_cell(w, 5.5, f"  {line}", fill=True, border="LR")
        self.set_x(self.l_margin)
        self.cell(w, 2, "", fill=True, border="BLR", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 0, 0)
        self.ln(3)

    def table_header(self, cols, widths):
        self.set_fill_color(40, 80, 140)
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 9)
        for col, w in zip(cols, widths):
            self.cell(w, 8, f" {col}", fill=True, border=1)
        self.ln()
        self.set_text_color(0, 0, 0)

    def table_row(self, values, widths, idx=0):
        self.set_fill_color(248, 250, 255) if idx % 2 == 0 else self.set_fill_color(255, 255, 255)
        self.set_font("Arial", "", 9)
        for val, w in zip(values, widths):
            self.cell(w, 7, f" {val}", fill=True, border=1)
        self.ln()


# ═════════════════════════════════════════════════════════════════════════════
#  LAB1.PDF  —  Sadece görevler ve sorular
# ═════════════════════════════════════════════════════════════════════════════
def build_lab(path):
    pdf = LabPDF()
    pdf.set_margins(18, 20, 18)
    pdf.set_auto_page_break(True, margin=20)
    pdf.add_page()

    # ── Kapak ────────────────────────────────────────────────────────────────
    pdf.cover(
        "microGPT — Lab 1",
        "Türkçe İsim Üretimi: Tokenizasyon, Eğitim ve Çıkarım",
        "Andrej Karpathy'nin microGPT uygulaması üzerine pratik çalışmalar",
    )

    pdf.body(
        "Bu laboratuvar çalışmasında, Andrej Karpathy'nin sıfırdan yazdığı microGPT "
        "uygulamasını inceleyecek ve üç farklı alıştırma üzerinde çalışacaksınız. Kod; "
        "öz-farklılaşma (autograd), transformer mimarisi, Adam optimizörü ve karakter "
        "düzeyinde tokenizasyonun tamamını harici kütüphane kullanmadan gerçekleştirmektedir."
    )
    pdf.ln(2)

    pdf.info_box("Ön Gereksinimler",
        "Python 3.x kurulu olmalıdır. microgpt.py ve isimler.txt dosyaları proje kök "
        "dizininde bulunmalıdır. Harici kütüphane gerekmemektedir.")

    pdf.sub_title("Proje Dosya Yapısı (Başlangıç)")
    pdf.code_block([
        "microgpt-lab/",
        "├── microgpt.py       # Orijinal tek-dosya uygulama (değiştirmeyin)",
        "├── isimler.txt       # 2 446 Türkçe isim içeren veri seti",
        "└── lab1/             # Oluşturacağınız dosyalar buraya gelecek",
    ])

    # ── Alıştırma 1 ──────────────────────────────────────────────────────────
    pdf.section_title(1, "Token Analizi — isimler.txt ile Kaç Farklı Token Var?")

    pdf.body(
        "microGPT, karakter düzeyinde bir tokenizasyon kullanmaktadır. Her benzersiz "
        "karakter (harf, boşluk vb.) bir token kimliğine (ID) karşılık gelir. "
        "Orijinal kodda veri 'input.txt' dosyasından okunmaktadır. Bu alıştırmada "
        "'isimler.txt' dosyasındaki Türkçe isimleri kullanacaksınız."
    )

    pdf.sub_title("Yapmanız Gerekenler")
    pdf.bullet("microgpt.py dosyasındaki veri yükleme satırını isimler.txt'i okuyacak şekilde değiştirin.")
    pdf.bullet("Programı çalıştırın ve vocab size değerini not edin.")
    pdf.bullet("Hangi karakterlerin token olarak kullanıldığını listeleyin.")
    pdf.ln(2)

    pdf.sub_title("Değiştirilmesi Gereken Kod Satırı")
    pdf.code_block([
        "# Orijinal",
        "docs = [line.strip() for line in open('input.txt') if line.strip()]",
        "",
        "# Değiştirin",
        "docs = [line.strip() for line in open('isimler.txt') if line.strip()]",
    ])

    pdf.sub_title("isimler.txt Veri Seti Hakkında")
    pdf.code_block([
        "Toplam isim sayısı : 2 446",
        "Örnek isimler      : JALE, ALİ, MAHMUT, MANSUR KÜRŞAD, GAMZE, MİRAÇ, YÜCEL ...",
        "Özellikler         : Büyük harf, Türkçe özel karakterler (Ç Ö Ü Ğ İ Ş),",
        "                     boşluklu bileşik isimler (BEDRİYE MÜGE vb.)",
    ])

    pdf.question_box([
        "Programı çalıştırdığınızda kaç farklı token (karakter) bulunmaktadır? BOS dahil vocab_size nedir?",
        "Türkçe isimlerde hiç kullanılmayan Latin harfleri hangileridir? Bu harflerin neden "
        "vocabulary'de yer almadığını açıklayın.",
        "isimler.txt dosyasında büyük harfli isimler ile birlikte küçük harfli isimler kullansaydık vocab_size nasıl değişirdi?",
        "BOS (Beginning of Sequence) tokeninin görevi nedir? Modelin eğitiminde ne işe yarar?",
    ])

    # ── Alıştırma 2 ──────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title(2, "Modüler Yapı — Eğitimi, Modeli ve Testi Ayırma")

    pdf.body(
        "Orijinal microgpt.py dosyası eğitim ve çıkarımı tek dosyada birleştirmektedir. "
        "Bu alıştırmada kodu iki ayrı dosyaya bölecek ve model ağırlıklarını pickle "
        "ile kaydedip yükleyeceksiniz."
    )

    pdf.sub_title("Oluşturmanız Gereken Dosyalar")
    pdf.code_block([
        "lab1/",
        "├── train.py     # Modeli eğitir, ağırlıkları 'model.pkl' olarak kaydeder",
        "├── model.pkl    # train.py tarafından oluşturulur",
        "└── test.py      # model.pkl'ı yükler, yeni Türkçe isimler üretir",
    ])
    pdf.ln(1)

    pdf.sub_title("train.py — İskelet Yapı")
    pdf.code_block([
        "import os, math, random, pickle",
        "random.seed(42)",
        "",
        "# 1. Veri yükleme",
        "docs = [line.strip() for line in open('isimler.txt') if line.strip()]",
        "random.shuffle(docs)",
        "",
        "# 2. Tokenizasyon",
        "uchars = sorted(set(''.join(docs)))",
        "BOS = len(uchars)",
        "vocab_size = len(uchars) + 1",
        "",
        "# 3. Value sınıfı, model parametreleri ve mimari (microgpt.py'den)",
        "",
        "# 4. Eğitim döngüsü (microgpt.py'deki for step ... bloğu)",
        "",
        "# 5. Modeli kaydet",
        "save_data = {",
        "    'uchars': uchars, 'BOS': BOS, 'vocab_size': vocab_size,",
        "    'state_dict_data': {k: [[p.data for p in row] for row in mat]",
        "                        for k, mat in state_dict.items()}",
        "}",
        "with open('model.pkl', 'wb') as f: pickle.dump(save_data, f)",
    ])

    pdf.sub_title("test.py — İskelet Yapı")
    pdf.code_block([
        "import random, math, pickle",
        "",
        "# 1. Modeli yükle",
        "with open('model.pkl', 'rb') as f:",
        "    save_data = pickle.load(f)",
        "",
        "uchars     = save_data['uchars']",
        "BOS        = save_data['BOS']",
        "vocab_size = save_data['vocab_size']",
        "",
        "# 2. Value sınıfını tanımla, state_dict_data'yı Value nesnelerine dönüştür",
        "",
        "# 3. Çıkarım — 20 yeni isim üret",
        "temperature = 0.5",
        "for sample_idx in range(20):",
        "    ...",
    ])

    pdf.warning_box("Dikkat — pickle ve Value Sınıfı",
        "pickle.dump doğrudan Value nesnelerini serileştiremez (iç içe computation graph "
        "nedeniyle). Yalnızca '.data' sayısal değerlerini kaydedin. test.py'de her değeri "
        "Value(float_value) olarak yeniden sarmalayın.")

    pdf.question_box([
        "train.py ve test.py ayrımının gerçek dünya ML projelerinde sağladığı avantajlar nelerdir?",
        "train.py çalıştırdıktan sonra model.pkl dosyasının boyutu nedir (bytes)? "
        "Bu boyutu model parametre sayısıyla ilişkilendirebilir misiniz?",
        "Modelin kaç parametresi bulunmaktadır? (İpucu: 'num params' çıktısına bakın.)",
        "random.seed(42) olmadan test.py'yi iki kez çalıştırsaydınız aynı isimleri üretir miydi? Neden?",
    ])

    # ── Alıştırma 3 ──────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title(3, "Temperature Parametresi — Yaratıcılık ve Belirlilik Dengesi")

    pdf.body(
        "Temperature, dil modellerinin çıktısını kontrol eden kritik bir hiperparametredir. "
        "Bu alıştırmada temperature değerini komut satırı argümanı olarak alan ayrı bir "
        "dosya yazacak ve farklı değerlerin çıktı üzerindeki etkisini inceleyeceksiniz."
    )

    pdf.sub_title("Oluşturmanız Gereken Dosya ve Kullanımı")
    pdf.code_block([
        "# Dosya: lab1/test_temperature.py",
        "",
        "python test_temperature.py --temperature 0.1",
        "python test_temperature.py --temperature 0.5",
        "python test_temperature.py --temperature 1.0",
        "python test_temperature.py --temperature 2.0",
    ])

    pdf.sub_title("test_temperature.py — İskelet Yapı")
    pdf.code_block([
        "import argparse, random, math, pickle",
        "",
        "parser = argparse.ArgumentParser(description='microGPT isim üretici')",
        "parser.add_argument('--temperature', type=float, default=0.5,",
        "                    help='Örnekleme sıcaklığı (0 < t)')",
        "args = parser.parse_args()",
        "temperature = args.temperature",
        "",
        "# Model yükleme kodu (test.py ile aynı)",
        "# ...",
        "",
        "# Temperature ölçeklemeli softmax",
        "probs = softmax([l / temperature for l in logits])",
    ])

    pdf.sub_title("Temperature'ın Matematiksel Etkisi")
    pdf.code_block([
        "P(token_i) = exp(logit_i / T) / Σ exp(logit_j / T)",
        "",
        "T → 0   : Olasılık tek token'da yoğunlaşır (greedy seçim)",
        "T = 0.5 : Yüksek olasılıklı tokenlar ön plana çıkar",
        "T = 1.0 : Ham softmax (değişiklik yok)",
        "T > 1.0 : Dağılım düzleşir, tüm tokenlar benzer olasılık kazanır",
    ])

    pdf.sub_title("Görev: Farklı Temperature Değerlerini Deneyin ve Tabloyu Doldurun")
    pdf.body("train.py ile eğitilmiş modeli kullanarak aşağıdaki tabloyu kendiniz doldurunuz:")

    col_w = [28, 40, 40, 30, 36]
    pdf.table_header(["Temperature", "Örnek 1", "Örnek 2", "Örnek 3", "Gözlemleriniz"], col_w)
    for i, t in enumerate(["0.1", "0.5", "1.0", "2.0"]):
        pdf.table_row([t, "", "", "", ""], col_w, i)
    pdf.ln(3)

    pdf.question_box([
        "T=0.1 ile T=2.0 arasında üretilen isimler arasındaki en belirgin fark nedir?",
        "Hangi temperature değerinde üretilen isimler gerçek Türkçe isimlere en çok benziyor? Neden?",
        "random.seed(42) ile aynı temperature için her çalıştırmada aynı sonuçlar mı üretilir? Neden?",
        "Temperature parametresi ile model ağırlıkları arasındaki temel fark nedir? "
        "Hangisi eğitimden etkilenir?",
        "Veri seti genişletme (data augmentation) amacıyla isim üretecek olsanız "
        "hangi temperature değerini seçerdiniz? Gerekçenizi açıklayın.",
    ])

    # ── Özet Sayfa ───────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.page_title("Özet ve Teslim Gereksinimleri")

    pdf.body("Bu laboratuvar çalışmasını tamamladığınızda aşağıdaki yapıya sahip olmalısınız:")
    pdf.code_block([
        "lab1/",
        "├── train.py              # Alıştırma 2",
        "├── test.py               # Alıştırma 2",
        "├── test_temperature.py   # Alıştırma 3",
        "├── model.pkl             # train.py tarafından üretilir",
        "└── rapor.pdf             # Soruların cevapları + tablo + gözlemler",
    ])
    pdf.ln(2)

    pdf.sub_title("Değerlendirme")
    items = [
        ("Alıştırma 1 — 25 puan",
         "isimler.txt doğru yükleniyor, vocab_size hesaplanmış, 4 soru yanıtlanmış."),
        ("Alıştırma 2 — 35 puan",
         "train.py ve test.py çalışıyor, model.pkl oluşturuluyor, 4 soru yanıtlanmış."),
        ("Alıştırma 3 — 30 puan",
         "test_temperature.py --temperature argümanını alıyor, tablo doldurulmuş, 5 soru yanıtlanmış."),
        ("Rapor kalitesi — 10 puan",
         "Cevaplar açık, teknik olarak doğru ve kendi cümlelerinizle yazılmış."),
    ]
    for t, d in items:
        pdf.set_font("Arial", "B", 9)
        pdf.set_x(pdf.l_margin)
        pdf.cell(60, 6, t)
        pdf.set_font("Arial", "", 9)
        pdf.multi_cell(0, 6, d)
        pdf.ln(1)

    pdf.ln(3)
    pdf.info_box("Hatırlatma",
        "microgpt.py dosyasını değiştirmeyin — referans olarak kullanacaksınız.\n"
        "Tüm yeni dosyalarınızı lab1/ klasörüne kaydedin.\n"
        "pickle kullanırken yalnızca .data sayısal değerlerini serileştirin.")

    pdf.output(path)
    print(f"Oluşturuldu: {path}")


# ═════════════════════════════════════════════════════════════════════════════
#  LAB1-CEVAPLAR.PDF  —  Sadece cevaplar
# ═════════════════════════════════════════════════════════════════════════════
def build_answers(path):
    pdf = LabPDF(header_label="microGPT Lab 1 — Cevap Anahtarı")
    pdf.set_margins(18, 20, 18)
    pdf.set_auto_page_break(True, margin=20)
    pdf.add_page()

    # ── Kapak ────────────────────────────────────────────────────────────────
    pdf.cover(
        "microGPT — Lab 1 Cevapları",
        "Tüm Alıştırmaların Cevap Anahtarı",
        "Bu dosya yalnızca eğitmen / kendi kendine değerlendirme içindir",
        bar_color=(80, 30, 30),
    )

    pdf.body(
        "Bu dosya Lab 1'deki üç alıştırmanın tüm soru cevaplarını içermektedir. "
        "Her cevap soru ile birlikte gösterilmiştir."
    )
    pdf.ln(2)

    # ── Alıştırma 1 Cevapları ────────────────────────────────────────────────
    pdf.section_title(1, "Token Analizi — Cevaplar", color=(120, 40, 40))

    pdf.answer_box(
        "Programı çalıştırdığınızda kaç farklı token bulunmaktadır? BOS dahil vocab_size nedir?",
        [
            "isimler.txt dosyasındaki tüm karakterler büyük harf ve Türkçe özel karakterlerden oluşur.",
            "Benzersiz karakter sayısı: 30",
            "  ' ' (boşluk)  A B C D E F G H I J K L M N O P R S T U V Y Z  Ç Ö Ü Ğ İ Ş",
            "BOS özel tokeni: +1",
            "Toplam vocab_size = 31",
        ], q_number=1
    )

    pdf.answer_box(
        "Türkçe isimlerde hiç kullanılmayan Latin harfleri hangileridir? Neden vocabulary'de yoklar?",
        [
            "Türkçe alfabesinde bulunmayan harfler: Q, W, X",
            "Tokenizer yalnızca eğitim verisinde gördüğü karakterleri vocabulary'e ekler.",
            "isimler.txt'deki isimlerin tamamı Türkçe olduğundan Q/W/X içeren hiçbir isim yoktur.",
            "Dolayısıyla bu karakterler uchars listesine girmez ve token ID almazlar.",
        ], q_number=2
    )

    pdf.answer_box(
        "isimler.txt dosyasında büyük harfli isimler ile birlikte küçük harfli isimler kullansaydık vocab_size nasıl değişirdi?",
        [
            "Tokenizer yalnızca eğitim verisinde gördüğü karakterleri vocabulary'e ekler.",
            "Büyük ve küçük harf farklı Unicode kod noktaları olduğundan ayrı token ID'si alır.",
            "Örnek: 'A' (ID=1) ve 'a' (ID=31) birbirinden bağımsız tokendır.",
            "",
            "Mevcut durum (yalnızca büyük harf):",
            "  30 benzersiz karakter + 1 BOS = vocab_size: 31",
            "",
            "Her ismin hem büyük hem küçük harfli biçimi bulunsaydı:",
            "  Büyük harf karakterleri : 30  (boşluk + A–Z + Ç Ö Ü Ğ İ Ş)",
            "  Küçük harf eklentisi    : +29 (boşluk zaten ortak; yeni: a–z + ç ö ü ğ i ş)",
            "  Toplam benzersiz karakter: 30 + 29 = 59",
            "  vocab_size = 59 + 1 BOS = 60",
            "",
            "Sonuç: vocab_size yaklaşık 2 katına çıkar (31 → 60).",
            "Bu durum wte ve lm_head matrislerini büyüterek parametre sayısını artırır",
            "  ve aynı kalıpları öğrenmek için daha fazla eğitim adımı gerektirir.",
        ], q_number=3
    )

    pdf.answer_box(
        "BOS (Beginning of Sequence) tokeninin görevi nedir? Modelin eğitiminde ne işe yarar?",
        [
            "BOS tokeni iki işlev üstlenir:",
            "  1. Başlangıç sinyali: Çıkarım sırasında modele 'yeni bir isim üret' komutunu verir.",
            "     Model ilk girdi olarak BOS'u alır ve ardından karakterleri tahmin eder.",
            "  2. Bitiş sinyali: Model bir ismin sonunda BOS üretince döngü durur.",
            "     Böylece modelin ne zaman duracağını öğrenmesi için ayrı bir EOS tokenine gerek kalmaz.",
            "Eğitimde her isim [BOS, k1, k2, ..., kn, BOS] şeklinde çerçevelenir;",
            "  model son BOS'u da tahmin etmeyi öğrenir.",
        ], q_number=4
    )

    # ── Alıştırma 2 Cevapları ────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title(2, "Modüler Yapı — Cevaplar", color=(120, 40, 40))

    pdf.answer_box(
        "train.py ve test.py ayrımının gerçek dünya ML projelerinde sağladığı avantajlar nelerdir?",
        [
            "a) Zaman tasarrufu: Modeli bir kez eğitip defalarca test edebilirsiniz;",
            "   her test için sıfırdan eğitmek gerekmez.",
            "b) Depolama: Eğitilmiş model kaydedilerek başka ortamlarda (sunucu, bulut) kullanılabilir.",
            "c) Tekrarlanabilirlik: Aynı model.pkl ile her test çalıştırması tutarlı sonuç verir.",
            "d) İş bölümü: Veri bilimcisi eğitimi, mühendis servis katmanını ayrı geliştirebilir.",
            "e) Hata ayıklama: Eğitim ve çıkarım sorunları izole biçimde incelenebilir.",
        ], q_number=1
    )

    pdf.answer_box(
        "train.py çalıştırdıktan sonra model.pkl dosyasının boyutu nedir? Parametre sayısıyla ilişkisi?",
        [
            "model.pkl boyutu: yaklaşık 40 KB (sisteme ve pickle protokolüne göre değişir).",
            "Model parametre sayısı: 4 320  (vocab_size=31 ile)",
            "  wte=496, wpe=256, lm_head=496, attn=1024, mlp=2048",
            "pickle her Python float'ı ~9 byte ile kodlar (1 opcode + 8 byte veri).",
            "  4 320 params × 9 byte ≈ 39 KB  +  dict/list/string overhead ≈ 1–2 KB",
            "  Toplam ≈ 40–42 KB",
            "Not: Orijinal microgpt (vocab_size≈65) ile daha fazla parametre → daha büyük dosya.",
            "Numpy/safetensors formatları daha verimli serileştirme sağlar.",
        ], q_number=2
    )

    pdf.answer_box(
        "Modelin kaç parametresi bulunmaktadır?",
        [
            "microgpt.py'deki varsayılan hiperparametrelerle:",
            "  n_embd=16, vocab_size=31, block_size=16, n_head=4, n_layer=1",
            "",
            "  wte         : 31 × 16 = 496",
            "  wpe         : 16 × 16 = 256",
            "  lm_head     : 31 × 16 = 496",
            "  attn_wq/wk/wv/wo : 4 × (16 × 16) = 1 024",
            "  mlp_fc1     : 64 × 16 = 1 024  (4*n_embd × n_embd)",
            "  mlp_fc2     : 16 × 64 = 1 024  (n_embd × 4*n_embd)",
            "  TOPLAM      : 496 + 256 + 496 + 1024 + 1024 + 1024 = 4 320",
            "",
            "Not: isimler.txt vocab_size=31 olduğundan orijinal kodun (vocab~65) çıktısından farklıdır.",
        ], q_number=3
    )

    pdf.answer_box(
        "random.seed(42) olmadan test.py'yi iki kez çalıştırsaydınız aynı isimleri üretir miydi?",
        [
            "Hayır, her çalıştırmada farklı isimler üretilirdi.",
            "random.choices() sistem saatine dayalı rastgele bir tohum kullanır.",
            "random.seed(42) ile tohum sabitlendiğinde rastgele sayı dizisi deterministik olur",
            "  ve her çalıştırmada birebir aynı örnekleme yapılır.",
            "Model ağırlıkları (model.pkl) değişmediğinden farklılık yalnızca örnekleme",
            "  rastgeleliğinden kaynaklanır — model logitleri her zaman aynıdır.",
        ], q_number=4
    )

    # ── Alıştırma 3 Cevapları ────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title(3, "Temperature Parametresi — Cevaplar", color=(120, 40, 40))

    pdf.sub_title("Doldurulmuş Örnek Tablo (yaklaşık değerler — modele göre değişir)")
    col_w = [28, 40, 40, 30, 36]
    pdf.table_header(["Temperature", "Örnek 1", "Örnek 2", "Örnek 3", "Gözlem"], col_w)
    rows = [
        ["0.1", "MEHMET", "MEHMET", "MEHMET", "Tekrarlayan"],
        ["0.5", "EMRE", "GÜLŞAH", "ALİ", "Dengeli"],
        ["1.0", "SERKAN", "MÜJDE", "HAYRÜYE", "Çeşitli"],
        ["2.0", "ÇTMBÖ", "AŞZĞÜR", "IÖBŞR", "Anlamsız"],
    ]
    for i, row in enumerate(rows):
        pdf.table_row(row, col_w, i)
    pdf.ln(4)

    pdf.answer_box(
        "T=0.1 ile T=2.0 arasında üretilen isimler arasındaki en belirgin fark nedir?",
        [
            "T=0.1: Model her seferinde aynı ya da çok benzer isimleri üretir. Dağılım tek bir",
            "  token üzerinde yoğunlaşır; çeşitlilik neredeyse sıfırdır.",
            "T=2.0: Olasılık dağılımı düzleşir, model neredeyse rastgele karakter seçer.",
            "  Üretilen diziler anlamsız harf kombinasyonlarına dönüşür.",
            "Fark: T=0.1'de aşırı belirlilik (ezber/kalıp), T=2.0'de aşırı rastgelelik (gürültü).",
        ], q_number=1
    )

    pdf.answer_box(
        "Hangi temperature değerinde üretilen isimler gerçek Türkçe isimlere en çok benziyor?",
        [
            "Genellikle T=0.5 en iyi dengeyi sağlar (orijinal kodun varsayılanı da budur).",
            "Bu değerde model, yüksek olasılıklı (öğrenilmiş) kalıpları ön plana çıkarırken",
            "  tamamen deterministik olmayan çeşitli isimler üretir.",
            "T=1.0 da kabul edilebilir sonuçlar verebilir; bazı modellerde daha doğal görünür.",
            "Neden: Düşük temperature, modelin en 'güvenli' tahminlerine kilitlenerek",
            "  eğitim verisindeki en sık isimleri tekrarlar. Orta temperature ise öğrenilen",
            "  fonotaktik (ses dizilimi) örüntüleri koruyarak yeni kombinasyonlar üretir.",
        ], q_number=2
    )

    pdf.answer_box(
        "random.seed(42) ile aynı temperature için her çalıştırmada aynı sonuçlar mı üretilir?",
        [
            "Evet, random.seed(42) tohumu sabitlendiğinde rastgele sayı üreteci aynı diziyi",
            "  üretir. Bu nedenle aynı temperature değeriyle her çalıştırmada birebir aynı",
            "  isimler elde edilir.",
            "Tohumu kaldırırsanız (veya farklı bir değer verirseniz) sonuçlar değişir.",
            "Bu özellik sonuçların tekrarlanabilir (reproducible) olmasını sağlar;",
            "  akademik çalışmalarda ve hata ayıklamada büyük önem taşır.",
        ], q_number=3
    )

    pdf.answer_box(
        "Temperature parametresi ile model ağırlıkları arasındaki temel fark nedir? Hangisi eğitimden etkilenir?",
        [
            "Model ağırlıkları (parametreler): Eğitim sırasında Adam optimizörü tarafından",
            "  güncellenir. Veriyi 'öğrenen' kısımdır; model.pkl'a kaydedilir.",
            "Temperature: Bir çıkarım (inference) hiperparametresidir. Eğitim sırasında",
            "  kullanılmaz; yalnızca örnekleme adımında softmax çıktısını ölçekler.",
            "Kısaca: Ağırlıklar eğitimden etkilenir, temperature etkilenmez.",
            "Temperature'ı değiştirmek için modeli yeniden eğitmek gerekmez.",
        ], q_number=4
    )

    pdf.answer_box(
        "Veri seti genişletme (data augmentation) amacıyla isim üretecek olsanız hangi temperature değerini seçerdiniz?",
        [
            "Önerilen aralık: T=0.7 – T=1.0",
            "Gerekçe:",
            "  • T çok düşük (≤0.3): Model eğitim verisindeki isimleri tekrar eder,",
            "    augmentation amacı ortadan kalkar.",
            "  • T çok yüksek (≥1.5): Üretilen isimler dilbilgisel açıdan geçersiz hale gelir,",
            "    gerçekçi isim kalıplarından uzaklaşır.",
            "  • T≈0.8: Model öğrendiği fonotaktik kuralları korurken yeterli çeşitlilik",
            "    sağlar — hem özgün hem de Türkçe isim kalıplarına uyan veriler üretir.",
        ], q_number=5
    )

    pdf.output(path)
    print(f"Oluşturuldu: {path}")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    build_lab(os.path.join(HERE, "lab1.pdf"))
    build_answers(os.path.join(HERE, "lab1-cevaplar.pdf"))
