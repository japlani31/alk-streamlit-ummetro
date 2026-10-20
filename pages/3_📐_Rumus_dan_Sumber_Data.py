# -*- coding: utf-8 -*-
"""Daftar rumus, kamus kolom, sumber data, dan keterbatasan."""
import pandas as pd
import streamlit as st

import core

core.set_page("Rumus & Sumber Data", "📐")
df = core.muat_data()

st.markdown("## 📐 Rumus & Sumber Data")

st.markdown("### Rumus yang dipakai")
st.dataframe(pd.DataFrame([
    ["P3", "Marjin laba kotor", "Laba kotor ÷ Pendapatan", "gp / revenue"],
    ["P3", "Marjin laba usaha", "Laba usaha ÷ Pendapatan", "opinc / revenue"],
    ["P3", "Marjin EBITDA", "EBITDA ÷ Pendapatan", "ebitda / revenue"],
    ["P3", "Marjin laba sebelum pajak", "Laba sebelum pajak ÷ Pendapatan", "pretax / revenue"],
    ["P3", "Marjin laba bersih", "Laba bersih milik induk ÷ Pendapatan", "netinc / revenue"],
    ["P3", "Tarif pajak efektif", "Beban pajak ÷ Laba sebelum pajak", "taxexp / pretax"],
    ["P3", "Pos tidak berulang", "Laba sebelum pajak − Laba sebelum pajak kegiatan berulang", "pretax − ebtExcl"],
    ["P3", "Laba berulang", "Laba bersih − Pos tidak berulang × (1 − tarif pajak efektif)", "tarif dibatasi 0–50%, selain itu 22%"],
    ["P3", "Rasio laba berulang", "Laba berulang ÷ Laba bersih", "hanya bila laba bersih > 0"],
    ["P4", "Arus kas bebas", "CFO − Belanja modal", "ncfo + capex (capex bertanda negatif)"],
    ["P4", "CFO terhadap laba", "CFO ÷ Laba bersih", "hanya bila laba bersih > 0"],
    ["P4", "Rasio akrual", "(Laba bersih − CFO) ÷ Rata-rata total aset", ""],
    ["P4", "Capex terhadap penyusutan", "Belanja modal ÷ Penyusutan & amortisasi", ""],
    ["P4", "Rasio pembayaran dividen", "Dividen kas dibayar ÷ Laba bersih", ""],
    ["P4", "PKL & pos ekuitas lainnya", "Δ Ekuitas − Laba − Dividen − Terbit saham − Beli kembali", "sisa rekonsiliasi"],
    ["P4", "Pola arus kas", "Tanda (CFO, CFI, CFF) menurut Dickinson (2011)", ""],
], columns=["Pertemuan", "Ukuran", "Rumus", "Catatan teknis"]), hide_index=True, width="stretch")

st.markdown("### Sumber data")
st.markdown("""
- **Laporan keuangan:** data olahan laporan keuangan tahunan emiten Bursa Efek Indonesia
  (berkas `negara_idx.csv`), satuan rupiah penuh, tahun buku 2021–2025.
- **Klasifikasi sektor:** IDX Industrial Classification (IDX-IC) 11 sektor, diambil dari berkas
  *Rekap Laporan Keuangan Vers. 1.9 Q4 2024*. Emiten yang tidak ada di berkas tersebut diberi label
  *Belum terklasifikasi* (tidak ditebak).
- **Uji konsistensi data:** laba kotor = pendapatan − beban pokok (99%), aset = liabilitas + ekuitas (100%),
  kenaikan kas laporan arus kas = perubahan kas neraca (97%).
""")

st.markdown("### Jumlah emiten per sektor")
n = df[df["tahun"] == max(core.tahun_utama(df))].groupby("sektor")["kode"].nunique().sort_values(ascending=False)
st.dataframe(n.rename("Jumlah emiten").reset_index().rename(columns={"sektor": "Sektor"}),
             hide_index=True, width="stretch")

st.markdown("### Keterbatasan")
st.markdown("""
- Data adalah hasil olahan pihak ketiga; untuk tugas resmi, **cocokkan dengan laporan keuangan asli** di situs BEI
  atau situs emiten.
- Pemisahan laba berulang memakai pos yang ditandai tidak berulang oleh penyedia data; analis tetap perlu membaca
  catatan atas laporan keuangan.
- Metode langsung pada aplikasi ini adalah **estimasi konversi**, bukan angka yang dilaporkan emiten.
- Penghasilan komprehensif lain tidak tersedia terpisah, sehingga ditaksir sebagai sisa rekonsiliasi ekuitas.
- Sektor Keuangan memiliki struktur laporan berbeda; bandingkan bank dengan bank.
""")
