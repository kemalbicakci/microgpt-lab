# -*- coding: utf-8 -*-
"""Generate lab2.pdf — Question paper for Lab 2."""

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
BLUE       = colors.HexColor('#1a3a5c')
LIGHT_BLUE = colors.HexColor('#e8f0f8')
GREEN      = colors.HexColor('#1a5c2a')
DARK_GREEN = colors.HexColor('#155724')
ANS_BG     = colors.HexColor('#f9f9f9')
TABLE_HEAD = colors.HexColor('#1a3a5c')
GRAY       = colors.HexColor('#555555')
LGRAY      = colors.HexColor('#f5f5f5')
BOX_BG     = colors.HexColor('#f0f4f8')

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
              textColor=BLUE, spaceBefore=8, spaceAfter=4)
sBody    = S('sBody',   fontSize=10, leading=14, spaceAfter=4)
sBodyB   = S('sBodyB',  fontName='AU-B', fontSize=10, leading=14, spaceAfter=4)
sBodyBW  = S('sBodyBW', fontName='AU-B', fontSize=10, leading=14, spaceAfter=4,
              textColor=colors.white)  # mavi/koyu zemin için beyaz başlık
sBullet  = S('sBullet', fontSize=10, leading=14, leftIndent=16, spaceAfter=3)
sCode    = S('sCode',   fontName='AU', fontSize=9, leading=13, spaceAfter=3,
              textColor=colors.HexColor('#333333'),
              backColor=colors.HexColor('#f4f4f4'),
              leftIndent=12, rightIndent=12)
sNote    = S('sNote',   fontSize=9, leading=13, textColor=GRAY,
              leftIndent=8, spaceAfter=4)

# ── Page chrome ───────────────────────────────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BLUE)
    canvas.rect(0, H - 1.2*cm, W, 1.2*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont('AU-B', 10)
    canvas.drawString(MARGIN, H - 0.85*cm, 'microGPT Lab 2')
    canvas.setFont('AU', 9)
    canvas.drawRightString(W - MARGIN, H - 0.85*cm,
                           'Attention Mekanizmasının Önemi')
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

def answer_box(height_cm=2.5, label='Yanıtınız:'):
    inner = Table(
        [[P(label, S('al', fontSize=8, textColor=GRAY))]],
        colWidths=[W - 2*MARGIN - 0.8*cm],
        rowHeights=[height_cm * cm]
    )
    inner.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), ANS_BG),
        ('BOX',           (0,0), (-1,-1), 0.8, colors.HexColor('#bbbbbb')),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    return inner

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
        ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#1a3a5c')),
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
    P('microGPT: Attention vs. MLP Karşılaştırması', sSubtitle),
    sp(4), hr(), sp(4),
]

