🔐 ESP32 Smart Door Motion Alarm System with Telegram Control
This project is a Wi-Fi-enabled smart door security system built using the ESP32-WROOM-32 microcontroller. It detects motion at the entrance using a PIR sensor, plays a short melodic alert with LEDs, and sends real-time Telegram notifications. Users can remotely ARM or DISARM the system using simple text commands in Telegram.

🛠️ Components Used
ESP32-WROOM-32
PIR Motion Sensor
PWM Buzzer
WS2812B Neopixel LEDs (2x)
Wi-Fi Network (Station Mode)
Telegram Bot (HTTP API)

🚀 How It Works
Startup & Wi-Fi Connection
On power-up, the ESP32 initializes the PIR sensor, buzzer, and LEDs. It then attempts to connect to the configured Wi-Fi network.

Telegram Command Listener
The ESP32 polls the Telegram Bot API for new messages in the group. It supports two commands:

ARM: Enables motion detection and blinks green LED once.
DISARM: Disables motion detection and turns on a solid red LED.

Motion Detection Logic
When motion is detected and the system is armed, the following actions occur:
A Telegram alert is sent: "🚪 Motion detected at the door!"
A short, 10-second Für Elise melody plays on the buzzer.
Neopixel LEDs flash in colorful sync with the melody.

Cooldown System
To prevent spamming, motion alerts are rate-limited using a 30-second cooldown timer.

LED Status Indicators
Green blink: System armed.
Red solid: System disarmed.
Off: Idle or no alert.

Failsafe Features
Reconnects to Wi-Fi if disconnected.
Handles Telegram API errors gracefully.
Prevents false triggers when disarmed.

📲 Use Case
Ideal for smart homes, office entry alerts, or hobbyist IoT security systems. The Telegram bot gives users remote control and real-time insights with zero subscription or cloud service dependencies.
