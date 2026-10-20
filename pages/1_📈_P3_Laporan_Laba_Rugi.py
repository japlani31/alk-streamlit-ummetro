# -*- coding: utf-8 -*-
"""Pertemuan 3 · Sub-CPMK3: laporan laba rugi dan penghasilan komprehensif lain."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import core
import hitung

core.set_page("P3 Laporan Laba Rugi", "📈")
df = core.muat_data()

st.markdown("""<div class="hero">
<span class="chip">Pertemuan 3</span><span class="chip">Sub-CPMK3 · CPMK1</span><span class="chip">Bobot 2%</span>
<h2>Laporan Laba Rugi & Penghasilan Komprehensif Lain</h2>
<p>Membaca susunan laba rugi bertingkat, menghitung marjin pada tiap tingkat laba, dan memisahkan
laba berulang dari laba tidak berulang memakai laporan keuangan emiten BEI, dikelompokkan per sektor.</p>
</div>""", unsafe_allow_html=True)
st.write("")

tab_materi, tab_emiten, tab_sektor, tab_unduh = st.tabs(
    ["📖 Materi inti", "🔎 Analisis satu emiten", "🏭 Perbandingan antarsektor", "📥 Unduh hasil hitungan"])

# =================================================================== MATERI
with tab_materi:
    k1, k2 = st.columns([3, 2])
    with k1:
        st.markdown("### 1. Susunan laporan laba rugi bertingkat")
        st.markdown("""
Laporan laba rugi menyajikan kinerja **selama satu periode**. Format bertingkat (*multiple step*)
memisahkan hasil dari kegiatan utama dan kegiatan di luar usaha, sehingga analis bisa melihat dari mana laba berasal.

| Tingkat | Isi | Pertanyaan analis |
|---|---|---|
| Pendapatan | Penjualan barang/jasa | Seberapa besar dan tumbuh berapa? |
| − Beban pokok | Biaya langsung produk | Seberapa efisien produksinya? |
| **= Laba kotor** | | Kekuatan harga & efisiensi produksi |
| − Beban usaha | Penjualan, umum, administrasi | Seberapa efisien operasinya? |
| **= Laba usaha** | | Kinerja inti bisnis |
| ± Pos di luar usaha | Bunga, kurs, asosiasi, lain-lain | Seberapa besar pengaruh pendanaan & pasar? |
| ± Pos tidak berulang | Pelepasan aset, penurunan nilai, restrukturisasi | Apakah laba ditopang kejadian sekali saja? |
| **= Laba sebelum pajak** − pajak | | |
| **= Laba bersih** | Milik entitas induk & nonpengendali | Hak pemegang saham induk |
""")
        st.markdown("### 2. Marjin pada tiap tingkat laba")
        for nama, rumus in [
            ("Marjin laba kotor", "Laba kotor ÷ Pendapatan"),
            ("Marjin laba usaha", "Laba usaha ÷ Pendapatan"),
            ("Marjin EBITDA", "(Laba usaha + Penyusutan & amortisasi) ÷ Pendapatan"),
            ("Marjin laba sebelum pajak", "Laba sebelum pajak ÷ Pendapatan"),
            ("Marjin laba bersih", "Laba bersih milik induk ÷ Pendapatan"),
            ("Tarif pajak efektif", "Beban pajak ÷ Laba sebelum pajak"),
        ]:
            st.markdown(f'<div class="rumus"><b>{nama}</b> = {rumus}</div>', unsafe_allow_html=True)
        st.markdown("### 3. Laba berulang vs laba tidak berulang")
        st.markdown("""
**Laba berulang** (*recurring*) berasal dari kegiatan normal yang diharapkan terjadi lagi tahun depan.
**Laba tidak berulang** (*non-recurring*) muncul dari kejadian khusus: menjual aset tetap, menurunkan nilai
aset atau goodwill, biaya restrukturisasi, atau penyelesaian perkara hukum.

Mengapa penting? Laba yang tampak melonjak karena menjual pabrik **tidak akan terulang**. Investor dan
kreditur menilai perusahaan dari laba yang berkelanjutan.
""")
        st.markdown('<div class="rumus">Pos tidak berulang = Laba sebelum pajak − Laba sebelum pajak dari kegiatan berulang</div>'
                    '<div class="rumus">Laba berulang (setelah pajak) = Laba bersih − Pos tidak berulang × (1 − tarif pajak efektif)</div>'
                    '<div class="rumus">Rasio laba berulang = Laba berulang ÷ Laba bersih dilaporkan</div>',
                    unsafe_allow_html=True)
        st.caption("Rasio laba berulang mendekati 1 berarti laba didominasi kegiatan inti. Jauh di bawah 1 berarti "
                   "laba tahun ini terdongkrak pos sekali saja; di atas 1 berarti laba tertekan kerugian sekali saja.")
        st.markdown("### 4. Penghasilan komprehensif lain (PKL)")
        st.markdown("""
