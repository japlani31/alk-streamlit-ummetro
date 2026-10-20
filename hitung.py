# -*- coding: utf-8 -*-
"""
Mesin perhitungan Analisa Laporan Keuangan, Pertemuan 3 dan 4.

Konvensi data sumber (sudah diverifikasi terhadap identitas akuntansi):
- Satuan rupiah penuh.
- Beban bunga, belanja modal (capex), dan dividen kas tercatat NEGATIF.
- Beban pokok (cor) dan beban usaha (opex) tercatat POSITIF.
- pretax = ebtExcl (laba sebelum pajak dari kegiatan berulang) + pos tidak berulang.
- netinc = pretax - taxexp + minorityInterest  (laba milik pemilik entitas induk;
  minorityInterest bertanda negatif bila mengurangi laba induk).

Pertemuan 3 (Sub-CPMK3): laba rugi bertingkat, ukuran umum (common size),
  marjin, laba berulang vs tidak berulang.
Pertemuan 4 (Sub-CPMK4): komponen arus kas, metode tidak langsung, estimasi
  metode langsung, perubahan ekuitas, hubungan keempat laporan pokok.
"""
import numpy as np
import pandas as pd

TARIF_PAJAK_DEFAULT = 0.22   # tarif PPh badan umum Indonesia (dipakai bila tarif efektif tak wajar)

POS_TIDAK_BERULANG = {
    "gainAssets": "Laba/rugi pelepasan aset",
    "gainInvestments": "Laba/rugi investasi",
    "assetWritedown": "Penurunan nilai aset",
    "impairmentGoodwill": "Penurunan nilai goodwill",
    "mergerRestructureCharges": "Biaya merger/restrukturisasi",
    "legalSettlements": "Penyelesaian perkara hukum",
    "otherUnusualItems": "Pos luar biasa lainnya",
}


def _n(x):
    """Angka aman: NaN bila kosong."""
    try:
        x = float(x)
        return x if np.isfinite(x) else np.nan
    except (TypeError, ValueError):
        return np.nan


def _bagi(a, b):
    a, b = _n(a), _n(b)
    if np.isnan(a) or np.isnan(b) or b == 0:
        return np.nan
    return a / b


def _nol(x):
    x = _n(x)
    return 0.0 if np.isnan(x) else x


