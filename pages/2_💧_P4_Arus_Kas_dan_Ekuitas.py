# -*- coding: utf-8 -*-
"""Pertemuan 4 · Sub-CPMK4: laporan arus kas, laporan perubahan ekuitas, hubungan keempat laporan."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import core
import hitung

core.set_page("P4 Arus Kas & Ekuitas", "💧")
df = core.muat_data()

st.markdown("""<div class="hero">
<span class="chip">Pertemuan 4</span><span class="chip">Sub-CPMK4 · CPMK1</span><span class="chip">Kuis 1</span>
<h2>Laporan Arus Kas, Perubahan Ekuitas & Hubungan Keempat Laporan</h2>
<p>Menelusuri kas dari kegiatan operasi, investasi, dan pendanaan; membandingkan metode langsung dan tidak
langsung; merekonsiliasi perubahan ekuitas; dan membuktikan bahwa keempat laporan pokok saling terhubung.</p>
</div>""", unsafe_allow_html=True)
st.write("")

tab_materi, tab_emiten, tab_sektor, tab_unduh = st.tabs(
    ["📖 Materi inti", "🔎 Analisis satu emiten", "🏭 Perbandingan antarsektor", "📥 Unduh hasil hitungan"])

# =================================================================== MATERI
with tab_materi:
    k1, k2 = st.columns([3, 2])
    with k1:
        st.markdown("### 1. Tiga kegiatan dalam laporan arus kas")
        st.markdown("""
| Kegiatan | Contoh arus masuk | Contoh arus keluar |
|---|---|---|
| **Operasi (CFO)** | Penerimaan dari pelanggan | Bayar pemasok, gaji, bunga*, pajak |
| **Investasi (CFI)** | Penjualan aset tetap/investasi | Belanja modal (capex), akuisisi |
| **Pendanaan (CFF)** | Pinjaman baru, penerbitan saham | Pelunasan utang, dividen, pembelian kembali saham |

*PSAK memberi pilihan klasifikasi bunga dan dividen; yang penting konsisten antarperiode.
""")
        st.markdown('<div class="rumus">Kenaikan (penurunan) kas = CFO + CFI + CFF + pengaruh selisih kurs</div>',
                    unsafe_allow_html=True)
        st.markdown("### 2. Metode langsung vs tidak langsung")
        st.markdown("""
Keduanya menghasilkan **angka CFO yang sama**; yang berbeda cara penyajiannya.

- **Metode langsung** merinci penerimaan dan pembayaran kas bruto (dari pelanggan, ke pemasok, ke karyawan).
  Mudah dipahami pemakai dan dianjurkan PSAK 2.
- **Metode tidak langsung** berangkat dari laba bersih lalu menyesuaikan pos nonkas dan perubahan modal kerja.
  Lebih banyak dipakai karena memperlihatkan **mengapa laba berbeda dari kas**.
""")
        st.markdown('<div class="rumus">CFO (tidak langsung) = Laba bersih + Penyusutan & amortisasi ± Pos nonkas lain − Kenaikan modal kerja</div>'
                    '<div class="rumus">Penerimaan dari pelanggan ≈ Pendapatan − Kenaikan piutang usaha</div>'
                    '<div class="rumus">Pembayaran ke pemasok ≈ Beban pokok + Kenaikan persediaan − Kenaikan utang usaha</div>',
                    unsafe_allow_html=True)
        st.markdown("### 3. Membaca kualitas arus kas")
        for nama, rumus, arti in [
            ("Arus kas operasi terhadap laba", "CFO ÷ Laba bersih", "di atas 1 menandakan laba didukung kas"),
            ("Akrual", "Laba bersih − CFO", "makin besar, makin banyak laba yang belum menjadi kas"),
            ("Rasio akrual", "(Laba bersih − CFO) ÷ Rata-rata total aset", "positif tinggi patut dicermati"),
            ("Arus kas bebas (FCF)", "CFO − Belanja modal", "kas yang tersisa untuk kreditur & pemegang saham"),
            ("Belanja modal terhadap penyusutan", "Capex ÷ Penyusutan", "> 1 ekspansi, < 1 aset menua"),
            ("Rasio pembayaran dividen (kas)", "Dividen kas dibayar ÷ Laba bersih", "porsi laba yang dibagikan"),
        ]:
            st.markdown(f'<div class="rumus"><b>{nama}</b> = {rumus} <span style="color:#475569">({arti})</span></div>',
                        unsafe_allow_html=True)
        st.markdown("### 4. Pola arus kas & siklus hidup perusahaan (Dickinson, 2011)")
        st.dataframe(pd.DataFrame([{"Tahap": k, "Tanda CFO, CFI, CFF & arti": v} for k, v in hitung.POLA_ARTI.items()]),
                     hide_index=True, width="stretch")
        st.markdown("### 5. Laporan perubahan ekuitas & hubungan keempat laporan")
        st.markdown('<div class="rumus">Ekuitas akhir = Ekuitas awal + Laba tahun berjalan + Penghasilan komprehensif lain '
                    '− Dividen + Penerbitan saham − Pembelian kembali saham</div>', unsafe_allow_html=True)
        st.markdown("""
