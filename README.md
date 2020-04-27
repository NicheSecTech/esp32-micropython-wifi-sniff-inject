# esp32-micropython-wifi-sniff-inject
esp32 build of micropython v1.12 using ESP-IDF v4.0 that supports 802.11 sniffing and injection.

MicroPython v1.12.0 for ESP32 with 802.11 packet sniffing and injection.

Firmware:		  micropython-v1.12-256-geae495a71-dirty_wifi_sniffer_injection_esp32-20200426.bin

MicroPython: 	v1.12-256-geae495a71-dirty

ESP-IDF: 		  v4.0

INSTRUCTIONS

Flash this micropython firmware to your ESP32. 

./esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash -z 0x1000 micropython-v1.12-256-geae495a71-dirty_wifi_sniffer_injection_esp32-20200426.bin

Examples of how to use it are in micropython_sniffer_injection_example.py.


