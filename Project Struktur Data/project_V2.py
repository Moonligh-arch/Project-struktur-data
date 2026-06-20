#!/usr/bin/env python3
"""
══════════════════════════════════════════════════════════════
  SISTEM SIMULASI LIFT GEDUNG CDAST SELATAN UNEJ
  Menggunakan Priority Queue
══════════════════════════════════════════════════════════════
  Struktur Kode (Kepingan Lego):
    BLOK 1 → Konstanta & Struktur Data
    BLOK 2 → Priority Queue
    BLOK 3 → Class Lift (Mesin Utama)
    BLOK 4 → Validasi & Menu Interaktif
    BLOK 5 → Main (Merakit Semua Lego)
══════════════════════════════════════════════════════════════
"""

# ╔════════════════════════════════════════════════════════════╗
# ║  BLOK 1: KONSTANTA & STRUKTUR DATA                       ║
# ╚════════════════════════════════════════════════════════════╝

from dataclasses import dataclass
from typing import List, Optional, Tuple
import heapq
import time
import os

# --- Konstanta Gedung ---
LANTAI_MIN     = 1
LANTAI_MAX     = 8
KAPASITAS_LIFT = 7
DELAY_GERAK    = 0.35  # detik per lantai (efek animasi)

# --- Konstanta Arah ---
NAIK  = "NAIK"
TURUN = "TURUN"
IDLE  = "IDLE"


@dataclass
class Penumpang:
    """Struktur data untuk satu penumpang lift."""
    nama: str
    lantai_asal: int
    lantai_tujuan: int

    @property
    def arah(self) -> str:
        """Arah pergerakan penumpang berdasarkan lantai asal & tujuan."""
        return NAIK if self.lantai_tujuan > self.lantai_asal else TURUN

    def __repr__(self):
        return f"{self.nama}(L{self.lantai_asal}→L{self.lantai_tujuan})"

# ─── Penjelasan Blok 1 ──────────────────────────────────────
# Mendefinisikan semua konstanta gedung (8 lantai, kapasitas 7)
# dan dataclass Penumpang sebagai unit data dasar.
# Property `arah` otomatis menghitung arah berdasarkan lantai
# asal vs tujuan.
# ─────────────────────────────────────────────────────────────


# ╔════════════════════════════════════════════════════════════╗
# ║  BLOK 2: PRIORITY QUEUE                                   ║
# ╚════════════════════════════════════════════════════════════╝

class AntrianPrioritas:
    """
    Priority Queue berbasis min-heap.
    Kunci prioritas: (skor_arah, jarak, urutan_masuk)
    → Lantai SEARAH & TERDEKAT dilayani duluan.
    """

    def __init__(self):
        self._heap: List[Tuple] = []
        self._seq: int = 0  # tie-breaker FIFO

    def push(self, lantai_stop: int, penumpang: Optional[Penumpang],
             posisi_lift: int, arah_lift: str, tipe: str = "PICKUP"):
        """
        Masukkan request ke antrian.
        tipe: "PICKUP" (jemput) atau "DROPOFF" (antar)
        """
        jarak = abs(lantai_stop - posisi_lift)

        # Hitung skor arah: 0 = searah (prioritas tinggi), 1 = berlawanan
        if arah_lift == IDLE:
            skor_arah = 0
        elif tipe == "DROPOFF":
            # Penumpang sudah di dalam lift, selalu diprioritaskan
            skor_arah = 0
        else:
            arah_req = penumpang.arah if penumpang else NAIK
            skor_arah = 0 if arah_req == arah_lift else 1

        heapq.heappush(
            self._heap,
            (skor_arah, jarak, self._seq, lantai_stop, penumpang, tipe)
        )
        self._seq += 1

    def pop(self) -> Optional[Tuple[int, Optional[Penumpang], str]]:
        """Ambil request dengan prioritas tertinggi (nilai terkecil)."""
        if self._heap:
            _, _, _, lantai, pnp, tipe = heapq.heappop(self._heap)
            return (lantai, pnp, tipe)
        return None

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)

    def recalculate(self, posisi_lift: int, arah_lift: str):
        """Hitung ulang SEMUA prioritas berdasarkan posisi & arah lift terkini."""
        old_items = []
        while self._heap:
            _, _, _, lt, pnp, tipe = heapq.heappop(self._heap)
            old_items.append((lt, pnp, tipe))
        for lt, pnp, tipe in old_items:
            self.push(lt, pnp, posisi_lift, arah_lift, tipe)

    def peek_all(self) -> List[Tuple]:
        """Lihat semua request tanpa menghapus (untuk display)."""
        return [
            (lt, pnp, tipe)
            for _, _, _, lt, pnp, tipe in sorted(self._heap)
        ]

