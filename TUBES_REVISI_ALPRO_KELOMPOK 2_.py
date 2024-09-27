import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import time

# Koneksi database
koneksi_0302 = sqlite3.connect('barbershop.db')
kursor_0302 = koneksi_0302.cursor()

# Membuat tabel
kursor_0302.execute('''CREATE TABLE IF NOT EXISTS pelanggan_0302 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT,
  kata_sandi TEXT,
  email TEXT
)''')

kursor_0302.execute('''CREATE TABLE IF NOT EXISTS tukang_cukur_0302 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nama TEXT,
  umur INTEGER,
  harga REAL,
  shift_tersisa INTEGER DEFAULT 8
)''')

kursor_0302.execute('''CREATE TABLE IF NOT EXISTS reservasi_0302 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pelanggan_id INTEGER,
  waktu TEXT,
  tukang_cukur_id INTEGER,
  status INTEGER DEFAULT 0, -- 0: pending, 1: completed
  FOREIGN KEY(pelanggan_id) REFERENCES pelanggan_0302(id),
  FOREIGN KEY(tukang_cukur_id) REFERENCES tukang_cukur_0302(id)
)''')

kursor_0302.execute('''CREATE TABLE IF NOT EXISTS dompet_0302 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pelanggan_id INTEGER,
  saldo REAL,
  FOREIGN KEY(pelanggan_id) REFERENCES pelanggan_0302(id)
)''')

kursor_0302.execute('''CREATE TABLE IF NOT EXISTS jadwal_0302 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tukang_cukur_id INTEGER,
  waktu TEXT,
  tersedia INTEGER,
  FOREIGN KEY(tukang_cukur_id) REFERENCES tukang_cukur_0302(id)
)''')

kursor_0302.execute('''CREATE TABLE IF NOT EXISTS transaksi_0302 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pelanggan_id INTEGER,
  tukang_cukur_id INTEGER,
  jumlah REAL,
  FOREIGN KEY(pelanggan_id) REFERENCES pelanggan_0302(id),
  FOREIGN KEY(tukang_cukur_id) REFERENCES tukang_cukur_0302(id)
)''')

koneksi_0302.commit()

# Menambahkan data tukang cukur
tukang_cukur_0302 = [
  (1, 'Muhammad Alif Rifki', 19, 100000, 8),
  (2, 'MK', 18, 120000, 8),
  (3, 'Faza Azah Gafafah', 21, 150000, 8),
  (4, 'Tamagochi', 22, 130000, 8)
]

kursor_0302.executemany("INSERT INTO tukang_cukur_0302 (id, nama, umur, harga, shift_tersisa) VALUES (?, ?, ?, ?, ?)", tukang_cukur_0302)
koneksi_0302.commit()

# Menambahkan jadwal awal
jadwal_0302 = [
  (1, '08:00AM - 11:59AM'),
  (2, '12:00PM - 03:59PM'),
  (3, '04:00PM - 07:59PM'),
  (4, '08:00PM - 12:00AM')
]

for tukang_cukur_id_0302, waktu_0302 in jadwal_0302:
  kursor_0302.execute("INSERT INTO jadwal_0302 (tukang_cukur_id, waktu, tersedia) VALUES (?, ?, 1)", (tukang_cukur_id_0302, waktu_0302))
koneksi_0302.commit()

# Menu Utama
def menu_utama_0302():
  while True:
    print("SELAMAT DATANG DI BOJONGSANTOS BARBERSHOP")
    print("1. Pelanggan")
    print("2. Admin")
    print("3. Tentang Kami")
    print("4. Keluar")
    pilihan_0302 = input("Pilih menu: ")

    if pilihan_0302 == '1':
      main_menu_0302()
    elif pilihan_0302 == '2':
      login_admin_0302()
    elif pilihan_0302 == '3':
      tentang_kami_0302()
    elif pilihan_0302 == '4':
      break
    else:
      print("Pilihan tidak valid!")

# Registrasi
def registrasi_0302():
  user_id_0302 = input("User ID: ")
  kata_sandi_0302 = input("Kata Sandi: ")
  email_0302 = input("Email: ")
  kursor_0302.execute("INSERT INTO pelanggan_0302 (user_id, kata_sandi, email) VALUES (?, ?, ?)", (user_id_0302, kata_sandi_0302, email_0302))
  koneksi_0302.commit()
  print("Registrasi berhasil!")

