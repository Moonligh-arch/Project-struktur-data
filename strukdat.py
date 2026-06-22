import time
import os

# ── KONSTANTA GEDUNG ─────────────────────────────────────────
LANTAI_MIN = 1
LANTAI_MAX = 8
KAPASITAS_MAX = 7

class Penumpang:
    def __init__(self, nama, asal, tujuan):
        self.nama = nama
        self.asal = asal
        self.tujuan = tujuan

class Lift:
    def __init__(self):
        self.lantai_sekarang = 8  # Mulai dari lantai 8 sesuai skenario pembuktian
        self.arah = "IDLE"        # NAIK, TURUN, atau IDLE
        self.penumpang_dalam = []

        # Menampung panggilan dari luar koridor gedung
        # Format: { lantai: {"NAIK": [list_penumpang], "TURUN": [list_penumpang]} }
        self.panggilan_luar = {i: {"NAIK": [], "TURUN": []} for i in range(LANTAI_MIN, LANTAI_MAX + 1)}

    def tambah_panggilan(self, penumpang):
        arah_req = "NAIK" if penumpang.tujuan > penumpang.asal else "TURUN"
        self.panggilan_luar[penumpang.asal][arah_req].append(penumpang)

    def ada_tugas(self):
        """Mengecek apakah masih ada penumpang di dalam lift atau antrean di luar."""
        if self.penumpang_dalam:
            return True
        for lantai in self.panggilan_luar:
            if self.panggilan_luar[lantai]["NAIK"] or self.panggilan_luar[lantai]["TURUN"]:
                return True
        return False

    def tentukan_arah_awal(self):
        """Menentukan arah gerak pertama kali ketika lift dalam kondisi IDLE."""
        panggilan_floors = []
        for lantai in self.panggilan_luar:
            if self.panggilan_luar[lantai]["NAIK"] or self.panggilan_luar[lantai]["TURUN"]:
                panggilan_floors.append(lantai)

        if not panggilan_floors:
            self.arah = "IDLE"
            return

        # Jika ada panggilan tepat di lantai lift sekarang berada
        if self.lantai_sekarang in panggilan_floors:
            if self.panggilan_luar[self.lantai_sekarang]["NAIK"]:
                self.arah = "NAIK"
            elif self.panggilan_luar[self.lantai_sekarang]["TURUN"]:
                self.arah = "TURUN"
            return

        # Ambil lantai panggilan terdekat untuk menentukan rute awal lift meluncur
        terdekat = min(panggilan_floors, key=lambda x: abs(x - self.lantai_sekarang))
        if terdekat > self.lantai_sekarang:
            self.arah = "NAIK"
        else:
            self.arah = "TURUN"

    def periksa_perubahan_arah(self):
        """
        Inti dari SCAN Algorithm: Memeriksa apakah tugas di arah saat ini sudah habis.
        Jika habis, lift baru diizinkan berbalik arah atau berubah menjadi IDLE.
        """
        if self.arah == "NAIK":
            ada_tugas_di_atas = False
            # Cek apakah ada penumpang di dalam yang mau turun di lantai atasnya lagi
            if any(p.tujuan > self.lantai_sekarang for p in self.penumpang_dalam):
                ada_tugas_di_atas = True
            # Cek apakah ada antrean di luar pada lantai-lantai di atasnya
            for f in range(self.lantai_sekarang + 1, LANTAI_MAX + 1):
                if self.panggilan_luar[f]["NAIK"] or self.panggilan_luar[f]["TURUN"]:
                    ada_tugas_di_atas = True

            # Jika di atas benar-benar bersih, cek apakah ada sisa tugas di bawah
            if not ada_tugas_di_atas:
                ada_tugas_di_bawah_atau_sini = False
                if self.panggilan_luar[self.lantai_sekarang]["TURUN"]:
                    ada_tugas_di_bawah_atau_sini = True
                for f in range(LANTAI_MIN, self.lantai_sekarang):
                    if self.panggilan_luar[f]["NAIK"] or self.panggilan_luar[f]["TURUN"]:
                        ada_tugas_di_bawah_atau_sini = True

                self.arah = "TURUN" if ada_tugas_di_bawah_atau_sini else "IDLE"

        elif self.arah == "TURUN":
            ada_tugas_di_bawah = False
            # Cek penumpang dalam lift yang tujuannya ada di bawah lantai sekarang
            if any(p.tujuan < self.lantai_sekarang for p in self.penumpang_dalam):
                ada_tugas_di_bawah = True
            # Cek antrean luar di lantai-lantai bawahnya
            for f in range(LANTAI_MIN, self.lantai_sekarang):
                if self.panggilan_luar[f]["NAIK"] or self.panggilan_luar[f]["TURUN"]:
                    ada_tugas_di_bawah = True

            # Jika di bawah bersih, cek apakah ada sisa tugas di atas
            if not ada_tugas_di_bawah:
                ada_tugas_di_atas_atau_sini = False
                if self.panggilan_luar[self.lantai_sekarang]["NAIK"]:
                    ada_tugas_di_atas_atau_sini = True
                for f in range(self.lantai_sekarang + 1, LANTAI_MAX + 1):
                    if self.panggilan_luar[f]["NAIK"] or self.panggilan_luar[f]["TURUN"]:
                        ada_tugas_di_atas_atau_sini = True

                self.arah = "NAIK" if ada_tugas_di_atas_atau_sini else "IDLE"

    def jalankan_simulasi(self):
        print("\n=================== SIMULASI LIFT DIMULAI ===================")
        if not self.ada_tugas():
            print("  [⚠️] Tidak ada antrean penumpang di dalam sistem.")
            return

        while self.ada_tugas():
            if self.arah == "IDLE":
                self.tentukan_arah_awal()

            # Validasi arah tepat sebelum memproses lantai (antisipasi batas mentok lantai)
            self.periksa_perubahan_arah()

            pintu_terbuka = False
            penumpang_keluar = []
            penumpang_masuk = []

            # 1. PROSES PENUMPANG KELUAR
            sisa_penumpang = []
            for p in self.penumpang_dalam:
                if p.tujuan == self.lantai_sekarang:
                    penumpang_keluar.append(p)
                    pintu_terbuka = True
                else:
                    sisa_penumpang.append(p)
            self.penumpang_dalam = sisa_penumpang

            # 2. PROSES PENUMPANG MASUK (BATCHING / SATU SESI PICKUP)
            if self.arah != "IDLE":
                antrean_di_lantai = self.panggilan_luar[self.lantai_sekarang][self.arah]
                if antrean_di_lantai:
                    pintu_terbuka = True
                    # Angkut semua orang di antrean lantai ini ke dalam satu sesi sampai penuh
                    while antrean_di_lantai and len(self.penumpang_dalam) < KAPASITAS_MAX:
                        p = antrean_di_lantai.pop(0)
                        self.penumpang_dalam.append(p)
                        penumpang_masuk.append(p)

                    # Jika lift penuh tapi di luar masih tersisa orang
                    if antrean_di_lantai and len(self.penumpang_dalam) == KAPASITAS_MAX:
                        print(f"  [⚠️] Lift PENUH! Sisa penumpang di Lantai {self.lantai_sekarang} harus antre di sesi berikutnya.")

            # Tampilkan Visualisasi Log per Lantai
            print(f"\n ─── [ Lantai {self.lantai_sekarang} ] ────────────────────────────────────────")
            print(f"  Status Arah  : {self.arah}")
            print(f"  Kapasitas    : {len(self.penumpang_dalam)}/{KAPASITAS_MAX} Orang")

            if pintu_terbuka:
                print("  🚪 Pintu Terbuka...")
                if penumpang_keluar:
                    print("    🔻 Keluar: " + ", ".join([f"{p.nama} (Selesai)" for p in penumpang_keluar]))
                if penumpang_masuk:
                    print("    🔺 Masuk (Satu Sesi): " + ", ".join([f"{p.nama} (Tujuan Lnt {p.tujuan})" for p in penumpang_masuk]))
                print("  🚪 Pintu Tertutup.")
                time.sleep(1)
            else:
                print("  ... Lift melewati lantai ini (Tidak ada aksi) ...")
                time.sleep(0.5)

            # Periksa rute lagi setelah aktivitas bongkar-muat selesai
            self.periksa_perubahan_arah()

            # Pergerakan mekanis motor lift ke lantai berikutnya
            if self.arah == "NAIK" and self.lantai_sekarang < LANTAI_MAX:
                self.lantai_sekarang += 1
            elif self.arah == "TURUN" and self.lantai_sekarang > LANTAI_MIN:
                self.lantai_sekarang -= 1
            elif self.arah == "IDLE":
                break

        print("\n=================== SIMULASI SELESAI ===================")
        print(f"Lift berhenti total di Lantai {self.lantai_sekarang} dengan status IDLE.\n")