# ── Ön Bilgi ──────────────────────────────────────────────────────────────────
story.append(section_bar('Ön Bilgi'))
story.append(sp(6))
ob = Table([[P(
    'Bir önceki laboratuvarda microGPT\'nin modüler mimarisini ve temperature '
    'parametresini inceledik. Bu laboratuvarda transformer modellerinin en kritik '
    'bileşeni olan self-attention mekanizmasını deneysel olarak sorguluyoruz, '
    'onun olmadığı bir modelle karşılaştırıyoruz.',
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

# ── Mimarilerin Tanımı ────────────────────────────────────────────────────────
story.append(section_bar('Mimarilerin Tanımı'))
story.append(sp(6))
story += [
    P('<b>Orijinal microGPT</b> (microgpt_ablasyon.py — Attention modeli):', sBody),
    P('Her katmanda Multi-Head Self-Attention + Feed-Forward MLP bloğu bulunur. '
      'Attention bloğu, her token\'ın tüm önceki tokenlara bakmasını sağlar.', sBullet),
    sp(4),
    P('<b>MLP-Only modeli</b> (microgpt_ablasyon.py — MLP-Only modeli):', sBody),
    P('Attention bloğu, eşit parametreli 2 katmanlı bir MLP ile değiştirilmiştir. '
      'Bu MLP her tokeni yalnızca kendi bilgisiyle işler; önceki tokenlara erişemez.', sBullet),
    sp(8),
]

# Parametre tablosu
story.append(P('Parametre Tablosu', sSection))
param_data = [
    [P('Bileşen', sBodyBW), P('Orijinal (Attention)', sBodyBW), P('MLP-Only', sBodyBW)],
    [P('Attention ağırlıkları (Wq, Wk, Wv, Wo)', sBody),
     P('4 × (16×16) = 1.024', sBody), P('—', sBody)],
    [P('Attention yerine ctx MLP (fc1, fc2)', sBody),
     P('—', sBody), P('(16×32)+(32×16) = 1.024', sBody)],
    [P('Feed-forward MLP (fc1, fc2)', sBody),
     P('(64×16)+(16×64) = 2.048', sBody), P('(64×16)+(16×64) = 2.048', sBody)],
    [P('Embedding + LM Head', sBody), P('~1.120', sBody), P('~1.120', sBody)],
    [P('<b>TOPLAM</b>', sBodyB), P('<b>~4.192</b>', sBodyB), P('<b>~4.192</b>', sBodyB)],
]
story += [data_table(param_data, [7*cm, 5.5*cm, 5.5*cm]), sp(6)]

note_t = Table([[P(
    '<b>Temel fark:</b> İki model aynı sayıda parametreye sahiptir. '
    'Bu deney, çıktı kalitesindeki farkın ekstra kapasiteden değil, '
    'mimarinin yapısından kaynaklandığını kanıtlamak için tasarlanmıştır.',
    sNote
)]], colWidths=[W - 2*MARGIN])
note_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), BOX_BG),
    ('BOX',           (0,0), (-1,-1), 1, colors.HexColor('#aabbcc')),
    ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ('RIGHTPADDING',  (0,0), (-1,-1), 10),
    ('TOPPADDING',    (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story += [note_t, sp(8)]

# ── Demo Açıklaması ───────────────────────────────────────────────────────────
story.append(section_bar('Deney: microgpt_ablasyon.py — Kontrollü Karşılaştırma'))
story.append(sp(8))

story += [
    P('Bu laboratuvarda iki model arasındaki farkı net gözlemleyebilmek için '
      'sentetik bir veri seti kullanan microgpt_ablasyon.py scripti kullanılmaktadır. '
      'Gerçek isim veri setlerinde attention avantajı kısa diziler ve pozisyon '
      'kodlaması nedeniyle maskelenmektedir. Kontrollü deney bunu ortadan kaldırır.',
      sBody),
    sp(4),
    P('Sentetik Görev Tanımı', sSection),
    P('Her dizi sabit uzunlukta (7 karakter) oluşturulur:', sBody),
    P('• <b>Anchor karakterler:</b> \'a\' veya \'z\'  (dizinin ilk ve son karakteri)', sBullet),
    P('• <b>Filler karakterler:</b> alfabe ortası (b–y), rastgele', sBullet),
    P('• <b>Kural:</b> ilk karakter \'a\' ise son karakter \'a\', \'z\' ise \'z\'', sBullet),
    sp(4),
]

ex_data = [
    [P('Dizi', sBodyBW), P('İlk Harf', sBodyBW), P('Kural', sBodyBW), P('Son Harf (hedef)', sBodyBW)],
    [P('"abcdfea"', sCode), P('a', sBody), P('a → a', sBody), P('a', sBody)],
    [P('"zxmkpqz"', sCode), P('z', sBody), P('z → z', sBody), P('z', sBody)],
    [P('"atocbda"', sCode), P('a', sBody), P('a → a', sBody), P('a', sBody)],
]
story += [data_table(ex_data, [6*cm, 3*cm, 4*cm, 5*cm]), sp(8)]

story += [
    P('Neden Bu Görev?', sSection),
    P('<b>Attention modeli:</b> Pozisyon 0\'daki anchor\'a doğrudan bakabilir — '
      'kural trivialdir, kayıp sıfıra yaklaşmalıdır.', sBullet),
    P('<b>MLP-only modeli:</b> Son filler pozisyonunda yalnızca (mevcut_harf, '
      'pozisyon) bilgisi vardır. Hangi anchor\'un geleceği bilinemez — '
      'en iyi ihtimalle ~%50 doğruluk.', sBullet),
    sp(8),
]

arch_data = [
    [P('Özellik', sBodyBW), P('Attention Modeli', sBodyBW), P('MLP-Only Modeli', sBodyBW)],
    [P('Bağlam erişimi', sBody),
     P('Tüm önceki tokenlar (Q×K^T)', sBody),
     P('Yalnızca mevcut token', sBody)],
    [P('KEY pozisyon tahmini', sBody),
     P('Pozisyon 0\'a bakarak anchor\'u bilir', sBody),
     P('Hangi anchor\'un geleceğini bilemez', sBody)],
    [P('Beklenen doğruluk', sBody),
     P('~%100', sBody), P('~%50 (rastgele)', sBody)],
]
story += [data_table(arch_data, [5*cm, 7*cm, 7*cm]), sp(8)]

# ── Attention Kafalarının Hesaplanması ───────────────────────────────────────
story.append(P('Attention Kafalarının Hesaplanması', sSection))
story += [
    P('Model 4 bağımsız attention kafasına sahiptir. 16 boyutlu vektör 4 kafaya '
      'eşit olarak bölünür: her kafa <b>head_dim = 16 / 4 = 4</b> boyutla çalışır.', sBody),
    sp(4),
    P('<b>Adım 1 — Benzerlik skoru:</b> pid=6\'daki token, her önceki tokenla '
      'nokta çarpımı hesaplar:', sBody),
]

formula1 = Table([[P('score(t) = Σⱼ  q[j] × k[t][j]  /  √head_dim',
                     S('f1', fontName='AU-B', fontSize=10, leading=14,
                       textColor=BLUE, alignment=1))]],
                 colWidths=[W - 2*MARGIN])
formula1.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), LIGHT_BLUE),
    ('BOX',           (0,0), (-1,-1), 1, BLUE),
    ('TOPPADDING',    (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
]))
story += [formula1, sp(6)]

story += [
    P('<b>Adım 2 — Softmax:</b> Skorlar olasılığa dönüştürülür — tüm '
      'pozisyonların ağırlıkları toplamı 1\'e eşit olur:', sBody),
]

formula2 = Table([[P('aw[t] = exp(score(t)) / Σₜ exp(score(t))',
                     S('f2', fontName='AU-B', fontSize=10, leading=14,
                       textColor=BLUE, alignment=1))]],
                 colWidths=[W - 2*MARGIN])
formula2.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), LIGHT_BLUE),
    ('BOX',           (0,0), (-1,-1), 1, BLUE),
    ('TOPPADDING',    (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
]))
story += [formula2, sp(6)]