# ============================================================ data tingkat baris
def siapkan(df):
    """Tambahkan nilai tahun lalu (untuk perubahan) dan semua rasio turunan."""
    df = df.sort_values(["kode", "tahun"]).copy()
    g = df.groupby("kode")
    for c in ["revenue", "netinc", "assets", "equity", "cashneq", "retearn",
              "accountsReceivable", "inventory", "accountsPayable"]:
        df[f"{c}_lalu"] = g[c].shift(1)
    # hanya pakai nilai lalu bila tahunnya memang berurutan
    berurut = (df["tahun"] - g["tahun"].shift(1)) == 1
    for c in [k for k in df.columns if k.endswith("_lalu")]:
        df.loc[~berurut, c] = np.nan

    # ----- Pertemuan 3: marjin -----
    rev = df["revenue"]
    ada_rev = rev.notna() & (rev > 0)
    df["marjin_kotor"] = np.where(ada_rev & df["gp"].notna() & df["cor"].notna(), df["gp"] / rev, np.nan)
    df["marjin_usaha"] = np.where(ada_rev, df["opinc"] / rev, np.nan)
    df["marjin_ebitda"] = np.where(ada_rev, df["ebitda"] / rev, np.nan)
    df["marjin_sebelum_pajak"] = np.where(ada_rev, df["pretax"] / rev, np.nan)
    df["marjin_bersih"] = np.where(ada_rev, df["netinc"] / rev, np.nan)
    df["tarif_pajak_efektif"] = np.where(df["pretax"] > 0, df["taxexp"] / df["pretax"], np.nan)

    # ----- Pertemuan 3: laba berulang vs tidak berulang -----
    jml_item = df[list(POS_TIDAK_BERULANG)].fillna(0).sum(axis=1)
    df["pos_tidak_berulang"] = np.where(
        df["pretax"].notna() & df["ebtExcl"].notna(), df["pretax"] - df["ebtExcl"], jml_item)
    t = df["tarif_pajak_efektif"].where(df["tarif_pajak_efektif"].between(0, 0.5), TARIF_PAJAK_DEFAULT)
    df["tidak_berulang_setelah_pajak"] = df["pos_tidak_berulang"] * (1 - t)
    df["laba_berulang"] = df["netinc"] - df["tidak_berulang_setelah_pajak"]
    df["porsi_tidak_berulang"] = np.where(
        df["pretax"].abs() > 0, df["pos_tidak_berulang"] / df["pretax"].abs(), np.nan)
    df["rasio_laba_berulang"] = np.where(df["netinc"] > 0, df["laba_berulang"] / df["netinc"], np.nan)
    df["tumbuh_pendapatan"] = np.where(df["revenue_lalu"] > 0, rev / df["revenue_lalu"] - 1, np.nan)
    df["tumbuh_laba"] = np.where(df["netinc_lalu"] > 0, df["netinc"] / df["netinc_lalu"] - 1, np.nan)

    # ----- Pertemuan 4: arus kas -----
    df["fcf"] = df["ncfo"] + df["capex"].fillna(0)            # capex negatif
    df["fcf_terhadap_pendapatan"] = np.where(ada_rev, df["fcf"] / rev, np.nan)
    df["cfo_terhadap_laba"] = np.where(df["netinc"] > 0, df["ncfo"] / df["netinc"], np.nan)
    df["akrual"] = df["netinc"] - df["ncfo"]
    rata_aset = (df["assets"] + df["assets_lalu"]) / 2
    df["rasio_akrual"] = np.where(rata_aset > 0, df["akrual"] / rata_aset, np.nan)
    df["capex_terhadap_penyusutan"] = np.where(
        df["totalDepAmorCF"].abs() > 0, -df["capex"] / df["totalDepAmorCF"].abs(), np.nan)
    df["rasio_pembayaran_dividen"] = np.where(
        df["netinc"] > 0, -df["commonDividendCF"].fillna(0) / df["netinc"], np.nan)
    df["pola_arus_kas"] = [pola_dickinson(a, b, c) for a, b, c in zip(df["ncfo"], df["ncfi"], df["ncff"])]

    # ----- Pertemuan 4: perubahan ekuitas & artikulasi -----
    df["laba_tahun_berjalan"] = df["netinc"] - df["minorityInterest"].fillna(0)   # termasuk bagian NCI
    df["dividen_kas"] = df["commonDividendCF"].fillna(0)
    df["penerbitan_saham"] = df["commonIssued"].fillna(0)
    df["pembelian_kembali"] = df["commonRepurchased"].fillna(0)
    df["perubahan_ekuitas"] = df["equity"] - df["equity_lalu"]
    df["ekuitas_lainnya"] = (df["perubahan_ekuitas"] - df["laba_tahun_berjalan"] - df["dividen_kas"]
                             - df["penerbitan_saham"] - df["pembelian_kembali"])
    df["selisih_kas"] = df["ncf"] - (df["cashneq"] - df["cashneq_lalu"])
    df["selisih_neraca"] = df["assets"] - (df["liabilities"] + df["equity"])
    df["selisih_saldo_laba"] = (df["retearn"] - df["retearn_lalu"]) - (df["netinc"] + df["dividen_kas"])
    return df


def pola_dickinson(cfo, cfi, cff):
    """Tahap siklus hidup menurut tanda arus kas (Dickinson, 2011)."""
    cfo, cfi, cff = _n(cfo), _n(cfi), _n(cff)
    if np.isnan(cfo) or np.isnan(cfi) or np.isnan(cff):
        return "Data tidak lengkap"
    s = ("+" if cfo >= 0 else "-") + ("+" if cfi >= 0 else "-") + ("+" if cff >= 0 else "-")
    return {
        "--+": "Perintisan", "+-+": "Pertumbuhan", "+--": "Kedewasaan",
        "---": "Penyesuaian", "+++": "Penyesuaian", "++-": "Penyesuaian",
        "-++": "Penurunan", "-+-": "Penurunan",
    }[s]


POLA_URUT = ["Perintisan", "Pertumbuhan", "Kedewasaan", "Penyesuaian", "Penurunan", "Data tidak lengkap"]
POLA_ARTI = {
    "Perintisan": "Arus kas operasi negatif, investasi besar, dibiayai pendanaan baru (CFO -, CFI -, CFF +).",
    "Pertumbuhan": "Operasi sudah menghasilkan kas, tetap ekspansi, masih menambah pendanaan (+, -, +).",
    "Kedewasaan": "Operasi menghasilkan kas yang cukup untuk investasi sekaligus membayar utang/dividen (+, -, -).",
    "Penyesuaian": "Pola campuran (---, +++, ++-): perusahaan sedang menata ulang bisnis atau asetnya.",
    "Penurunan": "Operasi negatif dan menutupnya dengan menjual aset (CFO -, CFI +).",
}