# ── MENU INTERAKTIF CLI ───────────────────────────────────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    lift = Lift()

    while True:
        print("====== SIMULASI LIFT PRIORITY QUEUE (SCAN) ======")
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
            print("\n── INPUT ANTRIAN LUAR LIFT ──")
            nama = input("Masukkan Nama Penumpang: ").strip()
            if not nama:
                print("Nama tidak boleh kosong!\n")
                continue

            try:
                asal = int(input(f"Lantai Asal ({LANTAI_MIN}-{LANTAI_MAX}): "))
                if asal < LANTAI_MIN or asal > LANTAI_MAX:
                    print(f"Lantai harus antara {LANTAI_MIN} sampai {LANTAI_MAX}!\n")
                    continue

                # Pengkondisian tombol lorong adaptif
                if asal == LANTAI_MIN:
                    print("Tombol otomatis diatur ke: NAIK (Lantai paling bawah)")
                    arah_pilihan = "1"
                elif asal == LANTAI_MAX:
                    print("Tombol otomatis diatur ke: TURUN (Lantai paling atas)")
                    arah_pilihan = "2"
                else:
                    print("Pilih Tombol Lorong:")
                    print(" 1. NAIK")
                    print(" 2. TURUN")
                    arah_pilihan = input("Pilihan Arah: ").strip()

                tujuan = int(input(f"Masukkan Lantai Tujuan ({LANTAI_MIN}-{LANTAI_MAX}): "))
                if tujuan < LANTAI_MIN or tujuan > LANTAI_MAX:
                    print("Lantai tujuan tidak valid!\n")
                    continue

                # Validasi keselarasan tombol luar dengan lantai tujuan
                if arah_pilihan == "1" and tujuan <= asal:
                    print(" Error: Tombol NAIK dipilih, lantai tujuan harus lebih tinggi dari lantai asal!\n")
                    continue
                elif arah_pilihan == "2" and tujuan >= asal:
                    print(" Error: Tombol TURUN dipilih, lantai tujuan harus lebih rendah dari lantai asal!\n")
                    continue

                p = Penumpang(nama, asal, tujuan)
                lift.tambah_panggilan(p)
                print(f"✅ Berhasil mendaftarkan {nama} di antrean luar Lantai {asal}!\n")

            except ValueError:
                print("❌ Input harus berupa angka valid!\n")

        elif pilihan == "2":
            lift.jalankan_simulasi()
            input("\nTekan Enter untuk kembali ke menu utama...")
            clear_screen()

        elif pilihan == "3":
            print("\n🔄 Mengonfigurasi Skenario Kasus...")
            lift = Lift() # Reset ke kondisi awal
            lift.lantai_sekarang = 8 # Lift standby di lantai 8

            # Skenario Kasus:
            # Lantai 1: Dava & Reza mau ke Lantai 3 (Tombol NAIK) -> Harus Masuk 1 Sesi
            lift.tambah_panggilan(Penumpang("Dava", 1, 3))
            lift.tambah_panggilan(Penumpang("Reza", 1, 3))

            # Lantai 2: Qoiq & Bojes mau ke Lantai 3 (Tombol NAIK)
            lift.tambah_panggilan(Penumpang("Qoiq", 2, 3))
            lift.tambah_panggilan(Penumpang("Bojes", 2, 3))

            print(" [Kondisi Skenario]:")
            print("   - Lift berada di Lantai 1")
            print("   - Lantai 1: Dava & Reza (Mencet NAIK ke Lantai 3)")
            print("   - Lantai 2: Qoiq & Bojes (Mencet NAIK ke Lantai 3)")
            print(" [Ekspektasi Algoritma]: Lift meluncur turun melewati lantai 2 tanpa mengambil Qoiq & Bojes dulu, langsung mentok ke lantai 1, lalu balik arah naik menyapu semua penumpang ke lantai 3.")

            input("\nTekan Enter untuk membuktikannya...")
            lift.jalankan_simulasi()
            input("\nTekan Enter untuk kembali ke menu utama...")
            clear_screen()

        elif pilihan == "4":
            lift = Lift()
            print("\n🔄 Sistem lift berhasil direset ke kondisi awal (Lantai 1, IDLE).\n")

        elif pilihan == "0":
            print("\nSampai jumpa, bre! Program ditutup.")
            break
        else:
            print("\nPilihan tidak valid, coba lagi!\n")

if __name__ == "__main__":
    main()