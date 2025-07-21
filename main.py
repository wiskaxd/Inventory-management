import json
import os
import csv

# Konstanta
DATA_FILE = 'inventory_data.json'
CSV_FILE = 'inventaris.csv'

# Kelas Item
class Item:
    def __init__(self, item_id, nama, jumlah, harga):
        self.item_id = item_id
        self.nama = nama
        self.jumlah = jumlah
        self.harga = harga

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'nama': self.nama,
            'jumlah': self.jumlah,
            'harga': self.harga
        }

    @staticmethod
    def from_dict(data):
        return Item(data['item_id'], data['nama'], data['jumlah'], data['harga'])

# Manajer Inventaris
class InventoryManager:
    def __init__(self):
        self.inventaris = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                self.inventaris = [Item.from_dict(item) for item in data]

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump([item.to_dict() for item in self.inventaris], f, indent=4)

    def tambah_item(self, item):
        self.inventaris.append(item)
        self.save_data()

    def tampilkan_inventaris(self, urut_berdasarkan=None):
        if not self.inventaris:
            print("\nInventaris kosong.\n")
            return

        inventaris_terurut = self.inventaris
        if urut_berdasarkan == "harga":
            inventaris_terurut = sorted(self.inventaris, key=lambda x: x.harga)
        elif urut_berdasarkan == "stok":
            inventaris_terurut = sorted(self.inventaris, key=lambda x: x.jumlah)

        print("\nInventaris Saat Ini:")
        print("+------+----------------------+--------+--------+")
        print("| ID   | Nama                 | Jumlah | Harga  |")
        print("+------+----------------------+--------+--------+")
        for item in inventaris_terurut:
            print(f"| {item.item_id:<4} | {item.nama:<20} | {item.jumlah:^6} | Rp{item.harga:<6.2f} |")
        print("+------+----------------------+--------+--------+")

    def edit_item(self, item_id):
        for item in self.inventaris:
            if item.item_id == item_id:
                nama = input("Masukkan nama baru (kosongkan jika tidak diubah): ") or item.nama
                jumlah = input("Masukkan jumlah baru (kosongkan jika tidak diubah): ")
                harga = input("Masukkan harga baru (kosongkan jika tidak diubah): ")

                if jumlah:
                    if not jumlah.isdigit():
                        print("Jumlah tidak valid!")
                        return
                    item.jumlah = int(jumlah)
                if harga:
                    try:
                        item.harga = float(harga)
                    except ValueError:
                        print("Harga tidak valid!")
                        return

                item.nama = nama
                self.save_data()
                print("Item berhasil diperbarui.")
                return
        print("ID item tidak ditemukan.")

    def hapus_item(self, item_id):
        for item in self.inventaris:
            if item.item_id == item_id:
                self.inventaris.remove(item)
                self.save_data()
                print("Item berhasil dihapus.")
                return
        print("ID item tidak ditemukan.")

    def cek_stok_rendah(self):
        print("\nItem dengan Stok Rendah (Jumlah < 50):")
        stok_rendah = [item for item in self.inventaris if item.jumlah < 50]
        if not stok_rendah:
            print("Semua item memiliki stok yang cukup.\n")
        else:
            for item in stok_rendah:
                print(f"ID: {item.item_id}, Nama: {item.nama}, Jumlah: {item.jumlah}")

    def cari_item(self, kata_kunci):
        hasil = [item for item in self.inventaris if kata_kunci.lower() in item.item_id.lower() or kata_kunci.lower() in item.nama.lower()]
        if not hasil:
            print("Item tidak ditemukan.")
        else:
            print("\nHasil Pencarian:")
            print("+------+----------------------+--------+--------+")
            print("| ID   | Nama                 | Jumlah | Harga  |")
            print("+------+----------------------+--------+--------+")
            for item in hasil:
                print(f"| {item.item_id:<4} | {item.nama:<20} | {item.jumlah:^6} | Rp{item.harga:<6.2f} |")
            print("+------+----------------------+--------+--------+")

    def ekspor_csv(self):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Nama', 'Jumlah', 'Harga'])
            for item in self.inventaris:
                writer.writerow([item.item_id, item.nama, item.jumlah, item.harga])
        print(f"Inventaris berhasil diekspor ke '{CSV_FILE}'")

    def cetak_struk(self):
        print("\n===== Struk Inventaris Saat Ini =====")
        total = 0
        for item in self.inventaris:
            subtotal = item.jumlah * item.harga
            print(f"{item.nama} (x{item.jumlah}) - Rp{subtotal:,.2f}")
            total += subtotal
        print(f"Total Nilai Inventaris: Rp{total:,.2f}")
        print("=====================================")

# Menu CLI
def tampilkan_menu():
    print("""
+----------------------------------------------+
|     Sistem Manajemen Inventaris Barang       |
+----+-----------------------------------------+
| No | Menu                                    |
+----+-----------------------------------------+
| 1  | Tambah Item                             |
| 2  | Lihat Inventaris                        |
| 3  | Edit Item                               |
| 4  | Hapus Item                              |
| 5  | Cek Stok Rendah                         |
| 6  | Keluar                                  |
| 7  | Cari Item                               |
| 8  | Ekspor ke CSV                           |
| 9  | Urutkan Inventaris (Harga/Jumlah)       |
| 10 | Cetak Struk Inventaris                  |
+----+-----------------------------------------+
""")

def input_angka(prompt, desimal=False):
    while True:
        value = input(prompt)
        try:
            return float(value) if desimal else int(value)
        except ValueError:
            print("Input tidak valid. Harus berupa angka.")

# Loop Utama
if __name__ == '__main__':
    manajer = InventoryManager()

    while True:
        tampilkan_menu()
        pilihan = input("Masukkan pilihan Anda (1-10): ")

        if pilihan == '1':
            item_id = input("Masukkan ID Item: ")
            nama = input("Masukkan Nama Item: ")
            jumlah = input_angka("Masukkan Jumlah: ")
            harga = input_angka("Masukkan Harga: Rp", desimal=True)
            manajer.tambah_item(Item(item_id, nama, jumlah, harga))
            print("Item berhasil ditambahkan.\n")

        elif pilihan == '2':
            manajer.tampilkan_inventaris()

        elif pilihan == '3':
            item_id = input("Masukkan ID Item yang akan diedit: ")
            manajer.edit_item(item_id)

        elif pilihan == '4':
            item_id = input("Masukkan ID Item yang akan dihapus: ")
            manajer.hapus_item(item_id)

        elif pilihan == '5':
            manajer.cek_stok_rendah()

        elif pilihan == '6':
            print("Keluar... Sampai jumpa pahari!!!")
            break

        elif pilihan == '7':
            kata_kunci = input("Masukkan ID atau Nama untuk dicari: ")
            manajer.cari_item(kata_kunci)

        elif pilihan == '8':
            manajer.ekspor_csv()

        elif pilihan == '9':
            jenis = input("Urutkan berdasarkan (harga/stok): ").strip().lower()
            if jenis in ["harga", "stok"]:
                manajer.tampilkan_inventaris(urut_berdasarkan=jenis)
            else:
                print("Pilihan pengurutan tidak valid.")

        elif pilihan == '10':
            manajer.cetak_struk()

        else:
            print("Pilihan tidak valid. Masukkan angka antara 1 sampai 10.")
