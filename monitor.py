import psutil
import time
import csv
from datetime import datetime

# Progi ostrzegawcze
CPU_THRESHOLD = 90
RAM_THRESHOLD = 90

# Nazwa pliku wyjściowego
filename = "system_monitoring.csv"

# Inicjalizacja pliku CSV z nagłówkami
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'CPU Usage (%)', 'RAM Usage (%)', 'Used Disk (%)'])

# Monitorowanie w tle
print("Monitoring started. Press Ctrl+C to stop.")
try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        # Zapis do CSV
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, cpu_usage, ram_usage, disk_usage])

        # Powiadomienia
        if cpu_usage > CPU_THRESHOLD:
            print(f"[{timestamp}] ⚠️ CPU usage high: {cpu_usage}%")
        if ram_usage > RAM_THRESHOLD:
            print(f"[{timestamp}] ⚠️ RAM usage high: {ram_usage}%")

        # Dodatkowe monitorowanie procesów (PID, nazwa, CPU%)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                print(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Czekaj 5 sekund przed kolejnym pomiarem
        time.sleep(5)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