# ─── Penjelasan Blok 2 ──────────────────────────────────────
# Min-heap dengan kunci (skor_arah, jarak, urutan). Searah dan
# terdekat = prioritas tertinggi. `recalculate()` dipanggil
# setiap kali lift berpindah posisi agar prioritas selalu akurat.
# ─────────────────────────────────────────────────────────────


# ╔════════════════════════════════════════════════════════════╗
# ║  BLOK 3: CLASS LIFT (MESIN UTAMA)                         ║
# ╚════════════════════════════════════════════════════════════╝

class Lift:
    """Representasi lift fisik beserta seluruh operasinya."""

    def __init__(self):
        self.posisi: int = 1            # Mulai dari lantai 1
        self.arah: str = IDLE
        self.penumpang: List[Penumpang] = []  # ← Vektor (list) penumpang
        self.pintu_terbuka: bool = False
        self.antrian = AntrianPrioritas()

    # ── Properties ──────────────────────────────────────────

    @property
    def jumlah_penumpang(self) -> int:
        return len(self.penumpang)

    @property
    def penuh(self) -> bool:
        return self.jumlah_penumpang >= KAPASITAS_LIFT

    # ── Display ─────────────────────────────────────────────

    def tampilkan_status(self):
        """Cetak box status lift saat ini."""
        isi   = f"{self.jumlah_penumpang}/{KAPASITAS_LIFT}"
        pintu = "TERBUKA" if self.pintu_terbuka else "TERTUTUP"
        sisa  = self.antrian.size()

        print()
        print("  ╔═══════════════════════════════════════════╗")
        print("  ║   🏢  STATUS LIFT CDAST SELATAN UNEJ      ║")
        print("  ╠═══════════════════════════════════════════╣")
        print(f"  ║  📍 Posisi     : Lantai {self.posisi:<17}║")
        print(f"  ║  🧭 Arah       : {self.arah:<25}║")
        print(f"  ║  👥 Penumpang  : {isi:<25}║")
        print(f"  ║  🚪 Pintu      : {pintu:<25}║")
        print(f"  ║  📋 Antrian    : {sisa} stop tersisa{' ' * max(0, 13 - len(str(sisa)))}║")
        print("  ╚═══════════════════════════════════════════╝")

        if self.penumpang:
            print("  ┌── Penumpang di dalam lift ──────────────┐")
            for p in self.penumpang:
                print(f"  │  • {p.nama:<16} → Lantai {p.lantai_tujuan:<8}│")
            print("  └────────────────────────────────────────┘")

    def tampilkan_gedung(self):
        """Visualisasi posisi lift di gedung."""
        print("\n  🏢 GEDUNG CDAST SELATAN UNEJ")
        print("  ┌─────────────────────────┐")
        for lantai in range(LANTAI_MAX, LANTAI_MIN - 1, -1):
            ikon  = " 🛗" if self.posisi == lantai else "   "
            tombol = _tombol_lantai(lantai)
            print(f"  │ L{lantai} {ikon}  {tombol:>12}    │")
        print("  └─────────────────────────┘")

    # ── Operasi Pintu ───────────────────────────────────────

    def _buka_pintu(self):
        self.pintu_terbuka = True
        print(f"\n  🔔 Lantai {self.posisi} — Pintu TERBUKA  ◄ ►")

    def _tutup_pintu(self):
        self.pintu_terbuka = False
        print(f"  🔔 Pintu TERTUTUP  ► ◄")

    # ── Operasi Penumpang ───────────────────────────────────

    def _turunkan_penumpang(self) -> int:
        """Turunkan semua penumpang yang tujuannya = lantai saat ini."""
        turun = [p for p in self.penumpang if p.lantai_tujuan == self.posisi]
        for p in turun:
            self.penumpang.remove(p)
            print(f"  ⬇  {p.nama} TURUN di lantai {self.posisi} ✓")
        if not turun:
            print(f"  —  Tidak ada penumpang turun di lantai ini")
        return len(turun)

    def _naikkan_penumpang(self, penumpang: Penumpang) -> bool:
        """
        Masukkan penumpang ke lift (vektor/list).
        Return False jika kapasitas >= 7 (PENUH).
        """
        if self.penuh:
            print(f"  ❌ LIFT PENUH! {penumpang.nama} DITOLAK "
                  f"(kapasitas maks {KAPASITAS_LIFT} orang)")
            return False

        self.penumpang.append(penumpang)
        print(f"  ⬆  {penumpang.nama} MASUK lift → tujuan Lantai {penumpang.lantai_tujuan}")

        # Tambahkan lantai tujuan penumpang sebagai DROPOFF ke antrian
        self.antrian.push(
            penumpang.lantai_tujuan, penumpang,
            self.posisi, self.arah, "DROPOFF"
        )
        return True

    # ── Pergerakan ──────────────────────────────────────────

    def _bergerak_ke(self, tujuan: int):
        """Gerakkan lift lantai demi lantai menuju tujuan."""
        if tujuan == self.posisi:
            return

        self.arah = NAIK if tujuan > self.posisi else TURUN
        simbol = "⬆" if self.arah == NAIK else "⬇"
        print(f"\n  {simbol}  Lift bergerak {self.arah} menuju Lantai {tujuan}...")

        while self.posisi != tujuan:
            time.sleep(DELAY_GERAK)
            self.posisi += (1 if self.arah == NAIK else -1)
            bar = "█" * self.posisi + "░" * (LANTAI_MAX - self.posisi)
            print(f"     [{bar}] Lantai {self.posisi}")

    def _update_arah(self):
        """Update arah lift berdasarkan penumpang yang ada di dalam."""
        if self.penumpang:
            closest = min(self.penumpang,
                          key=lambda p: abs(p.lantai_tujuan - self.posisi))
            if closest.lantai_tujuan > self.posisi:
                self.arah = NAIK
            elif closest.lantai_tujuan < self.posisi:
                self.arah = TURUN
        elif self.antrian.is_empty():
            self.arah = IDLE

    # ── Request ─────────────────────────────────────────────

    def tambah_request(self, penumpang: Penumpang):
        """Tambahkan permintaan PICKUP ke antrian prioritas."""
        self.antrian.push(
            penumpang.lantai_asal, penumpang,
            self.posisi, self.arah, "PICKUP"
        )
        print(f"  📩 Request: {penumpang.nama} di L{penumpang.lantai_asal} "
              f"→ L{penumpang.lantai_tujuan} ({penumpang.arah})")

    # ── Proses Utama (Loop Simulasi) ────────────────────────

    def proses_semua_antrian(self):
        """
        LOOP UTAMA: Proses seluruh antrian sampai habis.
        Alur per step:
          1. Recalculate prioritas
          2. Pop request teratas
          3. Gerak ke lantai target
          4. Buka pintu
          5. Turunkan penumpang (jika ada yang sampai tujuan)
          6. Naikkan penumpang (jika PICKUP & belum penuh)
          7. Tutup pintu
          8. Cek sisa antrian → ulangi atau selesai
        """
        step = 0

        while not self.antrian.is_empty():
            step += 1
            print(f"\n{'═' * 52}")
            print(f"  📌 STEP {step}")
            print(f"{'═' * 52}")

            # 1. Recalculate prioritas berdasarkan posisi terkini
            self._update_arah()
            self.antrian.recalculate(self.posisi, self.arah)

            # 2. Pop request prioritas tertinggi
            result = self.antrian.pop()
            if result is None:
                break
            lantai_target, pnp, tipe = result

            print(f"  🎯 Target: Lantai {lantai_target} "
                  f"({'JEMPUT ' + pnp.nama if tipe == 'PICKUP' and pnp else 'ANTAR penumpang'})")

            # 3. Gerak ke lantai target
            self._bergerak_ke(lantai_target)

            # 4. Buka pintu
            self._buka_pintu()

            # 5. Turunkan penumpang
            self._turunkan_penumpang()

            # 6. Naikkan penumpang (hanya jika PICKUP)
            if tipe == "PICKUP" and pnp:
                self._naikkan_penumpang(pnp)

            # Update arah setelah naik/turun penumpang
            self._update_arah()

            # 7. Tutup pintu
            self._tutup_pintu()

            # 8. Tampilkan status & cek sisa antrian
            self.tampilkan_status()

            sisa = self.antrian.size()
            if sisa > 0:
                print(f"\n  ⏳ Masih ada {sisa} stop tersisa di antrian...")
            else:
                # Cek apakah masih ada penumpang yang belum sampai
                if self.penumpang:
                    print(f"\n  ⏳ Masih ada {len(self.penumpang)} penumpang "
                          f"dalam lift yang perlu diantar...")

        # Selesai
        self.arah = IDLE
        print(f"\n{'═' * 52}")
        print("  ✅ SEMUA ANTRIAN & PENUMPANG TELAH DIPROSES!")
        print(f"  📍 Lift berhenti di Lantai {self.posisi}")
        print(f"  👥 Penumpang tersisa di dalam: {self.jumlah_penumpang}")
        print(f"{'═' * 52}")

