import tkinter as tk
from tkinter import messagebox

class Siswa:
    def __init__(self, nis, nama, nilai, evaluasi):
        self.nis = nis
        self.nama = nama
        self.nilai = nilai
        self.evaluasi = evaluasi

    def __str__(self):
        return f"{self.nis} {self.nama} {self.nilai} {self.evaluasi}"

class ManajemenSiswa:
    def __init__(self, filename):
        self.filename = filename
        self.siswa_list = self.load_data()

    def load_data(self):
        siswa_list = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    nis, nama, nilai, evaluasi = line.strip().split(',')
                    siswa_list.append(Siswa(nis, nama, int(nilai), evaluasi))
        except FileNotFoundError:
            pass
        return siswa_list

    def save_data(self):
        with open(self.filename, 'w') as file:
            for siswa in self.siswa_list:
                file.write(f"{siswa.nis},{siswa.nama},{siswa.nilai},{siswa.evaluasi}\n")

    def tambah_siswa(self, nis, nama, nilai, evaluasi):
        self.siswa_list.append(Siswa(nis, nama, nilai, evaluasi))
        self.save_data()

    def update_siswa(self, nis, nama_baru=None, nilai_baru=None, evaluasi_baru=None):
        for siswa in self.siswa_list:
            if siswa.nis == nis:
                if nama_baru is not None:
                    siswa.nama = nama_baru
                if nilai_baru is not None:
                    siswa.nilai = nilai_baru
                if evaluasi_baru is not None:
                    siswa.evaluasi = evaluasi_baru
                self.save_data()
                return True
        return False

    def hapus_siswa(self, nis):
        self.siswa_list = [siswa for siswa in self.siswa_list if siswa.nis != nis]
        self.save_data()

    def bubble_sort_by_name(self):
        n = len(self.siswa_list)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.siswa_list[j].nama > self.siswa_list[j+1].nama:
                    self.siswa_list[j], self.siswa_list[j+1] = self.siswa_list[j+1], self.siswa_list[j]

    def bubble_sort_by_nilai(self):
        n = len(self.siswa_list)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.siswa_list[j].nilai < self.siswa_list[j+1].nilai:
                    self.siswa_list[j], self.siswa_list[j+1] = self.siswa_list[j+1], self.siswa_list[j]

    def binary_search_by_name(self, target):
        self.bubble_sort_by_name()
        low = 0
        high = len(self.siswa_list) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.siswa_list[mid].nama == target:
                return self.siswa_list[mid]
            elif self.siswa_list[mid].nama < target:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def binary_search_by_nis(self, target):
        self.siswa_list.sort(key=lambda siswa: siswa.nis)
        low = 0
        high = len(self.siswa_list) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.siswa_list[mid].nis == target:
                return self.siswa_list[mid]
            elif self.siswa_list[mid].nis < target:
                low = mid + 1
            else:
                high = mid - 1
        return None
