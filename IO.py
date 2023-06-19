import csv

def write_header(file):
    with open(file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Tanggal', 'Waktu', 'Closing Time(s)', 'Reopening Time(s)', 'Closed Time(s)', 'Blink Duration(s)', 'Blink Frequency', "Microsleep", "Perclos", "Rata-rata Jarak", "Kategori Jarak", "Rata-rata Kecepatan", "Kategori Kecepatan"])

def write_data_to_csv(data, file):
    with open(file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
