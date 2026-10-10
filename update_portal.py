import json
import requests

# 1. Tentukan URL API MAC Portal Anda di sini
# Ganti URL di bawah ini dengan URL API/sumber MAC portal yang valid milik Anda
URL_SUMBER = "http://simpletv.uk/c/" 

def ambil_data_portal(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Mengasumsikan API mengembalikan data berformat JSON
        # Jika API Anda mengembalikan teks langsung, ganti dengan 'return response.text'
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengambil data dari portal: {e}")
        return None

def konversi_ke_m3u(data_json):
    """
    Fungsi untuk mengubah data mentah/JSON dari portal menjadi format M3U.
    Sesuaikan struktur 'data_json' di bawah ini dengan struktur asli dari API Anda.
    """
    m3u_content = "#EXTM3U\n"
    
    # Contoh jika data_json berupa daftar saluran/channel
    # Contoh struktur JSON: [{"name": "HBO", "url": "http://server:port/live/mac/..."}]
    if isinstance(data_json, list):
        for item in data_json:
            nama_channel = item.get("name", "Saluran Tanpa Nama")
            url_stream = item.get("url", "")
            logo_channel = item.get("logo", "") # Opsional jika ada logo
            
            if url_stream:
                m3u_content += f'#EXTINF:-1 tvg-logo="{logo_channel}",{nama_channel}\n'
                m3u_content += f'{url_stream}\n'
    
    # Jika API Anda ternyata sudah mengembalikan teks M3U langsung (bukan JSON):
    # Cukup hapus logika di atas dan langsung return data_json
    return m3u_content

def main():
    print("Memulai pengambilan data MAC Portal...")
    data_mentah = ambil_data_portal(URL_SUMBER)
    
    if not data_mentah:
        print("Proses dihentikan karena tidak ada data.")
        return

    # Proses konversi ke teks format M3U
    # Catatan: Jika API Anda sudah menghasilkan format M3U langsung, 
    # Anda bisa langsung mengisi: isi_m3u = data_mentah
    isi_m3u = konversi_ke_m3u(data_mentah)

    # 2. Ekspor data ke file 'playlist.m3u'
    nama_file_output = "playlist.m3u"
    try:
        with open(nama_file_output, "w", encoding="utf-8") as file:
            file.write(isi_m3u)
        print(f"Sukses! File '{nama_file_output}' berhasil dibuat dan diperbarui.")
    except IOError as e:
        print(f"Gagal menulis file output: {e}")

if __name__ == "__main__":
    main()