class AplikasiManajemenSiswa:
    def __init__(self, root):
        self.root = root
        self.root.title("Manajemen Siswa")
        self.manajemen = ManajemenSiswa("data_siswa.txt")
        
        self.create_widgets()

    def create_widgets(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=20)

        tk.Label(self.menu_frame, text="Menu:").grid(row=0, column=0, columnspan=2)
        
        tk.Button(self.menu_frame, text="Tambah Siswa", command=self.show_tambah_siswa).grid(row=1, column=0, pady=5)
        tk.Button(self.menu_frame, text="Update Siswa", command=self.show_update_siswa).grid(row=1, column=1, pady=5)
        tk.Button(self.menu_frame, text="Hapus Siswa", command=self.show_hapus_siswa).grid(row=2, column=0, pady=5)
        tk.Button(self.menu_frame, text="Lihat Siswa Berdasarkan Nama", command=self.lihat_siswa_berdasarkan_nama).grid(row=2, column=1, pady=5)
        tk.Button(self.menu_frame, text="Lihat Siswa Berdasarkan Nilai", command=self.lihat_siswa_berdasarkan_nilai).grid(row=3, column=0, pady=5)
        tk.Button(self.menu_frame, text="Cari Siswa Berdasarkan Nama", command=self.show_cari_siswa_berdasarkan_nama).grid(row=3, column=1, pady=5)
        tk.Button(self.menu_frame, text="Cari Siswa Berdasarkan NIS", command=self.show_cari_siswa_berdasarkan_nis).grid(row=4, column=0, pady=5)
        tk.Button(self.menu_frame, text="Keluar", command=self.root.quit).grid(row=4, column=1, pady=5)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=20)

        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(pady=20)

    def clear_output(self):
        for widget in self.output_frame.winfo_children():
            widget.destroy()

    def clear_input(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

    def show_tambah_siswa(self):
        self.clear_input()
        tk.Label(self.input_frame, text="NIS:").grid(row=0, column=0)
        self.nis_entry = tk.Entry(self.input_frame)
        self.nis_entry.grid(row=0, column=1)
        self.nis_entry.config(validate="key", validatecommand=(self.root.register(self.validate_nis), '%P'))

        tk.Label(self.input_frame, text="Nama:").grid(row=1, column=0)
        self.nama_entry = tk.Entry(self.input_frame)
        self.nama_entry.grid(row=1, column=1)
        self.nama_entry.config(validate="key", validatecommand=(self.root.register(self.validate_nama), '%P'))

        tk.Label(self.input_frame, text="Nilai:").grid(row=2, column=0)
        self.nilai_entry = tk.Entry(self.input_frame)
        self.nilai_entry.grid(row=2, column=1)
        self.nilai_entry.config(validate="key", validatecommand=(self.root.register(self.validate_nilai), '%P'))

        tk.Label(self.input_frame, text="Evaluasi:").grid(row=3, column=0)
        self.evaluasi_entry = tk.Entry(self.input_frame)
        self.evaluasi_entry.grid(row=3, column=1)

        tk.Button(self.input_frame, text="Tambah", command=self.tambah_siswa).grid(row=4, column=0, columnspan=2, pady=5)

    def validate_nis(self, nis):
        if nis == "":
            return True
        return len(nis) <= 4 and nis.isdigit()

    def validate_nama(self, nama):
        if nama == "":
            return True
        valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .'-"
        for char in nama:
            if char not in valid_chars:
                return False
        return True

    def validate_nilai(self, nilai):
        if nilai == "":
            return True
        if nilai.isdigit():
            nilai_int = int(nilai)
            return 0 <= nilai_int <= 100
        return False

    def tambah_siswa(self):
        nis = self.nis_entry.get()
        nama = self.nama_entry.get()
        nilai = self.nilai_entry.get()
        evaluasi = self.evaluasi_entry.get()

        if nis and nama and nilai and evaluasi:
            self.manajemen.tambah_siswa(nis, nama, int(nilai), evaluasi)
            messagebox.showinfo("Sukses", "Siswa berhasil ditambahkan.")
            self.clear_input()
        else:
            messagebox.showwarning("Error", "Data tidak lengkap.")

    def show_update_siswa(self):
        self.clear_input()
        tk.Label(self.input_frame, text="NIS:").grid(row=0, column=0)
        self.nis_entry = tk.Entry(self.input_frame)
        self.nis_entry.grid(row=0, column=1)
        self.nis_entry.config(validate="key", validatecommand=(self.root.register(self.validate_nis), '%P'))

        tk.Label(self.input_frame, text="Nama Baru:").grid(row=1, column=0)
        self.nama_baru_entry = tk.Entry(self.input_frame)
        self.nama_baru_entry.grid(row=1, column=1)
        self.nama_baru_entry.config(validate="key", validatecommand=(self.root.register(self.validate_nama), '%P'))

        tk.Label(self.input_frame, text="Nilai Baru:").grid(row=2, column=0)
        self.nilai_baru_entry = tk.Entry(self.input_frame)
        self.nilai_baru_entry.grid(row=2, column=1)
        self.nilai_baru_entry.config(validate="key", validatecommand=(self.root.register(self.validate_nilai), '%P'))

        tk.Label(self.input_frame, text="Evaluasi Baru:").grid(row=3, column=0)
        self.evaluasi_baru_entry = tk.Entry(self.input_frame)
        self.evaluasi_baru_entry.grid(row=3, column=1)

        tk.Button(self.input_frame, text="Update", command=self.update_siswa).grid(row=4, column=0, columnspan=2, pady=5)
        
def update_siswa(self):
        nis = self.nis_entry.get()
        nama_baru = self.nama_baru_entry.get()
        nilai_baru = self.nilai_baru_entry.get()
        evaluasi_baru = self.evaluasi_baru_entry.get()

        if nis:
            if self.manajemen.update_siswa(nis, 
                                           nama_baru if nama_baru else None, 
                                           int(nilai_baru) if nilai_baru else None, 
                                           evaluasi_baru if evaluasi_baru else None):
                messagebox.showinfo("Sukses", "Siswa berhasil diupdate.")
                self.clear_input()
            else:
                messagebox.showwarning("Error", "Siswa tidak ditemukan.")
        else:
            messagebox.showwarning("Error", "NIS tidak boleh kosong.")

    def show_hapus_siswa(self):
        self.clear_input()
        tk.Label(self.input_frame, text="NIS:").grid(row=0, column=0)
        self.nis_entry = tk.Entry(self.input_frame)
        self.nis_entry.grid(row=0, column=1)
        self.nis_entry.config(validate="key", validatecommand=(self.root.register(self.validate_nis), '%P'))

        tk.Button(self.input_frame, text="Hapus", command=self.hapus_siswa).grid(row=1, column=0, columnspan=2, pady=5)

    def hapus_siswa(self):
        nis = self.nis_entry.get()

        if nis:
            self.manajemen.hapus_siswa(nis)
            messagebox.showinfo("Sukses", "Siswa berhasil dihapus.")
            self.clear_input()
        else:
            messagebox.showwarning("Error", "NIS tidak boleh kosong.")

    def lihat_siswa_berdasarkan_nama(self):
        self.clear_output()
        self.manajemen.bubble_sort_by_name()
        if not self.manajemen.siswa_list:
            messagebox.showinfo("Info", "Tidak ada siswa yang tersedia.")
        else:
            self.tampilkan_siswa(self.manajemen.siswa_list)

    def lihat_siswa_berdasarkan_nilai(self):
        self.clear_output()
        self.manajemen.bubble_sort_by_nilai()
        if not self.manajemen.siswa_list:
            messagebox.showinfo("Info", "Tidak ada siswa yang tersedia.")
        else:
            self.tampilkan_siswa(self.manajemen.siswa_list)

    def tampilkan_siswa(self, siswa_list):
        headers = ["NIS", "Nama", "Nilai", "Evaluasi"]
        for i, header in enumerate(headers):
            tk.Label(self.output_frame, text=header, font=('bold', 12)).grid(row=0, column=i)

        for i, siswa in enumerate(siswa_list, start=1):
            tk.Label(self.output_frame, text=siswa.nis).grid(row=i, column=0)
            tk.Label(self.output_frame, text=siswa.nama).grid(row=i, column=1)
            tk.Label(self.output_frame, text=siswa.nilai).grid(row=i, column=2)
            tk.Label(self.output_frame, text=siswa.evaluasi).grid(row=i, column=3)

    def show_cari_siswa_berdasarkan_nama(self):
        self.clear_input()
        tk.Label(self.input_frame, text="Nama:").grid(row=0, column=0)
        self.nama_entry = tk.Entry(self.input_frame)
        self.nama_entry.grid(row=0, column=1)
        self.nama_entry.config(validate="key", validatecommand=(self.root.register(self.validate_nama), '%P'))

        tk.Button(self.input_frame, text="Cari", command=self.cari_siswa_berdasarkan_nama).grid(row=1, column=0, columnspan=2, pady=5)

    def cari_siswa_berdasarkan_nama(self):
        self.clear_output()
        target = self.nama_entry.get()
        result = self.manajemen.binary_search_by_name(target)
        if result:
            tk.Label(self.output_frame, text="Siswa Ditemukan:", font=('bold', 12)).grid(row=0, column=0, columnspan=4)
            tk.Label(self.output_frame, text=f"NIS: {result.nis}").grid(row=1, column=0, sticky='w')
            tk.Label(self.output_frame, text=f"Nama: {result.nama}").grid(row=2, column=0, sticky='w')
            tk.Label(self.output_frame, text=f"Nilai: {result.nilai}").grid(row=3, column=0, sticky='w')
            tk.Label(self.output_frame, text=f"Evaluasi: {result.evaluasi}").grid(row=4, column=0, sticky='w')
        else:
            messagebox.showinfo("Info", "Siswa tidak ditemukan.")

    def show_cari_siswa_berdasarkan_nis(self):
        self.clear_input()
        tk.Label(self.input_frame, text="NIS:").grid(row=0, column=0)
        self.nis_entry = tk.Entry(self.input_frame)
        self.nis_entry.grid(row=0, column=1)
        self.nis_entry.config(validate="key", validatecommand=(self.root.register(self.validate_nis), '%P'))

        tk.Button(self.input_frame, text="Cari", command=self.cari_siswa_berdasarkan_nis).grid(row=1, column=0, columnspan=2, pady=5)

    def cari_siswa_berdasarkan_nis(self):
        self.clear_output()
        target = self.nis_entry.get()
        result = self.manajemen.binary_search_by_nis(target)
        if result:
            tk.Label(self.output_frame, text="Siswa Ditemukan:", font=('bold', 12)).grid(row=0, column=0, columnspan=4)
            tk.Label(self.output_frame, text=f"NIS: {result.nis}").grid(row=1, column=0, sticky='w')
            tk.Label(self.output_frame, text=f"Nama: {result.nama}").grid(row=2, column=0, sticky='w')
            tk.Label(self.output_frame, text=f"Nilai: {result.nilai}").grid(row=3, column=0, sticky='w')
            tk.Label(self.output_frame, text=f"Evaluasi: {result.evaluasi}").grid(row=4, column=0, sticky='w')
        else:
            messagebox.showinfo("Info", "Siswa tidak ditemukan.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiManajemenSiswa(root)
    root.mainloop()
