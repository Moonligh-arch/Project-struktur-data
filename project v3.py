import time
import os

# ── konstanta gedung ─────────────────────────────────────────
lantai_min = 1
lantai_max = 8
kapasitas_max = 7



class Penumpang:
    def __init__(self, nama, asal, tujuan):
        self.nama = nama
        self.asal = asal
        self.tujuan = tujuan




class Lift:
    def __init__(self):
        self.lantai_sekarang = 1  # Mulai dari lantai 8 sesuai skenario pembuktian
        self.arah = "idle"        # naik, turun, atau idle
        self.penumpang_dalam = []
        
        # Menampung panggilan dari luar koridor gedung
        # Format: { lantai: {"naik": [list_penumpang], "turun": [list_penumpang]} }
        self.panggilan_luar = {i: {"naik": [], "turun": []} for i in range(lantai_min, lantai_max + 1)}

    def tambah_panggilan(self, penumpang):
        arah_req = "naik" if penumpang.tujuan > penumpang.asal else "turun"
        self.panggilan_luar[penumpang.asal][arah_req].append(penumpang)

    def ada_tugas(self):
        """Mengecek apakah masih ada penumpang di dalam lift atau antrean di luar."""
        if self.penumpang_dalam:
            return True
        for lantai in self.panggilan_luar:
            if self.panggilan_luar[lantai]["naik"] or self.panggilan_luar[lantai]["turun"]:
                return True
        return False

    def tentukan_arah_awal(self):
        """Menentukan arah gerak pertama kali ketika lift dalam kondisi idle."""
        panggilan_floors = []
        for lantai in self.panggilan_luar:
            if self.panggilan_luar[lantai]["naik"] or self.panggilan_luar[lantai]["turun"]:
                panggilan_floors.append(lantai)
        
        if not panggilan_floors:
            self.arah = "idle"
            return

        # Jika ada panggilan tepat di lantai lift sekarang berada
        if self.lantai_sekarang in panggilan_floors:
            if self.panggilan_luar[self.lantai_sekarang]["naik"]:
                self.arah = "naik"
            elif self.panggilan_luar[self.lantai_sekarang]["turun"]:
                self.arah = "turun"
            return

        # Ambil lantai panggilan terdekat untuk menentukan rute awal lift meluncur
        terdekat = min(panggilan_floors, key=lambda x: abs(x - self.lantai_sekarang))
        if terdekat > self.lantai_sekarang:
            self.arah = "naik"
        else:
            self.arah = "turun"


    def periksa_perubahan_arah(self):
        """
        Inti dari scan Algorithm: Memeriksa apakah tugas di arah saat ini sudah habis.
        Jika habis, lift baru diizinkan berbalik arah atau berubah menjadi idle.
        """
        if self.arah == "naik":
            ada_tugas_di_atas = False

            # Cek apakah ada penumpang di dalam yang mau turun di lantai atasnya lagi
            if any(p.tujuan > self.lantai_sekarang for p in self.penumpang_dalam):
                ada_tugas_di_atas = True

            # Cek apakah ada antrean di luar pada lantai-lantai di atasnya
            for f in range(self.lantai_sekarang + 1, lantai_max + 1):
                if self.panggilan_luar[f]["naik"] or self.panggilan_luar[f]["turun"]:
                    ada_tugas_di_atas = True
            
            # Jika di atas benar-benar bersih, cek apakah ada sisa tugas di bawah
            if not ada_tugas_di_atas:
                ada_tugas_di_bawah_atau_sini = False
                if self.panggilan_luar[self.lantai_sekarang]["turun"]:
                    ada_tugas_di_bawah_atau_sini = True
                for f in range(lantai_min, self.lantai_sekarang):
                    if self.panggilan_luar[f]["naik"] or self.panggilan_luar[f]["turun"]:
                        ada_tugas_di_bawah_atau_sini = True
                
                self.arah = "turun" if ada_tugas_di_bawah_atau_sini else "idle"

        elif self.arah == "turun":
            ada_tugas_di_bawah = False

            # Cek penumpang dalam lift yang tujuannya ada di bawah lantai sekarang
            if any(p.tujuan < self.lantai_sekarang for p in self.penumpang_dalam):
                ada_tugas_di_bawah = True

            # Cek antrean luar di lantai-lantai bawahnya
            for f in range(lantai_min, self.lantai_sekarang):
                if self.panggilan_luar[f]["naik"] or self.panggilan_luar[f]["turun"]:
                    ada_tugas_di_bawah = True
            
            # Jika di bawah bersih, cek apakah ada sisa tugas di atas
            if not ada_tugas_di_bawah:
                ada_tugas_di_atas_atau_sini = False
                if self.panggilan_luar[self.lantai_sekarang]["naik"]:
                    ada_tugas_di_atas_atau_sini = True
                for f in range(self.lantai_sekarang + 1, lantai_max + 1):
                    if self.panggilan_luar[f]["naik"] or self.panggilan_luar[f]["turun"]:
                        ada_tugas_di_atas_atau_sini = True
                
                self.arah = "naik" if ada_tugas_di_atas_atau_sini else "idle"

    def jalankan_simulasi(self):
        print("\n=================== simulasi lift dimulai ===================")
        if not self.ada_tugas():
            print("Tidak ada antrean penumpang di dalam sistem.")
            return

        while self.ada_tugas():
            if self.arah == "idle":
                self.tentukan_arah_awal()

            # Validasi arah tepat sebelum memproses lantai (antisipasi batas mentok lantai)
            self.periksa_perubahan_arah()

            pintu_terbuka = False
            penumpang_keluar = []
            penumpang_masuk = []

            # 1. proses penumpang keluar
            sisa_penumpang = []
            for p in self.penumpang_dalam:
                if p.tujuan == self.lantai_sekarang:
                    penumpang_keluar.append(p)
                    pintu_terbuka = True
                else:
                    sisa_penumpang.append(p)
            self.penumpang_dalam = sisa_penumpang

            # 2. proses penumpang masuk (batching / satu sesi pickup)
            if self.arah != "idle":
                antrean_di_lantai = self.panggilan_luar[self.lantai_sekarang][self.arah]
                if antrean_di_lantai:
                    pintu_terbuka = True
                    
                    # Angkut semua orang di antrean lantai ini ke dalam satu sesi sampai penuh
                    while antrean_di_lantai and len(self.penumpang_dalam) < kapasitas_max:
                        p = antrean_di_lantai.pop(0)
                        self.penumpang_dalam.append(p)
                        penumpang_masuk.append(p)
                    
                    # Jika lift penuh tapi di luar masih tersisa orang
                    if antrean_di_lantai and len(self.penumpang_dalam) == kapasitas_max:
                        print(f"     Lift penuh! Sisa penumpang di Lantai {self.lantai_sekarang} harus antre di sesi berikutnya.")

            # Tampilkan Visualisasi Log per Lantai
            print(f"\n ─── [ Lantai {self.lantai_sekarang} ] ────────────────────────────────────────")
            print(f"  Status Arah  : {self.arah}")
            print(f"  Kapasitas    : {len(self.penumpang_dalam)}/{kapasitas_max} Orang")
            
            if pintu_terbuka:
                print("Pintu Terbuka...")
                if penumpang_keluar:
                    print("       Keluar: " + ", ".join([f"{p.nama} (Selesai)" for p in penumpang_keluar]))
                if penumpang_masuk:
                    print("       Masuk (Satu Sesi): " + ", ".join([f"{p.nama} (Tujuan Lnt {p.tujuan})" for p in penumpang_masuk]))
                print("Pintu Tertutup.")
                time.sleep(1)
            else:
                print("  ... Lift melewati lantai ini (Tidak ada aksi) ...")
                time.sleep(0.5)

            # Periksa rute lagi setelah aktivitas bongkar-muat selesai
            self.periksa_perubahan_arah()

            # Pergerakan mekanis motor lift ke lantai berikutnya
            if self.arah == "naik" and self.lantai_sekarang < lantai_max:
                self.lantai_sekarang += 1
            elif self.arah == "turun" and self.lantai_sekarang > lantai_min:
                self.lantai_sekarang -= 1
            elif self.arah == "idle":
                break

        print("\n=================== simulasi selesai ===================")
        print(f"Lift berhenti total di Lantai {self.lantai_sekarang} dengan status idle.\n")





