import requests

# 1. Masukkan URL API atau Sumber MAC Portal Anda di sini
URL_SUMBER = "https://sumber-mac-portal.com" 

def ambil_dan_simpan_portal():
    try:
        # Mengambil data dari server portal
        print("Sedang mengambil data dari sumber...")
        response = requests.get(URL_SUMBER, timeout=30)
        
        # Pastikan request sukses (status code 200)
        if response.status_code == 200:
            data_portal = response.text
            
            # 2. Menyimpan data langsung menjadi file playlist.m3u
            with open("playlist.m3u", "w", encoding="utf-8") as file:
                file.write(data_portal)
            
            print("Berhasil! File 'playlist.m3u' telah diperbarui.")
        else:
            print(f"Gagal mengambil data. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"Terjadi kesalahan saat menjalankan skrip: {e}")

if __name__ == "__main__":
    ambil_dan_simpan_portal()