# ============================================================ tabel per emiten
def laba_rugi_bertingkat(r):
    """Baris laba rugi bertingkat: (pos, nilai, % pendapatan, jenis)."""
    rev = _n(r["revenue"])
    pos_tb = _nol(r["pos_tidak_berulang"])
    baris = [
        ("Pendapatan", r["revenue"], "utama"),
        ("Beban pokok pendapatan", -_nol(r["cor"]) if not np.isnan(_n(r["cor"])) else np.nan, "beban"),
        ("Laba kotor", r["gp"], "subtotal"),
        ("Beban penjualan, umum & administrasi", -_nol(r["sgna"]), "beban"),
        ("Beban usaha lainnya", -_nol(r["otheropex"]), "beban"),
        ("Laba usaha", r["opinc"], "subtotal"),
        ("Beban bunga", r["interestExpense"], "beban"),
        ("Pendapatan bunga", r["interestIncome"], "lain"),
        ("Bagian laba entitas asosiasi", r["incomeEquity"], "lain"),
        ("Laba/rugi selisih kurs", r["currencyGains"], "lain"),
        ("Pendapatan/beban lain-lain", r["otherNonOperating"], "lain"),
        ("Laba sebelum pajak dari kegiatan BERULANG", r["ebtExcl"], "subtotal"),
        ("Pos TIDAK BERULANG (jumlah)", pos_tb, "tidak_berulang"),
        ("Laba sebelum pajak", r["pretax"], "subtotal"),
        ("Beban pajak penghasilan", -_nol(r["taxexp"]), "beban"),
        ("Bagian kepentingan nonpengendali", r["minorityInterest"], "lain"),
        ("Laba bersih milik entitas induk", r["netinc"], "total"),
    ]
    out = []
    for nama, nilai, jenis in baris:
        v = _n(nilai)
        if np.isnan(v) and jenis in ("beban", "lain"):
            continue
        out.append({"Pos": nama, "Nilai": v, "% Pendapatan": _bagi(v, rev), "jenis": jenis})
    return pd.DataFrame(out)


def rincian_tidak_berulang(r):
    rows = [{"Pos tidak berulang": label, "Nilai": _n(r[k])}
            for k, label in POS_TIDAK_BERULANG.items() if not np.isnan(_n(r[k])) and _n(r[k]) != 0]
    return pd.DataFrame(rows)


def arus_kas_tidak_langsung(r):
    """Rekonsiliasi laba bersih ke arus kas operasi (metode tidak langsung)."""
    baris = [
        ("Laba bersih", r["netIncomeCF"]),
        ("(+) Penyusutan & amortisasi", r["totalDepAmorCF"]),
        ("(+/-) Penurunan nilai aset (nonkas)", r["assetWritedownCF"]),
        ("(+/-) Perubahan modal kerja", r["changeWorkingCapital"]),
        ("(+/-) Perubahan aset/liabilitas operasi lain", r["changeOtherNetOperAssets"]),
        ("(+/-) Penyesuaian nonkas lainnya", r["otheroperating"]),
        ("(+/-) Penyesuaian lain-lain", r["miscCashFlowAdjustments"]),
    ]
    out = [{"Pos": n, "Nilai": _n(v)} for n, v in baris if not np.isnan(_n(v))]
    jumlah = sum(x["Nilai"] for x in out)
    cfo = _n(r["ncfo"])
    if not np.isnan(cfo) and abs(cfo - jumlah) > max(1.0, 0.005 * abs(cfo)):
        out.append({"Pos": "(+/-) Pos rekonsiliasi lain (selisih)", "Nilai": cfo - jumlah})
    out.append({"Pos": "= Arus kas bersih dari aktivitas OPERASI", "Nilai": cfo})
    return pd.DataFrame(out)


def arus_kas_langsung_estimasi(r):
    """Estimasi metode langsung dari data laba rugi + perubahan neraca.
    Hanya ESTIMASI pendekatan konversi (buku teks); laporan resmi tetap acuan."""
    d_piutang = _n(r["accountsReceivable"]) - _n(r["accountsReceivable_lalu"])
    d_persediaan = _n(r["inventory"]) - _n(r["inventory_lalu"])
    d_utang = _n(r["accountsPayable"]) - _n(r["accountsPayable_lalu"])
    terima = _n(r["revenue"]) - _nol(d_piutang)
    bayar_pemasok = -(_nol(r["cor"]) + _nol(d_persediaan) - _nol(d_utang))
    bayar_beban = -(_nol(r["opex"]) - abs(_nol(r["totalDepAmorCF"])))
    bayar_bunga = _n(r["cashInterestPaid"])
    bayar_pajak = _n(r["cashTaxesPaid"])
    rows = [
        ("Penerimaan kas dari pelanggan", terima, "Pendapatan - kenaikan piutang usaha"),
        ("Pembayaran kas kepada pemasok", bayar_pemasok, "-(Beban pokok + kenaikan persediaan - kenaikan utang usaha)"),
        ("Pembayaran beban usaha (tunai)", bayar_beban, "-(Beban usaha - penyusutan & amortisasi)"),
        ("Pembayaran bunga", -abs(bayar_bunga) if not np.isnan(bayar_bunga) else np.nan, "dari pengungkapan arus kas"),
        ("Pembayaran pajak", -abs(bayar_pajak) if not np.isnan(bayar_pajak) else np.nan, "dari pengungkapan arus kas"),
    ]
    df = pd.DataFrame([{"Pos": a, "Nilai": b, "Cara hitung": c} for a, b, c in rows])
    est = df["Nilai"].sum(skipna=True)
    df = pd.concat([df, pd.DataFrame([
        {"Pos": "= Estimasi arus kas operasi (metode langsung)", "Nilai": est, "Cara hitung": "jumlah di atas"},
        {"Pos": "Arus kas operasi menurut laporan", "Nilai": _n(r["ncfo"]), "Cara hitung": "laporan arus kas"},
    ])], ignore_index=True)
    return df


