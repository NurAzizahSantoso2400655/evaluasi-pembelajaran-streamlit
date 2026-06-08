# Aplikasi Analisis Butir Soal (Evaluasi Pembelajaran)

Aplikasi berbasis web interaktif ini dibangun menggunakan Python dan Streamlit untuk melakukan perhitungan dan analisis otomatis terhadap instrumen tes (butir soal pilihan ganda). 

Proyek ini dikembangkan sebagai implementasi komprehensif untuk pemenuhan tugas mata kuliah Evaluasi Pembelajaran di program studi Pendidikan Ilmu Komputer, Universitas Pendidikan Indonesia.

## Fitur Utama

Aplikasi ini dapat memproses data skor siswa (1 untuk benar, 0 untuk salah) dan secara otomatis melakukan empat analisis utama dalam evaluasi pembelajaran:

1. **Uji Validitas:** Menghitung Korelasi Point Biserial (r-hitung) untuk mengetahui kevalidan setiap butir soal dibandingkan dengan r-tabel.
2. **Tingkat Kesukaran (P):** Menghitung proporsi jawaban benar untuk mengategorikan soal menjadi Mudah, Sedang, atau Sukar.
3. **Daya Pembeda (D):** Membagi siswa ke dalam kelompok atas dan kelompok bawah untuk melihat kemampuan soal dalam membedakan tingkat pemahaman siswa.
4. **Uji Reliabilitas (KR-20 / Alpha Cronbach):** Menghitung varians setiap butir soal dan varians total untuk menentukan tingkat konsistensi atau keandalan instrumen tes.
5. **Visualisasi Data:** Dilengkapi dengan grafik batang (bar chart), diagram lingkaran (pie chart), dan gauge chart untuk mempermudah interpretasi data secara visual.

## Teknologi yang Digunakan

- Python 3.x
- Streamlit (Web Framework)
- Pandas (Manipulasi Data)
- NumPy (Perhitungan Array dan Matematika)
- SciPy (Perhitungan Statistik)
- Matplotlib (Visualisasi Grafik)

## Cara Menjalankan Aplikasi Secara Lokal

Jika Anda ingin menjalankan aplikasi ini di komputer Anda sendiri, ikuti langkah-langkah berikut:

1. **Clone repository ini**
   ```bash
   git clone [https://github.com/USERNAME-GITHUB-KAMU/NAMA-REPOSITORY-KAMU.git](https://github.com/USERNAME-GITHUB-KAMU/NAMA-REPOSITORY-KAMU.git)
   cd NAMA-REPOSITORY-KAMU

```

2. **Install library yang dibutuhkan**
Pastikan Anda sudah menginstal Python. Sangat disarankan menggunakan virtual environment.
```bash
pip install -r requirements.txt

```


3. **Jalankan aplikasi Streamlit**
```bash
streamlit run analisis_butir_soal.py

```


4. **Buka di Browser**
Aplikasi akan otomatis terbuka di browser Anda melalui alamat http://localhost:8501.

## Catatan Penggunaan

* Data mentah (dataset) siswa dan kunci jawaban saat ini terpasang secara hardcoded di dalam source code untuk tujuan kemudahan demonstrasi dan pencetakan hasil laporan.
* Anda dapat mengubah array `kunci` dan `jawaban_raw` di dalam file `analisis_butir_soal.py` untuk menguji dataset yang berbeda.

---

*Dibuat untuk keperluan penyusunan analisis instrumen tes yang berkualitas dan akurat.*

```

```
