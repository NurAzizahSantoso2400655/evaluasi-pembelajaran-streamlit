import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analisis Butir Soal",
    layout="wide"
)

# ─── CUSTOM CSS & FONTAWESOME ──────────────────────────────────────────────────
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
  .stApp { background: linear-gradient(135deg, #e8f5fb 0%, #f5fafd 50%, #eaf3f8 100%); }
  .header-banner { background: linear-gradient(135deg, #77B0C9 0%, #4A8FAD 50%, #2C6E8A 100%); border-radius: 16px; padding: 1.8rem 2rem; margin-bottom: 1.5rem; color: white; text-align: center; }
  .header-banner h1 { font-size: 28px; font-weight: 700; margin: 0; }
  .header-banner p  { font-size: 14px; opacity: 0.88; margin: 6px 0 0; }
  .section-card { background: white; border-radius: 14px; padding: 1.4rem 1.6rem; margin-bottom: 1.2rem; border: 1px solid #cce5f0; box-shadow: 0 2px 8px rgba(119,176,201,0.10); }
  .info-box { background: #e6f4fb; border-left: 4px solid #77B0C9; border-radius: 0 10px 10px 0; padding: 0.75rem 1rem; font-size: 13.5px; color: #1a3a4a; margin-bottom: 0.9rem; line-height: 1.65; }
  .formula-box { background: #f0f8fc; border: 1.5px dashed #77B0C9; border-radius: 10px; padding: 0.75rem 1rem; font-family: 'Courier New', monospace; font-size: 13px; color: #1a3a4a; margin-bottom: 0.9rem; }
  [data-testid="stMetric"], [data-testid="metric-container"] { background: white !important; border: 1px solid #cce5f0 !important; border-radius: 12px !important; padding: 0.9rem 1rem !important; box-shadow: 0 1px 4px rgba(119,176,201,0.10) !important; }
  [data-testid="stMetric"] p, [data-testid="stMetric"] div, [data-testid="stMetric"] span, [data-testid="stMetricLabel"] *, [data-testid="stMetricValue"] * { color: #1a3a4a !important; }
  .stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; flex-wrap: wrap; }
  .stTabs [data-baseweb="tab"] { background: white; border: 1.5px solid #77B0C9; border-radius: 20px; color: #2C6E8A; font-weight: 500; font-size: 13px; padding: 6px 18px; }
  .stTabs [aria-selected="true"] { background: #77B0C9 !important; color: white !important; border-color: #77B0C9 !important; }
  .stTabs [data-baseweb="tab-border"] { display: none; }
  .stTabs [data-baseweb="tab-panel"] { padding-top: 1rem; }
  h4 { color: #2C6E8A; font-weight: 700; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# ─── DATA ──────────────────────────────────────────────────────────────────────
kunci = ['A','B','B','A','C','C','A','C','D','E','E','D','D','C','C','B','B','A','A','E']

nama_siswa = [f"Siswa {i+1}" for i in range(20)]

jawaban_raw = [
    ['B','B','A','B','A','C','C','C','B','A','E','D','D','C','C','B','B','C','B','B'],
    ['A','A','B','B','A','C','C','A','C','A','C','D','E','E','C','B','B','A','A','A'],
    ['B','B','B','A','C','C','C','A','D','E','E','D','D','C','C','B','B','C','B','B'],
    ['A','A','B','B','A','D','C','A','D','E','E','D','D','C','C','C','B','B','A','E'],
    ['B','A','B','A','D','C','A','C','D','E','E','A','C','C','A','D','B','B','C','B'],
    ['B','B','A','D','C','A','C','D','E','E','D','D','D','E','C','B','B','A','A','C'],
    ['A','B','B','A','D','C','A','C','C','A','C','D','E','E','C','B','B','A','C','B'],
    ['C','A','C','D','E','E','D','D','D','D','D','A','C','C','A','C','D','E','E','E'],
    ['A','B','B','C','A','C','D','E','E','D','D','A','C','C','B','B','C','B','B','B'],
    ['A','C','C','A','C','D','E','E','D','E','B','B','A','C','C','B','B','C','B','B'],
    ['C','C','A','A','D','A','A','A','B','B','C','A','B','C','D','D','E','E','A','E'],
    ['A','A','C','C','A','A','D','A','A','A','B','B','C','A','B','C','D','D','E','A'],
    ['A','C','A','A','A','C','A','A','D','B','B','C','A','B','C','D','D','D','C','C'],
    ['B','B','A','A','A','A','B','B','A','C','C','A','C','D','A','A','B','B','A','C'],
    ['C','A','C','D','E','E','D','D','C','C','B','B','A','C','C','A','C','D','E','D'],
    ['D','C','C','B','B','A','A','A','A','A','C','D','E','E','B','B','A','C','A','D'],
    ['E','E','D','D','E','A','C','C','A','C','D','E','E','D','D','B','B','A','C','C'],
    ['B','B','A','A','A','C','A','B','C','A','C','C','C','A','C','C','A','C','D','E'],
    ['E','B','B','A','E','A','B','B','A','C','C','E','E','D','D','E','D','D','B','B'],
    ['A','B','A','A','E','B','A','C','A','C','D','E','E','D','D','E','D','D','B','B'],
]

N  = len(jawaban_raw)
NS = len(kunci)

# ─── FUNGSI PERHITUNGAN ────────────────────────────────────────────────────────
def hitung_skor(jawaban, kunci):
    return [sum(1 for j, k in zip(row, kunci) if j == k) for row in jawaban]

def hitung_validitas(jawaban, kunci, skor):
    hasil = []
    for j in range(len(kunci)):
        xi = [1 if row[j] == kunci[j] else 0 for row in jawaban]
        r, _ = stats.pearsonr(xi, skor)
        hasil.append(round(r, 4))
    return hasil

def hitung_kesukaran(jawaban, kunci):
    hasil = []
    for j in range(len(kunci)):
        benar = sum(1 for row in jawaban if row[j] == kunci[j])
        p = benar / len(jawaban)
        kat = "Sukar" if p < 0.30 else ("Sedang" if p <= 0.70 else "Mudah")
        hasil.append({"benar": benar, "p": round(p, 4), "kategori": kat})
    return hasil

def hitung_daya_pembeda(jawaban, kunci, skor):
    urut  = sorted(range(len(skor)), key=lambda i: skor[i], reverse=True)
    upper = urut[:len(urut)//2]
    lower = urut[len(urut)//2:]
    hasil = []
    for j in range(len(kunci)):
        bU = sum(1 for i in upper if jawaban[i][j] == kunci[j])
        bL = sum(1 for i in lower if jawaban[i][j] == kunci[j])
        D  = (bU - bL) / (len(urut) // 2)
        if D < 0:       kat = "Jelek Sekali"
        elif D < 0.20:  kat = "Jelek"
        elif D < 0.40:  kat = "Cukup"
        elif D < 0.70:  kat = "Baik"
        else:           kat = "Baik Sekali"
        hasil.append({"bU": bU, "bL": bL, "D": round(D, 4), "kategori": kat})
    return hasil

def hitung_reliabilitas(jawaban, kunci, skor):
    k = len(kunci)
    var_soal = []
    for j in range(k):
        xi = [1 if row[j] == kunci[j] else 0 for row in jawaban]
        var_soal.append(np.var(xi, ddof=0))
    sum_var   = sum(var_soal)
    var_total = np.var(skor, ddof=0)
    alpha     = (k / (k - 1)) * (1 - sum_var / var_total)
    return round(alpha, 4), round(sum_var, 4), round(var_total, 4), [round(v, 4) for v in var_soal]

# ─── HITUNG ────────────────────────────────────────────────────────────────────
skor      = hitung_skor(jawaban_raw, kunci)
r_hitung  = hitung_validitas(jawaban_raw, kunci, skor)
r_tabel   = 0.444
valid     = [r >= r_tabel for r in r_hitung]
kesukaran = hitung_kesukaran(jawaban_raw, kunci)
daya      = hitung_daya_pembeda(jawaban_raw, kunci, skor)
alpha, sum_var_soal, var_total, var_per_soal = hitung_reliabilitas(jawaban_raw, kunci, skor)

# ─── WARNA ─────────────────────────────────────────────────────────────────────
BIRU  = "#4A8FAD"; BIRU2 = "#77B0C9"
HIJAU = "#1a7a50"; MERAH = "#b03020"
OREN  = "#c07010"; UNGU  = "#6B2E9E"

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <h1><i class="fa-solid fa-chart-line"></i> Analisis Butir Soal</h1>
  <p>Validitas · Daya Pembeda · Tingkat Kesukaran · Reliabilitas &nbsp;|&nbsp; Data 20 Siswa (Absen 21–45)</p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["Data Siswa", "Validitas", "Tingkat Kesukaran", "Daya Pembeda", "Reliabilitas", "Rekap"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 : DATA SISWA
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Jumlah Siswa",   N)
    c2.metric("Jumlah Soal",    NS)
    c3.metric("Rata-rata Skor", f"{np.mean(skor):.2f}")
    c4.metric("Skor Tertinggi", max(skor))
    c5.metric("Skor Terendah",  min(skor))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h4><i class="fa-solid fa-table-list"></i> Tabel Jawaban Siswa</h4>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
    <i class="fa-solid fa-circle-info"></i> Sel <span style="background:#d4f0e4;color:#1a5c36;padding:1px 6px;border-radius:4px;font-weight:600">hijau</span> = jawaban <b>benar</b> &nbsp;|&nbsp;
    Sel <span style="background:#fde8e8;color:#8c2020;padding:1px 6px;border-radius:4px;font-weight:600">merah</span> = jawaban <b>salah</b>
    </div>""", unsafe_allow_html=True)

    cols_soal = [f"S{i+1}" for i in range(NS)]
    df_jaw = pd.DataFrame(jawaban_raw, columns=cols_soal)
    df_jaw.insert(0, "Nama", nama_siswa)
    df_jaw["Skor"] = skor

    def style_sel(df_source):
        def _style(val, col):
            j = cols_soal.index(col)
            benar = (val == kunci[j])
            bg    = "#d4f0e4" if benar else "#fde8e8"
            fg    = "#1a5c36" if benar else "#8c2020"
            return f"background-color:{bg};color:{fg};font-weight:600"
        styled = pd.DataFrame("", index=df_source.index, columns=df_source.columns)
        for col in cols_soal:
            styled[col] = df_source[col].map(lambda v, c=col: _style(v, c))
        styled["Skor"] = "font-weight:700;color:#2C6E8A"
        return styled

    st.dataframe(
        df_jaw.style.apply(style_sel, axis=None),
        use_container_width=True, height=460
    )

    st.markdown("**Kunci Jawaban:**")
    kunci_df = pd.DataFrame([kunci], columns=cols_soal, index=["Kunci"])
    st.dataframe(kunci_df.style.set_properties(**{
        "background-color": "#e6f4fb", "color": "#1a3a4a",
        "font-weight": "600", "text-align": "center"
    }), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 : VALIDITAS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
    <i class="fa-solid fa-circle-check"></i> <b>Apa itu Validitas?</b> Validitas mengukur sejauh mana butir soal benar-benar mengukur apa yang
    seharusnya diukur. Soal dikatakan <b>valid</b> jika r-hitung ≥ r-tabel (0.444).
    </div>""", unsafe_allow_html=True)
    st.markdown("""<div class="formula-box">
    r = Σ(Xi − X̄)(Yi − Ȳ) / √[Σ(Xi−X̄)² × Σ(Yi−Ȳ)²]<br>
    Xi = skor butir (1=benar, 0=salah) · Yi = skor total siswa · r-tabel (N=20, α=0.05) = <b>0.444</b>
    </div>""", unsafe_allow_html=True)

    jml_valid = sum(valid)
    v1,v2,v3 = st.columns(3)
    v1.metric("Soal Valid",     jml_valid)
    v2.metric("Tidak Valid",    NS - jml_valid)
    v3.metric("% Valid",        f"{jml_valid/NS*100:.0f}%")

    st.markdown("---")
    df_val = pd.DataFrame({
        "Butir Soal": [f"Soal {i+1}" for i in range(NS)],
        "Kunci":      kunci,
        "r-hitung":   r_hitung,
        "r-tabel":    [r_tabel]*NS,
        "Selisih":    [round(r - r_tabel, 4) for r in r_hitung],
        "Keterangan": ["Valid" if v else "Tidak Valid" for v in valid],
    })

    def style_keterangan(val):
        if val == "Valid":
            return "background-color:#d4f0e4;color:#1a5c36;font-weight:700;text-align:center"
        elif val == "Tidak Valid":
            return "background-color:#fde8e8;color:#8c2020;font-weight:700;text-align:center"
        return ""

    st.dataframe(
        df_val.style
            .map(style_keterangan, subset=["Keterangan"])
            .background_gradient(subset=["r-hitung"], cmap="RdYlGn", vmin=-0.5, vmax=1)
            .format({"r-hitung": "{:.4f}", "r-tabel": "{:.3f}", "Selisih": "{:.4f}"}),
        use_container_width=True, height=430
    )

    # Bar chart
    fig, ax = plt.subplots(figsize=(12, 3.8))
    colors_v = [HIJAU if v else MERAH for v in valid]
    bars = ax.bar([f"S{i+1}" for i in range(NS)], r_hitung, color=colors_v,
                  edgecolor="white", linewidth=0.8, width=0.65)
    ax.axhline(r_tabel, color="#1a3a4a", linestyle="--", linewidth=1.8,
               label=f"r-tabel = {r_tabel}")
    ax.axhline(0, color="#aaa", linewidth=0.8)
    ax.set_ylim(-0.65, 1.1)
    ax.set_ylabel("r-hitung", fontsize=11, color="#1a3a4a")
    ax.set_title("Koefisien Validitas Per Butir Soal", fontsize=13,
                 fontweight="bold", color="#1a3a4a", pad=10)
    ax.legend(fontsize=10)
    ax.set_facecolor("#f8fbfd"); fig.patch.set_facecolor("#f8fbfd")
    ax.tick_params(colors="#1a3a4a")
    for bar, r in zip(bars, r_hitung):
        y = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2,
                y + (0.025 if y >= 0 else -0.07),
                f"{r:.2f}", ha="center", va="bottom", fontsize=8, color="#1a3a4a",
                fontweight="600")
    h1 = mpatches.Patch(color=HIJAU, label="Valid")
    h2 = mpatches.Patch(color=MERAH, label="Tidak Valid")
    ax.legend(handles=[h1, h2,
        plt.Line2D([0],[0], color="#1a3a4a", linestyle="--", linewidth=1.8,
                   label=f"r-tabel={r_tabel}")],
        fontsize=9, loc="upper right")
    plt.tight_layout()
    st.pyplot(fig); plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 : TINGKAT KESUKARAN
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
    <i class="fa-solid fa-arrow-trend-up"></i> <b>Apa itu Tingkat Kesukaran?</b> Proporsi siswa yang menjawab benar pada suatu butir soal.
    Soal yang baik memiliki tingkat kesukaran <b>sedang</b> (0.30 – 0.70).
    </div>""", unsafe_allow_html=True)
    st.markdown("""<div class="formula-box">
    P = B / N<br>
    B = jumlah siswa menjawab benar · N = total siswa (20)<br>
    P &lt; 0.30 = <b>Sukar</b> &nbsp;|&nbsp; 0.30 ≤ P ≤ 0.70 = <b>Sedang</b> &nbsp;|&nbsp; P &gt; 0.70 = <b>Mudah</b>
    </div>""", unsafe_allow_html=True)

    cnt_k = {"Mudah": 0, "Sedang": 0, "Sukar": 0}
    for k in kesukaran: cnt_k[k["kategori"]] += 1
    k1,k2,k3 = st.columns(3)
    k1.metric("Mudah",  cnt_k["Mudah"])
    k2.metric("Sedang", cnt_k["Sedang"])
    k3.metric("Sukar",  cnt_k["Sukar"])

    st.markdown("---")
    df_kes = pd.DataFrame({
        "Butir Soal": [f"Soal {i+1}" for i in range(NS)],
        "Kunci":      kunci,
        "Jml Benar":  [k["benar"] for k in kesukaran],
        "Jml Salah":  [N - k["benar"] for k in kesukaran],
        "P (Indeks)": [k["p"] for k in kesukaran],
        "Kategori":   [k["kategori"] for k in kesukaran],
    })

    def style_kat_kes(val):
        m = {
            "Mudah":  "background-color:#fff0c8;color:#6b4400;font-weight:700",
            "Sedang": "background-color:#d8eef8;color:#1a3a6a;font-weight:700",
            "Sukar":  "background-color:#ead8f8;color:#4a1a7a;font-weight:700",
        }
        return m.get(val, "")

    st.dataframe(
        df_kes.style
            .map(style_kat_kes, subset=["Kategori"])
            .background_gradient(subset=["P (Indeks)"], cmap="RdYlGn", vmin=0, vmax=1)
            .format({"P (Indeks)": "{:.4f}"}),
        use_container_width=True, height=430
    )

    # Bar chart
    fig, ax = plt.subplots(figsize=(12, 3.8))
    colors_k2 = [OREN if k["kategori"]=="Mudah" else
                 (BIRU if k["kategori"]=="Sedang" else UNGU) for k in kesukaran]
    p_vals = [k["p"] for k in kesukaran]
    ax.bar([f"S{i+1}" for i in range(NS)], p_vals, color=colors_k2,
           edgecolor="white", linewidth=0.8, width=0.65)
    ax.axhline(0.30, color=MERAH, linestyle="--", linewidth=1.5)
    ax.axhline(0.70, color=HIJAU, linestyle="--", linewidth=1.5)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Indeks Kesukaran (P)", fontsize=11, color="#1a3a4a")
    ax.set_title("Tingkat Kesukaran Per Butir Soal", fontsize=13,
                 fontweight="bold", color="#1a3a4a", pad=10)
    ax.set_facecolor("#f8fbfd"); fig.patch.set_facecolor("#f8fbfd")
    ax.tick_params(colors="#1a3a4a")
    for i, p in enumerate(p_vals):
        ax.text(i, p + 0.025, f"{p:.2f}", ha="center", va="bottom",
                fontsize=8, color="#1a3a4a", fontweight="600")
    p1 = mpatches.Patch(color=OREN, label="Mudah (P>0.70)")
    p2 = mpatches.Patch(color=BIRU, label="Sedang (0.30–0.70)")
    p3 = mpatches.Patch(color=UNGU, label="Sukar (P<0.30)")
    ax.legend(handles=[p1,p2,p3], fontsize=9, loc="upper right")
    plt.tight_layout()
    st.pyplot(fig); plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 : DAYA PEMBEDA
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
    <i class="fa-solid fa-arrows-split-up-and-left"></i> <b>Apa itu Daya Pembeda?</b> Kemampuan soal membedakan siswa berkemampuan tinggi
    (kelompok atas = 10 siswa) dengan berkemampuan rendah (kelompok bawah = 10 siswa).
    </div>""", unsafe_allow_html=True)
    st.markdown("""<div class="formula-box">
    D = (BA − BB) / (N/2)<br>
    BA = benar kelompok atas · BB = benar kelompok bawah · N/2 = 10<br>
    D &lt; 0.20 = <b>Jelek</b> &nbsp;|&nbsp; 0.20–0.39 = <b>Cukup</b> &nbsp;|&nbsp; 0.40–0.69 = <b>Baik</b> &nbsp;|&nbsp; ≥ 0.70 = <b>Baik Sekali</b>
    </div>""", unsafe_allow_html=True)

    cnt_d = {"Baik Sekali":0,"Baik":0,"Cukup":0,"Jelek":0,"Jelek Sekali":0}
    for d in daya: cnt_d[d["kategori"]] += 1
    d1,d2,d3,d4 = st.columns(4)
    d1.metric("Baik Sekali", cnt_d["Baik Sekali"])
    d2.metric("Baik",        cnt_d["Baik"])
    d3.metric("Cukup",      cnt_d["Cukup"])
    d4.metric("Jelek",       cnt_d["Jelek"]+cnt_d["Jelek Sekali"])

    st.markdown("---")
    df_daya = pd.DataFrame({
        "Butir Soal": [f"Soal {i+1}" for i in range(NS)],
        "Kunci":      kunci,
        "BA (Atas)":  [d["bU"] for d in daya],
        "BB (Bawah)": [d["bL"] for d in daya],
        "D (Indeks)": [d["D"]  for d in daya],
        "Kategori":   [d["kategori"] for d in daya],
    })

    def style_kat_daya(val):
        m = {
            "Baik Sekali":  "background-color:#b8f0d8;color:#0d4a2a;font-weight:700",
            "Baik":         "background-color:#d4f0e4;color:#1a5c36;font-weight:700",
            "Cukup":        "background-color:#d8eef8;color:#1a3a6a;font-weight:700",
            "Jelek":        "background-color:#fde8e8;color:#8c2020;font-weight:700",
            "Jelek Sekali": "background-color:#fcc8c8;color:#7a1010;font-weight:700",
        }
        return m.get(val, "")

    st.dataframe(
        df_daya.style
            .map(style_kat_daya, subset=["Kategori"])
            .background_gradient(subset=["D (Indeks)"], cmap="RdYlGn", vmin=-0.5, vmax=1)
            .format({"D (Indeks)": "{:.4f}"}),
        use_container_width=True, height=430
    )

    # Bar chart
    fig, ax = plt.subplots(figsize=(12, 3.8))
    D_vals   = [d["D"] for d in daya]
    colors_d = [HIJAU if d>=0.4 else (BIRU if d>=0.2 else MERAH) for d in D_vals]
    ax.bar([f"S{i+1}" for i in range(NS)], D_vals, color=colors_d,
           edgecolor="white", linewidth=0.8, width=0.65)
    ax.axhline(0.40, color=HIJAU, linestyle="--", linewidth=1.5)
    ax.axhline(0.20, color=BIRU2, linestyle="--", linewidth=1.5)
    ax.axhline(0,    color="#888", linewidth=0.8)
    ax.set_ylim(-0.65, 1.15)
    ax.set_ylabel("Indeks Daya Pembeda (D)", fontsize=11, color="#1a3a4a")
    ax.set_title("Daya Pembeda Per Butir Soal", fontsize=13,
                 fontweight="bold", color="#1a3a4a", pad=10)
    ax.set_facecolor("#f8fbfd"); fig.patch.set_facecolor("#f8fbfd")
    ax.tick_params(colors="#1a3a4a")
    for i, d in enumerate(D_vals):
        ax.text(i, d + (0.025 if d >= 0 else -0.07),
                f"{d:.2f}", ha="center", va="bottom",
                fontsize=8, color="#1a3a4a", fontweight="600")
    h1 = mpatches.Patch(color=HIJAU, label="Baik / Baik Sekali (≥0.40)")
    h2 = mpatches.Patch(color=BIRU,  label="Cukup (0.20–0.39)")
    h3 = mpatches.Patch(color=MERAH, label="Jelek (<0.20)")
    ax.legend(handles=[h1,h2,h3], fontsize=9, loc="upper right")
    plt.tight_layout()
    st.pyplot(fig); plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 : RELIABILITAS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
    <i class="fa-solid fa-shield-halved"></i> <b>Apa itu Reliabilitas?</b> Reliabilitas mengukur konsistensi/keandalan tes.
    Semakin tinggi nilai Alpha Cronbach, semakin konsisten instrumen tersebut.
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="formula-box">
    α = (k / (k−1)) × (1 − Σσᵢ² / σₜ²)<br>
    k = {NS} soal &nbsp;|&nbsp; Σσᵢ² = {sum_var_soal} &nbsp;|&nbsp; σₜ² = {var_total}<br>
    α ≥ 0.80 = <b>Tinggi</b> &nbsp;|&nbsp; 0.60–0.79 = <b>Cukup</b> &nbsp;|&nbsp; &lt; 0.60 = <b>Rendah</b>
    </div>""", unsafe_allow_html=True)

    if alpha >= 0.80:
        interp, bg_color, fg_color = "Reliabilitas TINGGI", "#d4f0e4", "#1a5c36"
    elif alpha >= 0.60:
        interp, bg_color, fg_color = "Reliabilitas CUKUP", "#d8eef8", "#1a3a6a"
    else:
        interp, bg_color, fg_color = "Reliabilitas RENDAH", "#fde8e8", "#8c2020"

    st.markdown(f"""
    <div style="text-align:center;background:{bg_color};border-radius:16px;
                padding:2rem;margin:1rem 0;border:2px solid {fg_color}30">
      <div style="font-size:14px;color:#5a7a8a;margin-bottom:6px">Koefisien Alpha Cronbach</div>
      <div style="font-size:58px;font-weight:700;color:{fg_color}">{alpha}</div>
      <div style="font-size:17px;font-weight:600;color:{fg_color};margin-top:8px">{interp}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h4><i class="fa-solid fa-calculator"></i> Langkah Perhitungan</h4>', unsafe_allow_html=True)
    st.markdown(f"""
    1. Hitung skor tiap siswa → rata-rata = **{np.mean(skor):.2f}**
    2. Hitung varians tiap butir soal (σᵢ²)
    3. Jumlahkan varians soal → Σσᵢ² = **{sum_var_soal}**
    4. Hitung varians total skor → σₜ² = **{var_total}**
    5. α = ({NS}/{NS-1}) × (1 − {sum_var_soal}/{var_total}) = **{alpha}**
    """)

    st.markdown('<h4><i class="fa-solid fa-chart-bar"></i> Varians Per Butir Soal (σᵢ²)</h4>', unsafe_allow_html=True)
    df_var = pd.DataFrame([var_per_soal],
                          columns=[f"S{i+1}" for i in range(NS)],
                          index=["σᵢ²"])
    st.dataframe(
        df_var.style
            .background_gradient(cmap="Blues")
            .format("{:.4f}"),
        use_container_width=True
    )

    # Gauge chart
    fig, ax = plt.subplots(figsize=(7, 3.5))
    segments = [(0, 0.40, "#fde8e8"), (0.40, 0.60, "#fef3d8"),
                (0.60, 0.80, "#d8eef8"), (0.80, 1.0, "#d4f0e4")]
    for lo, hi, col in segments:
        th = np.linspace(np.pi*(1-lo), np.pi*(1-hi), 80)
        ax.fill_between(np.cos(th), 0, np.sin(th), color=col, alpha=0.95)
        ax.plot(np.cos(th), np.sin(th), color="white", linewidth=2)
    angle = np.pi * (1 - alpha)
    ax.annotate("", xy=(np.cos(angle)*0.72, np.sin(angle)*0.72), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#1a3a4a", lw=2.8))
    ax.text(0, -0.22, f"α = {alpha}", ha="center", fontsize=17,
            fontweight="bold", color="#1a3a4a")
    for val, lbl in [(0,"0"),(0.4,"0.4"),(0.6,"0.6"),(0.8,"0.8"),(1.0,"1.0")]:
        a2 = np.pi*(1-val)
        ax.text(np.cos(a2)*1.12, np.sin(a2)*1.12, lbl,
                ha="center", va="center", fontsize=9, color="#1a3a4a", fontweight="600")
    for lbl, pos, col in [("Rendah",(0,"0.2"), MERAH),("Cukup",(0,"0.5"), BIRU),
                           ("Tinggi",(0,"0.9"), HIJAU)]:
        pass
    ax.set_xlim(-1.35,1.35); ax.set_ylim(-0.35,1.25)
    ax.axis("off"); ax.set_facecolor("#f8fbfd"); fig.patch.set_facecolor("#f8fbfd")
    ax.set_title("Gauge Reliabilitas Alpha Cronbach", fontsize=12,
                 fontweight="bold", color="#1a3a4a")
    plt.tight_layout()
    st.pyplot(fig); plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 : REKAP
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h4><i class="fa-solid fa-layer-group"></i> Rekapitulasi Lengkap Analisis Butir Soal</h4>', unsafe_allow_html=True)

    jml_valid = sum(valid)
    cnt_k2 = {"Mudah":0,"Sedang":0,"Sukar":0}
    for k in kesukaran: cnt_k2[k["kategori"]] += 1
    cnt_d2 = {"Baik Sekali":0,"Baik":0,"Cukup":0,"Jelek":0,"Jelek Sekali":0}
    for d in daya: cnt_d2[d["kategori"]] += 1

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Valid",             f"{jml_valid}/{NS}")
    m2.metric("Kesukaran Sedang",  f"{cnt_k2['Sedang']}/{NS}")
    m3.metric("Daya Pembeda Baik", f"{cnt_d2['Baik']+cnt_d2['Baik Sekali']}/{NS}")
    m4.metric("Alpha Cronbach",    alpha)

    st.markdown("---")
    st.markdown("**Tabel Rekap Semua Butir Soal:**")
    df_rekap = pd.DataFrame({
        "Soal":       [f"Soal {i+1}" for i in range(NS)],
        "Kunci":      kunci,
        "r-hitung":   r_hitung,
        "Validitas":  ["Valid" if v else "Tidak Valid" for v in valid],
        "P Kes.":     [k["p"] for k in kesukaran],
        "Kat.Kes.":   [k["kategori"] for k in kesukaran],
        "D Daya":     [d["D"] for d in daya],
        "Kat.Daya":   [d["kategori"] for d in daya],
    })

    def style_rekap_val(val):
        if val == "Valid": return "background-color:#d4f0e4;color:#1a5c36;font-weight:700"
        if val == "Tidak Valid": return "background-color:#fde8e8;color:#8c2020;font-weight:700"
        return ""

    def style_rekap_kes(val):
        m = {"Mudah":"background-color:#fff0c8;color:#6b4400;font-weight:700",
             "Sedang":"background-color:#d8eef8;color:#1a3a6a;font-weight:700",
             "Sukar":"background-color:#ead8f8;color:#4a1a7a;font-weight:700"}
        return m.get(val,"")

    def style_rekap_daya(val):
        m = {"Baik Sekali":"background-color:#b8f0d8;color:#0d4a2a;font-weight:700",
             "Baik":"background-color:#d4f0e4;color:#1a5c36;font-weight:700",
             "Cukup":"background-color:#d8eef8;color:#1a3a6a;font-weight:700",
             "Jelek":"background-color:#fde8e8;color:#8c2020;font-weight:700",
             "Jelek Sekali":"background-color:#fcc8c8;color:#7a1010;font-weight:700"}
        return m.get(val,"")

    st.dataframe(
        df_rekap.style
            .map(style_rekap_val,  subset=["Validitas"])
            .map(style_rekap_kes,  subset=["Kat.Kes."])
            .map(style_rekap_daya, subset=["Kat.Daya"])
            .background_gradient(subset=["r-hitung"], cmap="RdYlGn", vmin=-0.5, vmax=1)
            .background_gradient(subset=["P Kes."],   cmap="RdYlGn", vmin=0, vmax=1)
            .background_gradient(subset=["D Daya"],   cmap="RdYlGn", vmin=-0.5, vmax=1)
            .format({"r-hitung":"{:.4f}","P Kes.":"{:.4f}","D Daya":"{:.4f}"}),
        use_container_width=True, height=440
    )

    st.markdown("---")
    st.markdown('<h4><i class="fa-solid fa-chart-pie"></i> Visualisasi Ringkasan</h4>', unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    fig.patch.set_facecolor("#f8fbfd")

    # Pie validitas
    axes[0].pie(
        [jml_valid, NS-jml_valid],
        labels=["Valid","Tidak Valid"],
        colors=[HIJAU, MERAH], autopct="%1.0f%%", startangle=90,
        wedgeprops={"edgecolor":"white","linewidth":2},
        textprops={"color":"#1a3a4a","fontweight":"600","fontsize":11}
    )
    axes[0].set_title("Validitas", fontweight="bold", color="#1a3a4a", fontsize=12)

    # Pie kesukaran
    axes[1].pie(
        [cnt_k2["Mudah"], cnt_k2["Sedang"], cnt_k2["Sukar"]],
        labels=["Mudah","Sedang","Sukar"],
        colors=[OREN, BIRU, UNGU], autopct="%1.0f%%", startangle=90,
        wedgeprops={"edgecolor":"white","linewidth":2},
        textprops={"color":"#1a3a4a","fontweight":"600","fontsize":11}
    )
    axes[1].set_title("Tingkat Kesukaran", fontweight="bold", color="#1a3a4a", fontsize=12)

    # Pie daya pembeda
    baik_tot = cnt_d2["Baik Sekali"]+cnt_d2["Baik"]
    axes[2].pie(
        [baik_tot, cnt_d2["Cukup"], cnt_d2["Jelek"]+cnt_d2["Jelek Sekali"]],
        labels=["Baik","Cukup","Jelek"],
        colors=[HIJAU, BIRU, MERAH], autopct="%1.0f%%", startangle=90,
        wedgeprops={"edgecolor":"white","linewidth":2},
        textprops={"color":"#1a3a4a","fontweight":"600","fontsize":11}
    )
    axes[2].set_title("Daya Pembeda", fontweight="bold", color="#1a3a4a", fontsize=12)

    for ax in axes:
        ax.set_facecolor("#f8fbfd")

    plt.tight_layout(pad=2)
    st.pyplot(fig); plt.close()
    st.markdown('</div>', unsafe_allow_html=True)