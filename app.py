# -*- coding: utf-8 -*-
"""
Beranda aplikasi Analisa Laporan Keuangan (MNJ-ALK).
Prodi Sarjana Manajemen, FEB Universitas Muhammadiyah Metro.

Jalankan:  streamlit run app.py
"""
import streamlit as st

import core

core.set_page("Beranda", "📊")
df = core.muat_data()

st.markdown(f"""<div class="hero">
<span class="chip">MNJ-ALK</span><span class="chip">S1 Manajemen · Semester 5</span><span class="chip">3 SKS</span>
<h1>Analisa Laporan Keuangan</h1>
<p>Laboratorium hitung laporan keuangan emiten Bursa Efek Indonesia. Pilih emiten, lihat perhitungannya
langkah demi langkah, lalu bandingkan dengan sektornya. Dosen: {core.DOSEN}.</p>
</div>""", unsafe_allow_html=True)
st.write("")

n_emt, n_lap = df["kode"].nunique(), len(df)
n_sek = df.loc[df["sektor"] != "Belum terklasifikasi", "sektor"].nunique()
tahun = core.tahun_utama(df)
c = st.columns(4)
for col, angka, ket in [(c[0], f"{n_emt}", "Emiten BEI"), (c[1], f"{n_lap:,}".replace(",", "."), "Laporan tahunan"),
                        (c[2], f"{n_sek}", "Sektor IDX-IC"), (c[3], f"{min(tahun)}–{max(tahun)}", "Periode")]:
    col.markdown(f"""<div class="kartu" style="text-align:center"><div style="font-size:1.9rem;font-weight:800;
    color:#1d4ed8;font-family:'Space Grotesk'">{angka}</div><small>{ket}</small></div>""", unsafe_allow_html=True)

st.write("")
st.markdown("### Materi yang tersedia")
a, b = st.columns(2)
a.markdown("""<div class="kartu"><h4>📈 Pertemuan 3 · Sub-CPMK3</h4>
<b>Laporan laba rugi & penghasilan komprehensif lain</b><br>
• Laba rugi bertingkat & ukuran umum (common size)<br>
• Marjin kotor, usaha, EBITDA, sebelum pajak, bersih<br>
• Tarif pajak efektif<br>
• Laba berulang vs tidak berulang & rasio laba berulang<br>
• Perbandingan median per sektor<br><br>
<small>Profetik: Fathonah · QS Al An'am ayat 160</small></div>""", unsafe_allow_html=True)
b.markdown("""<div class="kartu"><h4>💧 Pertemuan 4 · Sub-CPMK4</h4>
<b>Laporan arus kas, perubahan ekuitas & hubungan keempat laporan</b><br>
• Arus kas operasi, investasi, pendanaan, arus kas bebas<br>
• Metode tidak langsung & estimasi metode langsung<br>
• Kualitas laba: CFO ÷ laba, akrual, capex ÷ penyusutan<br>
• Rekonsiliasi perubahan ekuitas & uji artikulasi laporan<br>
• Pola siklus hidup (Dickinson) per sektor<br><br>
<small>Profetik: Amanah · QS Al Furqan ayat 67 · Kuis 1</small></div>""", unsafe_allow_html=True)

st.write("")
st.markdown("### Cara memakai")
st.markdown("""
1. Buka halaman pertemuan di panel kiri.
2. Tab **Materi inti** berisi konsep dan rumus.
3. Tab **Analisis satu emiten**: pilih sektor, emiten, dan tahun. Semua hitungan tampil beserta grafiknya.
4. Tab **Perbandingan antarsektor**: lihat median tiap sektor untuk ukuran yang dipilih.
5. Tab **Unduh**: simpan hasil hitungan ke Excel untuk dicek ulang di lembar kerja.
""")
st.caption("Sumber data: laporan keuangan tahunan emiten BEI (data olahan). Klasifikasi sektor: IDX Industrial "
           "Classification (IDX-IC). Untuk keperluan pembelajaran, bukan rekomendasi investasi.")
