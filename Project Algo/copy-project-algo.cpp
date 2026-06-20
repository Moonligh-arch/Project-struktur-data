#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream> // Buat parsing CSV nanti

using namespace std;

// 1. Setup Struct sesuai PRD
struct Barang {
    string ID_Barang;
    string Nama_Barang;
    int Harga_Barang;
};

// 2. Gunakan std::vector sebagai penyimpan data dinamis
vector<Barang> inventaris;
string namaFile = "inventaris.csv";

// --- DEKLARASI FUNGSI ---

// Fungsi MVP Tahap 1: File I/O
void bacaDataCSV() {
    // TODO: Bikin logika baca file inventaris.csv dan masukin ke vector
}

void simpanDataCSV() {
    // TODO: Bikin logika simpan data dari vector ke inventaris.csv
}

// Fungsi MVP Tahap 1 & 2: Searching dan Sorting
void cariBarangBinarySearch() {
    // TODO: Logika Binary Search berdasarkan ID_Barang
}

void tambahBarangDenganInsertionSort() {
    // TODO: Input data barang baru (ID, Nama, Harga)
    // TODO: Langsung terapkan Insertion Sort tiap kali data masuk biar selalu terurut
}

void tampilkanInventaris() {
    if (inventaris.empty()) {
        cout << "Inventaris kosong, bre!" << endl;
        return;
    }
    cout << "\n=== DAFTAR BARANG TOKO JALLALUDIN ===" << endl;
    for (const auto& item : inventaris) {
        cout << "ID: " << item.ID_Barang 
             << " | Nama: " << item.Nama_Barang 
             << " | Harga: Rp" << item.Harga_Barang << endl;
    }
}

// --- MAIN MENU ---
int main() {
    // Load data pas program baru jalan
    bacaDataCSV();
    
    int pilihan;
    bool lanjut = true;
    
    while (lanjut) {
        cout << "\n==== SISTEM INVENTARIS TOKO JALLALUDIN ====" << endl;
        cout << "1. Tambah Barang Masuk" << endl;
        cout << "2. Lihat Semua Inventaris" << endl;
        cout << "3. Cari Barang (ID)" << endl;
        cout << "4. Keluar" << endl;
        cout << "Pilih menu (1-4): ";
        cin >> pilihan;
        cin.ignore(); // Bersihin buffer
        
        if (pilihan == 1) {
            tambahBarangDenganInsertionSort();
        } else if (pilihan == 2) {
            tampilkanInventaris();
        } else if (pilihan == 3) {
            cariBarangBinarySearch();
        } else if (pilihan == 4) {
            simpanDataCSV();
            cout << "Data disimpan. Cabut dulu, bre!" << endl;
            lanjut = false;
        } else {
            cout << "Pilihan kaga bener, coba lagi dah." << endl;
        }
    }
    return 0;
}