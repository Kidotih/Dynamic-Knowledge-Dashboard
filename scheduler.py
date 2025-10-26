import schedule
import time
from main import run_dashboard

schedule.every().day.at("09:00").do(run_dashboard)

print("Scheduler started. Running daily at 09:00...")
while True:
    schedule.run_pending()
    time.sleep(60)
