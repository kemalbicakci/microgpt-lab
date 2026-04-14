"""
Attention vs MLP — Kontrollü Demonstrasyon

Sentetik kural:
  Her dizi ANCHOR('a' veya 'z') ile başlar ve biter; ortası rastgele filler.
  Örnek:  'a' + 'bcdfe' + 'a'  →  "abcdfea"
          'z' + 'xmkpq' + 'z'  →  "zxmkpqz"

Son anchor'ı tahmin etmek için ilk karakteri HATIRLAMAK gerekir.
  Attention → pozisyon 0'a bakabilir → öğrenir
  MLP-only  → sadece (şimdiki_harf, pozisyon) → ~%50 doğruluk
"""

import math, random, sys
random.seed(42)

# ── Veri ─────────────────────────────────────────────────────────────────────
ANCHOR = ['a', 'z']
FILLER = list('bcdefghijklmnopqrstuvwxy')   # 'a' ve 'z' içermez

def make_seq(length=7):
    # Sabit uzunluk → pozisyon tabanlı hile önlenir
    first  = random.choice(ANCHOR)
    middle = [random.choice(FILLER) for _ in range(length - 2)]
    return first + ''.join(middle) + first

SEQ_LEN = 7                                  # sabit uzunluk
docs    = [make_seq(SEQ_LEN) for _ in range(3000)]
print(f"num docs: {len(docs)}")
print(f"örnekler: {docs[:6]}")

uchars     = sorted(set(''.join(docs)))
BOS        = len(uchars)
vocab_size = len(uchars) + 1
block_size = 16
print(f"vocab size: {vocab_size}  (BOS={BOS})")
print(f"KEY_POS={SEQ_LEN-1}  "
      f"(filler→anchor: tokens[{SEQ_LEN-1}]→tokens[{SEQ_LEN}])\n")

# ── Autograd ──────────────────────────────────────────────────────────────────
class Value:
    __slots__ = ('data', 'grad', '_children', '_local_grads')
    def __init__(self, data, children=(), local_grads=()):
        self.data = data; self.grad = 0
        self._children = children; self._local_grads = local_grads
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data+other.data, (self,other), (1,1))
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data*other.data, (self,other), (other.data,self.data))
    def __pow__(self, e): return Value(self.data**e, (self,), (e*self.data**(e-1),))
    def log(self):  return Value(math.log(self.data),  (self,), (1/self.data,))
    def exp(self):  return Value(math.exp(self.data),  (self,), (math.exp(self.data),))
    def relu(self): return Value(max(0,self.data),     (self,), (float(self.data>0),))
    def __neg__(self):         return self*-1
    def __radd__(self,o):      return self+o
    def __sub__(self,o):       return self+(-o)
    def __rsub__(self,o):      return o+(-self)
    def __rmul__(self,o):      return self*o
    def __truediv__(self,o):   return self*o**-1
    def __rtruediv__(self,o):  return o*self**-1
    def backward(self):
        topo, vis = [], set()
        def build(v):
            if v not in vis:
                vis.add(v)
                for c in v._children: build(c)
                topo.append(v)
        build(self); self.grad = 1
        for v in reversed(topo):
            for ch, lg in zip(v._children, v._local_grads):
                ch.grad += lg * v.grad

# ── Mimari ────────────────────────────────────────────────────────────────────
n_embd      = 16
n_head      = 4
head_dim    = n_embd // n_head
attn_hidden = 32   # 2×(16×32)=1024 = 4×(16×16) — parametre eşitliği

def mat(r, c): return [[Value(random.gauss(0,.08)) for _ in range(c)] for _ in range(r)]
def linear(x, w): return [sum(wi*xi for wi,xi in zip(row,x)) for row in w]
def softmax(ls):
    m=max(v.data for v in ls); e=[(v-m).exp() for v in ls]; s=sum(e)
    return [ei/s for ei in e]
def rmsnorm(x):
    sc=(sum(xi*xi for xi in x)/len(x)+1e-5)**-.5
    return [xi*sc for xi in x]

# ── Model A — Attention ───────────────────────────────────────────────────────
random.seed(42)
A = {'wte':mat(vocab_size,n_embd),'wpe':mat(block_size,n_embd),'lm_head':mat(vocab_size,n_embd),
     'wq':mat(n_embd,n_embd),'wk':mat(n_embd,n_embd),'wv':mat(n_embd,n_embd),'wo':mat(n_embd,n_embd),
     'fc1':mat(4*n_embd,n_embd),'fc2':mat(n_embd,4*n_embd)}
