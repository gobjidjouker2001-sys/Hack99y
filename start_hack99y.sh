#!/bin/bash

# 1. إنشاء ملف الأسماء إذا لم يكن موجوداً
if [ ! -f names.txt ]; then
    echo "[*] Creating names.txt..."
    for i in {0..99}; do echo "Hacky$i" >> names.txt; done
fi

# 2. تحويل الكروت لوضع المراقبة
echo "[*] Setting interfaces to monitor mode..."
sudo airmon-ng start wlan0
sudo airmon-ng start wlan1

# 3. تشغيل الأداة
sudo python3 Hack99y.py
