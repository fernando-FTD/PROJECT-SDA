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