# ─── Penjelasan Blok 3 ──────────────────────────────────────
# Class Lift mengelola: posisi, arah, vektor penumpang (list),
# status pintu, dan antrian prioritas. Method utama adalah
# `proses_semua_antrian()` yang menjalankan loop simulasi.
# Saat penumpang masuk, tujuannya otomatis ditambahkan sebagai
# DROPOFF ke antrian, sehingga priority queue mengelola SEMUA
# pemberhentian (jemput & antar) secara terpadu.
# ─────────────────────────────────────────────────────────────


# ╔════════════════════════════════════════════════════════════╗
# ║  BLOK 4: VALIDASI & MENU INTERAKTIF                       ║
# ╚════════════════════════════════════════════════════════════╝

def _tombol_lantai(lantai: int) -> str:
    """Tombol adaptif: L1=[▲], L8=[▼], L2-7=[▲▼]"""
    if lantai == LANTAI_MIN:
        return "[▲]"
    elif lantai == LANTAI_MAX:
        return "[▼]"
    return "[▲▼]"


def validasi_tombol(lantai_asal: int, lantai_tujuan: int) -> Tuple[bool, str]:
    """
    Validasi tombol adaptif:
    - Lantai 1: hanya tombol NAIK
    - Lantai 8: hanya tombol TURUN
    - Lantai 2-7: tombol NAIK & TURUN
    """
    if not (LANTAI_MIN <= lantai_asal <= LANTAI_MAX):
        return False, f"Lantai asal harus antara {LANTAI_MIN}-{LANTAI_MAX}"
    if not (LANTAI_MIN <= lantai_tujuan <= LANTAI_MAX):
        return False, f"Lantai tujuan harus antara {LANTAI_MIN}-{LANTAI_MAX}"
    if lantai_asal == lantai_tujuan:
        return False, "Lantai asal dan tujuan tidak boleh sama"

    arah = NAIK if lantai_tujuan > lantai_asal else TURUN

    if lantai_asal == LANTAI_MIN and arah == TURUN:
        return False, (f"Lantai {LANTAI_MIN} hanya memiliki tombol [▲ NAIK]. "
                       f"Tidak bisa turun dari sini!")
    if lantai_asal == LANTAI_MAX and arah == NAIK:
        return False, (f"Lantai {LANTAI_MAX} hanya memiliki tombol [▼ TURUN]. "
                       f"Tidak bisa naik dari sini!")

    return True, "OK"


