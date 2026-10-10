import requests
import json
import re
from urllib.parse import quote

def main():
    print("Sedang mengambil data dari portal...")
    
    # 1. ATUR ALAMAT PORTAL DAN MAC ADDRESS ANDA DI SINI
    portal_url = "http://simpletv.uk/c/"  # Ganti dengan URL portal asli Anda
    mac_address = "A0:BB:3E:0B:2A:B6"                  # Ganti dengan MAC address Anda
    
    # Bersihkan slash di ujung URL portal jika ada
    portal_url = portal_url.rstrip('/')

    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stalker/",
        "Cookie": f"mac={mac_address}"
    }

    try:
        # 2. Proses Handshake & Pembuatan Token Sesi
        handshake_url = f"{portal_url}/server/load.php?type=stb&action=handshake"
        req_handshake = requests.get(handshake_url, headers=headers, timeout=15)
        
        token = ""
        if req_handshake.status_code == 200:
            try:
                res_json = req_handshake.json()
                token = res_json.get("js", {}).get("token", "")
                if token:
                    headers["Authorization"] = f"Bearer {token}"
            except:
                pass

        # 3. Request daftar channel dari API Portal
        channel_url = f"{portal_url}/server/load.php?type=itv&action=get_all_channels"
        response = requests.get(channel_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Gagal memuat portal. Status kode: {response.status_code}")
            return
            
        data = response.json()
        channels = data.get("js", {}).get("data", [])
        
        if not channels:
            channels = data.get("js", []) if isinstance(data.get("js"), list) else []

        if not channels:
            print("Tidak ada channel yang ditemukan.")
            return

        # 4. Bangun isi file M3U yang kompatibel dengan OTT Navigator
        m3u_content = "#EXTM3U\n"
        
        for ch in channels:
            name = ch.get("name", "Unknown Channel")
            ch_id = ch.get("id", "")
            
            # Ekstrak atau bangun Link Streaming
            cmd = ch.get("cmd", "")
            stream_url = ""
            if "http" in cmd:
                match = re.search(r'(https?://[^\s"\']+)', cmd)
                stream_url = match.group(1) if match else cmd
            else:
                stream_url = f"{portal_url}/itv/{ch_id}"

            # --- PERBAIKAN LOGO DENGAN ALAMAT MAC PORTAL ---
            # Ambil properti gambar bawaan dari database portal
            logo_file = ch.get("logo", ch.get("tvg_logo", ch.get("icon", "")))
            logo_url = ""
            
            if logo_file:
                if logo_file.startswith("http"):
                    logo_url = logo_file
                else:
                    # Gabungkan file logo dengan direktori bawaan server MAC Portal Anda
                    logo_url = f"{portal_url}/misc/logos/{logo_file}"
            else:
                # STRATEGI FALLBACK: Jika portal kosong, buat generator logo otomatis berbasis teks/nama channel
                # Ini memastikan OTT Navigator tetap menampilkan icon visual unik alih-alih kotak kosong biasa
                encoded_name = quote(name)
                logo_url = f"https://ui-avatars.com{encoded_name}&background=random&color=fff&size=256&font-size=0.33"

            group_title = ch.get("tvg_genre", "Lainnya")

            # Format tag M3U spesifik yang sangat disukai oleh parser OTT Navigator
            m3u_content += f'#EXTINF:-1 tvg-id="{ch_id}" tvg-name="{name}" tvg-logo="{logo_url}" group-title="{group_title}",{name}\n'
            
            # Tambahkan header user-agent dan cookie agar OTT Navigator dapat menembus keamanan portal saat memutar video
            m3u_content += f'#EXTVLCOPT:http-user-agent={headers["User-Agent"]}\n'
            m3u_content += f'#EXTVLCOPT:http-cookie=mac={mac_address}\n'
            m3u_content += f'{stream_url}\n'

        # 5. Ekspor data ke file playlist.m3u
        with open("playlist.m3u", "w", encoding="utf-8") as file:
            file.write(m3u_content)

        print("Berhasil! File 'playlist.m3u' dioptimalkan untuk OTT Navigator beserta sistem logonya.")

    except Exception as e:
        print(f"Terjadi kesalahan saat memproses skrip: {e}")

if __name__ == "__main__":
    main()