# Login
def login_0302():
  for attempt_0302 in range(3):
    user_id_0302 = input("User ID / Email: ")
    kata_sandi_0302 = input("Kata Sandi: ")
    kursor_0302.execute("SELECT * FROM pelanggan_0302 WHERE (user_id=? OR email=?) AND kata_sandi=?", (user_id_0302, user_id_0302, kata_sandi_0302))
    pelanggan_0302 = kursor_0302.fetchone()
    if pelanggan_0302:
      print("Login berhasil!")
      dasbor_pelanggan_0302(pelanggan_0302[0])
      return
    else:
      print(f"Login gagal, coba lagi! ({attempt_0302 + 1}/3)")
  print("Anda telah mencoba login 3 kali, kembali ke menu utama.")
  menu_utama_0302()

def dasbor_pelanggan_0302(pelanggan_id_0302):
  while True:
    print("Selamat datang di Bojongsantos Barbershop")
    print("1. Reservasi")
    print("2. Style Rambut")
    print("3. Tentang Tukang Cukur")
    print("4. Dompet")
    print("5. Pembayaran")
    print("6. Cek Jadwal")
    print("7. Cek Saldo")
    print("8. Tambah Saldo")
    print("0. Kembali ke Menu Utama")
    pilihan_0302 = input("Pilih menu: ")

    if pilihan_0302 == '1':
      reservasi_0302(pelanggan_id_0302)
    elif pilihan_0302 == '2':
      style_rambut_0302()
    elif pilihan_0302 == '3':
      tentang_tukang_cukur_0302()
    elif pilihan_0302 == '4':
      dompet_0302(pelanggan_id_0302)
    elif pilihan_0302 == '5':
      pembayaran_0302(pelanggan_id_0302)
    elif pilihan_0302 == '6':
      cek_jadwal_0302()
    elif pilihan_0302 == '7':
      cek_saldo_0302(pelanggan_id_0302)
    elif pilihan_0302 == '8':
      tambah_saldo_0302(pelanggan_id_0302)
    elif pilihan_0302 == '0':
      break
    else:
      print("Pilihan tidak valid!")

def cek_jadwal_0302():
  kursor_0302.execute("SELECT id, tukang_cukur_id, waktu, tersedia FROM jadwal_0302")
  jadwal = kursor_0302.fetchall()
  if jadwal:
    print("Jadwal:")
    for id, tukang_cukur_id, waktu, tersedia in jadwal:
      print(f"{id}. Tukang Cukur ID: {tukang_cukur_id}, Waktu: {waktu}, Tersedia: {'Ya' if tersedia else 'Tidak'}")
  else:
    print("Tidak ada jadwal yang tersedia.")

# Reservasi
def reservasi_0302(pelanggan_id_0302):
  kursor_0302.execute("SELECT * FROM tukang_cukur_0302")
  tukang_cukur_0302 = kursor_0302.fetchall()
  tabel_0302 = PrettyTable(["ID", "Nama", "Umur", "Harga", "Shift Tersisa"])
  for tukang_0302 in tukang_cukur_0302:
    tabel_0302.add_row([tukang_0302[0], tukang_0302[1], tukang_0302[2], tukang_0302[3], tukang_0302[4]])
  print(tabel_0302)

  tukang_cukur_id_0302 = input("Masukkan ID Tukang Cukur: ")
  kursor_0302.execute("SELECT * FROM jadwal_0302 WHERE tukang_cukur_id=? AND tersedia=1", (tukang_cukur_id_0302,))
  jadwal_tersedia_0302 = kursor_0302.fetchall()
  if jadwal_tersedia_0302:
    print("Jadwal tersedia:")
    for jadwal in jadwal_tersedia_0302:
      print(f"ID: {jadwal[0]}, Waktu: {jadwal[2]}")
    jadwal_id_0302 = input("Masukkan ID Jadwal yang dipilih: ")
    kursor_0302.execute("INSERT INTO reservasi_0302 (pelanggan_id, waktu, tukang_cukur_id, status) VALUES (?, (SELECT waktu FROM jadwal_0302 WHERE id=?), ?, 0)", (pelanggan_id_0302, jadwal_id_0302, tukang_cukur_id_0302))
    kursor_0302.execute("UPDATE jadwal_0302 SET tersedia=0 WHERE id=?", (jadwal_id_0302,))
    kursor_0302.execute("UPDATE tukang_cukur_0302 SET shift_tersisa=shift_tersisa-1 WHERE id=?", (tukang_cukur_id_0302,))
    koneksi_0302.commit()
    print("Reservasi berhasil!")
  else:
    print("Tidak ada jadwal yang tersedia untuk tukang cukur tersebut.")

