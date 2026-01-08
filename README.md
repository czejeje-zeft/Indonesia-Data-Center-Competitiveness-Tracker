# 🇮🇩 Indonesia Data Center Competitiveness Tracker 2026

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://indonesia-data-center-competitiveness-tracker.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-green)
![Scikit-Learn](https://img.shields.io/badge/AI-KMeans%20Clustering-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

> **Sistem Intelijen Bisnis & Benchmarking Strategis:** Memetakan daya saing infrastruktur digital Indonesia dalam kancah global menggunakan **Machine Learning (Clustering)** dan Visualisasi Interaktif, dengan fokus pada SDG 9 (Infrastruktur) & SDG 13 (Climate Action).

---

## 📖 Latar Belakang Penelitian

Di tahun 2026, Indonesia telah mengukuhkan posisinya sebagai ekonomi digital terbesar di Asia Tenggara dengan **penetrasi internet mencapai >80%**. Namun, terdapat paradoks strategis:
*   **Demand Tinggi:** Aktivitas digital masif (e-commerce, fintech, AI adoption).
*   **Supply Terbatas:** Kapasitas infrastruktur fisik (*Data Center*) masih tertinggal dibandingkan hub regional seperti Singapura.
*   **Isu Lingkungan:** Tekanan global untuk mencapai *Net-Zero Emission* menuntut transisi dari energi fosil ke energi terbarukan.

**Dashboard ini dibangun untuk menjawab 3 pertanyaan krusial:**
1.  Seberapa besar kesenjangan kapasitas daya (*MW*) Indonesia dibanding kompetitor global?
2.  Di mana posisi Indonesia dalam matriks pasar (*Supply vs Demand*)?
3.  Bagaimana segmentasi negara menggunakan **AI Clustering** untuk memvalidasi posisi kompetitif Indonesia?

🔗 **Live Demo:** [Klik di sini untuk mengakses Dashboard](https://indonesia-data-center-competitiveness-tracker.streamlit.app/)

---

## 📂 Struktur Repository

Repository ini berisi source code aplikasi utama serta dokumentasi lengkap hasil bootcamp.

```text
├── 📂 Laporan Bootcamp/           # [DOKUMENTASI UTAMA]
│   ├── Laporan_Akhir_Kelompok2.pdf  # Naskah lengkap penelitian (Bab I-V) untuk HKI
│   └── Poster_Penelitian.html       # Desain Poster Infografis (HTML Responsive)
│
├── 📂 Project FDA sebelumnya/     # [ARSIP TUGAS]
│   └── (Kumpulan tugas Fundamental Data Analysis sebelum Final Project)
│
├── dashboard_dc.py                # [SOURCE CODE] Main Driver Aplikasi Streamlit
├── analyst.ipynb                  # Notebook Eksplorasi Data (EDA) & Prototyping ML
├── Book1 (1).csv                  # Dataset Global Data Center 2024-2026 (Processed)
├── requirements.txt               # Daftar library (Streamlit, Pandas, Sklearn)
└── README.md                      # Dokumentasi Proyek ini
```

---

## 📊 Fitur Unggulan Sistem

Aplikasi ini dikembangkan menggunakan pendekatan *Data Science* end-to-end:

### 1. AI-Powered Analysis (Machine Learning) 🤖
Menggunakan algoritma **K-Means Clustering** (Unsupervised Learning) untuk mengelompokkan negara secara otomatis ke dalam 4 segmen strategis berdasarkan kemiripan infrastruktur multidimensi:
*   *Top Tier (Global Hub)* - contoh: USA, China.
*   *Mature Market* - contoh: Singapura, Jerman.
*   *High Growth / Emerging* - **Posisi Indonesia teridentifikasi di sini.**
*   *Early Stage*

### 2. Advanced Data Cleaning Engine 🛠️
Sistem dilengkapi algoritma berbasis **Regex (Regular Expression)** untuk membersihkan data mentah yang tidak terstruktur:
*   **Numeric Parsing:** Mengekstrak angka valid dari teks kotor (contoh: mengubah `~12,000+ MW` menjadi integer `12000`).
*   **Tier Quality Extraction:** Mem-parsing deskripsi teks `tier_distribution` untuk menghitung skor ketahanan infrastruktur (*High-Availability Score*).
*   **Range Handling:** Mengkonversi rentang nilai (misal: `20-30`) menjadi nilai rata-rata skalar secara otomatis.

### 3. Visualisasi Analitik Multidimensi 📈
*   **Infrastructure Gap (Log Scale):** Grafik batang logaritmik untuk membandingkan kapasitas daya negara berkembang vs negara maju secara proporsional.
*   **Market Quadrant (Scatter Plot):** Memetakan posisi negara ke dalam 4 kuadran. Indonesia teridentifikasi di kuadran *"Opportunity Gap"* (High Demand, Low Supply).
*   **Competitive Radar:** Analisis *head-to-head* antara Indonesia vs Singapura dalam 5 parameter kunci (Growth, Power, Quality, Internet, Green Energy).
*   **Sustainability Meter:** Visualisasi *Lollipop Chart* untuk memeringkat negara berdasarkan adopsi energi terbarukan.

---

## 🛠️ Teknologi (Tech Stack)

| Komponen | Teknologi | Kegunaan |
| :--- | :--- | :--- |
| **Bahasa Utama** | Python 3.10+ | Logika backend dan pemrosesan algoritma |
| **Framework** | Streamlit | Membangun antarmuka web (UI) interaktif |
| **Machine Learning** | Scikit-Learn | Implementasi K-Means Clustering & Scaling |
| **Data Processing** | Pandas & NumPy | Manipulasi dataframe, cleaning, dan agregasi |
| **Visualisasi** | Plotly (Express & GO) | Membuat grafik interaktif (*zoom, pan, hover*) |
| **Pattern Matching** | Re (Regex) | Ekstraksi informasi dari data teks kompleks |

---

## 🚀 Panduan Instalasi (Lokal)

Untuk menjalankan dashboard ini di komputer Anda:

**1. Clone Repository**
```bash
git clone https://github.com/USERNAME_KAMU/NAMA_REPO.git
cd NAMA_REPO
```

**2. Siapkan Virtual Environment**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install Library**
```bash
pip install -r requirements.txt
```

**4. Jalankan Aplikasi**
```bash
streamlit run dashboard_dc.py
```

---

## 💡 Temuan Utama (Key Insights)

1.  **Defisit Kapasitas (Infrastructure Gap):**
    Meskipun jumlah gedung data center bersaing, total kapasitas daya (*MW*) Indonesia masih sangat kecil dibanding Singapura. Ini mengindikasikan dominasi fasilitas skala kecil/ritel, bukan *Hyperscale*.

2.  **Posisi Pasar (Market Opportunity):**
    Indonesia berada di posisi unik: **Penetrasi Internet Tinggi** namun **Infrastruktur Rendah**. Ini adalah sinyal kuat bagi investor bahwa pasar Indonesia sangat *underserved* (membutuhkan investasi besar).

3.  **Tantangan Hijau (Green Lag):**
    Adopsi energi terbarukan Indonesia masih berkisar di angka **~20%**, tertinggal jauh dari standar global (>50%). Ini menjadi tantangan utama dalam menarik investor *Big Tech* yang memiliki target *Net-Zero*.

---

## 👥 Tim Peneliti - Kelompok 2

Proyek ini disusun sebagai Laporan Akhir Bootcamp Data Science 2026.

1.  **Jaenal Arifin** (19240216)
2.  **Erwin Gouw** (19240336)
3.  **Afriza** (19240293)
4.  **Belinda** (19240846)
5.  **Rianti** (19240211)
6.  **Amelia Ulya Nashifa** (19240192)
7.  **Alexhandra Dea Alfani** (19241661)

---

## 📜 Lisensi & Atribusi

*   **Hak Cipta:** © 2026 Kelompok 2.
*   **Sumber Data:** Dikompilasi dari Laporan Industri Global (Uptime Institute, IEA, Google e-Conomy SEA).

---
*Dibuat dengan ❤️ menggunakan Python, Streamlit & Scikit-Learn*
```