PA = [p for m in A.values() for row in m for p in row]

def fwd_attn(tid, pid, keys, vals):
    x = rmsnorm([t+p for t,p in zip(A['wte'][tid], A['wpe'][pid])])
    xr=x; x=rmsnorm(x)
    q=linear(x,A['wq']); k=linear(x,A['wk']); v=linear(x,A['wv'])
    keys.append(k); vals.append(v)
    xa=[]
    for h in range(n_head):
        hs=h*head_dim
        qh=q[hs:hs+head_dim]
        kh=[ki[hs:hs+head_dim] for ki in keys]
        vh=[vi[hs:hs+head_dim] for vi in vals]
        al=[sum(qh[j]*kh[t][j] for j in range(head_dim))/head_dim**.5 for t in range(len(kh))]
        aw=softmax(al)
        xa+=[sum(aw[t]*vh[t][j] for t in range(len(vh))) for j in range(head_dim)]
    x=linear(xa,A['wo']); x=[a+b for a,b in zip(x,xr)]
    xr=x; x=rmsnorm(x); x=linear(x,A['fc1']); x=[xi.relu() for xi in x]
    x=linear(x,A['fc2']); x=[a+b for a,b in zip(x,xr)]
    return linear(x,A['lm_head'])

# ── Model B — MLP-Only ────────────────────────────────────────────────────────
random.seed(42)
B = {'wte':mat(vocab_size,n_embd),'wpe':mat(block_size,n_embd),'lm_head':mat(vocab_size,n_embd),
     'cx1':mat(attn_hidden,n_embd),'cx2':mat(n_embd,attn_hidden),
     'fc1':mat(4*n_embd,n_embd),'fc2':mat(n_embd,4*n_embd)}
PB = [p for m in B.values() for row in m for p in row]

def fwd_mlp(tid, pid):
    x=rmsnorm([t+p for t,p in zip(B['wte'][tid],B['wpe'][pid])])
    xr=x; x=rmsnorm(x); x=linear(x,B['cx1']); x=[xi.relu() for xi in x]
    x=linear(x,B['cx2']); x=[a+b for a,b in zip(x,xr)]
    xr=x; x=rmsnorm(x); x=linear(x,B['fc1']); x=[xi.relu() for xi in x]
    x=linear(x,B['fc2']); x=[a+b for a,b in zip(x,xr)]
    return linear(x,B['lm_head'])

print(f"attention params: {len(PA)}  |  mlp params: {len(PB)}\n")

# ── Adam ──────────────────────────────────────────────────────────────────────
def make_adam(ps): return [0.]*len(ps), [0.]*len(ps)
ma,va=make_adam(PA); mb,vb=make_adam(PB)
LR,B1,B2,EPS=0.01,.85,.99,1e-8

def adam(ps, m, v, step):
    lrt=LR*(1-step/num_steps)
    for i,p in enumerate(ps):
        m[i]=B1*m[i]+(1-B1)*p.grad; v[i]=B2*v[i]+(1-B2)*p.grad**2
        p.data-=lrt*(m[i]/(1-B1**(step+1)))/((v[i]/(1-B2**(step+1)))**.5+EPS)
        p.grad=0

# ── KEY_POS: sabit uzunluk sayesinde tam bilinen pozisyon ────────────────────
# tokens = [BOS, c0, c1, c2, c3, c4, c5, c6, BOS]
# indexler:  0    1   2   3   4   5   6   7   8
# KEY_POS = SEQ_LEN - 1 = 6  →  tokens[6]=son_filler, target=tokens[7]=anchor
KEY_POS = SEQ_LEN - 1   # pos_id=6: son filler → anchor (ilgili tahmin)

# ── Yardımcı: ilerleme çubuğu ─────────────────────────────────────────────────
def progress_bar(step, total, kpa=None, kpb=None, bar_width=28):
    pct   = (step + 1) / total
    filled = int(bar_width * pct)
    bar   = '█' * filled + '░' * (bar_width - filled)
    loss_str = ''
    if kpa is not None:
        loss_str = f'  attn={kpa:.3f}  mlp={kpb:.3f}'
    sys.stdout.write(f'\r  [{bar}] {step+1:4d}/{total}  (%{pct*100:5.1f}){loss_str}   ')
    sys.stdout.flush()

# ── Eğitim ────────────────────────────────────────────────────────────────────
num_steps = 1000
kp_losses_a, kp_losses_b = [], []
print("Eğitim başlıyor...\n")

