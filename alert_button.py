import os
import requests
import time
import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv("/home/ensign/alert_button/.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN or CHAT_ID is missing from .env")


TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Alert button monitoring system is now active. Press Ctrl+C to stop.")

button_pressed = False

try:
    while True:
        if GPIO.input(7) == GPIO.HIGH and not button_pressed:
            print("Someone pressed the alert button!")

            # Send an alert message through Telegram
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            response = requests.post(url, data={
                "chat_id": CHAT_ID,
                "text": "Someone pressed the alert button!"
            })
            print("Telegram response:", response.status_code)

            button_pressed = True

        elif GPIO.input(7) == GPIO.LOW:
            button_pressed = False

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
    GPIO.cleanup()
