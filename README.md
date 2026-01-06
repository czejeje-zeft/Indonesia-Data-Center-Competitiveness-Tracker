# 🇮🇩 Indonesia Data Center Competitiveness Tracker 2026

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://indonesia-data-center-competitiveness-tracker.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-green)
![License](https://img.shields.io/badge/License-Academic-orange)

> **Sistem Intelijen Bisnis & Benchmarking Strategis:** Memetakan daya saing infrastruktur digital Indonesia dalam kancah global, berfokus pada Kapasitas, Ketahanan, dan Transisi Energi Hijau (SDG 9 & 13).

---

## 📖 Latar Belakang Penelitian

Di tahun 2026, Indonesia telah mengukuhkan posisinya sebagai ekonomi digital terbesar di Asia Tenggara dengan **penetrasi internet mencapai >80%**. Namun, terdapat paradoks strategis:
*   **Demand Tinggi:** Aktivitas digital masif (e-commerce, fintech, AI adoption).
*   **Supply Terbatas:** Kapasitas infrastruktur fisik (*Data Center*) masih tertinggal dibandingkan hub regional seperti Singapura.
*   **Isu Lingkungan:** Tekanan global untuk mencapai *Net-Zero Emission* menuntut transisi dari energi fosil ke energi terbarukan.

**Dashboard ini dibangun untuk menjawab 3 pertanyaan krusial:**
1.  Seberapa besar kesenjangan kapasitas daya (*MW*) Indonesia dibanding kompetitor global?
2.  Di mana posisi Indonesia dalam matriks pasar (*Supply vs Demand*)?
3.  Seberapa siap Indonesia menghadapi standar *Green Data Center* (SDG 13)?

🔗 **Live Demo:** [Klik di sini untuk mengakses Dashboard](https://indonesia-data-center-competitiveness-tracker.streamlit.app/)

---

## 📊 Fitur Unggulan Sistem

Aplikasi ini dikembangkan menggunakan pendekatan *Data Science* end-to-end:

### 1. Advanced Data Cleaning Engine 🛠️
Menggunakan algoritma berbasis **Regex (Regular Expression)** untuk memproses data mentah yang tidak terstruktur:
*   **Numeric Parsing:** Mengekstrak angka valid dari teks kotor (contoh: `~12,000+ MW` $\rightarrow$ `12000`).
*   **Tier Quality Extraction:** Mem-parsing deskripsi teks `tier_distribution` untuk menghitung skor ketahanan infrastruktur (*High-Availability Score*).
*   **Range Handling:** Mengkonversi rentang nilai (misal: `20-30`) menjadi nilai rata-rata skalar.

### 2. Visualisasi Analitik Multidimensi 📈
*   **Infrastructure Gap (Log Scale):** Grafik batang logaritmik untuk membandingkan kapasitas daya negara berkembang vs negara maju secara proporsional.
*   **Market Quadrant (Scatter Plot):** Memetakan posisi negara ke dalam 4 kuadran. Indonesia teridentifikasi di kuadran *"Opportunity Gap"* (High Demand, Low Supply).
*   **Competitive Radar:** Analisis *head-to-head* antara Indonesia vs Singapura dalam 5 parameter kunci (Growth, Power, Quality, Internet, Green Energy).
*   **Sustainability Meter:** Visualisasi *Lollipop Chart* untuk memeringkat adopsi energi terbarukan.

---

## 🛠️ Teknologi (Tech Stack)

| Komponen | Teknologi | Kegunaan |
| :--- | :--- | :--- |
| **Bahasa Utama** | Python 3.10+ | Logika backend dan pemrosesan algoritma |
| **Framework** | Streamlit | Membangun antarmuka web (UI) interaktif |
| **Data Processing** | Pandas & NumPy | Manipulasi dataframe, cleaning, dan agregasi |
| **Visualisasi** | Plotly (Express & GO) | Membuat grafik interaktif (*zoom, pan, hover*) |
| **Pattern Matching** | Re (Regex) | Ekstraksi informasi dari data teks kompleks |

---

## 📂 Struktur Repository

```text
├── dashboard_dc.py      # Source code utama aplikasi (Main Driver)
├── Book1 (1).csv        # Dataset sekunder (Global Data Center 2024-2026)
├── requirements.txt     # Daftar dependensi library untuk deployment
└── README.md            # Dokumentasi lengkap proyek
