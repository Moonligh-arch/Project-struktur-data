# 🏢 Simulasi Lift Terjadwal (Elevator SCAN Algorithm)

Proyek ini adalah simulasi sistem pergerakan lift (elevator) berbasis Terminal/CLI yang mengimplementasikan **Priority Queue** melalui **Algoritma SCAN**. Proyek ini dibuat untuk mengeksplorasi penggunaan struktur data dalam dunia nyata (Tugas Struktur Data).

## 🚀 Versi Proyek (Evolusi Algoritma)

Proyek ini dibangun secara bertahap dari yang paling sederhana hingga efisien:

*   **V1**: Menggunakan struktur data *Circular Queue* biasa (FIFO). Lift bergerak secara naif mengikuti urutan antrean pertama yang masuk.
*   **V2**: Menggunakan *Priority Queue* murni (modul `heapq`). Lift bergerak mencari target dengan skor prioritas jarak terdekat dan searah.
*   **V3 & V4**: Implementasi optimal dari **Algoritma SCAN (Elevator Algorithm)**. Lift akan terus meluncur ke satu arah (naik atau turun) untuk menyapu seluruh penumpang yang searah di jalurnya hingga mentok.
    *   *Catatan: V4 adalah versi final penyempurnaan V3 dengan perbaikan bug logika, penyesuaian gaya kodingan standar Python (PEP-8 clean), dan perbaikan class shadowing.*

## 🛠️ Fitur Utama (V4)

*   **Input Interaktif**: Mampu menambahkan penumpang manual dengan lantai asal (1-8) dan lantai tujuan.
*   **Simulasi Perjalanan**: Visualisasi log pergerakan lift saat menjemput, membuka pintu, dan mengantar penumpang (Kapasitas maksimal: 7 Orang).
*   **Monitor Status**: Menu untuk melihat isi orang di dalam lift serta daftar antrean lengkap dari setiap lantai.
*   **Skenario Demo (*Stress Test*)**: Tersedia menu khusus untuk mendemonstrasikan efisiensi algoritma saat kondisi lift ramai.

## 💻 Cara Menjalankan

Pastikan Anda telah menginstal **Python 3**. Buka terminal, masuk ke direktori proyek, dan jalankan perintah:

```bash
python3 project_V4.py
```
Lalu ikuti instruksi menu yang tampil di layar terminal.

## 🏗️ Penjelasan Struktur Data (V4)

Alih-alih menggunakan array statis, V4 menggunakan struktur data yang dinamis berupa **Dictionary bersarang (Nested Dictionary)** yang dipetakan berdasarkan index Lantai dan Arah (`Naik` atau `Turun`). Secara logis dan teknis waktu eksekusinya, metode penyapuan ini mengimplementasikan konsep *Priority Queue* yang bekerja jauh lebih efisien untuk sistem lift sungguhan.
