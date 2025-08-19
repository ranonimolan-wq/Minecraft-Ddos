from mcstatus import JavaServer
import time
import threading
import random
import socket
from concurrent.futures import ThreadPoolExecutor

def check_server(ip, port=25565):
    """Sunucu durumunu kontrol eder"""
    try:
        server = JavaServer.lookup(f"{ip}:{port}")
        status = server.status()
        return {
            "online": True,
            "players": status.players.online,
            "version": status.version.name,
            "latency": status.latency
        }
    except Exception as e:
        return {"online": False, "error": str(e)}

def simulate_player(ip, port, player_id):
    """Tek bir bot oyuncuyu simüle eder"""
    try:
        # Rastgele gecikme (0-5 sn arası)
        time.sleep(random.uniform(0, 5))
        
        # Sunucuya bağlanma simülasyonu
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((ip, port))
            
        # Rastgele çevrimiçi kalma süresi (10-120 sn)
        online_time = random.uniform(10, 120)
        time.sleep(online_time)
        
        return f"👤 Bot #{player_id}: {online_time:.1f}s çevrimiçi kaldı"
    
    except Exception as e:
        return f"❌ Bot #{player_id} hata: {str(e)}"

def mass_simulation(ip, port, bot_count, max_threads=500):
    """Binlerce botu simüle eder"""
    print(f"⏳ {bot_count} bot bağlantısı simüle ediliyor...")
    
    successful = 0
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for i in range(1, bot_count + 1):
            futures.append(executor.submit(simulate_player, ip, port, i))
        
        for future in futures:
            try:
                result = future.result()
                print(result)
                if "👤" in result:
                    successful += 1
            except Exception as e:
                print(f"⚠️ İşlem hatası: {e}")
    
    duration = time.time() - start_time
    print(f"\n✅ {successful}/{bot_count} bot başarıyla simüle edildi")
    print(f"⏱️ Toplam süre: {duration:.2f} saniye")
    print(f"🚀 Saniyede {successful/max(1, duration):.2f} bağlantı")

if __name__ == "__main__":
    # KONFİGÜRASYON
    SERVER_IP = "127.0.0.1"  # SADECE KENDİ SUNUCUNUZ
    SERVER_PORT = 25565
    BOT_COUNT = 1000  # Simüle edilecek bot sayısı
    
    # Önce sunucu durumunu kontrol et
    print("🔍 Sunucu durumu kontrol ediliyor...")
    status = check_server(SERVER_IP, SERVER_PORT)
    
    if status["online"]:
        print(f"✅ Sunucu çevrimiçi! {status['players']} oyuncu | Versiyon: {status['version']} | Ping: {status['latency']}ms")
        
        # Binlerce bot simülasyonu
        mass_simulation(SERVER_IP, SERVER_PORT, BOT_COUNT)
    else:
        print(f"❌ Sunucu kapalı: {status['error']}")
        print("Simülasyon iptal edildi.")