Keempat laporan pokok saling mengunci:
1. **Laba rugi → Arus kas:** laba bersih menjadi titik awal metode tidak langsung.
2. **Laba rugi → Perubahan ekuitas:** laba bersih menambah saldo laba.
3. **Arus kas → Posisi keuangan:** kenaikan kas sama dengan perubahan saldo kas di neraca.
4. **Perubahan ekuitas → Posisi keuangan:** ekuitas akhir masuk ke neraca, menjaga *Aset = Liabilitas + Ekuitas*.
""")
    with k2:
        core.kotak_ayat(4, "Amanah", "QS Al Furqan ayat 67",
                        "وَالَّذِينَ إِذَا أَنفَقُوا لَمْ يُسْرِفُوا وَلَمْ يَقْتُرُوا وَكَانَ بَيْنَ ذَٰلِكَ قَوَامًا",
                        "Dan orang-orang yang apabila membelanjakan harta, mereka tidak berlebihan dan tidak pula kikir, "
                        "dan adalah pembelanjaan itu di tengah antara keduanya.",
                        "Sifat membelanjakan tidak berlebihan dan tidak kikir menuntun pembacaan arus kas sebagai "
                        "ukuran kewajaran pengeluaran.")
        st.write("")
        st.markdown("""<div class="kartu"><b>🎯 Capaian pertemuan ini</b><br>
