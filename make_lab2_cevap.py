# -*- coding: utf-8 -*-
"""Generate lab2-cevap.pdf — Answer key for Lab 2."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Fonts ─────────────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('AU',  '/Library/Fonts/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('AU-B','/System/Library/Fonts/Supplemental/Arial.ttf'))

W, H = A4
MARGIN = 2 * cm

# ── Colours ───────────────────────────────────────────────────────────────────
BLUE        = colors.HexColor('#1a3a5c')
LIGHT_BLUE  = colors.HexColor('#e8f0f8')
GREEN       = colors.HexColor('#1a5c2a')
LIGHT_GREEN = colors.HexColor('#e8f5e9')
DARK_GREEN  = colors.HexColor('#155724')
ANS_BG      = colors.HexColor('#f0fff4')
TABLE_HEAD  = colors.HexColor('#2e7d32')
GRAY        = colors.HexColor('#555555')
LGRAY       = colors.HexColor('#f5f5f5')
RED_ACCENT  = colors.HexColor('#c62828')

# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    defaults = dict(fontName='AU', fontSize=10, leading=14, textColor=colors.black)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

sTitle   = S('sTitle',  fontName='AU-B', fontSize=22, leading=28,
              textColor=BLUE, spaceAfter=4, alignment=1)
sSubtitle= S('sSub',    fontName='AU-B', fontSize=13, leading=17,
              textColor=GREEN, spaceAfter=2, alignment=1)
sSection = S('sSec',    fontName='AU-B', fontSize=13, leading=17,
              textColor=BLUE, spaceBefore=14, spaceAfter=6)
sQ       = S('sQ',      fontName='AU-B', fontSize=11, leading=15,
              textColor=GREEN, spaceBefore=10, spaceAfter=4)
sBody    = S('sBody',   fontSize=10, leading=14, spaceAfter=4)
sBodyB   = S('sBodyB',  fontName='AU-B', fontSize=10, leading=14, spaceAfter=4)
sBullet  = S('sBullet', fontSize=10, leading=14, leftIndent=16, spaceAfter=3)
sAns     = S('sAns',    fontSize=10, leading=14, spaceAfter=3,
              textColor=DARK_GREEN, leftIndent=8)
sAnsB    = S('sAnsB',   fontName='AU-B', fontSize=10, leading=14, spaceAfter=3,
              textColor=DARK_GREEN, leftIndent=8)
sCode    = S('sCode',   fontName='AU', fontSize=9, leading=13, spaceAfter=3,
              textColor=colors.HexColor('#333333'),
              backColor=colors.HexColor('#f4f4f4'),
              leftIndent=12, rightIndent=12)
sAnsTag  = S('sAnsTag', fontName='AU-B', fontSize=11, leading=14,
              textColor=colors.white, spaceAfter=4)
sResult  = S('sResult', fontName='AU-B', fontSize=10, leading=14,
              textColor=RED_ACCENT, leftIndent=8, spaceAfter=3)

# ── Page chrome ───────────────────────────────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BLUE)
    canvas.rect(0, H - 1.2*cm, W, 1.2*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont('AU-B', 10)
    canvas.drawString(MARGIN, H - 0.85*cm, 'microGPT Lab 2 — CEVAP ANAHTARI')
    canvas.setFont('AU', 9)
    canvas.drawRightString(W - MARGIN, H - 0.85*cm,
                           'Attention vs. MLP Karşılaştırması')
    canvas.setFillColor(BLUE)
    canvas.rect(0, 0, W, 1.0*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont('AU', 8)
    canvas.drawString(MARGIN, 0.35*cm,
                      'microGPT Lab — Transformer Mimarisi Serisi')
    canvas.drawRightString(W - MARGIN, 0.35*cm, f'Sayfa {doc.page}')
    canvas.restoreState()

# ── Helpers ───────────────────────────────────────────────────────────────────
def P(text, style=None):
    return Paragraph(text, style or sBody)

def sp(n=6):
    return Spacer(1, n)

def hr():
    return HRFlowable(width='100%', thickness=0.5,
                      color=colors.HexColor('#cccccc'),
                      spaceAfter=4, spaceBefore=4)

def answer_box(content_paras, label='CEVAP'):
    cell = [P(label, sAnsTag)] + content_paras
    t = Table([[cell]], colWidths=[W - 2*MARGIN - 0.4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), ANS_BG),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BOX',           (0,0), (-1,-1), 1.5, GREEN),
        ('LINEABOVE',     (0,0), (-1,0),  4,   GREEN),
    ]))
    return t

def section_bar(title):
    t = Table([[P(title, S('sh', fontName='AU-B', fontSize=12,
                           textColor=colors.white))]],
              colWidths=[W - 2*MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), BLUE),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def q_header(num, title, pts):
    txt = f'Soru {num} — {title} ({pts} puan)'
    t = Table([[P(txt, S('qh', fontName='AU-B', fontSize=11,
                         textColor=colors.white))]],
              colWidths=[W - 2*MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), GREEN),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def data_table(data, col_widths, head_bg=TABLE_HEAD):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  head_bg),
        ('TEXTCOLOR',     (0,0), (-1,0),  colors.white),
        ('FONTNAME',      (0,0), (-1,0),  'AU-B'),
        ('FONTNAME',      (0,1), (-1,-1), 'AU'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('LEADING',       (0,0), (-1,-1), 13),
        ('ALIGN',         (0,0), (-1,-1), 'LEFT'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#aaaaaa')),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, LGRAY]),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
# Story
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── Başlık ────────────────────────────────────────────────────────────────────
story += [
    sp(8),
    P('Lab 2 — Attention Mekanizmasının Önemi', sTitle),
    P('CEVAP ANAHTARI', S('ct', fontName='AU-B', fontSize=16,
                          textColor=GREEN, alignment=1, spaceAfter=2)),
    P('microGPT: Attention vs. MLP Karşılaştırması', sSubtitle),
    sp(4), hr(), sp(4),
]

# ── Ön Bilgi ──────────────────────────────────────────────────────────────────
story.append(section_bar('Ön Bilgi'))
story.append(sp(6))
ob = Table([[P(
    'Bir önceki laboratuvarda microGPT\'nin modüler mimarisini ve temperature '
    'parametresini inceledik. Bu laboratuvarda transformer modellerinin en kritik '
    'bileşeni olan self-attention mekanizmasını deneysel olarak sorguluyoruz: '
    'attention olmadan, ama tam olarak eşit parametreyle, model ne kadar başarılı olur?',
    sBody
)]], colWidths=[W - 2*MARGIN])
ob.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), LIGHT_BLUE),
    ('BOX',           (0,0), (-1,-1), 1, BLUE),
    ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ('RIGHTPADDING',  (0,0), (-1,-1), 10),
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
]))
story += [ob, sp(8)]

# ── Demo Açıklaması ───────────────────────────────────────────────────────────
story.append(section_bar('Deney: microgpt_ablasyon.py — Kontrollü Karşılaştırma'))
story.append(sp(8))

story += [
    P('Bu laboratuvarda iki model arasındaki farkı net gözlemleyebilmek için sentetik '
      'bir veri seti kullanan microgpt_ablasyon.py scripti çalıştırılmıştır. Gerçek isim '
      'veri setlerinde attention avantajı kısa diziler ve pozisyon kodlaması nedeniyle '
      'maskelenmektedir. Kontrollü deney bunu ortadan kaldırır.', sBody),
    sp(4),
    P('Sentetik Görev Tanımı', sSection),
    P('Her dizi sabit uzunlukta (7 karakter) oluşturulur:', sBody),
    P('• <b>Anchor karakterler:</b> \'a\' veya \'z\'  (dizinin ilk ve son karakteri)', sBullet),
    P('• <b>Filler karakterler:</b> alfabe ortası (b–y), rastgele', sBullet),
    P('• <b>Kural:</b> ilk karakter \'a\' ise son karakter \'a\', \'z\' ise \'z\'', sBullet),
    sp(4),
]

ex_data = [
    [P('Dizi', sBodyB), P('İlk Harf', sBodyB), P('Kural', sBodyB), P('Son Harf (hedef)', sBodyB)],
    [P('"abcdfea"', sCode), P('a', sBody), P('a → a', sBody), P('a', sBody)],
    [P('"zxmkpqz"', sCode), P('z', sBody), P('z → z', sBody), P('z', sBody)],
    [P('"atocbda"', sCode), P('a', sBody), P('a → a', sBody), P('a', sBody)],
]
story += [data_table(ex_data, [6*cm, 3*cm, 4*cm, 5*cm]), sp(8)]

story += [
    P('Neden Bu Görev?', sSection),
    P('<b>Attention modeli</b> için: Pozisyon 0\'daki anchor\'a doğrudan bakabilir — '
      'kural trivialdir, kayıp sıfıra yaklaşmalıdır.', sBullet),
    P('<b>MLP-only modeli</b> için: Son filler pozisyonunda yalnızca (mevcut_harf, '
      'pozisyon) bilgisi vardır. Hangi anchor\'un geleceği bilinemez — en iyi '
      'ihtimalle ~%50 doğru tahmin yapabilir.', sBullet),
    P('<b>Parametre eşitliği:</b> Her iki model tam olarak 4.192 eğitilebilir '
      'parametreye sahiptir. Fark kapasiteden değil, mimari yapıdan kaynaklanır.', sBullet),
    sp(8),
    P('Mimarilerin Karşılaştırılması', sSection),
]

arch_data = [
    [P('Özellik', sBodyB), P('Attention Modeli', sBodyB), P('MLP-Only Modeli', sBodyB)],
    [P('Bağlam erişimi', sBody),
     P('Tüm önceki tokenlar (Q×K^T)', sBody),
     P('Yalnızca mevcut token', sBody)],
    [P('Attention bloğu', sBody),
     P('Wq, Wk, Wv, Wo: 4×(16×16)=1.024', sBody),
     P('ctx_fc1+fc2: (16×32)+(32×16)=1.024', sBody)],
    [P('Feed-forward MLP', sBody),
     P('fc1+fc2: (64×16)+(16×64)=2.048', sBody),
     P('fc1+fc2: (64×16)+(16×64)=2.048', sBody)],
    [P('Embedding + LM Head', sBody), P('~1.120', sBody), P('~1.120', sBody)],
    [P('<b>TOPLAM</b>', sBodyB), P('<b>4.192</b>', sBodyB), P('<b>4.192</b>', sBodyB)],
]
story += [data_table(arch_data, [5*cm, 7*cm, 7*cm]), sp(8)]

story.append(P('Gerçek Deney Sonuçları (Referans Değerler)', sSection))
res_data = [
    [P('Metrik', sBodyB), P('Attention', sBodyB), P('MLP-Only', sBodyB)],
    [P('KEY pozisyon kaybı (son 500 adım)', sBody),
     P('0.0018', sResult), P('0.7114', sResult)],
    [P('Kayıp farkı', sBody),
     P('+0.7096  (teorik maks: log(2)=0.6931)', sResult), P('—', sBody)],
    [P('Doğruluk (100 yeni örnek)', sBody),
     P('100/100 = %100', sResult), P('42/100 = %42', sResult)],
]
res_t = Table(res_data, colWidths=[7*cm, 5.5*cm, 5.5*cm])
res_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  TABLE_HEAD),
    ('TEXTCOLOR',     (0,0), (-1,0),  colors.white),
    ('FONTNAME',      (0,0), (-1,0),  'AU-B'),
    ('FONTNAME',      (0,1), (-1,-1), 'AU'),
    ('FONTSIZE',      (0,0), (-1,-1), 9),
    ('LEADING',       (0,0), (-1,-1), 13),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#aaaaaa')),
    ('BACKGROUND',    (1,1), (1,-1),  colors.HexColor('#e8f5e9')),
    ('BACKGROUND',    (2,1), (2,-1),  colors.HexColor('#fff3e0')),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ('TOPPADDING',    (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story += [res_t, sp(8)]

# ── Attention Kafalarının Hesaplanması ───────────────────────────────────────
story.append(P('Attention Kafalarının Hesaplanması', sSection))
story += [
    P('Model 4 bağımsız attention kafasına sahiptir. 16 boyutlu vektör 4 kafaya '
      'eşit olarak bölünür: her kafa <b>head_dim = 16 / 4 = 4</b> boyutla çalışır.', sBody),
    sp(4),
    P('<b>Adım 1 — Benzerlik skoru:</b> pid=6\'daki token, her önceki tokenla '
      'nokta çarpımı hesaplar:', sBody),
]

def formula_box(text):
    t = Table([[P(text, S('fx', fontName='AU-B', fontSize=10, leading=14,
                          textColor=BLUE, alignment=1))]],
              colWidths=[W - 2*MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LIGHT_BLUE),
        ('BOX',           (0,0), (-1,-1), 1, BLUE),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    return t

story += [
    formula_box('score(t) = Σⱼ  q[j] × k[t][j]  /  √head_dim'),
    sp(5),
    P('<b>Adım 2 — Softmax:</b> Skorlar olasılığa dönüştürülür — '
      'tüm pozisyonların ağırlıkları toplamı 1\'e eşit olur:', sBody),
    formula_box('aw[t] = exp(score(t)) / Σₜ exp(score(t))'),
    sp(5),
    P('<b>Adım 3 — Ağırlıklı toplam:</b> Her pozisyonun V vektörü '
      'attention ağırlığıyla çarpılarak toplanır:', sBody),
    formula_box('out[j] = Σₜ  aw[t] × v[t][j]'),
    sp(5),
    P('Her kafa bu hesabı <b>bağımsız olarak</b> yapar. Eğitim sırasında her kafa '
      'farklı bir örüntüye odaklanmayı öğrenebilir.', sBody),
    sp(8),
]

# ── Ön Hazırlık ───────────────────────────────────────────────────────────────
story.append(section_bar('Ön Hazırlık'))
story.append(sp(6))
story += [
    P('Deneye başlamadan önce aşağıdaki komutu çalıştırın ve çıktıları kaydedin:',
      sBody),
    sp(3),
]
cmd_t = Table([[P('python microgpt_ablasyon.py', sCode)]],
              colWidths=[W - 2*MARGIN])
cmd_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#f4f4f4')),
    ('BOX',           (0,0), (-1,-1), 1, colors.HexColor('#aaaaaa')),
    ('LEFTPADDING',   (0,0), (-1,-1), 12),
    ('TOPPADDING',    (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story += [cmd_t, sp(6)]
story += [
    P('Beklenen çıktı yapısı:', sBody),
    P('• Her 200 adımda kayıp değerleri (attn key_loss ve mlp key_loss)', sBullet),
    P('• Son 500 adım özet tablosu', sBullet),
    P('• 100 yeni örnekte doğruluk testi', sBullet),
    P('• 4 örnek için attention ağırlık tablosu (her kafa × her pozisyon)', sBullet),
    sp(8), hr(), sp(4),
]

# ── Sorular ───────────────────────────────────────────────────────────────────
story.append(P('SORULAR VE CEVAP ANAHTARI',
               S('sqh', fontName='AU-B', fontSize=14, textColor=BLUE,
                 alignment=1, spaceAfter=6)))
story += [hr(), sp(4)]

# ─── Soru 1 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(1, 'Kayıp Değeri Analizi', 20),
    sp(6),
    P('microgpt_ablasyon.py çıktısından her 200 adımda bir attn key_loss ve mlp key_loss '
      'değerlerini tabloya yazın. Son 500 adım ortalama kayıp değerini de belirtin.',
      sBody),
    sp(6),
]))

train_data = [
    [P('Adım',  sBodyB), P('attn key_loss', sBodyB),
     P('mlp key_loss', sBodyB), P('Fark (+)', sBodyB)],
    [P('200',  sBody), P('~0.913', sAns), P('~0.971', sAns), P('~0.058', sAns)],
    [P('400',  sBody), P('~0.041', sAns), P('~0.766', sAns), P('~0.726', sAns)],
    [P('600',  sBody), P('~0.006', sAns), P('~0.726', sAns), P('~0.721', sAns)],
    [P('800',  sBody), P('~0.002', sAns), P('~0.718', sAns), P('~0.717', sAns)],
    [P('1000', sBody), P('~0.001', sAns), P('~0.707', sAns), P('~0.706', sAns)],
    [P('<b>Son 500 adım ort.</b>', sBodyB),
     P('<b>0.0018</b>', sAnsB), P('<b>0.7114</b>', sAnsB), P('<b>+0.7096</b>', sAnsB)],
]
story += [data_table(train_data, [3*cm, 4.5*cm, 4.5*cm, 4*cm]), sp(6)]

story.append(answer_box([
    P('Attention modeli: Son 500 adım key_loss = <b>0.0018</b>', sAns),
    P('MLP-Only modeli: Son 500 adım key_loss = <b>0.7114</b>', sAns),
    P('Teorik maksimum fark: log(2) = 0.6931 nat', sAns),
    P('Gerçek fark: 0.7096 — teorik maksimumun yaklaşık %102\'si, beklenen aralıkta.', sAns),
    sp(4),
    P('<b>Yorum:</b> Attention modeli neredeyse sıfır kayba ulaşırken MLP-only model '
      'log(2)\'ye çok yakın kayıpta takılıp kalmıştır. Bu, MLP\'nin iki sınıfın birini '
      '(~%50 olasılıkla) rastgele seçmekten daha iyi yapamadığı anlamına gelir.', sAns),
]))
story.append(sp(10))

# ─── Soru 2 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(2, 'Doğruluk Karşılaştırması', 25),
    sp(6),
    P('100 yeni örnekteki doğruluk sonuçlarını karşılaştırın.', sBody),
    sp(6),
]))

story.append(P('2a) Özet Tablo', sQ))
acc_data = [
    [P('Model', sBodyB), P('Doğru Tahmin', sBodyB),
     P('Doğruluk', sBodyB), P('Beklenen?', sBodyB)],
    [P('Attention', sBody), P('100/100', sAns), P('%100', sAns),
     P('Evet — anchor\'a bakabilir', sAns)],
    [P('MLP-Only',  sBody), P('42/100',  sAns), P('%42',  sAns),
     P('Evet — ~%50 rastgele tahmin', sAns)],
]
story += [data_table(acc_data, [4.5*cm, 4*cm, 3*cm, 6.5*cm]), sp(6)]

story.append(P('2b) Bireysel Tahmin Örnekleri', sQ))
pred_data = [
    [P('Prefix', sBodyB), P('Doğru', sBodyB),
     P('Attention Tahmini', sBodyB), P('MLP Tahmini', sBodyB)],
    [P('znhugi', sCode), P('z', sBody), P('z (0.00/1.00)', sAns),
     P('a (0.55/0.45) — YANLIŞ', sAns)],
    [P('afdjyn', sCode), P('a', sBody), P('a (1.00/0.00)', sAns),
     P('a (0.55/0.44)', sAns)],
    [P('zrhupc', sCode), P('z', sBody), P('z (0.00/1.00)', sAns),
     P('a (0.55/0.45) — YANLIŞ', sAns)],
    [P('auqhoy', sCode), P('a', sBody), P('a (1.00/0.00)', sAns),
     P('a (0.56/0.44)', sAns)],
]
story += [data_table(pred_data, [3.5*cm, 2.5*cm, 5.5*cm, 6.5*cm]), sp(6)]

story.append(answer_box([
    P('<b>Gözlem:</b> MLP modeli hemen hemen her zaman \'a\' tahmin eder '
      '(çıktı dağılımı ~0.55/0.45 ile sabit kalır).', sAns),
    P('MLP\'nin \'z\' ile başlayan dizilerde bile \'a\' tahmin etmesinin nedeni: '
      'Son filler pozisyonunda yalnızca (mevcut_harf, pozisyon) bilgisi vardır; '
      'hangi anchor\'un geleceği bilinemez. Prior\'a göre \'a\' tahmin eder.', sAns),
    P('Attention ise pozisyon 0\'daki tokeni doğrudan okuyabilir; Q×K^T attention '
      'ağırlığı ile ilk token\'ın V vektörünü çekerek mevcut tokena aktarır.', sAns),
]))
story.append(sp(10))

# ─── Soru 3 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(3, 'Neden Parametre Sayısı Eşit?', 20),
    sp(6),
    P('microgpt_ablasyon.py dosyasındaki attention ve MLP bloklarının parametre sayılarını '
      'matematiksel olarak gösterin. attn_hidden=32 değerinin nasıl seçildiğini açıklayın.',
      sBody),
    sp(6),
]))

story.append(answer_box([
    P('<b>Attention bloğu parametre hesabı:</b>', sAnsB),
    P('Wq: 16×16 = 256', sAns),
    P('Wk: 16×16 = 256', sAns),
    P('Wv: 16×16 = 256', sAns),
    P('Wo: 16×16 = 256', sAns),
    P('<b>Toplam: 4 × 256 = 1.024 parametre</b>', sAnsB),
    sp(4),
    P('<b>ctx_fc1 + ctx_fc2 parametre hesabı:</b>', sAnsB),
    P('ctx_fc1: attn_hidden × n_embd = 32 × 16 = 512', sAns),
    P('ctx_fc2: n_embd × attn_hidden = 16 × 32 = 512', sAns),
    P('<b>Toplam: 512 + 512 = 1.024 parametre</b>', sAnsB),
    sp(4),
    P('<b>attn_hidden = 32 seçiminin nedeni:</b>', sAnsB),
    P('2 × (n_embd × attn_hidden) = 4 × n_embd²', sAns),
    P('2 × (16 × attn_hidden) = 4 × 256  →  attn_hidden = 1024 / 32 = 32', sAns),
    sp(4),
    P('<b>Neden eşit parametre önemlidir?</b>', sAnsB),
    P('Eğer MLP-only modeline daha fazla parametre verilseydi, zayıf performans '
      '"yetersiz kapasite" ile açıklanabilirdi. Parametre eşitliği, gözlemlenen farkın '
      'YALNIZCA mimarinin bağlam erişim kapasitesinden kaynaklandığını kanıtlar.', sAns),
]))
story.append(sp(10))

# ─── Soru 4 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(4, 'Attention Mekanizmasının Temeli', 25),
    sp(6),
]))

story += [
    P('4a) Bağlam erişimi', sQ),
    answer_box([
        P('<b>Attention bloğu:</b> KEY_POS=6\'daki token, tüm önceki tokenlarla '
          'Q×K^T hesaplar. Pozisyon 0\'dan 5\'e kadar 6 tokenle doğrudan iletişim '
          'kurabilir; özellikle pozisyon 0\'daki anchor tokene odaklanabilir.', sAns),
        P('<b>MLP bloğu:</b> Yalnızca mevcut token\'in (token_id, pos_id) bilgisine '
          'erişebilir. Önceki tokenlar hakkında hiçbir bilgi yoktur — bağlam erişimi sıfırdır.',
          sAns),
    ]),
    sp(6),
    P('4b) Attention formülü açıklaması', sQ),
    answer_box([
        P('Attention(Q, K, V) = softmax(Q × K^T / √d_k) × V', sAnsB),
        sp(4),
        P('<b>Q (Query):</b> Mevcut tokenin "ne arıyorum?" sorusunu temsil eden vektör. '
          'Wq matrisi ile hesaplanır.', sAns),
        P('<b>K (Key):</b> Her önceki tokenin "ben bununla ilgiliyim" etiketini '
          'temsil eden vektör. Wk matrisi ile hesaplanır.', sAns),
        P('<b>V (Value):</b> Her önceki tokenin gerçek bilgi içeriği. '
          'Wv matrisi ile hesaplanır; attention ağırlıklarıyla ağırlıklı toplam alınır.', sAns),
        sp(4),
        P('<b>√d_k ile bölmenin amacı:</b> Q×K^T çarpımı yüksek boyutlu uzaylarda '
          'çok büyük değerler üretir. Bu değerler softmax\'i doyuma sokar ve '
          'gradyanları sıfıra yaklaştırır. √d_k ile bölmek skoru normalize ederek '
          'kararlı gradyan akışını sağlar.', sAns),
    ]),
    sp(6),
    P('4c) MLP-only dezavantajının açıklaması', sQ),
    answer_box([
        P('MLP-only model her tokeni izole olarak işler: yalnızca mevcut karakteri ve '
          'pozisyonunu görür. "abcdef" dizisinde son filler karakteri olan \'f\'yi '
          'gördüğünde, bunun \'a\' ile mi yoksa \'z\' ile mi başlayan bir dizide '
          'olduğunu bilemez.', sAns),
        P('Bu laboratuvarın görevinde kural şudur: ilk karakter \'a\' ise son karakter '
          '\'a\', \'z\' ise \'z\'dir. Bu bilgi pozisyon 0\'dadır; son filler '
          'pozisyonundan (pozisyon 5) erişilmesi ancak attention ile mümkündür.', sAns),
        P('MLP birden fazla tokeni doğrudan "hatırlamaz" — ne kadar büyük olursa olsun, '
          'keyfi uzunluktaki pozisyon 0 bilgisini mevcut pozisyona aktaramaz. '
          'Bu nedenle rastgele tahmin (%50) doğruluğunun üzerini geçemez.', sAns),
    ]),
    sp(10),
]

# ─── Soru 5 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(5, 'Deney Tasarımı', 10),
    sp(6),
    P('Bu deneyin "kontrollü" olduğunu savunun. Parametre sayısını sabit tutmanın '
      'bilimsel önemi nedir?', sBody),
    sp(6),
]))

story.append(answer_box([
    P('<b>Kontrollü deney kriterleri:</b>', sAnsB),
    P('1. <b>Bağımsız değişken:</b> Mimari (attention var/yok)', sAns),
    P('2. <b>Sabit tutulanlar:</b> Parametre sayısı (4.192), öğrenme hızı, veri seti, '
      'eğitim adımları, rastgele tohum', sAns),
    P('3. <b>Bağımlı değişken:</b> KEY pozisyon kaybı ve doğruluk', sAns),
    sp(4),
    P('<b>Parametre eşitliğinin bilimsel önemi:</b>', sAnsB),
    P('Eğer MLP-only modeline daha az parametre verilseydi: Zayıf sonuç '
      '"yetersiz kapasite" ile açıklanabilirdi — attention lehine adaletsiz.', sAns),
    P('Eğer MLP-only modeline daha fazla parametre verilseydi: İyi sonuç '
      '"daha fazla kapasite" ile açıklanabilirdi — MLP lehine adaletsiz.', sAns),
    P('Eşit parametre: Gözlemlenen fark YALNIZCA tokenlar arası iletişime (attention) '
      'atfedilebilir. Bu, bilimsel çıkarım için gerekli kontrol koşulunu sağlar.', sAns),
    sp(4),
    P('<b>MLP-only modeline daha fazla parametre verilseydi:</b>', sAnsB),
    P('Performansı biraz artabilirdi. Ancak kritik nokta şudur: MLP ne kadar büyük '
      'olursa olsun, keyfi uzunluktaki pozisyon 0 bilgisini mevcut pozisyona aktaramaz. '
      'Bu iş için attention gibi dinamik, içeriğe bağlı bir mekanizma gereklidir. '
      'Büyük MLP belki ezberleme yapabilir ama genelleme yapamazdı.', sAns),
]))
story.append(sp(10))

# ─── Soru 6 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(6, 'Attention Kafası Uzmanlaşması', 15),
    sp(6),
    P('microgpt_ablasyon.py çıktısının attention ağırlık tablosunu inceleyin.', sBody),
    sp(6),
]))

story.append(P('6a) Gerçek Ağırlık Değerleri (örnek: "zlhihe", anchor=\'z\')', sQ))

head_data = [
    [P('Kafa', S('hw', fontName='AU-B', fontSize=9, textColor=colors.white)),
     P('pid=0\n(BOS)',    S('hw2', fontName='AU-B', fontSize=9, textColor=colors.white)),
     P('pid=1\n(anchor)', S('hw3', fontName='AU-B', fontSize=9, textColor=colors.white)),
     P('pid=2', S('hw4', fontName='AU-B', fontSize=9, textColor=colors.white)),
     P('pid=3', S('hw5', fontName='AU-B', fontSize=9, textColor=colors.white)),
     P('pid=4', S('hw6', fontName='AU-B', fontSize=9, textColor=colors.white)),
     P('pid=5', S('hw7', fontName='AU-B', fontSize=9, textColor=colors.white)),
     P('pid=6', S('hw8', fontName='AU-B', fontSize=9, textColor=colors.white))],
    [P('Kafa 1', sBody), P('0.05', sAns), P('0.25', sAns), P('0.38', sAns),
     P('0.05', sAns), P('0.08', sAns), P('0.05', sAns), P('0.13', sAns)],
    [P('Kafa 2', sBody), P('0.02', sAns), P('0.04', sAns), P('0.35', sAns),
     P('0.12', sAns), P('0.30', sAns), P('0.12', sAns), P('0.05', sAns)],
    [P('Kafa 3', sBody), P('0.00', sAnsB), P('<b>0.95</b>', sAnsB), P('0.05', sAnsB),
     P('0.00', sAnsB), P('0.00', sAnsB), P('0.00', sAnsB), P('0.00', sAnsB)],
    [P('Kafa 4', sBody), P('0.07', sAns), P('0.27', sAns), P('0.15', sAns),
     P('0.14', sAns), P('0.12', sAns), P('0.14', sAns), P('0.12', sAns)],
    [P('<b>Ortalama</b>', sBodyB), P('0.04', sAnsB), P('<b>0.38</b>', sAnsB),
     P('0.23', sAnsB), P('0.08', sAnsB), P('0.13', sAnsB), P('0.08', sAnsB), P('0.07', sAnsB)],
]
ht = Table(head_data, colWidths=[1.8*cm, 2.0*cm, 2.3*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm])
ht.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  TABLE_HEAD),
    ('BACKGROUND',    (0,3), (-1,3),  colors.HexColor('#e8f5e9')),
    ('FONTNAME',      (0,0), (-1,0),  'AU-B'),
    ('FONTNAME',      (0,1), (-1,-1), 'AU'),
    ('FONTSIZE',      (0,0), (-1,-1), 8.5),
    ('LEADING',       (0,0), (-1,-1), 12),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#aaaaaa')),
    ('ROWBACKGROUNDS',(0,1), (-1,-2), [colors.white, colors.HexColor('#f5f5f5')]),
    ('LEFTPADDING',   (0,0), (-1,-1), 5),
    ('RIGHTPADDING',  (0,0), (-1,-1), 5),
    ('TOPPADDING',    (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
]))
story += [ht, sp(6)]

story.append(answer_box([
    P('<b>6b) Uzmanlaşma gözlemi:</b>', sAnsB),
    P('<b>Kafa 3</b> her örnekte pid=1\'e (anchor pozisyonu) neredeyse %100 '
      'ağırlık veriyor. Diğer örneklerde de:', sAns),
    P('kafa 3: 0.00 / <b>1.00</b> / 0.00 / 0.00 / 0.00 / 0.00 / 0.00  (anchor=\'a\')', sCode),
    P('kafa 3: 0.00 / <b>0.92</b> / 0.00 / 0.01 / 0.06 / 0.02 / 0.00  (anchor=\'z\')', sCode),
    sp(3),
    P('Kafa 3 tamamen "anchor dedektörü" rolüne uzmanlaşmıştır: ne olursa olsun '
      'pozisyon 1\'e bak, oradan anchor bilgisini al.', sAns),
    P('Diğer kafalar daha genel örüntülere odaklanmış — kafa 1/4 geniş bağlam, '
      'kafa 2 yerel komşuluk.', sAns),
], label='CEVAP'))
story.append(sp(6))

story.append(answer_box([
    P('<b>6c) Uzmanlaşma nasıl oluştu?</b>', sAnsB),
    P('Eğitim sırasında geri yayılım (backprop) Wq ve Wk matrislerini günceller. '
      'pid=6\'da pid=1\'e yüksek ağırlık vermek kaybı düşürüyor — bu durum sürekli '
      'pekiştirildi.', sAns),
    P('Mekanizma:', sAnsB),
    P('• Wq: pid=6\'nın sorgu vektörünü öyle ayarlar ki pid=1\'in anahtar vektörüyle '
      'nokta çarpımı maksimum olsun.', sAns),
    P('• Wk: pid=1\'in anahtar vektörünü öyle ayarlar ki pid=6\'nın sorgu vektörüyle '
      'nokta çarpımı maksimum olsun.', sAns),
    P('• Softmax: fark büyüdükçe (%e^9 vs e^-8) ağırlık 1.0\'a yaklaşır.', sAns),
    P('Kafa 3 için bu "anlaşma" mükemmelleşti — diğer kafalar farklı görevler üstlendi.', sAns),
], label='CEVAP'))
story.append(sp(10))

# ── Kapanış notu ──────────────────────────────────────────────────────────────
story.append(HRFlowable(width='100%', thickness=2, color=GREEN,
                        spaceAfter=6, spaceBefore=6))
story.append(P(
    'Cevap anahtarı öğretmen kullanımına mahsustur. '
    'microgpt_ablasyon.py çıktısı deterministik değildir (farklı donanım/platform üzerinde '
    'hafif farklılıklar görülebilir). Temel sonuç değişmez: attention ~%100, MLP ~%42–55. '
    'Kafa 3 uzmanlaşması her çalıştırmada gözlemlenir.',
    S('fn', fontSize=8, leading=12, textColor=GRAY, alignment=1)
))

# ── Build ─────────────────────────────────────────────────────────────────────
OUT   = '/Users/kemalbicakci/Desktop/microgpt-lab/lab2-cevap.pdf'
frame = Frame(MARGIN, 1.2*cm, W - 2*MARGIN, H - 2.8*cm, id='main')
tmpl  = PageTemplate(id='p', frames=[frame], onPage=header_footer)
doc   = BaseDocTemplate(OUT, pagesize=A4, pageTemplates=[tmpl],
                        leftMargin=MARGIN, rightMargin=MARGIN,
                        topMargin=1.6*cm, bottomMargin=1.2*cm)
doc.build(story)
print('lab2-cevap.pdf OK')
