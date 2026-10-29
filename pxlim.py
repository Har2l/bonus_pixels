import frida
import sys
import os
import subprocess
import time
from PIL import Image

# 1. Define the path to your PCX file
pcx_file_path = r"C:\Users\talmid\Downloads\marbles.pcx"

# Convert the PCX image using PIL (Pillow) to a format Paint understands
try:
    with Image.open(pcx_file_path) as img:
        temp_bmp_path = pcx_file_path.replace(".pcx", "_temp.png")
        print(f"[+] Converting PCX to a standard format layout ({temp_bmp_path})...")
        img.save(temp_bmp_path)
except Exception as e:
    print(f"[-] PIL conversion failed: {e}")
    sys.exit(1)

# Double-check that our new temporary converted file actually exists
if not os.path.exists(temp_bmp_path):
    print(f"[-] Error: Converted file not found at path: {temp_bmp_path}")
    sys.exit(1)

# CHANGED HERE: We now pass temp_bmp_path so Paint opens the successful PNG version
print(f"[+] Launching Paint natively to open: {temp_bmp_path}")

try:
    # 2. Launch Paint with the CONVERTED file path
    paint_process = subprocess.Popen(["cmd.exe", "/c", "start", "pbrush.exe", temp_bmp_path])

    # Give Windows a brief moment to unpack and initialize the background Paint process
    time.sleep(1.5)

    # 3. Connect Frida to the local machine
    device = frida.get_local_device()

    # 4. Attach directly to the active instance of Paint by its process name
    print("[*] Hooking into the running Paint process...")
    session = device.attach("mspaint.exe")

    print("[+] Successfully attached! MS Paint should now render the image successfully.")

    # Keep the Python session active so Frida stays connected while Paint loads
    print("[*] Press Ctrl+C to exit.")
    sys.stdin.read()

except Exception as e:
    print(f"[-] Operation failed: {e}")
