import schedule
import time
import subprocess
import datetime

def run_dashboard():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n🕒 Running Dynamic Knowledge Dashboard at {timestamp}...\n")
    subprocess.run(["python", "main.py"], check=True)
    print("\n✅ Dashboard run complete.\n")

# Schedule the dashboard to run once per day at 08:00 AM
schedule.every().day.at("08:00").do(run_dashboard)

print("📅 Scheduler is running... (Ctrl + C to stop)")

while True:
    schedule.run_pending()
    time.sleep(60)

