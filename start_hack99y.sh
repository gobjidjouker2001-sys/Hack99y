#!/bin/bash

echo "--- [ Hack99y Automator ] ---"

# 1. التثبيت والتحقق من الأدوات
echo "[*] Installing dependencies..."
sudo apt-get update -y && sudo apt-get install aircrack-ng python3-pip -y
sudo pip3 install scapy --break-system-packages --quiet

# 2. إنشاء قائمة الأسماء الـ 100
echo "[*] Generating names.txt (Hacky0 - Hacky99)..."
python3 -c "print('\n'.join(['Hacky' + str(i) for i in range(100)]))" > names.txt

# 3. تفعيل وضع المراقبة
echo "[*] Killing conflicting processes..."
sudo airmon-ng check kill
echo "[*] Starting Monitor Mode on wlan0 and wlan1..."
sudo airmon-ng start wlan0
sudo airmon-ng start wlan1

# 4. تشغيل الأداة
sudo python3 Hack99y.py
