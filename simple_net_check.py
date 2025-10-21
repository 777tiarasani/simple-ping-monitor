#!/usr/bin/env python3
import os
import re
import subprocess

# Daftar host untuk diuji
hosts = ["google.com", "github.com", "openai.com"]

print("="*50)
print("🔍 Simple Network Quality Check")
print("="*50)

for host in hosts:
    print(f"\nPinging {host}...")
    try:
        # Jalankan ping 4 kali
        result = subprocess.run(["ping", "-c", "4", host],
                                capture_output=True, text=True)
        output = result.stdout

        # Ambil packet loss
        loss_match = re.search(r'(\d+)% packet loss', output)
        loss = int(loss_match.group(1)) if loss_match else None

        # Ambil average time
        avg_match = re.search(r'avg = ([\d.]+)', output)
        if not avg_match:
            avg_match = re.search(r'=\s[\d.]+/([\d.]+)/', output)
        avg = float(avg_match.group(1)) if avg_match else None

        # Tentukan status jaringan
        if loss is None or avg is None:
            status = "❌ Tidak dapat mengukur"
        elif loss > 50 or avg > 300:
            status = "🔴 Buruk"
        elif loss > 20 or avg > 150:
            status = "🟠 Tidak Stabil"
        else:
            status = "🟢 Baik"

        print(f"Hasil: {loss}% packet loss, Avg time: {avg} ms, Status: {status}")

    except Exception as e:
        print(f"Gagal ping {host}: {e}")

print("\nSelesai menguji semua host.")