# Tentang Kami
def tentang_kami_0302():
  print("Tentang Bojongsantos Barbershop")
  print("Bojongsantos Barbershop adalah barbershop modern dengan berbagai layanan potong rambut dan perawatan pria. Kami memiliki tukang cukur profesional dan berpengalaman.")

# Tentang Tukang Cukur
def tentang_tukang_cukur_0302():
  kursor_0302.execute("SELECT * FROM tukang_cukur_0302")
  tukang_cukur_0302 = kursor_0302.fetchall()
  tabel_0302 = PrettyTable(["ID", "Nama", "Umur", "Harga", "Shift Tersisa"])
  for tukang_0302 in tukang_cukur_0302:
    tabel_0302.add_row([tukang_0302[0], tukang_0302[1], tukang_0302[2], tukang_0302[3], tukang_0302[4]])
  print(tabel_0302)

# Style Rambut
def style_rambut_0302():
  styles_0302 = {
    "Classic Cut": "Potongan rambut klasik dengan tampilan rapi dan elegan.",
    "Undercut": "Potongan rambut dengan sisi dan belakang lebih pendek dari bagian atas.",
    "Fade": "Potongan rambut dengan gradasi panjang dari bawah ke atas.",
    "Pompadour": "Potongan rambut dengan volume besar di bagian atas kepala."
  }
  print("Gaya Rambut:")
  for style_0302, deskripsi_0302 in styles_0302.items():
    print(f"{style_0302}: {deskripsi_0302}")

# Dompet
def dompet_0302(pelanggan_id_0302):
  kursor_0302.execute("SELECT saldo FROM dompet_0302 WHERE pelanggan_id=?", (pelanggan_id_0302,))
  saldo_0302 = kursor_0302.fetchone()
  if saldo_0302:
    print(f"Saldo Anda: {saldo_0302[0]}")
  else:
    kursor_0302.execute("INSERT INTO dompet_0302 (pelanggan_id, saldo) VALUES (?, 0)", (pelanggan_id_0302,))
    koneksi_0302.commit()
    print("Saldo Anda: 0")

# Pembayaran
def pembayaran_0302(pelanggan_id_0302):
    jumlah_0302 = float(input("Masukkan jumlah pembayaran: "))
    kursor_0302.execute("SELECT saldo FROM dompet_0302 WHERE pelanggan_id=?", (pelanggan_id_0302,))
    saldo_0302 = kursor_0302.fetchone()
    if saldo_0302 and saldo_0302[0] >= jumlah_0302:
        kursor_0302.execute("UPDATE dompet_0302 SET saldo=saldo-? WHERE pelanggan_id=?", (jumlah_0302, pelanggan_id_0302))
        kursor_0302.execute("INSERT INTO transaksi_0302 (pelanggan_id, tukang_cukur_id, jumlah) VALUES (?, ?, ?)", (pelanggan_id_0302, None, jumlah_0302))  # Add transaction record
        koneksi_0302.commit()
        kursor_0302.execute("SELECT saldo FROM dompet_0302 WHERE pelanggan_id=?", (pelanggan_id_0302,))
        saldo_terbaru_0302 = kursor_0302.fetchone()[0]
        print("Pembayaran berhasil!")
        print(f"Sisa saldo Anda: {saldo_terbaru_0302}")
        kursor_0302.execute("UPDATE reservasi_0302 SET status=1 WHERE pelanggan_id=? AND status=0", (pelanggan_id_0302,))
        koneksi_0302.commit()
    else:
        print("Saldo tidak cukup!")

def tambah_saldo_0302(pelanggan_id_0302):
  jumlah_tambah_0302 = float(input("Masukkan jumlah saldo yang ingin ditambahkan: "))
  kursor_0302.execute("SELECT saldo FROM dompet_0302 WHERE pelanggan_id=?", (pelanggan_id_0302,))
  saldo_0302 = kursor_0302.fetchone()
  if saldo_0302:
    saldo_baru_0302 = saldo_0302[0] + jumlah_tambah_0302
    kursor_0302.execute("UPDATE dompet_0302 SET saldo=? WHERE pelanggan_id=?", (saldo_baru_0302, pelanggan_id_0302))
  else:
    kursor_0302.execute("INSERT INTO dompet_0302 (pelanggan_id, saldo) VALUES (?, ?)", (pelanggan_id_0302, jumlah_tambah_0302))
  koneksi_0302.commit()
  print(f"Saldo berhasil ditambahkan! Saldo sekarang: {saldo_baru_0302 if saldo_0302 else jumlah_tambah_0302}")