def clear_screen():
    """Bersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def tampilkan_header():
    """Tampilkan header program."""
    print()
    print("  ╔═══════════════════════════════════════════════════╗")
    print("  ║                                                   ║")
    print("  ║   🏢  SISTEM SIMULASI LIFT                        ║")
    print("  ║       GEDUNG CDAST SELATAN UNEJ                   ║")
    print("  ║       Menggunakan Priority Queue                  ║")
    print("  ║                                                   ║")
    print("  ╚═══════════════════════════════════════════════════╝")


def tampilkan_menu():
    """Tampilkan menu utama."""
    print("\n  ┌──────────────── MENU ─────────────────────┐")
    print("  │                                            │")
    print("  │   1.  Tambah Penumpang                     │")
    print("  │   2.  Jalankan Simulasi                    │")
    print("  │   3.  Lihat Status Lift & Gedung           │")
    print("  │   4.  Lihat Isi Antrian                    │")
    print("  │   5.  Demo Otomatis (Data Preset)          │")
    print("  │   6.  Reset Lift                           │")
    print("  │   0.  Keluar                               │")
    print("  │                                            │")
    print("  └────────────────────────────────────────────┘")


def input_penumpang(lift: Lift):
    """Input data penumpang baru dengan validasi tombol adaptif."""
    print("\n  ── TAMBAH PENUMPANG ──────────────────────")
    nama = input("  Nama penumpang  : ").strip()
    if not nama:
        print("   Nama tidak boleh kosong!")
        return

    try:
        asal   = int(input(f"  Lantai asal  ({LANTAI_MIN}-{LANTAI_MAX}): "))
        tujuan = int(input(f"  Lantai tujuan({LANTAI_MIN}-{LANTAI_MAX}): "))
    except ValueError:
        print("   Input harus berupa angka!")
        return

    valid, pesan = validasi_tombol(asal, tujuan)
    if not valid:
        print(f"  ❌ {pesan}")
        return

    penumpang = Penumpang(nama, asal, tujuan)
    lift.tambah_request(penumpang)
    print(f"  ✅ {nama} berhasil ditambahkan ke antrian!")


def lihat_antrian(lift: Lift):
    """Tampilkan seluruh isi antrian saat ini."""
    entries = lift.antrian.peek_all()
    if not entries:
        print("\n  📋 Antrian kosong — tidak ada request.")
        return

    print(f"\n  📋 ANTRIAN ({len(entries)} request)")
    print("  ┌─────┬──────────────┬─────────┬────────────────┐")
    print("  │ No  │ Lantai Stop  │  Tipe   │ Penumpang      │")
    print("  ├─────┼──────────────┼─────────┼────────────────┤")
    for i, (lt, pnp, tipe) in enumerate(entries, 1):
        nama = pnp.nama if pnp else "—"
        print(f"  │ {i:<3} │    L{lt:<8} │ {tipe:<7} │ {nama:<14} │")
    print("  └─────┴──────────────┴─────────┴────────────────┘")


def demo_otomatis(lift: Lift):
    """
    Jalankan demo dengan 9 penumpang preset.
    Sengaja 9 orang agar kapasitas (maks 7) terlampaui → demo penolakan.
    """
    print("\n  🎬 ══ DEMO OTOMATIS ═══════════════════════")
    print("  Skenario: 9 penumpang mendaftar, kapasitas lift = 7")
    print("  ═" * 23)

    data_demo = [
        Penumpang("Andi",   1, 5),
        Penumpang("Budi",   3, 7),
        Penumpang("Citra",  8, 2),
        Penumpang("Diana",  2, 6),
        Penumpang("Eko",    5, 1),
        Penumpang("Fani",   4, 8),
        Penumpang("Galih",  6, 3),
        Penumpang("Hana",   1, 4),
        Penumpang("Irfan",  7, 1),
    ]

    print(f"\n  📋 Daftar {len(data_demo)} penumpang:")
    print("  ┌────────────┬────────┬─────────┬────────┐")
    print("  │ Nama       │  Asal  │ Tujuan  │  Arah  │")
    print("  ├────────────┼────────┼─────────┼────────┤")
    for p in data_demo:
        print(f"  │ {p.nama:<10} │  L{p.lantai_asal:<4} │  L{p.lantai_tujuan:<5} │ {p.arah:<6} │")
    print("  └────────────┴────────┴─────────┴────────┘")

    print()
    for p in data_demo:
        lift.tambah_request(p)

    input("\n  ⏎  Tekan ENTER untuk mulai simulasi...")
    lift.proses_semua_antrian()

# ─── Penjelasan Blok 4 ──────────────────────────────────────
# Fungsi-fungsi UI: validasi tombol adaptif (L1=▲, L8=▼,
# L2-7=▲▼), input penumpang dengan error handling, display
# antrian, dan demo otomatis dengan 9 penumpang preset.
# ─────────────────────────────────────────────────────────────


# ╔════════════════════════════════════════════════════════════╗
# ║  BLOK 5: MAIN — MERAKIT SEMUA LEGO                        ║
# ╚════════════════════════════════════════════════════════════╝

def main():
    """
    Titik masuk program.
    Merakit semua blok: buat objek Lift → tampilkan menu → loop.
    """
    clear_screen()
    tampilkan_header()

    # Inisialisasi lift (posisi awal: Lantai 1, arah: IDLE)
    lift = Lift()

    while True:
        tampilkan_menu()
        pilihan = input("\n  Pilihan Anda ▶ ").strip()

        if pilihan == "1":
            input_penumpang(lift)

        elif pilihan == "2":
            if lift.antrian.is_empty():
                print("\n  ⚠️  Antrian kosong! Tambah penumpang terlebih dahulu.")
            else:
                print("\n  🚀 Memulai simulasi...")
                lift.proses_semua_antrian()

        elif pilihan == "3":
            lift.tampilkan_gedung()
            lift.tampilkan_status()

        elif pilihan == "4":
            lihat_antrian(lift)

        elif pilihan == "5":
            lift = Lift()  # Reset sebelum demo
            demo_otomatis(lift)

        elif pilihan == "6":
            lift = Lift()
            print("\n  🔄 Lift berhasil direset ke kondisi awal (Lantai 1, IDLE).")

        elif pilihan == "0":
            print("\n  👋 Terima kasih telah menggunakan Simulasi Lift CDAST!")
            print("     Sampai jumpa!\n")
            break

        else:
            print("\n  ❌ Pilihan tidak valid! Masukkan angka 0-6.")


# ── Cara Menjalankan ─────────────────────────────────────────
# Cukup jalankan file ini langsung:
#   python "struktur data, demo.py"
#
# Atau import dan panggil main():
#   from struktur_data_demo import main
#   main()
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