def perubahan_ekuitas(r):
    rows = [
        ("Ekuitas awal tahun", r["equity_lalu"]),
        ("(+) Laba tahun berjalan (termasuk nonpengendali)", r["laba_tahun_berjalan"]),
        ("(-) Dividen kas dibayar", r["dividen_kas"]),
        ("(+) Penerbitan saham", r["penerbitan_saham"]),
        ("(-) Pembelian kembali saham", r["pembelian_kembali"]),
        ("(+/-) Penghasilan komprehensif lain & pos ekuitas lainnya*", r["ekuitas_lainnya"]),
        ("= Ekuitas akhir tahun", r["equity"]),
    ]
    return pd.DataFrame([{"Pos": a, "Nilai": _n(b)} for a, b in rows])


def artikulasi(r):
    """Hubungan keempat laporan pokok. Selisih kecil wajar karena pembulatan/reklasifikasi."""
    def status(selisih, acuan):
        s, a = _n(selisih), abs(_n(acuan)) if not np.isnan(_n(acuan)) else np.nan
        if np.isnan(s):
            return "Data tidak cukup"
        return "Cocok" if (np.isnan(a) and abs(s) < 1) or abs(s) <= 0.02 * max(a, 1) else "Ada selisih"
    return pd.DataFrame([
        {"Hubungan": "Laba bersih di Laba Rugi = titik awal Laporan Arus Kas",
         "Selisih": _n(r["netinc"]) - _n(r["netIncomeCF"]),
         "Status": status(_n(r["netinc"]) - _n(r["netIncomeCF"]), r["netinc"])},
        {"Hubungan": "Kenaikan kas di Laporan Arus Kas = perubahan kas di Posisi Keuangan",
         "Selisih": r["selisih_kas"], "Status": status(r["selisih_kas"], r["ncf"])},
        {"Hubungan": "Perubahan saldo laba = laba bersih - dividen (Perubahan Ekuitas)",
         "Selisih": r["selisih_saldo_laba"], "Status": status(r["selisih_saldo_laba"], r["netinc"])},
        {"Hubungan": "Aset = Liabilitas + Ekuitas (Posisi Keuangan)",
         "Selisih": r["selisih_neraca"], "Status": status(r["selisih_neraca"], r["assets"])},
    ])


# ============================================================ agregat sektor
def agregat_sektor(df, tahun, kolom, keluarkan_keuangan=False, min_n=3):
    """Median, kuartil, dan jumlah emiten per sektor untuk satu rasio."""
    d = df[(df["tahun"] == tahun) & df[kolom].notna()]
    if keluarkan_keuangan:
        d = d[d["sektor"] != "Keuangan"]
    lo, hi = d[kolom].quantile([0.02, 0.98]) if len(d) > 10 else (d[kolom].min(), d[kolom].max())
    d = d.assign(_v=d[kolom].clip(lo, hi))
    g = d.groupby("sektor")["_v"]
    out = pd.DataFrame({"Median": g.median(), "Kuartil 1": g.quantile(0.25),
                        "Kuartil 3": g.quantile(0.75), "Jumlah emiten": g.count()})
    out = out[out["Jumlah emiten"] >= min_n].sort_values("Median", ascending=False)
    return out.reset_index().rename(columns={"sektor": "Sektor"})


def sebaran_pola(df, tahun, keluarkan_keuangan=False):
    d = df[df["tahun"] == tahun]
    if keluarkan_keuangan:
        d = d[d["sektor"] != "Keuangan"]
    t = pd.crosstab(d["sektor"], d["pola_arus_kas"], normalize="index") * 100
    return t.reindex(columns=[p for p in POLA_URUT if p in t.columns])


def peringkat_dalam_sektor(df, tahun, sektor, kolom, kode):
    d = df[(df["tahun"] == tahun) & (df["sektor"] == sektor) & df[kolom].notna()]
    if kode not in set(d["kode"]):
        return None, len(d)
    urut = d.sort_values(kolom, ascending=False).reset_index(drop=True)
    return int(urut.index[urut["kode"] == kode][0]) + 1, len(d)