story += [
    P('<b>Adım 3 — Ağırlıklı toplam:</b> Her pozisyonun V (value) vektörü, '
      'attention ağırlığıyla çarpılarak toplanır:', sBody),
]

formula3 = Table([[P('out[j] = Σₜ  aw[t] × v[t][j]',
                     S('f3', fontName='AU-B', fontSize=10, leading=14,
                       textColor=BLUE, alignment=1))]],
                 colWidths=[W - 2*MARGIN])
formula3.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), LIGHT_BLUE),
    ('BOX',           (0,0), (-1,-1), 1, BLUE),
    ('TOPPADDING',    (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
]))
story += [formula3, sp(6)]

story += [
    P('Her kafa bu hesabı <b>bağımsız olarak</b> yapar — kendi Wq ve Wk '
      'matrislerine sahiptir. Eğitim sırasında her kafa farklı bir örüntüye '
      'odaklanmayı öğrenebilir.', sBody),
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
    P('• 100 yeni örnekte doğruluk testi (prefix + doğru tahmin + model tahminleri)',
      sBullet),
    P('• 4 örnek için attention ağırlık tablosu (her kafa × her pozisyon)', sBullet),
    sp(8), hr(), sp(4),
]

# ── Sorular ───────────────────────────────────────────────────────────────────
story.append(P('SORULAR',
               S('sqh', fontName='AU-B', fontSize=14, textColor=BLUE,
                 alignment=1, spaceAfter=6)))
story += [hr(), sp(4)]