# ── menu interaktif cli ───────────────────────────────────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    lift = Lift()
    
    while True:
        print("====== simulasi lift priority queue (scan) ======")
        print(f" Posisi Lift Saat Ini: Lantai {lift.lantai_sekarang} ({lift.arah})")
        print("=================================================")
        print(" 1. Tambah Penumpang (Input Manual)")
        print(" 2. Jalankan Simulasi")
        print(" 3. Demo Otomatis Skenario Kasus Panas (Dava, Reza, Qoiq, Bojes)")
        print(" 4. Reset Sistem Lift")
        print(" 0. Keluar")
        print("=================================================")
        
        pilihan = input("Pilih menu ▶ ").strip()
        
        if pilihan == "1":
            print("\n── input antrian luar lift ──")
            nama = input("Masukkan Nama Penumpang: ").strip()
            if not nama:
                print("Nama tidak boleh kosong!\n")
                continue
                
            try:
                asal = int(input(f"Lantai Asal ({lantai_min}-{lantai_max}): "))
                if asal < lantai_min or asal > lantai_max:
                    print(f"Lantai harus antara {lantai_min} sampai {lantai_max}!\n")
                    continue
                
                # Pengkondisian tombol lorong adaptif
                if asal == lantai_min:
                    print("Tombol otomatis diatur ke: naik (Lantai paling bawah)")
                    arah_pilihan = "1"
                elif asal == lantai_max:
                    print("Tombol otomatis diatur ke: turun (Lantai paling atas)")
                    arah_pilihan = "2"
                else:
                    print("Pilih Tombol Lorong:")
                    print(" 1. naik")
                    print(" 2. turun")
                    arah_pilihan = input("Pilihan Arah: ").strip()
                
                tujuan = int(input(f"Masukkan Lantai Tujuan ({lantai_min}-{lantai_max}): "))
                if tujuan < lantai_min or tujuan > lantai_max:
                    print("Lantai tujuan tidak valid!\n")
                    continue
                
                # Validasi keselarasan tombol luar dengan lantai tujuan
                if arah_pilihan == "1" and tujuan <= asal:
                    print(" Error: Tombol naik dipilih, lantai tujuan harus lebih tinggi dari lantai asal!\n")
                    continue
                elif arah_pilihan == "2" and tujuan >= asal:
                    print(" Error: Tombol turun dipilih, lantai tujuan harus lebih rendah dari lantai asal!\n")
                    continue
                
                p = Penumpang(nama, asal, tujuan)
                lift.tambah_panggilan(p)
                print(f"  Berhasil mendaftarkan {nama} di antrean luar Lantai {asal}!\n")
                
            except ValueError:
                print("  Input harus berupa angka valid!\n")

        elif pilihan == "2":
            lift.jalankan_simulasi()
            input("\nTekan Enter untuk kembali ke menu utama...")
            clear_screen()

        elif pilihan == "3":
            print("\n  Mengonfigurasi Skenario Kasus...")
            lift = Lift() # Reset ke kondisi awal
            lift.lantai_sekarang = 1 # Lift standby di lantai 1
            
            # Skenario Kasus:
            # Lantai 1: Dava & Reza mau ke Lantai 6 (Tombol naik) -> Harus Masuk 1 Sesi
            lift.tambah_panggilan(Penumpang("Dava", 8, 6))
            lift.tambah_panggilan(Penumpang("Reza", 8, 6))
            
            # Lantai 2: Qoiq & Bojes mau ke Lantai 6 (Tombol naik)
            lift.tambah_panggilan(Penumpang("Qoiq", 7, 6))
            lift.tambah_panggilan(Penumpang("Bojes", 7, 6))
            
            print(" [Kondisi Skenario]:")
            print("   - Lift berada di Lantai 1")
            print("   - Lantai 1: Dava & Reza (Mencet turun ke Lantai 6)")
            print("   - Lantai 2: Qoiq & Bojes (Mencet turun ke Lantai 6)")
            print(" [Ekspektasi Algoritma]: Lift meluncur naik melewati lantai 7 tanpa mengambil Qoiq & Bojes dulu, langsung mentok ke lantai 8, lalu balik arah naik menyapu semua penumpang ke lantai 6.")
            
            input("\nTekan Enter untuk membuktikannya...")
            lift.jalankan_simulasi()
            input("\nTekan Enter untuk kembali ke menu utama...")
            clear_screen()

        elif pilihan == "4":
            lift = Lift()
            print("\n  Sistem lift berhasil direset ke kondisi awal (Lantai 1, idle).\n")

        elif pilihan == "0":
            print("\n  Sampai jumpa, bre! Program ditutup.")
            break
        else:
            print("\nPilihan tidak valid, coba lagi!\n")

if __name__ == "__main__":
    main()