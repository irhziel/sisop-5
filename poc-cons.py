import threading
import time
import random
from threading import Semaphore

# Ukuran buffer
BUFFER_SIZE = 5
buffer = [None] * BUFFER_SIZE
in_index = 0
out_index = 0

# Sinkronisasi (Semaphore & Mutex)
empty = Semaphore(BUFFER_SIZE) # Menghitung ketersediaan slot kosong
full = Semaphore(0)            # Menghitung ketersediaan slot terisi
mutex = threading.Lock()       # Mutex untuk memastikan hanya satu thread yang mengakses buffer

# Fungsi Producer
def producer(producer_id):
    global in_index
    # Modifikasi: Diubah dari while True menjadi for loop agar program bisa selesai
    for _ in range(5):
        item = random.randint(1, 100) # Memproduksi item berupa angka acak
        
        empty.acquire()               # Tunggu jika buffer penuh (slot kosong = 0)
        mutex.acquire()               # Masuk ke critical section (kunci buffer)
        
        # Memasukkan item ke dalam buffer
        buffer[in_index] = item
        # Modifikasi: Menambahkan f-string dan memperbaiki variabel 'index' menjadi 'in_index'
        print(f"Producer {producer_id} memproduksi {item} di buffer[{in_index}]")
        in_index = (in_index + 1) % BUFFER_SIZE
        
        mutex.release()               # Keluar dari critical section (buka kunci)
        full.release()                # Kirim sinyal bahwa ada item baru (full + 1)
        
        time.sleep(random.uniform(0.5, 1.5)) # Jeda simulasi waktu produksi 

# Fungsi Consumer
def consumer(consumer_id):
    global out_index
    # Modifikasi: Diubah dari while True menjadi for loop agar program bisa selesai
    for _ in range(5):
        full.acquire()                # Tunggu jika buffer kosong (slot terisi = 0)
        mutex.acquire()               # Masuk ke critical section (kunci buffer)
        
        # Mengambil item dari buffer
        item = buffer[out_index]
        print(f"Consumer {consumer_id} mengonsumsi {item} dari buffer[{out_index}]")
        buffer[out_index] = None      # (Opsional) Hapus item dari buffer secara visual
        out_index = (out_index + 1) % BUFFER_SIZE
        
        mutex.release()               # Keluar dari critical section (buka kunci)
        empty.release()               # Kirim sinyal bahwa ada slot kosong (empty + 1)
        
        time.sleep(random.uniform(1, 2))  # Jeda simulasi waktu konsumsi

# Membuat thread untuk producer dan consumer
producer_threads = []
consumer_threads = []

print("Memulai Proses...\n")

for i in range(3):  # Membuat 3 producer
    t = threading.Thread(target=producer, args=(i+1,))
    producer_threads.append(t)
    t.start()

for i in range(3):  # Membuat 3 consumer
    t = threading.Thread(target=consumer, args=(i+1,))
    consumer_threads.append(t)
    t.start()

# Modifikasi: Menunggu semua thread selesai dieksekusi sebelum menutup program
for t in producer_threads:
    t.join()
for t in consumer_threads:
    t.join()

print("\nSemua proses selesai.")