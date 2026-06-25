import csv
import os

class NodePasien:
    """Node untuk struktur data Queue (Linked List Based)"""
    def __init__(self, id_pasien, nama, keluhan):
        self.id_pasien = id_pasien
        self.nama = nama
        self.keluhan = keluhan
        self.next = None

class QueueKlinik:
    """Implementasi Struktur Data Queue menggunakan Linked List"""
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, id_pasien, nama, keluhan):
        new_node = NodePasien(id_pasien, nama, keluhan)
        if self.tail is None:
            self.head = self.tail = new_node
            return
        self.tail.next = new_node
        self.tail = new_node

    def dequeue(self):
        if self.head is None:
            return None
        temp = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return temp

    def is_empty(self):
        return self.head is None

class SistemRumahSakit:
    def __init__(self):
        self.csv_file = 'pasien.csv'
        self.antrean = QueueKlinik()
        self.database_pasien = {} # Hash Map untuk simpan rekam medis (ID: Data)
        self.load_from_csv()

    # --- DATABASE OPERATIONS (CSV) ---
    def load_from_csv(self):
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.database_pasien[row['id_pasien']] = {
                        'nama': row['nama'],
                        'usia': row['usia'],
                        'diagnosis': row['diagnosis']
                    }

    def save_to_csv(self):
        with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['id_pasien', 'nama', 'usia', 'diagnosis']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for id_p, data in self.database_pasien.items():
                writer.writerow({
                    'id_pasien': id_p,
                    'nama': data['nama'],
                    'usia': data['usia'],
                    'diagnosis': data['diagnosis']
                })

    # --- CRUD OPERATIONS ---
    def create_pasien(self, id_pasien, nama, usia, diagnosis="Belum Diperiksa"):
        """CREATE"""
        if id_pasien in self.database_pasien:
            print("[-] ID Pasien sudah terdaftar!")
            return False
        self.database_pasien[id_pasien] = {
            'nama': nama,
            'usia': usia,
            'diagnosis': diagnosis
        }
        self.save_to_csv()
        print("[+] Pasien berhasil didaftarkan ke sistem.")
        return True

    def read_all_pasien(self):
        """READ (with Sorting)"""
        if not self.database_pasien:
            print("[-] Belum ada data pasien.")
            return
        
        # Sorting berdasarkan Nama menggunakan Bubble Sort/Teks biasa
        sorted_keys = sorted(self.database_pasien.keys(), key=lambda k: self.database_pasien[k]['nama'])
        
        print("\n=== DAFTAR REKAM MEDIS PASIEN (Terurut Nama) ===")
        for id_p in sorted_keys:
            p = self.database_pasien[id_p]
            print(f"ID: {id_p} | Nama: {p['nama']} | Usia: {p['usia']} Thn | Diagnosis: {p['diagnosis']}")

    def update_diagnosis(self, id_pasien, diagnosis_baru):
        """UPDATE"""
        if id_pasien in self.database_pasien:
            self.database_pasien[id_pasien]['diagnosis'] = diagnosis_baru
            self.save_to_csv()
            print("[+] Diagnosis pasien berhasil diperbarui.")
        else:
            print("[-] ID Pasien tidak ditemukan.")

    def delete_pasien(self, id_pasien):
        """DELETE"""
        if id_pasien in self.database_pasien:
            del self.database_pasien[id_pasien]
            self.save_to_csv()
            print("[+] Data rekam medis pasien berhasil dihapus.")
        else:
            print("[-] ID Pasien tidak ditemukan.")

    # --- SEARCHING & QUEUE FEATURES ---
    def cari_pasien(self, id_pasien):
        """SEARCHING menggunakan Hash Map (O(1))"""
        pasien = self.database_pasien.get(id_pasien)
        if pasien:
            print(f"\n[ Data Ditemukan ]\nID: {id_pasien}\nNama: {pasien['nama']}\nUsia: {pasien['usia']}\nDiagnosis: {pasien['diagnosis']}")
        else:
            print("[-] Pasien dengan ID tersebut tidak ditemukan.")

    def tambah_ke_antrean(self, id_pasien, keluhan):
        if id_pasien not in self.database_pasien:
            print("[-] ID Pasien tidak terdaftar di sistem. Daftarkan dulu via Menu 1.")
            return
        nama = self.database_pasien[id_pasien]['nama']
        self.antrean.enqueue(id_pasien, nama, keluhan)
        print(f"[+] {nama} berhasil dimasukkan ke antrean poliklinik.")

    def panggil_antrean(self):
        pasien_sekarang = self.antrean.dequeue()
        if pasien_sekarang is None:
            print("[-] Antrean kosong.")
            return
        
        print(f"\n[ Memeriksa Pasien ]\nNama: {pasien_sekarang.nama}\nKeluhan: {pasien_sekarang.keluhan}")
        diagnosis = input("Masukkan hasil diagnosis dokter: ")
        self.update_diagnosis(pasien_sekarang.id_pasien, diagnosis)

# --- MENU INTERFACE (CLI) ---
def main():
    rs = SistemRumahSakit()
    
    while True:
        print("\n" + "="*40)
        print("  SISTEM REKAM MEDIS & ANTRIAN RS  ")
        print("="*40)
        print("1. Registrasi Pasien Baru (Create)")
        print("2. Masukkan Pasien ke Antrean Poliklinik")
        print("3. Panggil & Periksa Pasien Terdepan (Dequeue + Update)")
        print("4. Lihat Semua Rekam Medis Pasien (Read + Sort)")
        print("5. Cari Rekam Medis Pasien (Search)")
        print("6. Hapus Data Pasien (Delete)")
        print("7. Keluar Aplikasi")
        pilihan = input("Pilih menu (1-7): ")

        if pilihan == '1':
            id_p = input("Masukkan ID Pasien Baru (cth: P01): ")
            nama = input("Masukkan Nama: ")
            usia = input("Masukkan Usia: ")
            rs.create_pasien(id_p, nama, usia)
        elif pilihan == '2':
            id_p = input("Masukkan ID Pasien: ")
            keluhan = input("Keluhan utama: ")
            rs.tambah_ke_antrean(id_p, keluhan)
        elif pilihan == '3':
            rs.panggil_antrean()
        elif pilihan == '4':
            rs.read_all_pasien()
        elif pilihan == '5':
            id_p = input("Masukkan ID Pasien yang dicari: ")
            rs.cari_pasien(id_p)
        elif pilihan == '6':
            id_p = input("Masukkan ID Pasien yang ingin dihapus: ")
            rs.delete_pasien(id_p)
        elif pilihan == '7':
            print("[+] Terima kasih telah menggunakan sistem.")
            break
        else:
            print("[-] Pilihan tidak valid.")

if __name__ == "__main__":
    main()