# Cek Saldo
def cek_saldo_0302(pelanggan_id_0302):
  kursor_0302.execute("SELECT saldo FROM dompet_0302 WHERE pelanggan_id=?", (pelanggan_id_0302,))
  saldo_0302 = kursor_0302.fetchone()
  if saldo_0302:
    print(f"Saldo Anda: {saldo_0302[0]}")
  else:
    print("Saldo Anda: 0")

# Login Admin
def login_admin_0302():
  admin_id_0302 = input("Admin ID: ")
  admin_kata_sandi_0302 = input("Kata Sandi: ")
  # Gantilah dengan logika autentikasi admin yang sesuai
  if admin_id_0302 == "admin" and admin_kata_sandi_0302 == "admin":
    print("Login admin berhasil!")
    menu_admin_0302()
  else:
    print("Login admin gagal!")

# Menu Admin
def menu_admin_0302():
  while True:
    print("Menu Admin")
    print("1. Lihat Data Pelanggan")
    print("2. Lihat Data Tukang Cukur")
    print("3. Lihat Data Reservasi")
    print("4. Lihat Data Dompet")
    print("5. Tambah Tukang Cukur")
    print("6. Tambah Jadwal Tukang Cukur")
    print("7. Invoice")
    print("0 Keluar")
    pilihan_0302 = input("Pilih menu: ")

    if pilihan_0302 == '1':
      lihat_data_pelanggan_0302()
    elif pilihan_0302 == '2':
      lihat_data_tukang_cukur_0302()
    elif pilihan_0302 == '3':
      lihat_data_reservasi_0302()
    elif pilihan_0302 == '4':
      lihat_data_dompet_0302()
    elif pilihan_0302 == '5':
      tambah_tukang_cukur_0302()
    elif pilihan_0302 == '6':
      tambah_jadwal_tukang_cukur_0302()
    elif pilihan_0302 == '7':
      invoice_0302()
    elif pilihan_0302 == '8':
      grafik_penjualan_0302()
    elif pilihan_0302 == '0':
      break
    else:
      print("Pilihan tidak valid!")

# Lihat Data Pelanggan
def lihat_data_pelanggan_0302():
  kursor_0302.execute("SELECT * FROM pelanggan_0302")
  pelanggan_0302 = kursor_0302.fetchall()
  tabel_0302 = PrettyTable(["ID", "User ID", "Email"])
  for pelanggan_0302 in pelanggan_0302:
    tabel_0302.add_row([pelanggan_0302[0], pelanggan_0302[1], pelanggan_0302[3]])
  print(tabel_0302)

# Lihat Data Tukang Cukur
def lihat_data_tukang_cukur_0302():
  kursor_0302.execute("SELECT * FROM tukang_cukur_0302")
  tukang_cukur_0302 = kursor_0302.fetchall()
  tabel_0302 = PrettyTable(["ID", "Nama", "Umur", "Harga", "Shift Tersisa"])
  for tukang_cukur_0302 in tukang_cukur_0302:
    tabel_0302.add_row([tukang_cukur_0302[0], tukang_cukur_0302[1], tukang_cukur_0302[2], tukang_cukur_0302[3], tukang_cukur_0302[4]])
  print(tabel_0302)

# Lihat Data Reservasi
def lihat_data_reservasi_0302():
  kursor_0302.execute("SELECT * FROM reservasi_0302")
  reservasi_0302 = kursor_0302.fetchall()
  tabel_0302 = PrettyTable(["ID", "Pelanggan ID", "Waktu", "Tukang Cukur ID", "Status"])
  for reservasi_0302 in reservasi_0302:
    tabel_0302.add_row([reservasi_0302[0], reservasi_0302[1], reservasi_0302[2], reservasi_0302[3], "Selesai" if reservasi_0302[4] == 1 else "Pending"])
  print(tabel_0302)

