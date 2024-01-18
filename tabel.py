from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

class DataGuru(Tk):
    def __init__(self):
        super().__init__()
        self.title("Registrasi Data Siswa")
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
        Label(self, text="NIS").grid(row=0, column=0, padx=10, pady=10)
        self.Nis_entry = Entry(self, width=50)
        self.Nis_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self, text="Nama").grid(row=1, column=0, padx=10, pady=10)
        self.Nama_entry = Entry(self, width=50)
        self.Nama_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(self, text="Jurusan").grid(row=2, column=0, padx=10, pady=10)
        self.Jurusan_entry = Entry(self, width=50)
        self.Jurusan_entry.grid(row=2, column=1, padx=10, pady=10)

        Label(self, text="Alamat").grid(row=3, column=0, padx=10, pady=10)
        self.Alamat_entry = Entry(self, width=50)
        self.Alamat_entry.grid(row=3, column=1, padx=10, pady=10)

        # Menambahkan Treeview
        self.tree = ttk.Treeview(self, columns=("NIS", "Nama", "Jurusan","Alamat"), show="headings")
        self.tree.heading("NIS", text="NIS")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Jurusan", text="Jurusan")
        self.tree.heading("Alamat", text="Alamat")
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
        self.Nis_entry.insert(0, data[0])
        self.Nama_entry.insert(0, data[1])
        self.Jurusan_entry.insert(0, data[2])
        self.Alamat_entry.insert(0, data[3])

        # Menambahkan tombol update di form
        Button(self, text="Update", command=lambda:
        self.proses_update(data[0])).grid(row=4, column=1, columnspan=2, pady=10)

    
    def simpan_data(self):
        Nis = self.Nis_entry.get()
        Nama = self.Nama_entry.get()
        Jurusan = self.Jurusan_entry.get()
        Alamat = self.Alamat_entry.get()
        query = "INSERT INTO siswa (Nis, Nama, Jurusan, Alamat) VALUES (%s,%s, %s, %s)"
        values = (Nis, Nama, Jurusan, Alamat)
        
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        self.Nis_entry.delete(0, END)
        self.Nama_entry.delete(0, END)
        self.Jurusan_entry.delete(0, END)
        self.Alamat_entry.delete(0, END)

    def tampilkan_data(self):
        # Hapus data pada treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ambil data dari database
        self.cursor.execute("SELECT * FROM siswa")
        data = self.cursor.fetchall()

        #Masukkan data ke treeview
        for row in data:
            self.tree.insert("", "end", values=row)

    def proses_update(self, nis_to_update):
        Nis = self.Nis_entry.get()
        Nama = self.Nama_entry.get()
        Jurusan = self.Jurusan_entry.get()
        Alamat = self.Alamat_entry.get()

        query = "UPDATE siswa SET nis=%s, nama=%s, jurusan=%s, alamat=%s WHERE nis=%s"
        values = (Nis, Nama, Jurusan, Alamat, nis_to_update)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil diupdate!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        # Bersihkan form setelah update
        self.Nis_entry.delete(0, END)
        self.Nama_entry.delete(0, END)
        self.Jurusan_entry.delete(0, END)
        self.Alamat_entry.delete(0, END)

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
                values = (nis_to_delete,)
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