PKL memuat keuntungan/kerugian yang **belum terealisasi** dan langsung masuk ekuitas, bukan laba rugi:
selisih kurs penjabaran laporan anak usaha luar negeri, perubahan nilai wajar instrumen keuangan tertentu,
surplus revaluasi aset tetap, dan pengukuran kembali program imbalan pasti.

**Laba komprehensif = Laba tahun berjalan + Penghasilan komprehensif lain.**
Pada aplikasi ini, besaran PKL ditelusuri lewat rekonsiliasi perubahan ekuitas di **Pertemuan 4**.
""")
    with k2:
        core.kotak_ayat(3, "Fathonah", "QS Al An'am ayat 160",
                        "مَن جَاءَ بِالْحَسَنَةِ فَلَهُ عَشْرُ أَمْثَالِهَا",
                        "Barangsiapa membawa amal yang baik maka baginya sepuluh kali lipat amalnya.",
                        "Penegasan bahwa balasan diberikan setara amal menuntun penyajian pendapatan dan "
                        "beban secara sepadan (prinsip penandingan).")
        st.write("")
        st.markdown("""<div class="kartu"><b>🎯 Capaian pertemuan ini</b><br>
Setelah pertemuan ini kamu mampu:<br>
1. Menjelaskan susunan laba rugi bertingkat.<br>
2. Menghitung dan menafsirkan marjin tiap tingkat laba.<br>
3. Memisahkan laba berulang dan tidak berulang.<br>
4. Membandingkan struktur laba antarsektor.<br><br>
<b>Penilaian:</b> praktik penyelesaian kasus lapangan (non-tes).</div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div class="catatan">💡 <b>Sektor keuangan</b> (bank, asuransi, multifinance) tidak
memiliki beban pokok penjualan, sehingga marjin kotor tidak dihitung. Bandingkan bank dengan bank.</div>""",
                    unsafe_allow_html=True)

# =================================================================== EMITEN
with tab_emiten:
    r, d_emt = core.pemilih_emiten(df, "p3")
    st.caption(f"Subsektor: {r['subsektor']} · Satuan: miliar rupiah (M) · Sumber: laporan tahunan emiten BEI")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Pendapatan", core.rp(r["revenue"], "auto"),
              core.persen(r["tumbuh_pendapatan"]) if pd.notna(r["tumbuh_pendapatan"]) else None)
    m2.metric("Laba bersih", core.rp(r["netinc"], "auto"),
              core.persen(r["tumbuh_laba"]) if pd.notna(r["tumbuh_laba"]) else None)
    m3.metric("Marjin kotor", core.persen(r["marjin_kotor"]))
    m4.metric("Marjin usaha", core.persen(r["marjin_usaha"]))
    m5.metric("Marjin bersih", core.persen(r["marjin_bersih"]))

    st.markdown("#### Laporan laba rugi bertingkat & ukuran umum (common size)")
    lr = hitung.laba_rugi_bertingkat(r)
    kiri, kanan = st.columns([3, 2])
    with kiri:
        tampil = core.tabel_rp(lr.drop(columns="jenis"), kolom_persen="% Pendapatan")

        def gaya(baris):
            j = lr.loc[baris.name, "jenis"]
            if j in ("subtotal", "total"):
                return ["font-weight:700;background:#eef2ff"] * len(baris)
            if j == "tidak_berulang":
                return ["font-weight:700;background:#fef3c7"] * len(baris)
            return [""] * len(baris)
        st.dataframe(tampil.style.apply(gaya, axis=1), hide_index=True, width="stretch", height=600)
    with kanan:
        alur = lr[lr["Pos"].isin(["Pendapatan", "Laba kotor", "Laba usaha",
                                   "Laba sebelum pajak", "Laba bersih milik entitas induk"])]
        fig = go.Figure(go.Funnel(y=["Pendapatan", "Laba kotor", "Laba usaha", "Laba sebelum pajak", "Laba bersih"][:len(alur)],
                                  x=(alur["Nilai"] / 1e9).round(1),
                                  textinfo="value+percent initial",
                                  marker=dict(color=["#1e3a8a", "#1d4ed8", "#3b82f6", "#60a5fa", "#93c5fd"][:len(alur)])))
        fig.update_layout(height=380, margin=dict(t=30, l=10, r=10, b=10), title="Dari pendapatan ke laba bersih (miliar Rp)")
        st.plotly_chart(fig, width="stretch")
        pr, n = hitung.peringkat_dalam_sektor(df, r["tahun"], r["sektor"], "marjin_bersih", r["kode"])
        if pr:
            st.info(f"Marjin bersih **{r['kode']}** berada di peringkat **{pr} dari {n}** emiten sektor "
                    f"**{r['sektor']}** tahun {r['tahun']}.")

    st.markdown("#### Tren marjin 5 tahun")
    tren = d_emt[["tahun", "marjin_kotor", "marjin_usaha", "marjin_ebitda", "marjin_bersih"]].melt(
        "tahun", var_name="Marjin", value_name="Nilai").dropna()
    tren["Marjin"] = tren["Marjin"].map({"marjin_kotor": "Kotor", "marjin_usaha": "Usaha",
                                         "marjin_ebitda": "EBITDA", "marjin_bersih": "Bersih"})
    fig = px.line(tren, x="tahun", y="Nilai", color="Marjin", markers=True)
    fig.update_layout(height=330, yaxis_tickformat=".0%", margin=dict(t=10), xaxis=dict(dtick=1), legend_title=None)
    st.plotly_chart(fig, width="stretch")

    st.markdown("#### Laba berulang vs laba tidak berulang")
    a, b = st.columns([3, 2])
    with a:
        dd = d_emt[["tahun", "laba_berulang", "tidak_berulang_setelah_pajak"]].copy()
        fig = go.Figure()
        fig.add_bar(x=dd["tahun"], y=dd["laba_berulang"] / 1e9, name="Laba berulang", marker_color=core.WARNA["utama"])
        fig.add_bar(x=dd["tahun"], y=dd["tidak_berulang_setelah_pajak"] / 1e9, name="Pos tidak berulang (setelah pajak)",
                    marker_color=core.WARNA["aksen"])
        fig.add_scatter(x=d_emt["tahun"], y=d_emt["netinc"] / 1e9, name="Laba bersih dilaporkan",
                        mode="lines+markers", line=dict(color="#111827", width=3))
        fig.update_layout(barmode="relative", height=340, margin=dict(t=10), yaxis_title="miliar Rp",
                          xaxis=dict(dtick=1), legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, width="stretch")
    with b:
        st.metric("Rasio laba berulang", core.kali(r["rasio_laba_berulang"]))
        st.metric("Porsi pos tidak berulang thd laba sebelum pajak", core.persen(r["porsi_tidak_berulang"]))
        rinci = hitung.rincian_tidak_berulang(r)
        if rinci.empty:
            st.success("Tidak ada pos tidak berulang yang material tahun ini. Laba berasal dari kegiatan berulang.")
        else:
            st.dataframe(core.tabel_rp(rinci), hide_index=True, width="stretch")
        rasio = r["rasio_laba_berulang"]
        if pd.notna(rasio):
            if rasio < 0.8:
                st.warning("Laba tahun ini **terdongkrak** pos tidak berulang. Laba inti lebih rendah dari yang dilaporkan.")
            elif rasio > 1.2:
                st.warning("Laba tahun ini **tertekan** kerugian tidak berulang. Laba inti lebih baik dari yang dilaporkan.")
            else:
                st.success("Laba dilaporkan mencerminkan kinerja inti (kualitas laba baik).")

    st.markdown("#### Dibanding median sektornya")
    banding = []
    for kol, label in [("marjin_kotor", "Marjin kotor"), ("marjin_usaha", "Marjin usaha"),
                       ("marjin_bersih", "Marjin bersih"), ("tarif_pajak_efektif", "Tarif pajak efektif"),
                       ("rasio_laba_berulang", "Rasio laba berulang")]:
        med = df[(df["tahun"] == r["tahun"]) & (df["sektor"] == r["sektor"])][kol].median()
        banding.append({"Ukuran": label, r["kode"]: r[kol], f"Median {r['sektor']}": med})
    bd = pd.DataFrame(banding)
    for c in bd.columns[1:]:
        bd[c] = [core.kali(v) if u == "Rasio laba berulang" else core.persen(v) for u, v in zip(bd["Ukuran"], bd[c])]
    st.dataframe(bd, hide_index=True, width="stretch")

# =================================================================== SEKTOR
UKURAN_P3 = {
    "Marjin laba kotor": "marjin_kotor",
    "Marjin laba usaha": "marjin_usaha",
    "Marjin EBITDA": "marjin_ebitda",
    "Marjin laba bersih": "marjin_bersih",
    "Tarif pajak efektif": "tarif_pajak_efektif",
    "Rasio laba berulang": "rasio_laba_berulang",
    "Porsi pos tidak berulang": "porsi_tidak_berulang",
    "Pertumbuhan pendapatan": "tumbuh_pendapatan",
}

with tab_sektor:
    c1, c2, c3 = st.columns([1, 2, 2])
    tahun = c1.selectbox("Tahun", core.tahun_utama(df), key="p3s_thn")
    label = c2.selectbox("Ukuran", list(UKURAN_P3), index=3, key="p3s_uk")
    keluar = c3.toggle("Keluarkan sektor Keuangan", value=label == "Marjin laba kotor", key="p3s_keu")
    kol = UKURAN_P3[label]
    ag = hitung.agregat_sektor(df, tahun, kol, keluarkan_keuangan=keluar)
    rasio = kol == "rasio_laba_berulang"

    fig = go.Figure(go.Bar(
        x=ag["Median"], y=ag["Sektor"], orientation="h", marker_color=core.WARNA["utama"],
        error_x=dict(type="data", symmetric=False, array=ag["Kuartil 3"] - ag["Median"],
                     arrayminus=ag["Median"] - ag["Kuartil 1"], color="#94a3b8"),
        text=[core.kali(v) if rasio else core.persen(v) for v in ag["Median"]], textposition="outside"))
    fig.update_layout(height=470, margin=dict(t=40, l=10), yaxis=dict(autorange="reversed"),
                      title=f"Median {label.lower()} per sektor, {tahun} (garis = kuartil 1 sampai 3)",
                      xaxis_tickformat=None if rasio else ".0%")
    st.plotly_chart(fig, width="stretch")

    t = ag.copy()
    for c in ["Median", "Kuartil 1", "Kuartil 3"]:
        t[c] = t[c].map(core.kali if rasio else core.persen)
    st.dataframe(t, hide_index=True, width="stretch")
    st.caption("Median dipakai (bukan rata-rata) agar tidak terseret emiten dengan nilai ekstrem. "
               "Nilai di luar persentil 2-98 dipangkas untuk grafik. Sektor dengan kurang dari 3 emiten disembunyikan.")

    st.markdown("#### Sebaran emiten dalam satu sektor")
    s1, s2 = st.columns([2, 3])
    sek = s1.selectbox("Pilih sektor", ag["Sektor"].tolist(), key="p3s_sek")
    d = df[(df["tahun"] == tahun) & (df["sektor"] == sek) & df[kol].notna()].sort_values(kol, ascending=False)
    with s2:
        st.caption(f"{len(d)} emiten · urut dari {label.lower()} tertinggi")
    top = d[["kode", "nama", "subsektor", kol, "revenue", "netinc"]].head(15).copy()
    top[kol] = top[kol].map(core.kali if rasio else core.persen)
    top["revenue"] = top["revenue"].map(lambda v: core.rp(v))
    top["netinc"] = top["netinc"].map(lambda v: core.rp(v))
    st.dataframe(top.rename(columns={"kode": "Kode", "nama": "Nama", "subsektor": "Subsektor",
                                     kol: label, "revenue": "Pendapatan", "netinc": "Laba bersih"}),
                 hide_index=True, width="stretch")

# =================================================================== UNDUH
with tab_unduh:
    st.markdown("#### Unduh hasil hitungan Pertemuan 3 ke Excel")
    u1, u2 = st.columns(2)
    thn = u1.selectbox("Tahun", core.tahun_utama(df), key="p3u_thn")
    sek_u = u2.multiselect("Sektor", sorted(df["sektor"].unique()), default=[], key="p3u_sek",
                           placeholder="Kosongkan = semua sektor")
    d = df[df["tahun"] == thn]
    if sek_u:
        d = d[d["sektor"].isin(sek_u)]
    kolom = ["kode", "nama", "sektor", "subsektor", "tahun", "revenue", "cor", "gp", "opex", "opinc", "ebtExcl",
             "pos_tidak_berulang", "pretax", "taxexp", "netinc", "marjin_kotor", "marjin_usaha", "marjin_ebitda",
             "marjin_sebelum_pajak", "marjin_bersih", "tarif_pajak_efektif", "laba_berulang", "rasio_laba_berulang",
             "tumbuh_pendapatan", "tumbuh_laba"]
    data = d[kolom]
    ringkas = pd.concat([hitung.agregat_sektor(df, thn, k).assign(Ukuran=lbl)
                         for lbl, k in UKURAN_P3.items()], ignore_index=True)
    st.write(f"{len(data)} emiten siap diunduh.")
    st.download_button("📥 Unduh Excel (data emiten + ringkasan sektor)",
                       core.ke_excel({"P3 per emiten": data, "P3 median sektor": ringkas}),
                       file_name=f"ALK_P3_LabaRugi_{thn}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.caption("Kolom nilai dalam rupiah penuh; kolom rasio dalam bentuk desimal (0,25 = 25%).")