# ─── Soru 1 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(1, 'Kayıp Değeri Analizi', 20),
    sp(6),
    P('microgpt_ablasyon.py çıktısından her 200 adımda bir attn key_loss ve '
      'mlp key_loss değerlerini aşağıdaki tabloya yazın. '
      'Son 500 adım ortalama kayıp değerini de belirtin.', sBody),
    sp(6),
]))

train_data = [
    [P('Adım',  sBodyBW), P('attn key_loss', sBodyBW),
     P('mlp key_loss', sBodyBW), P('Fark (+)', sBodyBW)],
    [P('200',  sBody), P('', sBody), P('', sBody), P('', sBody)],
    [P('400',  sBody), P('', sBody), P('', sBody), P('', sBody)],
    [P('600',  sBody), P('', sBody), P('', sBody), P('', sBody)],
    [P('800',  sBody), P('', sBody), P('', sBody), P('', sBody)],
    [P('1000', sBody), P('', sBody), P('', sBody), P('', sBody)],
    [P('<b>Son 500 adım ort.</b>', sBodyB),
     P('', sBody), P('', sBody), P('', sBody)],
]
story += [data_table(train_data, [3*cm, 4.5*cm, 4.5*cm, 4*cm]), sp(6)]

story += [
    P('Hangi model daha düşük kayba ulaşmıştır? Bu fark istatistiksel olarak anlamlı '
      'mı yoksa rastlantısal mı olabilir? Neden?', sBody),
    answer_box(3.0),
    sp(10),
]

# ─── Soru 2 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(2, 'Doğruluk Karşılaştırması', 25),
    sp(6),
    P('Doğruluk testi çıktısından ilk 10 örneği aşağıdaki tabloya yazın, '
      'ardından soruları yanıtlayın.', sBody),
    sp(6),
]))

pred_data = [
    [P('#', sBodyBW), P('Prefix', sBodyBW), P('Doğru', sBodyBW),
     P('Attention Tahmini', sBodyBW), P('MLP Tahmini', sBodyBW)],
] + [
    [P(str(i), sBody), P('', sBody), P('', sBody), P('', sBody), P('', sBody)]
    for i in range(1, 11)
] + [
    [P('<b>Toplam doğru</b>', sBodyB), P('', sBody), P('', sBody),
     P('___/100', sBody), P('___/100', sBody)],
]
story += [data_table(pred_data, [1.2*cm, 3.5*cm, 2*cm, 4.5*cm, 4.8*cm]), sp(6)]

story += [
    P('a) Attention modelinin ürettiği tahminler nasıldı? '
      'Tutarlı bir örüntü gözlemlediniz mi?', sBody),
    answer_box(2.0),
    sp(4),
    P('b) MLP-only modelinin tahminleri nasıldı? Belirgin bir eğilim var mı?', sBody),
    answer_box(2.0),
    sp(4),
    P('c) İki model arasındaki en belirgin farkı kendi cümlelerinizle açıklayın.', sBody),
    answer_box(2.5),
    sp(10),
]

# ─── Soru 3 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(3, 'Neden Parametre Sayısı Eşit?', 20),
    sp(6),
    P('microgpt_ablasyon.py dosyasını inceleyin. Attention bloğunun 4 matrisini '
      '(Wq, Wk, Wv, Wo) neden tam olarak 2 matrislik bir MLP ile değiştirdiğimizi '
      've attn_hidden=32 değerinin nasıl seçildiğini matematiksel olarak gösterin.',
      sBody),
    sp(6),
    answer_box(5.0),
    sp(10),
]))

# ─── Soru 4 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(4, 'Attention Mekanizmasının Temeli', 25),
    sp(6),
]))

story += [
    P('a) Attention bloğu, bir token\'ı işlerken kaç önceki token\'ın bilgisini '
      'kullanır? MLP bloğu kaçını kullanır?', sBody),
    answer_box(2.0),
    sp(4),
    P('b) Attention mekanizması çıktısını hesaplamak için şu formülü kullanır:', sBody),
]

formula_t = Table([[P('Attention(Q, K, V) = softmax(Q × K^T / √d_k) × V',
                      S('ft', fontName='AU-B', fontSize=11, leading=16,
                        textColor=BLUE, alignment=1))]],
                  colWidths=[W - 2*MARGIN])