for step in range(num_steps):
    doc    = docs[step % len(docs)]
    tokens = [BOS] + [uchars.index(c) for c in doc] + [BOS]
    n      = len(tokens) - 1

    # Attention
    ks,vs=[],[]
    la=[]
    for pid in range(n):
        tid,tgt=tokens[pid],tokens[pid+1]
        logits=fwd_attn(tid,pid,ks,vs)
        pr=softmax(logits); l=-pr[tgt].log(); la.append(l)
        if pid==KEY_POS: kp_losses_a.append(l.data)
    loss_a=(1/n)*sum(la); loss_a.backward(); adam(PA,ma,va,step)

    # MLP
    lb=[]
    for pid in range(n):
        tid,tgt=tokens[pid],tokens[pid+1]
        logits=fwd_mlp(tid,pid)
        pr=softmax(logits); l=-pr[tgt].log(); lb.append(l)
        if pid==KEY_POS: kp_losses_b.append(l.data)
    loss_b=(1/n)*sum(lb); loss_b.backward(); adam(PB,mb,vb,step)

    # Her adımda çubuk güncelle
    w = min(50, step + 1)
    kpa = sum(kp_losses_a[-w:]) / w
    kpb = sum(kp_losses_b[-w:]) / w
    progress_bar(step, num_steps, kpa, kpb)

    if (step+1) % 200 == 0:
        w200 = 200
        kpa200 = sum(kp_losses_a[-w200:]) / min(w200, len(kp_losses_a))
        kpb200 = sum(kp_losses_b[-w200:]) / min(w200, len(kp_losses_b))
        # Çubuğu temizle, sonra özet satırını yaz
        sys.stdout.write('\r' + ' ' * 70 + '\r')
        print(f"  adım {step+1:4d}  │  "
              f"attn key_loss={kpa200:.3f}  │  "
              f"mlp  key_loss={kpb200:.3f}  │  "
              f"fark={kpb200-kpa200:+.3f}  "
              f"(teorik max={math.log(2):.3f})")

# Son çubuğu temizle
sys.stdout.write('\r' + ' ' * 70 + '\r')
sys.stdout.flush()

# ── Sonuç özeti ───────────────────────────────────────────────────────────────
W=500
kpa_final=sum(kp_losses_a[-W:])/W
kpb_final=sum(kp_losses_b[-W:])/W
print()
print("═"*58)
print(f"Son {W} adım — KEY pozisyonu kaybı (son filler → anchor):")
print(f"  Attention : {kpa_final:.4f}")
print(f"  MLP-Only  : {kpb_final:.4f}")
print(f"  Fark      : {kpb_final-kpa_final:+.4f}  "
      f"(teorik max log(2)={math.log(2):.4f})")
print("═"*58)

# ── Doğruluk testi ────────────────────────────────────────────────────────────
print("\nDoğruluk testi (100 yeni örnek):")
print("Kural: ilk harf 'a' → son harf 'a',  'z' → 'z'")
print(f"{'Dizi (prefix)':20s} {'doğru':6s} {'attn_pred':10s} {'mlp_pred':10s}")
print("-"*50)
correct_a=correct_b=0
random.seed(99)   # eğitim seed'inden farklı → unseen örnekler

for _ in range(100):
    first  = random.choice(ANCHOR)
    middle = [random.choice(FILLER) for _ in range(SEQ_LEN-2)]
    prefix = first + ''.join(middle)          # son anchor YOK — model tahmin edecek
    tokens = [BOS]+[uchars.index(c) for c in prefix]
    n      = len(tokens)

    ks,vs=[],[]
    for pid in range(n): la=fwd_attn(tokens[pid],pid,ks,vs)
    for pid in range(n): lb=fwd_mlp(tokens[pid],pid)

    idx_a=uchars.index('a'); idx_z=uchars.index('z')
    pa_a=softmax(la); pa_b=softmax(lb)
    pred_a = 'a' if pa_a[idx_a].data>pa_a[idx_z].data else 'z'
    pred_b = 'a' if pa_b[idx_a].data>pa_b[idx_z].data else 'z'

    if pred_a==first: correct_a+=1
    if pred_b==first: correct_b+=1

    if _<10:   # ilk 10'u göster
        print(f"  {prefix:20s} {first:6s} "
              f"{pred_a}({pa_a[idx_a].data:.2f}/{pa_a[idx_z].data:.2f})   "
              f"{pred_b}({pa_b[idx_a].data:.2f}/{pa_b[idx_z].data:.2f})")

print()
print(f"  Attention doğruluk: {correct_a}/100 = %{correct_a}")
print(f"  MLP-Only  doğruluk: {correct_b}/100 = %{correct_b}")
