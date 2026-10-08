
import requests
import time
import RPi.GPIO as GPIO

BOT_TOKEN = "8568791949:AAFstA7Q2jJQJZCmx3pEitu6yGeiPtZIaZc"
CHAT_ID = "6993827186"

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
