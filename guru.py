from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

class DataGuru(Tk):
    def __init__(self):
        super().__init__()
        self.title("Registrasi Data Guru")
        self.geometry("400x300")
        
        # Koneksi ke database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="registrasi"
        )

        # Membuat kursor
        self.cursor = self.db.cursor()

        # Membuat dan menampilkan GUI
        self.tampilan_gui()

    def tampilan_gui(self):
        Label(self, text="Kode_Guru").grid(row=0, column=0, padx=10, pady=10)
        self.Kode_Guru_entry = Entry(self, width=50)
        self.Kode_Guru_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self, text="Nama").grid(row=1, column=0, padx=10, pady=10)
        self.Nama_entry = Entry(self, width=50)
        self.Nama_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(self, text="Kelompok_Guru").grid(row=2, column=0, padx=10, pady=10)
        self.Kelompok_Guru_entry = Entry(self, width=50)
        self.Kelompok_Guru_entry.grid(row=2, column=1, padx=10, pady=10)

        Label(self, text="Mata_Pelajaran").grid(row=3, column=0, padx=10, pady=10)
        self.Mata_Pelajaran_entry = Entry(self, width=50)
        self.Mata_Pelajaran_entry.grid(row=3, column=1, padx=10, pady=10)

        # Menambahkan Treeview
        self.tree = ttk.Treeview(self, columns=("Kode_Guru", "Nama", "Kelompok_Guru","Mata_Pelajaran"), show="headings")
        self.tree.heading("Kode_Guru", text="Kode_Guru")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Kelompok_Guru", text="Kelompok_Guru")
        self.tree.heading("Mata_Pelajaran", text="Mata_Pelajaran")
        self.tree.grid(row=5, column=0, columnspan=8, pady=10, padx=10)

        Button(self, text="Simpan Data", command=self.simpan_data).grid(row=4, column=0, columnspan=2, pady=10)

                # Menambahkan tombol refresh data
        Button(self, text="Refresh Data",
        command=self.tampilkan_data).grid(row=6, column=0, columnspan=2, pady=10,
        padx=10)

        # Menambahkan tombol update data
        Button(self, text="Update Data", command=self.update_data).grid(row=6, column=2, columnspan=2, pady=10, padx=10)
        
        # Menambahkan tombol delete data
        Button(self, text="Delete Data", command=self.hapus_data).grid(row=6,
        column=1, columnspan=2, pady=10, padx=10)
        
        self.tampilkan_data()


    def update_data(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan diupdate.")
            return

        # Ambil data terpilih dari treeview
        data = self.tree.item(selected_item[0], 'values')

        # Tampilkan form update dengan data terpilih
        self.Kode_Guru_entry.insert(0, data[0])
        self.Nama_entry.insert(0, data[1])
        self.Kelompok_Guru_entry.insert(0, data[2])
        self.Mata_Pelajaran_entry.insert(0, data[3])

        # Menambahkan tombol update di form
        Button(self, text="Update", command=lambda:
        self.proses_update(data[0])).grid(row=4, column=1, columnspan=2, pady=10)

    
    def simpan_data(self):
        Kode_Guru = self.Kode_Guru_entry.get()
        Nama = self.Nama_entry.get()
        Kelompok_Guru = self.Kelompok_Guru_entry.get()
        Mata_Pelajaran = self.Mata_Pelajaran_entry.get()
        query = "INSERT INTO guru (kode_guru, nama_guru, kelompok_guru, mata_pelajaran) VALUES (%s,%s, %s, %s)"
        values = (Kode_Guru, Nama, Kelompok_Guru, Mata_Pelajaran)
        
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        self.Kode_Guru_entry.delete(0, END)
        self.Nama_entry.delete(0, END)
        self.Kelompok_Guru_entry.delete(0, END)
        self.Mata_Pelajaran_entry.delete(0, END)

    def tampilkan_data(self):
        # Hapus data pada treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ambil data dari database
        self.cursor.execute("SELECT * FROM guru")
        data = self.cursor.fetchall()

        #Masukkan data ke treeview
        for row in data:
            self.tree.insert("", "end", values=row)

    def proses_update(self, kode_guru_to_update):
        Kelompok_Guru = self.Kelompok_Guru_entry.get()
        Nama = self.Nama_entry.get()
        Kode_Guru = self.Kode_Guru_entry.get()
        Mata_Pelajaran = self.Mata_Pelajaran_entry.get()

        query = "UPDATE guru SET kode_guru=%s, nama_guru=%s, kelompok_guru=%s, mata_pelajaran=%s WHERE Kode_Guru=%s"
        values = (Kode_Guru, Nama, Kode_Guru, Mata_Pelajaran, kode_guru_to_update)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil diupdate!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        # Bersihkan form setelah update
        self.Kode_Guru_entry.delete(0, END)
        self.Nama_entry.delete(0, END)
        self.Kelompok_Guru_entry.delete(0, END)
        self.Mata_Pelajaran_entry.delete(0, END)

        # Tampilkan kembali data setelah diupdate
        self.tampilkan_data()

    def hapus_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus.")
            return
        confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")

        if confirmation:
            for item in selected_item:
                data = self.tree.item(item, 'values')
                nis_to_delete = data[0]
                query = "DELETE FROM siswa WHERE nis = %s"
                values = ("kode_guru_to_delete")
                try:
                    self.cursor.execute(query, values)
                    self.db.commit()
                    messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                except Exception as e:
                    messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        self.tampilkan_data()

if __name__== "__main__":
    app = DataGuru()
    app.mainloop()