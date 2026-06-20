#include <iostream>
#include <fstream>
#include <string>
using namespace std;

// buat globalisasinya
string datakaryawan[100][4];
int jumlahkaryawan = 0;


// FUNGSI - HARUS DI LUAR MAIN
void bacadatakaryawan() {
    ifstream file("datakaryawan.txt");
    jumlahkaryawan = 0;
    
    while (file >> datakaryawan[jumlahkaryawan][0] 
                >> datakaryawan[jumlahkaryawan][1] 
                >> datakaryawan[jumlahkaryawan][2] 
                >> datakaryawan[jumlahkaryawan][3]) {
        jumlahkaryawan++;
        if (jumlahkaryawan >= 100) break;
    }
    file.close();
}


// fungsi buat nampilin data karyawan
void menampilkandatakaryawan() {
    if (jumlahkaryawan == 0) {
        cout << "belum ada data karyawan." << endl;
        return;
    }
    cout << "data karyawan :" << endl;
    for (int i = 0; i < jumlahkaryawan; i++) {
        cout << i+1 << ". " << datakaryawan[i][0] << " , "
             << datakaryawan[i][1] << " , "
             << datakaryawan[i][2] << " , "
             << datakaryawan[i][3] << endl;
    }
}


// fungsi buat simpan datanya ke file
void menyimpandatakefile(){
    ofstream file("datakaryawan.txt");
    for (int i = 0; i < jumlahkaryawan; i++) {
        file << datakaryawan[i][0] << " "
             << datakaryawan[i][1] << " " 
             << datakaryawan[i][2] << " "
             << datakaryawan[i][3] << endl;
    }
}


// fungsi buat nambah data karyawan
void tambahdatakaryawan() {
    if (jumlahkaryawan >= 100) {
        cout << "Data sudah penuh!" << endl;
        return;
    }
    cout << "\n=== TAMBAH DATA KARYAWAN ===" << endl;

    cout << "NIK: ";
    cin >> datakaryawan[jumlahkaryawan][0];
    for (int i = 0; i < jumlahkaryawan; i++) {
        if (datakaryawan[i][0] == datakaryawan[jumlahkaryawan][0]) {
            cout << "Error: NIK sudah ada!" << endl;
            return;
        }
    }
    cout << "Nama: ";
    cin.ignore(); 
    getline(cin, datakaryawan[jumlahkaryawan][1]);
    cout << "Departemen: ";
    getline(cin, datakaryawan[jumlahkaryawan][2]);
    cout << "Jabatan: ";
    getline(cin, datakaryawan[jumlahkaryawan][3]);
    jumlahkaryawan++;
    menyimpandatakefile();
    cout << "Data berhasil ditambahkan!" << endl;
}


// fungsi buat ubah data karyawan
void mengubahdatakaryawan(){
    if (jumlahkaryawan == 0){
        cout << "data karyawannya gak ada!!" << endl;
        return;
    }
    menampilkandatakaryawan();
    int pilihan;
    cout << "\n pilih nomor mana yang ingin di ubah datanya: ";
    cin >> pilihan;
    if (pilihan < 1 || pilihan > jumlahkaryawan) {
        cout << "Nomor tidak valid!" << endl;
        return;
    }
     int index = pilihan - 1;
     cout << "\n=== MENGUBAH DATA KARYAWAN ===" << endl;
    cin.ignore();
    
    cout << "NIK baru: ";
    getline(cin, datakaryawan[index][0]);

    cout << "Nama baru: ";
    getline(cin, datakaryawan[index][1]);
    
    cout << "Departemen baru: ";
    getline(cin, datakaryawan[index][2]);
    
    cout << "Jabatan baru: ";
    getline(cin, datakaryawan[index][3]);

    menyimpandatakefile();
    cout << "Datanya berhasil diubah!" << endl;
}


// fungsi buat hapus karyawan
void hapusdatakaryawan() {
if (jumlahkaryawan == 0) {
        cout << "data karyawannya gak ada!!" << endl;
        return;
    }
    menampilkandatakaryawan();
    int pilihan;
    cout << "\n pilih nomor data yang ingin dihapus: ";
    cin >> pilihan;
    
    if (pilihan < 1 || pilihan > jumlahkaryawan) {
        cout << "Nomor tidak valid!" << endl;
        return;
    }
    
    int index = pilihan - 1;
    string namadihapus = datakaryawan[index][1];
    
    for (int i = index; i < jumlahkaryawan - 1; i++) {
        datakaryawan[i][0] = datakaryawan[i+1][0];
        datakaryawan[i][1] = datakaryawan[i+1][1];
        datakaryawan[i][2] = datakaryawan[i+1][2];
        datakaryawan[i][3] = datakaryawan[i+1][3];
    }
    jumlahkaryawan--;
    menyimpandatakefile();
    cout << "Data " << namadihapus << " berhasil dihapus!" << endl;
}



 // Pertama-pertama buat menunya dulu
int main() {
    int pilihan;
    bool lanjut = true;
    
    bacadatakaryawan();

    while (lanjut) {
        cout << "==== SISTEM MANAJEMEN KARYAWAN ====" << endl;
        cout << "1. menambah data karyawan" << endl;
        cout << "2. melihat semua data karyawan" << endl;
        cout << "3. mengubah data karyawan" << endl;
        cout << "4. menghapus data karyawan" << endl;
        cout << "5. keluar dari program" << endl;
        cout << " masukan pilihan anda ; ";
        cin >> pilihan;

        if (pilihan == 1) {
           tambahdatakaryawan() ;
        } else if (pilihan == 2) {
            menampilkandatakaryawan() ;  
        } else if (pilihan == 3) {
            mengubahdatakaryawan() ;
        } else if (pilihan == 4) {
            hapusdatakaryawan() ;
        } else if (pilihan == 5) {
            menyimpandatakefile() ; 
            cout << "keluar dari program" << endl;
            lanjut = false;
        } else {
            cout << "maaf pilihan anda salah, mohon dicoba lagi" << endl;
        }
    }
    return 0;
}