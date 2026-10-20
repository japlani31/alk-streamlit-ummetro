# -*- coding: utf-8 -*-
"""
Menyiapkan data kerja aplikasi Analisa Laporan Keuangan (sekali jalan).

Sumber:
  1. G:\\Drive Saya\\DATA_LAPORAN_KEUANGAN\\negara_idx.csv
     (laporan keuangan emiten BEI, satuan rupiah penuh)
  2. data\\sektor_raw.csv (klasifikasi IDX-IC dari berkas
     "Rekap Laporan Keuangan Vers. 1.9 - Q4 2024.xlsb")

Hasil: data\\alk_data.csv.gz  (laporan TAHUNAN Q4, 2021-2025, kolom terpilih + sektor)

Jalankan:  python siapkan_data.py [path_negara_idx.csv]
"""
import os
import sys

import pandas as pd

SUMBER = sys.argv[1] if len(sys.argv) > 1 else r"G:\Drive Saya\DATA_LAPORAN_KEUANGAN\negara_idx.csv"
DIR = os.path.dirname(os.path.abspath(__file__))

SEKTOR_ID = {
    "Energy": "Energi",
    "Basic Materials": "Barang Baku",
    "Industrials": "Perindustrian",
    "Consumer Non-Cyclicals": "Barang Konsumen Primer",
    "Consumer Cyclicals": "Barang Konsumen Non-Primer",
    "Healthcare": "Kesehatan",
    "Financials": "Keuangan",
    "Properties & Real Estate": "Properti & Real Estat",
    "Technology": "Teknologi",
    "Infrastructures": "Infrastruktur",
    "Transportation & Logistic": "Transportasi & Logistik",
}

KOLOM = [
    # laba rugi
    "revenue", "cor", "gp", "sgna", "otheropex", "opex", "opinc",
    "interestExpense", "interestIncome", "incomeEquity", "currencyGains", "otherNonOperating",
    "ebtExcl", "gainAssets", "gainInvestments", "assetWritedown", "otherUnusualItems",
    "impairmentGoodwill", "mergerRestructureCharges", "legalSettlements",
    "pretax", "taxexp", "minorityInterest", "netinc", "earningsDiscontinued",
    "ebitda", "depAmorEbitda",
    # posisi keuangan
    "cashneq", "accountsReceivable", "inventory", "assetsc", "assets",
    "accountsPayable", "currentLiabilities", "liabilities",
    "commonStock", "additionalPaidInCapital", "retearn", "treasuryStock", "otherEquity",
    "totalCommonEquity", "minorityInterestBS", "equity",
    # arus kas
    "netIncomeCF", "totalDepAmorCF", "changeWorkingCapital", "otheroperating",
    "assetWritedownCF", "changeOtherNetOperAssets", "miscCashFlowAdjustments", "ncfo",
    "capex", "ncfi", "commonDividendCF", "commonIssued", "commonRepurchased",
    "netDebtIssued", "ncff", "exchangeRateAdjustments", "ncf",
    "cashInterestPaid", "cashTaxesPaid",
]


def main():
    df = pd.read_csv(SUMBER, low_memory=False)
    df = df[(df["fiscalQuarter"] == "Q4") & (df["datekey"] != "TTM")].copy()
    df["kode"] = df["symbol"].str.split("/").str[-1].str.upper()
    df = df.rename(columns={"fiscalYear": "tahun", "name": "nama"})
    df = df[(df["tahun"] >= 2020) & (df["tahun"] <= 2025)]
    df = df.drop_duplicates(["kode", "tahun"], keep="first")

    sek = pd.read_csv(os.path.join(DIR, "data", "sektor_raw.csv"))
    sek["sektor"] = sek["sector"].map(SEKTOR_ID)
    sek = sek.rename(columns={"sub_sector": "subsektor"})[["kode", "sektor", "subsektor"]]
    df = df.merge(sek, on="kode", how="left")
    df["sektor"] = df["sektor"].fillna("Belum terklasifikasi")
    df["subsektor"] = df["subsektor"].fillna("-")

    keluar = df[["kode", "nama", "sektor", "subsektor", "tahun"] + KOLOM].sort_values(["kode", "tahun"])
    path = os.path.join(DIR, "data", "alk_data.csv.gz")
    keluar.to_csv(path, index=False, compression="gzip")
    print(f"Tersimpan {path}: {len(keluar)} baris, {keluar.kode.nunique()} emiten")
    print(keluar.groupby("sektor").kode.nunique().sort_values(ascending=False).to_string())


if __name__ == "__main__":
    main()
