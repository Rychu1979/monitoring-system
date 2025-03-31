import psutil
import time
import csv
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Wczytaj dane logowania z pliku .env
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL = EMAIL_ADDRESS  # Wysyłka do siebie

# Progi ostrzegawcze
CPU_THRESHOLD = 90
RAM_THRESHOLD = 90

# Funkcja wysyłająca e-mail
def send_email(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"❌ Błąd podczas wysyłania e-maila: {e}")

# Nazwa pliku CSV
filename = "system_monitoring.csv"

# Zapis nagłówków
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'CPU Usage (%)', 'RAM Usage (%)', 'Used Disk (%)'])

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

        # Ostrzeżenia i e-mail
        if cpu_usage > CPU_THRESHOLD:
            msg = f"[{timestamp}] ⚠️ CPU usage high: {cpu_usage}%"
            print(msg)
            send_email("⚠️ CPU Usage Alert", msg)

        if ram_usage > RAM_THRESHOLD:
            msg = f"[{timestamp}] ⚠️ RAM usage high: {ram_usage}%"
            print(msg)
            send_email("⚠️ RAM Usage Alert", msg)

        # Monitorowanie procesów
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                print(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        time.sleep(5)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")

