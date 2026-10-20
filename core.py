# -*- coding: utf-8 -*-
"""Komponen bersama: tema, pemuatan data, format angka, pemilih emiten."""
import io
import os

import numpy as np
import pandas as pd
import streamlit as st

import hitung

DIR = os.path.dirname(os.path.abspath(__file__))
DOSEN = "Ardiansyah Japlani, S.E., M.B.A."

WARNA = {"utama": "#1d4ed8", "naik": "#059669", "turun": "#dc2626", "netral": "#64748b",
         "aksen": "#f59e0b", "ungu": "#7c3aed"}
WARNA_POLA = {"Perintisan": "#f59e0b", "Pertumbuhan": "#10b981", "Kedewasaan": "#1d4ed8",
              "Penyesuaian": "#a855f7", "Penurunan": "#dc2626", "Data tidak lengkap": "#cbd5e1"}


def set_page(judul, ikon="📊"):
    st.set_page_config(page_title=f"{judul} · Analisa Laporan Keuangan", page_icon=ikon, layout="wide")
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');
html, body, [class*="css"], p, li, label, span { font-family:'Plus Jakarta Sans',sans-serif; }
h1,h2,h3,h4 { font-family:'Space Grotesk',sans-serif; letter-spacing:-.01em; }
.stApp { background: radial-gradient(1000px 420px at 100% -10%, #e0e7ff 0%, transparent 55%), #f7f8fc; }
.hero { background:linear-gradient(120deg,#1e3a8a,#1d4ed8 55%,#0ea5e9); color:#fff; border-radius:22px;
  padding:1.8rem 2rem; box-shadow:0 16px 44px rgba(29,78,216,.25); }
.hero h1,.hero h2 { color:#fff; margin:0; }
.hero p { color:rgba(255,255,255,.92); margin:.4rem 0 0; max-width:70ch; }
.chip { display:inline-block; background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.35);
  color:#fff; border-radius:999px; padding:.2rem .8rem; font-size:.8rem; font-weight:600; margin:0 .3rem .4rem 0; }
.kartu { background:#fff; border:1px solid #e5e7f2; border-radius:16px; padding:1.1rem 1.3rem;
  box-shadow:0 6px 18px rgba(30,58,138,.05); height:100%; line-height:1.65; }
.rumus { background:#f1f5ff; border-left:4px solid #1d4ed8; border-radius:10px; padding:.7rem 1rem;
  font-family:'Space Grotesk',monospace; margin:.4rem 0; }
.ayat { background:linear-gradient(120deg,#fff7ed,#fef3c7); border:1px solid #fde68a; border-radius:14px;
  padding:1rem 1.2rem; color:#78350f; }
.ayat .ar { font-size:1.4rem; direction:rtl; text-align:right; line-height:2.1; }
.catatan { background:#f8fafc; border:1px dashed #94a3b8; border-radius:12px; padding:.7rem 1rem;
  color:#334155; font-size:.92rem; }
</style>""", unsafe_allow_html=True)


@st.cache_data(show_spinner="Memuat data laporan keuangan...")
def muat_data():
    df = pd.read_csv(os.path.join(DIR, "data", "alk_data.csv.gz"))
    return hitung.siapkan(df)


def tahun_utama(df, min_emiten=100):
    """Tahun yang datanya cukup untuk perbandingan sektor (terbaru dulu)."""
    n = df.groupby("tahun")["kode"].nunique()
    return sorted(n[n >= min_emiten].index, reverse=True)


# ---------------------------------------------------------------- format
def rp(v, satuan="M"):
    """Rupiah ringkas: M = miliar, T = triliun. Format Indonesia."""
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    if satuan == "auto":
        satuan = "T" if abs(v) >= 1e12 else "M"
    bagi, label = (1e12, "T") if satuan == "T" else (1e9, "M")
    s = f"{v / bagi:,.1f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"Rp{s} {label}"


def persen(v, desimal=1):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    return f"{v * 100:,.{desimal}f}%".replace(".", ",")


def kali(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(v) else f"{v:,.2f}x".replace(".", ",")


def tabel_rp(df, kolom_nilai="Nilai", kolom_persen=None):
    """Salin DataFrame dengan kolom nilai diformat rupiah miliar (untuk ditampilkan)."""
    t = df.copy()
    t[kolom_nilai] = t[kolom_nilai].map(lambda x: rp(x))
    if kolom_persen and kolom_persen in t:
        t[kolom_persen] = t[kolom_persen].map(persen)
    return t


def ke_excel(lembar: dict) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xw:
        for nama, d in lembar.items():
            d.to_excel(xw, sheet_name=nama[:31], index=False)
    return buf.getvalue()


# ---------------------------------------------------------------- pemilih
def pemilih_emiten(df, kunci, default_kode="ICBP"):
    """Pilih sektor -> emiten -> tahun. Kembalikan (baris, data_emiten_semua_tahun)."""
    sektor_list = sorted(df["sektor"].unique(), key=lambda s: (s == "Belum terklasifikasi", s))
    default_sektor = df.loc[df["kode"] == default_kode, "sektor"].iloc[0] if default_kode in set(df["kode"]) else sektor_list[0]
    c1, c2, c3 = st.columns([2, 3, 1])
    sektor = c1.selectbox("Sektor (IDX-IC)", sektor_list, index=sektor_list.index(default_sektor), key=f"{kunci}_sek")
    d_sek = df[df["sektor"] == sektor].drop_duplicates("kode").sort_values("kode")
    opsi = [f"{k} · {n}" for k, n in zip(d_sek["kode"], d_sek["nama"])]
    idx = next((i for i, o in enumerate(opsi) if o.startswith(default_kode + " ")), 0)
    pilih = c2.selectbox("Emiten", opsi, index=idx, key=f"{kunci}_emt")
    kode = pilih.split(" · ")[0]
    d_emt = df[df["kode"] == kode].sort_values("tahun")
    tahun_list = sorted(d_emt["tahun"].unique(), reverse=True)
    tahun = c3.selectbox("Tahun", tahun_list, key=f"{kunci}_thn")
    baris = d_emt[d_emt["tahun"] == tahun].iloc[0]
    return baris, d_emt


def kotak_ayat(pekan, nilai, surah, arab, terjemah, relevansi):
    st.markdown(f"""<div class="ayat"><b>Integrasi Profetik · {nilai}</b> · {surah}
    <div class="ar">{arab}</div><i>{terjemah}</i><br><br><b>Relevansi:</b> {relevansi}</div>""",
                unsafe_allow_html=True)
