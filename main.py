from machine import Pin, PWM
import neopixel
import time
import network
import urequests
import ujson

# Hardware Setup
pir = Pin(12, Pin.IN)
buzzer = PWM(Pin(13), freq=440, duty=0)
led_pin = 14
num_leds = 2
np = neopixel.NeoPixel(Pin(led_pin), num_leds)

# Wi-Fi Credentials
ssid = "Replace this with your Wifi SSID" 
password = "Replace this with your Wifi Password"

# Telegram Bot Details
bot_token = "Replace this with your bot_token"
group_chat_id = "Replace this with your group_chat_id"

# Fur Elise Melody (sweet 10s version)
melody = [
    (330, 300), (311, 300), (330, 300), (311, 300), (330, 300),
    (247, 400), (294, 400), (262, 400), (220, 900),
    (146, 300), (174, 400), (220, 400), (247, 900),
    (174, 300), (233, 400), (247, 400), (262, 900)
]

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

cooldown_duration = 30000  # 30 seconds
last_notification_time = 0

motion_enabled = True  # Default to ARM
last_update_id = None  # Track last Telegram message

# Wi-Fi Connection
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(ssid, password)
        retry = 0
        while not wlan.isconnected() and retry < 20:
            time.sleep(0.5)
            retry += 1
        if wlan.isconnected():
            print("Connected! IP:", wlan.ifconfig()[0])
        else:
            print("Failed to connect.")
    return wlan

# Send Telegram Message
def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={group_chat_id}&text={text}"
        r = urequests.get(url)
        r.close()
        print(f"Message sent: {text}")
    except Exception as e:
        print("Telegram Error:", e)

# Check for ARM/DISARM commands
def check_telegram_commands():
    global last_update_id, motion_enabled
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates?timeout=1"
        if last_update_id:
            url += f"&offset={last_update_id + 1}"
        r = urequests.get(url)
        data = r.json()
        r.close()

        for result in data["result"]:
            last_update_id = result["update_id"]
            message = result.get("message", {}).get("text", "").strip().upper()
            if message == "DISARM":
                motion_enabled = False
                set_led_color((255, 0, 0))  # Red
                send_telegram_message("🚫 Motion Detection is turned off.")
            elif message == "ARM":
                motion_enabled = True
                blink_led_once((0, 255, 0))  # Green
                send_telegram_message("✅ Motion Detection is turned on.")
    except Exception as e:
        print("Command Check Error:", e)

# Play Melody
def play_melody():
    start_time = time.ticks_ms()
    for i, (freq, dur) in enumerate(melody):
        if time.ticks_diff(time.ticks_ms(), start_time) >= 10000:
            break
        color = colors[i % len(colors)]
        buzzer.freq(freq)
        buzzer.duty(600)
        for j in range(num_leds):
            np[j] = color
        np.write()
        time.sleep_ms(dur)
        buzzer.duty(0)
        time.sleep_ms(20)
    stop_all()

# Stop buzzer & LEDs
def stop_all():
    buzzer.duty(0)
    set_led_color((0, 0, 0))  # Turn off

# Set constant LED color
def set_led_color(color):
    for i in range(num_leds):
        np[i] = color
    np.write()

# Blink LED once
def blink_led_once(color):
    set_led_color(color)
    time.sleep(0.5)
    stop_all()

# Main
wlan = connect_wifi()
motion_detected = False

while True:
    if not wlan.isconnected():
        wlan = connect_wifi()

    check_telegram_commands()

    if motion_enabled:
        motion = pir.value()
        if motion and not motion_detected:
            motion_detected = True
            now = time.ticks_ms()
            if time.ticks_diff(now, last_notification_time) >= cooldown_duration:
                send_telegram_message("🚪 Motion detected at the door!")
                last_notification_time = now
            play_melody()
        elif not motion:
            motion_detected = False
    else:
        motion_detected = False  # Clear any residual motion

    time.sleep_ms(100)