1. Mengelompokkan arus kas ke kegiatan operasi, investasi, pendanaan.<br>
2. Menyusun rekonsiliasi metode tidak langsung dan memahami metode langsung.<br>
3. Menyusun laporan perubahan ekuitas.<br>
4. Membuktikan hubungan keempat laporan pokok.<br>
5. Menilai kualitas laba lewat arus kas, antarsektor.<br><br>
<b>Penilaian:</b> Kuis 1 daring di SPADA (satu soal benar bernilai sepuluh).</div>""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""<div class="catatan">💡 Arus kas <b>bank</b> berbeda: perubahan simpanan nasabah dan
kredit masuk kegiatan operasi, sehingga CFO bank sangat berfluktuasi. Karena itu sektor Keuangan bisa
dikeluarkan saat membandingkan sektor.</div>""", unsafe_allow_html=True)

# =================================================================== EMITEN
with tab_emiten:
    r, d_emt = core.pemilih_emiten(df, "p4")
    st.caption(f"Subsektor: {r['subsektor']} · Satuan: miliar rupiah (M)")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Arus kas operasi", core.rp(r["ncfo"], "auto"))
    m2.metric("Arus kas investasi", core.rp(r["ncfi"], "auto"))
    m3.metric("Arus kas pendanaan", core.rp(r["ncff"], "auto"))
    m4.metric("Arus kas bebas", core.rp(r["fcf"], "auto"))
    m5.metric("CFO ÷ Laba bersih", core.kali(r["cfo_terhadap_laba"]))

    pola = r["pola_arus_kas"]
    st.markdown(f"""<div class="kartu">Pola arus kas {r['tahun']}: <b style="color:{core.WARNA_POLA.get(pola, '#000')}">{pola}</b><br>
    {hitung.POLA_ARTI.get(pola, '')}</div>""", unsafe_allow_html=True)
    st.write("")

    st.markdown("#### Komposisi arus kas 5 tahun")
    fig = go.Figure()
    for kol, nama, warna in [("ncfo", "Operasi", core.WARNA["utama"]), ("ncfi", "Investasi", core.WARNA["aksen"]),
                             ("ncff", "Pendanaan", core.WARNA["ungu"])]:
        fig.add_bar(x=d_emt["tahun"], y=d_emt[kol] / 1e9, name=nama, marker_color=warna)
    fig.add_scatter(x=d_emt["tahun"], y=d_emt["fcf"] / 1e9, name="Arus kas bebas", mode="lines+markers",
                    line=dict(color=core.WARNA["naik"], width=3))
    fig.add_scatter(x=d_emt["tahun"], y=d_emt["netinc"] / 1e9, name="Laba bersih", mode="lines+markers",
                    line=dict(color="#111827", width=2, dash="dot"))
    fig.update_layout(barmode="group", height=360, margin=dict(t=10), yaxis_title="miliar Rp",
                      xaxis=dict(dtick=1), legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, width="stretch")

    st.markdown("#### Metode tidak langsung vs estimasi metode langsung")
    a, b = st.columns(2)
    with a:
        st.markdown("**Metode tidak langsung (dari laporan)**")
        tl = hitung.arus_kas_tidak_langsung(r)
        st.dataframe(core.tabel_rp(tl), hide_index=True, width="stretch")
        wf = tl.iloc[:-1]
        fig = go.Figure(go.Waterfall(
            x=[p.replace("(+/-) ", "").replace("(+) ", "") for p in wf["Pos"]] + ["Arus kas operasi"],
            y=list(wf["Nilai"] / 1e9) + [0], measure=["absolute"] + ["relative"] * (len(wf) - 1) + ["total"],
            connector=dict(line=dict(color="#cbd5e1"))))
        fig.update_layout(height=330, margin=dict(t=10, b=10), yaxis_title="miliar Rp", showlegend=False)
        st.plotly_chart(fig, width="stretch")
    with b:
        st.markdown("**Metode langsung (estimasi konversi)**")
        ld = hitung.arus_kas_langsung_estimasi(r)
        st.dataframe(core.tabel_rp(ld), hide_index=True, width="stretch")
        est, lap = ld["Nilai"].iloc[-2], ld["Nilai"].iloc[-1]
        if pd.notna(est) and pd.notna(lap) and lap != 0:
            st.caption(f"Selisih estimasi terhadap laporan: {core.persen((est - lap) / abs(lap))}. Wajar terjadi karena "
                       "pendekatan konversi tidak memuat seluruh pos (uang muka, beban dibayar dimuka, akrual lain). "
                       "Pelajaran utamanya: angka yang sama bisa dibaca dari dua sisi.")

    st.markdown("#### Kualitas laba dilihat dari arus kas")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Akrual (laba − CFO)", core.rp(r["akrual"], "auto"))
    q2.metric("Rasio akrual", core.persen(r["rasio_akrual"]))
    q3.metric("Capex ÷ penyusutan", core.kali(r["capex_terhadap_penyusutan"]))
    q4.metric("Pembayaran dividen (kas)", core.persen(r["rasio_pembayaran_dividen"]))
    if pd.notna(r["cfo_terhadap_laba"]):
        if r["cfo_terhadap_laba"] >= 1:
            st.success("Arus kas operasi melampaui laba bersih: laba didukung kas nyata.")
        elif r["cfo_terhadap_laba"] >= 0.5:
            st.info("Sebagian laba belum menjadi kas. Periksa kenaikan piutang dan persediaan.")
        else:
            st.warning("Laba jauh lebih besar dari kas operasi. Telusuri akrual dan modal kerja.")

    st.markdown("#### Laporan perubahan ekuitas (rekonsiliasi)")
    c, e = st.columns([3, 2])
    with c:
        pe = hitung.perubahan_ekuitas(r)
        st.dataframe(core.tabel_rp(pe), hide_index=True, width="stretch")
        st.caption("*Dihitung sebagai sisa rekonsiliasi: memuat penghasilan komprehensif lain (selisih kurs penjabaran, "
                   "pengukuran kembali imbalan kerja, revaluasi), perubahan kepemilikan nonpengendali, dan pos ekuitas lain.")
    with e:
        if pe["Nilai"].notna().iloc[[0, -1]].all():
            fig = go.Figure(go.Waterfall(
                x=["Awal", "Laba", "Dividen", "Terbit saham", "Beli kembali", "PKL & lainnya", "Akhir"],
                y=list(pe["Nilai"].iloc[:-1] / 1e9) + [0],
                measure=["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
                connector=dict(line=dict(color="#cbd5e1"))))
            fig.update_layout(height=320, margin=dict(t=10, b=10), yaxis_title="miliar Rp")
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Ekuitas tahun sebelumnya tidak tersedia, rekonsiliasi tidak dapat disusun untuk tahun ini.")

    st.markdown("#### Hubungan keempat laporan pokok")
    art = hitung.artikulasi(r)
    art["Selisih"] = art["Selisih"].map(lambda v: core.rp(v))
    art["Status"] = art["Status"].map({"Cocok": "✅ Cocok", "Ada selisih": "⚠️ Ada selisih",
                                       "Data tidak cukup": "➖ Data tidak cukup"})
    st.dataframe(art, hide_index=True, width="stretch")
    st.caption("Selisih kecil (≤2%) dianggap wajar karena pembulatan, reklasifikasi, atau kas yang dibatasi penggunaannya.")

# =================================================================== SEKTOR
UKURAN_P4 = {
    "CFO terhadap laba bersih": ("cfo_terhadap_laba", "kali"),
    "Rasio akrual": ("rasio_akrual", "persen"),
    "Arus kas bebas terhadap pendapatan": ("fcf_terhadap_pendapatan", "persen"),
    "Belanja modal terhadap penyusutan": ("capex_terhadap_penyusutan", "kali"),
    "Rasio pembayaran dividen (kas)": ("rasio_pembayaran_dividen", "persen"),
}

with tab_sektor:
    tahun_list = core.tahun_utama(df)
    c1, c2 = st.columns([1, 3])
    tahun = c1.selectbox("Tahun", tahun_list, key="p4s_thn")
    keluar = c2.toggle("Keluarkan sektor Keuangan (disarankan untuk arus kas)", value=True, key="p4s_keu")

    st.markdown("#### Pola arus kas (siklus hidup) per sektor")
    sp = hitung.sebaran_pola(df, tahun, keluarkan_keuangan=keluar)
    sp = sp.drop(index=[i for i in sp.index if i == "Belum terklasifikasi"], errors="ignore")
    panjang = sp.reset_index().melt("sektor", var_name="Pola", value_name="Persen")
    fig = px.bar(panjang, y="sektor", x="Persen", color="Pola", orientation="h",
                 color_discrete_map=core.WARNA_POLA, category_orders={"Pola": hitung.POLA_URUT})
    fig.update_layout(height=460, margin=dict(t=10), xaxis_title="% emiten dalam sektor", yaxis_title=None,
                      legend=dict(orientation="h", y=-0.15), barmode="stack")
    st.plotly_chart(fig, width="stretch")
    st.caption("Sektor dengan porsi 'Kedewasaan' besar umumnya sudah mampu membiayai investasi dan membayar "
               "kreditur/pemegang saham dari kas operasinya sendiri.")

    st.markdown("#### Ukuran kualitas arus kas per sektor")
    label = st.selectbox("Ukuran", list(UKURAN_P4), key="p4s_uk")
    kol, jenis = UKURAN_P4[label]
    fmt = core.kali if jenis == "kali" else core.persen
    ag = hitung.agregat_sektor(df, tahun, kol, keluarkan_keuangan=keluar)
    fig = go.Figure(go.Bar(
        x=ag["Median"], y=ag["Sektor"], orientation="h", marker_color=core.WARNA["utama"],
        error_x=dict(type="data", symmetric=False, array=ag["Kuartil 3"] - ag["Median"],
                     arrayminus=ag["Median"] - ag["Kuartil 1"], color="#94a3b8"),
        text=[fmt(v) for v in ag["Median"]], textposition="outside"))
    fig.update_layout(height=450, margin=dict(t=40, l=10), yaxis=dict(autorange="reversed"),
                      title=f"Median {label.lower()} per sektor, {tahun}",
                      xaxis_tickformat=".0%" if jenis == "persen" else None)
    st.plotly_chart(fig, width="stretch")
    t = ag.copy()
    for c in ["Median", "Kuartil 1", "Kuartil 3"]:
        t[c] = t[c].map(fmt)
    st.dataframe(t, hide_index=True, width="stretch")

# =================================================================== UNDUH
with tab_unduh:
    st.markdown("#### Unduh hasil hitungan Pertemuan 4 ke Excel")
    u1, u2 = st.columns(2)
    thn = u1.selectbox("Tahun", core.tahun_utama(df), key="p4u_thn")
    sek_u = u2.multiselect("Sektor", sorted(df["sektor"].unique()), default=[], key="p4u_sek",
                           placeholder="Kosongkan = semua sektor")
    d = df[df["tahun"] == thn]
    if sek_u:
        d = d[d["sektor"].isin(sek_u)]
    kolom = ["kode", "nama", "sektor", "subsektor", "tahun", "netinc", "totalDepAmorCF", "changeWorkingCapital",
             "ncfo", "capex", "ncfi", "commonDividendCF", "ncff", "ncf", "fcf", "cfo_terhadap_laba", "akrual",
             "rasio_akrual", "fcf_terhadap_pendapatan", "capex_terhadap_penyusutan", "rasio_pembayaran_dividen",
             "pola_arus_kas", "equity_lalu", "laba_tahun_berjalan", "dividen_kas", "penerbitan_saham",
             "pembelian_kembali", "ekuitas_lainnya", "equity", "selisih_kas", "selisih_saldo_laba", "selisih_neraca"]
    ringkas = pd.concat([hitung.agregat_sektor(df, thn, k).assign(Ukuran=lbl)
                         for lbl, (k, _) in UKURAN_P4.items()], ignore_index=True)
    pola = hitung.sebaran_pola(df, thn).round(1).reset_index()
    st.write(f"{len(d)} emiten siap diunduh.")
    st.download_button("📥 Unduh Excel (emiten + median sektor + pola arus kas)",
                       core.ke_excel({"P4 per emiten": d[kolom], "P4 median sektor": ringkas,
                                      "P4 pola arus kas (%)": pola}),
                       file_name=f"ALK_P4_ArusKas_Ekuitas_{thn}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