# Lihat Data Dompet
def lihat_data_dompet_0302():
  kursor_0302.execute("SELECT * FROM dompet_0302")
  dompet_0302 = kursor_0302.fetchall()
  tabel_0302 = PrettyTable(["ID", "Pelanggan ID", "Saldo"])
  for dompet_0302 in dompet_0302:
    tabel_0302.add_row([dompet_0302[0], dompet_0302[1], dompet_0302[2]])
  print(tabel_0302)

# Tambah Tukang Cukur
def tambah_tukang_cukur_0302():
  nama_0302 = input("Nama: ")
  umur_0302 = int(input("Umur: "))
  harga_0302 = float(input("Harga: "))
  shift_tersisa_0302 = 8  # Default shift tersisa
  kursor_0302.execute("INSERT INTO tukang_cukur_0302 (nama, umur, harga, shift_tersisa) VALUES (?, ?, ?, ?)", (nama_0302, umur_0302, harga_0302, shift_tersisa_0302))
  koneksi_0302.commit()
  print("Tukang cukur berhasil ditambahkan!")

# Tambah Jadwal Tukang Cukur
def tambah_jadwal_tukang_cukur_0302():
  tukang_cukur_id_0302 = int(input("Tukang Cukur ID: "))
  waktu_0302 = input("Waktu (YYYY-MM-DD HH:MM:SS): ")
  tersedia_0302 = 1  # Default tersedia
  kursor_0302.execute("INSERT INTO jadwal_0302 (tukang_cukur_id, waktu, tersedia) VALUES (?, ?, ?)", (tukang_cukur_id_0302, waktu_0302, tersedia_0302))
  koneksi_0302.commit()
  print("Jadwal berhasil ditambahkan!")

# Invoice atau Struk Pemesanan
def invoice_0302():
    kursor_0302.execute("""
    SELECT 
        transaksi_0302.id, pelanggan_0302.user_id, transaksi_0302.jumlah, transaksi_0302.tukang_cukur_id 
    FROM 
        transaksi_0302 
    JOIN 
        pelanggan_0302 ON transaksi_0302.pelanggan_id = pelanggan_0302.id
    """)
    transaksi_0302 = kursor_0302.fetchall()
    tabel_0302 = PrettyTable(["ID Transaksi", "User ID Pelanggan", "Jumlah Pembayaran", "Tukang Cukur ID"])
    total_pendapatan = 0
    for transaksi_0302 in transaksi_0302:
        tabel_0302.add_row([transaksi_0302[0], transaksi_0302[1], transaksi_0302[2], transaksi_0302[3]])
        total_pendapatan += transaksi_0302[2]
    print(tabel_0302)
    print(f"Total Pendapatan: {total_pendapatan}")

# Fungsi Grafik Penjualan
def grafik_penjualan_0302():
  kursor_0302.execute('''SELECT strftime('%Y-%m', reservasi_0302.waktu) AS bulan, SUM(transaksi_0302.jumlah)
                         FROM transaksi_0302
                         JOIN reservasi_0302 ON transaksi_0302.pelanggan_id = reservasi_0302.pelanggan_id
                         GROUP BY bulan''')
  data_penjualan_0302 = kursor_0302.fetchall()
  if data_penjualan_0302:
    bulan_0302, jumlah_0302 = zip(*data_penjualan_0302)
    plt.bar(bulan_0302, jumlah_0302)
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penjualan')
    plt.title('Grafik Penjualan Bulanan')
    plt.show()
  else:
    print("Tidak ada data penjualan untuk ditampilkan.")

# Main Menu
def main_menu_0302():
  while True:
    print("Bojongsantos Barbershop")
    print("1. Registrasi")
    print("2. Login")
    print("3. Tentang Kami")
    print("4. Tentang Tukang Cukur")
    print("5. Style Rambut")
    print("0. Keluar")
    pilihan_0302 = input("Pilih menu: ")

    if pilihan_0302 == '1':
      registrasi_0302()
    elif pilihan_0302 == '2':
      login_0302()
    elif pilihan_0302 == '3':
      tentang_kami_0302()
    elif pilihan_0302 == '4':
      tentang_tukang_cukur_0302()
    elif pilihan_0302 == '5':
      style_rambut_0302()
    elif pilihan_0302 == '0':
      break
    else:
      print("Pilihan tidak valid!")

# Menjalankan main menu
menu_utama_0302()
# Menutup koneksi ke database
koneksi_0302.close()
