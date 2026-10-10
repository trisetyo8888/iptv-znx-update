import requests

def main():
    # 1. Ganti URL di bawah ini dengan URL API/sumber MAC Portal Anda yang sebenarnya
    url_sumber = "http://simpletv.uk/c/" 
    
    print("Sedang mengambil data dari portal...")
    try:
        response = requests.get(url_sumber, timeout=30)
        response.raise_for_status() # Memastikan tidak ada error HTTP
        
        # Mengambil teks response
        data_portal = response.text
        
        # 2. Membuat dan menulis data ke file playlist.m3u
        with open("playlist.m3u", "w", encoding="utf-8") as file:
            file.write(data_portal)
            
        print("Berhasil! File 'playlist.m3u' telah dibuat dan diperbarui.")
        
    except Exception as e:
        print(f"Terjadi kesalahan saat memperbarui data: {e}")

if __name__ == "__main__":
    main()
