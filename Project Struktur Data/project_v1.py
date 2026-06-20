# ================================================================
#  PROJECT STRUKTUR DATA - V1
# ================================================================
#  Judul  : Simulasi Antrian Lift Gedung Cdast
#           Menggunakan Circular Queue
# ----------------------------------------------------------------
#  Nama   : [Nama Kamu]
#  NIM    : [NIM Kamu]
#  Kelas  : [Kelas Kamu]
# ================================================================

import os
import time
import sys


# =====================
# KONFIGURASI GEDUNG
# =====================
JUMLAH_LANTAI = 10
KAPASITAS_LIFT = 8
LANTAI_DASAR = 1


def clear_screen():
    """Bersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def delay(detik=0.5):
    """Delay untuk efek animasi."""
    time.sleep(detik)


def garis(karakter="=", panjang=50):
    """Print garis pembatas."""
    print(karakter * panjang)


# ================================================================
# CLASS: CircularQueue
# ================================================================
class CircularQueue:
    """
    Implementasi Circular Queue untuk antrian tujuan lift.
    
    Circular Queue menggunakan array dengan ukuran tetap.
    Ketika rear mencapai akhir array, ia kembali ke index 0
    (melingkar/circular), sehingga memanfaatkan ruang kosong
    di depan array yang sudah di-dequeue.
    
    Visualisasi:
        FRONT              REAR
          ↓                  ↓
      ┌───┬───┬───┬───┬───┬───┬───┬───┐
      │ 3 │ 5 │ 7 │   │   │   │   │   │
      └───┴───┴───┴───┴───┴───┴───┴───┘
        0   1   2   3   4   5   6   7
    """

    def __init__(self, kapasitas):
        """Inisialisasi circular queue."""
        self.kapasitas = kapasitas
        self.queue = [None] * kapasitas
        self.front = -1
        self.rear = -1
        self.count = 0

    def is_full(self):
        """Cek apakah queue penuh."""
        return self.count == self.kapasitas

    def is_empty(self):
        """Cek apakah queue kosong."""
        return self.count == 0

    def enqueue(self, lantai_tujuan):
        """
        EnQueue - Menambahkan lantai tujuan ke antrian.
        Dipanggil saat penumpang menekan tombol lantai tujuan.
        
        Returns: True jika berhasil, False jika gagal (penuh).
        """
        if self.is_full():
            print("  ❌ LIFT PENUH! Kapasitas maksimal tercapai.")
            print(f"     Kapasitas: {self.count}/{self.kapasitas}")
            return False

        if self.is_empty():
            # Queue masih kosong, set front dan rear ke 0
            self.front = 0
            self.rear = 0
        else:
            # Geser rear secara circular
            self.rear = (self.rear + 1) % self.kapasitas

        self.queue[self.rear] = lantai_tujuan
        self.count += 1
        return True

    def dequeue(self):
        """
        DeQueue - Mengeluarkan lantai tujuan dari antrian.
        Dipanggil saat lift sampai di lantai tujuan.
        
        Returns: lantai yang di-dequeue, atau None jika kosong.
        """
        if self.is_empty():
            print("  ℹ️  Antrian kosong. Lift tidak ada tujuan.")
            return None

        lantai = self.queue[self.front]
        self.queue[self.front] = None

        if self.count == 1:
            # Elemen terakhir, reset queue
            self.front = -1
            self.rear = -1
        else:
            # Geser front secara circular
            self.front = (self.front + 1) % self.kapasitas

        self.count -= 1
        return lantai

    def peek(self):
        """Lihat lantai tujuan berikutnya tanpa menghapus."""
        if self.is_empty():
            return None
        return self.queue[self.front]

    def get_all_tujuan(self):
        """Ambil semua lantai tujuan dalam antrian (berurutan)."""
        if self.is_empty():
            return []

        hasil = []
        idx = self.front
        for _ in range(self.count):
            hasil.append(self.queue[idx])
            idx = (idx + 1) % self.kapasitas
        return hasil

    def display(self):
        """Tampilkan visualisasi circular queue."""
        print()
        print("  ┌─── CIRCULAR QUEUE ──────────────────────┐")
        print("  │                                          │")

        # Tampilkan slot array
        slot_str = "  │  "
        for i in range(self.kapasitas):
            if self.queue[i] is not None:
                slot_str += f"[{self.queue[i]:>2}]"
            else:
                slot_str += "[  ]"
        slot_str += "  │"
        print(slot_str)

        # Tampilkan index
        idx_str = "  │   "
        for i in range(self.kapasitas):
            idx_str += f" {i}  "
        idx_str += " │"
        print(idx_str)

        # Tampilkan pointer
        pointer_str = "  │   "
        for i in range(self.kapasitas):
            if i == self.front and i == self.rear and not self.is_empty():
                pointer_str += "F/R "
            elif i == self.front and not self.is_empty():
                pointer_str += " F  "
            elif i == self.rear and not self.is_empty():
                pointer_str += " R  "
            else:
                pointer_str += "    "
        pointer_str += " │"
        print(pointer_str)

        print("  │                                          │")
        print(f"  │  Front: {self.front:>2}  |  Rear: {self.rear:>2}  |  "
              f"Isi: {self.count}/{self.kapasitas}   │")
        print("  └──────────────────────────────────────────┘")
        print()


# ================================================================
# CLASS: Penumpang
# ================================================================
class Penumpang:
    """Representasi seorang penumpang lift."""
    _id_counter = 0

    def __init__(self, lantai_asal, lantai_tujuan):
        Penumpang._id_counter += 1
        self.id = Penumpang._id_counter
        self.lantai_asal = lantai_asal
        self.lantai_tujuan = lantai_tujuan

    def __str__(self):
        return (f"Penumpang #{self.id} "
                f"(Lt.{self.lantai_asal} → Lt.{self.lantai_tujuan})")


# ================================================================
# CLASS: Lift
# ================================================================
class Lift:
    """
    Representasi Lift Gedung Cdast.
    Menggunakan Circular Queue untuk mengatur antrian tujuan.
    """

    def __init__(self):
        """Inisialisasi lift di lantai dasar."""
        self.lantai_sekarang = LANTAI_DASAR
        self.antrian = CircularQueue(KAPASITAS_LIFT)
        self.penumpang_list = []  # List penumpang di dalam lift
        self.status = "DIAM"     # DIAM / NAIK / TURUN
        self.log = []            # Log aktivitas

    def tampilkan_gedung(self):
        """Tampilkan visualisasi gedung dan posisi lift."""
        print()
        print("  🏢 GEDUNG CDAST")
        print("  ┌──────────────────────┐")
        for lantai in range(JUMLAH_LANTAI, 0, -1):
            if lantai == self.lantai_sekarang:
                # Lift ada di lantai ini
                penumpang_icon = "👤" * len(self.penumpang_list)
                if not penumpang_icon:
                    penumpang_icon = "  "
                print(f"  │ Lt.{lantai:>2}  🛗 [{penumpang_icon}]", end="")
                # Tampilkan panah arah
                if self.status == "NAIK":
                    print(" ▲", end="")
                elif self.status == "TURUN":
                    print(" ▼", end="")
                print()
            else:
                print(f"  │ Lt.{lantai:>2}  ·            │")
        print("  └──────────────────────┘")
        print()

    def panggil_lift(self, lantai_pemanggil):
        """Lift dipanggil ke lantai tertentu."""
        if lantai_pemanggil < 1 or lantai_pemanggil > JUMLAH_LANTAI:
            print(f"  ❌ Lantai {lantai_pemanggil} tidak valid! "
                  f"(1-{JUMLAH_LANTAI})")
            return

        if self.lantai_sekarang == lantai_pemanggil:
            print(f"  ℹ️  Lift sudah ada di lantai {lantai_pemanggil}.")
            print("  🔔 Pintu terbuka. Silakan masuk!")
            return

        print(f"  🔔 Lift dipanggil dari lantai {lantai_pemanggil}...")
        print(f"     Lift sedang di lantai {self.lantai_sekarang}")
        delay(0.3)

        # Animasi lift bergerak ke lantai pemanggil
        self._bergerak_ke(lantai_pemanggil, alasan="menuju pemanggil")

        print(f"\n  ✅ Lift tiba di lantai {lantai_pemanggil}.")
        print("  🔔 Pintu terbuka. Silakan masuk!")

    def penumpang_masuk(self, lantai_tujuan):
        """
        Penumpang masuk ke lift dan menekan tombol tujuan.
        Lantai tujuan di-EnQueue ke Circular Queue.
        """
        if lantai_tujuan < 1 or lantai_tujuan > JUMLAH_LANTAI:
            print(f"  ❌ Lantai {lantai_tujuan} tidak valid! "
                  f"(1-{JUMLAH_LANTAI})")
            return False

        if lantai_tujuan == self.lantai_sekarang:
            print(f"  ❌ Anda sudah di lantai {lantai_tujuan}!")
            return False

        if self.antrian.is_full():
            print("  ❌ LIFT PENUH! Tidak bisa masuk.")
            print(f"     Kapasitas: {self.antrian.count}/{KAPASITAS_LIFT}")
            return False

        # Buat penumpang baru
        penumpang = Penumpang(self.lantai_sekarang, lantai_tujuan)
        self.penumpang_list.append(penumpang)

        # EnQueue lantai tujuan
        berhasil = self.antrian.enqueue(lantai_tujuan)

        if berhasil:
            print(f"\n  👤 {penumpang}")
            print(f"  ✅ EnQueue → Lantai {lantai_tujuan} "
                  f"ditambahkan ke antrian")
            print(f"     Jumlah penumpang: "
                  f"{self.antrian.count}/{KAPASITAS_LIFT}")

            self.log.append(
                f"EnQueue: {penumpang} | "
                f"Antrian: {self.antrian.get_all_tujuan()}"
            )
            return True
        return False

    def jalankan_lift(self):
        """
        Proses antrian - Lift bergerak ke setiap tujuan secara FIFO.
        DeQueue setiap kali sampai di lantai tujuan.
        """
        if self.antrian.is_empty():
            print("\n  ℹ️  Antrian kosong. Lift tidak ada tujuan.")
            print("     Masukkan penumpang terlebih dahulu!")
            return

        print("\n  🛗 LIFT MULAI BERGERAK!")
        garis("-", 50)

        while not self.antrian.is_empty():
            # Peek tujuan berikutnya
            tujuan = self.antrian.peek()
            jumlah_sebelum = self.antrian.count

            print(f"\n  📍 Tujuan berikutnya: Lantai {tujuan}")
            print(f"     Antrian saat ini: {self.antrian.get_all_tujuan()}")
            delay(0.5)

            # Gerakkan lift
            self._bergerak_ke(tujuan, alasan="mengantar penumpang")

            # DeQueue - sampai di tujuan
            lantai_selesai = self.antrian.dequeue()

            # Cari dan keluarkan penumpang yang turun di lantai ini
            penumpang_turun = [
                p for p in self.penumpang_list
                if p.lantai_tujuan == lantai_selesai
            ]

            print(f"\n  🔔 Lift sampai di lantai {lantai_selesai}!")
            print(f"  ✅ DeQueue → Lantai {lantai_selesai} "
                  f"dikeluarkan dari antrian")

            for p in penumpang_turun:
                print(f"  🚶 {p} TURUN")
                self.penumpang_list.remove(p)
                self.log.append(
                    f"DeQueue: {p} turun di Lt.{lantai_selesai} | "
                    f"Sisa: {self.antrian.get_all_tujuan()}"
                )

            sisa = self.antrian.count
            print(f"     Sisa antrian: {sisa} penumpang")

            if not self.antrian.is_empty():
                print(f"     Tujuan selanjutnya: {self.antrian.get_all_tujuan()}")

            delay(0.5)

        garis("-", 50)
        print("\n  ✅ Semua penumpang sudah diantar!")
        print(f"  📍 Lift sekarang di lantai {self.lantai_sekarang}")
        self.status = "DIAM"

    def _bergerak_ke(self, lantai_tujuan, alasan=""):
        """Animasi lift bergerak lantai per lantai."""
        if self.lantai_sekarang < lantai_tujuan:
            self.status = "NAIK"
            arah = "▲"
        elif self.lantai_sekarang > lantai_tujuan:
            self.status = "TURUN"
            arah = "▼"
        else:
            return

        print(f"     {arah} Lift bergerak {self.status.lower()}...", end="")
        sys.stdout.flush()

        step = 1 if self.lantai_sekarang < lantai_tujuan else -1
        while self.lantai_sekarang != lantai_tujuan:
            self.lantai_sekarang += step
            print(f" [{self.lantai_sekarang}]", end="")
            sys.stdout.flush()
            delay(0.3)

        print()  # Newline setelah animasi
        self.status = "DIAM"

    def tampilkan_status(self):
        """Tampilkan status lift lengkap."""
        print()
        garis("═", 50)
        print("  📊 STATUS LIFT GEDUNG CDAST")
        garis("─", 50)
        print(f"  📍 Posisi       : Lantai {self.lantai_sekarang}")
        print(f"  📶 Status       : {self.status}")
        print(f"  👥 Penumpang    : {self.antrian.count}/{KAPASITAS_LIFT}")
        print(f"  📋 Antrian      : {self.antrian.get_all_tujuan()}")

        if self.penumpang_list:
            print()
            print("  👤 Daftar Penumpang:")
            for p in self.penumpang_list:
                print(f"     • {p}")
        garis("═", 50)

        # Tampilkan visualisasi gedung
        self.tampilkan_gedung()

        # Tampilkan visualisasi queue
        self.antrian.display()

    def tampilkan_log(self):
        """Tampilkan log aktivitas lift."""
        print()
        garis("═", 50)
        print("  📜 LOG AKTIVITAS LIFT")
        garis("─", 50)
        if not self.log:
            print("  (Belum ada aktivitas)")
        else:
            for i, entry in enumerate(self.log, 1):
                print(f"  {i:>3}. {entry}")
        garis("═", 50)


# ================================================================
# MENU & MAIN
# ================================================================
def tampilkan_header():
    """Tampilkan header program."""
    clear_screen()
    garis("═", 50)
    print("  🏢 SIMULASI ANTRIAN LIFT GEDUNG CDAST 🛗")
    print("     Menggunakan Circular Queue")
    garis("═", 50)


def tampilkan_menu():
    """Tampilkan menu utama."""
    print()
    garis("─", 50)
    print("  📌 MENU UTAMA")
    garis("─", 50)
    print("  1. 🔔 Panggil Lift ke Lantai Tertentu")
    print("  2. 👤 Masuk & Pilih Lantai Tujuan (EnQueue)")
    print("  3. 🛗 Jalankan Lift (Proses Antrian)")
    print("  4. 📊 Lihat Status Lift & Gedung")
    print("  5. 📋 Lihat Antrian (Circular Queue)")
    print("  6. 📜 Lihat Log Aktivitas")
    print("  7. 🔄 Reset Lift")
    print("  0. ❌ Keluar (Done ✅)")
    garis("─", 50)


def input_angka(prompt, min_val=None, max_val=None):
    """Input angka dengan validasi."""
    while True:
        try:
            nilai = int(input(prompt))
            if min_val is not None and nilai < min_val:
                print(f"  ⚠️  Minimal {min_val}!")
                continue
            if max_val is not None and nilai > max_val:
                print(f"  ⚠️  Maksimal {max_val}!")
                continue
            return nilai
        except ValueError:
            print("  ⚠️  Masukkan angka yang valid!")


def main():
    """Fungsi utama program."""
    lift = Lift()

    tampilkan_header()
    print(f"\n  📍 Lift dimulai di lantai {LANTAI_DASAR}")
    print(f"  🏢 Gedung Cdast: {JUMLAH_LANTAI} lantai")
    print(f"  👥 Kapasitas lift: {KAPASITAS_LIFT} orang")

    while True:
        tampilkan_menu()
        pilihan = input("\n  Pilih menu (0-7): ").strip()

        if pilihan == "1":
            # Panggil Lift
            print("\n  🔔 PANGGIL LIFT")
            garis("─", 50)
            lantai = input_angka(
                f"  Panggil lift ke lantai berapa? (1-{JUMLAH_LANTAI}): ",
                1, JUMLAH_LANTAI
            )
            lift.panggil_lift(lantai)

        elif pilihan == "2":
            # Masuk & Pilih Lantai (EnQueue)
            print("\n  👤 PENUMPANG MASUK")
            garis("─", 50)
            print(f"  📍 Lift sekarang di lantai {lift.lantai_sekarang}")

            # Tanya berapa penumpang mau masuk
            while True:
                lantai = input_angka(
                    f"  Lantai tujuan? (1-{JUMLAH_LANTAI}, 0=selesai): ",
                    0, JUMLAH_LANTAI
                )
                if lantai == 0:
                    break
                lift.penumpang_masuk(lantai)

                if lift.antrian.is_full():
                    print("\n  ⚠️  Lift sudah penuh!")
                    break

        elif pilihan == "3":
            # Jalankan Lift (Proses Antrian)
            lift.jalankan_lift()

        elif pilihan == "4":
            # Status Lift
            lift.tampilkan_status()

        elif pilihan == "5":
            # Lihat Antrian
            print("\n  📋 ANTRIAN LIFT (CIRCULAR QUEUE)")
            garis("─", 50)
            print(f"  Antrian: {lift.antrian.get_all_tujuan()}")
            lift.antrian.display()

        elif pilihan == "6":
            # Log Aktivitas
            lift.tampilkan_log()

        elif pilihan == "7":
            # Reset
            konfirmasi = input("\n  ⚠️  Reset lift? (y/n): ").strip().lower()
            if konfirmasi == 'y':
                lift = Lift()
                print("  ✅ Lift berhasil direset!")

        elif pilihan == "0":
            # Keluar
            print()
            garis("═", 50)
            print("  ✅ DONE! Program selesai.")
            print("  🏢 Terima kasih telah menggunakan Lift Gedung Cdast!")
            garis("═", 50)
            print()
            break

        else:
            print("  ⚠️  Pilihan tidak valid! Masukkan 0-7.")

        input("\n  Tekan Enter untuk lanjut...")


# ================================================================
# JALANKAN PROGRAM
# ================================================================
if __name__ == "__main__":
    main()