formula_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), LIGHT_BLUE),
    ('BOX',           (0,0), (-1,-1), 1, BLUE),
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
]))
story += [formula_t, sp(6)]
story += [
    P('Bu formülde Q, K ve V ne anlama gelir? √d_k ile bölmenin amacı nedir?', sBody),
    answer_box(4.0),
    sp(4),
    P('c) MLP-only modelin, bir sonraki harfi tahmin ederken neden dezavantajlı '
      'olduğunu 3–5 cümleyle açıklayın.', sBody),
    answer_box(3.5),
    sp(10),
]

# ─── Soru 5 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(5, 'Deney Tasarımı', 10),
    sp(6),
    P('Bu deneyin "kontrollü" bir deney olduğunu söyleyebilir miyiz? '
      'Parametre sayısını sabit tutmanın bilimsel önemi nedir? '
      'Eğer MLP-only modeline daha fazla parametre verilseydi, '
      'bu deneyin sonuçlarını nasıl yorumlardınız?', sBody),
    sp(6),
    answer_box(4.0),
    sp(10),
]))

# ─── Soru 6 ───────────────────────────────────────────────────────────────────
story.append(KeepTogether([
    q_header(6, 'Attention Kafası Uzmanlaşması', 15),
    sp(6),
    P('microgpt_ablasyon.py çıktısının attention ağırlık tablosunu inceleyin.', sBody),
    sp(4),
]))

story += [
    P('a) 4 kafanın ağırlık değerlerini aşağıdaki tabloya yazın '
      '(herhangi bir örnek için — dizi ve anchor\'u da belirtin):', sBody),
    sp(4),
]

head_data = [
    [P('Kafa', sBodyBW),
     P('pid=0 (BOS)', sBodyBW), P('pid=1 (anchor)', sBodyBW),
     P('pid=2', sBodyBW), P('pid=3', sBodyBW),
     P('pid=4', sBodyBW), P('pid=5', sBodyBW), P('pid=6', sBodyBW)],
    [P('Kafa 1', sBody)] + [P('', sBody)]*7,
    [P('Kafa 2', sBody)] + [P('', sBody)]*7,
    [P('Kafa 3', sBody)] + [P('', sBody)]*7,
    [P('Kafa 4', sBody)] + [P('', sBody)]*7,
    [P('<b>Ortalama</b>', sBodyB)] + [P('', sBody)]*7,
]
story += [data_table(head_data,
                     [1.8*cm, 2.2*cm, 2.5*cm, 1.6*cm, 1.6*cm, 1.6*cm, 1.6*cm, 1.6*cm]),
          sp(6)]

story += [
    P('b) Hangi kafa hangi pozisyona odaklanmış? Bu kafanın rolünü açıklayın.', sBody),
    answer_box(2.5),
    sp(6),
    P('c) Eğitim sırasında bu uzmanlaşma nasıl oluştu? '
      'Wq ve Wk matrislerinin rolünü açıklayın.', sBody),
    answer_box(3.0),
    sp(10),
]

# ── Kapanış ───────────────────────────────────────────────────────────────────
story.append(HRFlowable(width='100%', thickness=2, color=BLUE,
                        spaceAfter=6, spaceBefore=6))
story.append(P(
    'Toplam: 115 puan  |  '
    'microgpt_ablasyon.py çalışma süresi: ~2–5 dakika  |  '
    'Tüm yanıtları kendi cümlelerinizle yazın.',
    S('fn', fontSize=8, leading=12, textColor=GRAY, alignment=1)
))

# ── Build ─────────────────────────────────────────────────────────────────────
OUT   = '/Users/kemalbicakci/Desktop/microgpt-lab/lab2.pdf'
frame = Frame(MARGIN, 1.2*cm, W - 2*MARGIN, H - 2.8*cm, id='main')
tmpl  = PageTemplate(id='p', frames=[frame], onPage=header_footer)
doc   = BaseDocTemplate(OUT, pagesize=A4, pageTemplates=[tmpl],
                        leftMargin=MARGIN, rightMargin=MARGIN,
                        topMargin=1.6*cm, bottomMargin=1.2*cm)
doc.build(story)
print('lab2.pdf OK')
