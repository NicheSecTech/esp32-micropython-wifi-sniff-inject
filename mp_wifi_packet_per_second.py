
## Make sure you have uploaded wifi.py to the ESP32.
## Usage:
## >>> import mp_wifi_packet_per_second
## Output will be:
## <Channel> <PacketsPerSecond>
## Example output:
# 1 50
# 2 21
# 3 12
# 4 27
# 5 15
# 6 44
# 7 0
# 8 1
# 9 15
# 10 0
# 11 26
# 12 0
# 13 0
# 14 0

import machine
machine.freq(240000000)
import network
import _thread
import socket
import uselect
import time
import wifi
from wifi import *

@micropython.viper
def monitorWiFi():
	sta = network.WLAN(network.STA_IF)
	sta.active(False)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(("127.0.0.1", 20001))
	packet = wifi.packet()
	count = 0
	channel = 1
	lasttime = time.ticks_ms()
	print("Starting sniffer....")
	sta.sniffer(ch=channel)
	in_socks = [sock]
	while (True):
		tt = time.ticks_ms()
		ts = int(tt) - int(lasttime)
		if int(ts) >= int(1000):
			print(channel,count)
			channel = ((channel + 1) % 15)
			if channel == 0:
				channel = 1
			sta.set_channel(channel)
			count = 0
			lasttime = time.ticks_ms()
		inputready, outputready, exceptready = uselect.select(in_socks, [], [], 1)
		for temp in inputready:
			count = count + 1
			temp_packet = temp.recv(4096)
			# packet.update(temp_packet)
			# packet.print_summary()

print("Starting thread...")
_thread.start_new_thread(monitorWiFi, ())

