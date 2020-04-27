import machine
import _thread
import socket
import time

machine.freq(240000000)

## DEFINE FUNCTION TO RECEIVE SNIFFED PACKETS FROM NETWORK SOCKET
def wifi_sniff():
	localIP     = "127.0.0.1"
	localPort   = 20001
	bufferSize  = 4096
	UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	UDPServerSocket.bind((localIP, localPort))
	print("UDP server up and listening for WiFi packets.")
	count = 0
	countme = 0
	while(True):
		count = count + 1
		bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
		# bytesAddressPair[0] is the data
		# bytesAddressPair[1] is the remote (ip,port) ('127.0.0.1',20002). Ignore this.
		print(bytesAddressPair)
		countme = countme + len(bytesAddressPair[0])
		if count >= 100:
			print("Server: %d  %d" % (time.ticks_ms(),countme))
			count = 0

## START SNIFFING THREAD BEFORE CALLING sta.sniffer(ch=8)
_thread.start_new_thread(wifi_sniff, ())

## TURN ON THE WIFI
import network
ap = network.WLAN(network.AP_IF)
ap.active(False)
sta = network.WLAN(network.STA_IF)
sta.active(False)
## START SNIFFER
sta.sniffer(ch=8)
## STOP SNIFFER
sta.sniffer_stop()

## Configure your ESP32 with AP mode or set the channel with sniffer
## first before doing injection.
sta.sniffer(ch=8)
sta.sniffer_stop()

## PACKET INJECTION (BEACON 'ESPTEST' ON CHANNEL 8)
buf = b"\x80\x00\x00\x00\xff\xff\xff\xff\xff\xff\xba\xde\xaf\xfe\x00\x06\xba\xde\xaf\xfe\x00\x06\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x64\x00\x31\x04\x00\x07\x45\x53\x50\x54\x45\x53\x54\x01\x08\x82\x84\x8b\x96\x0c\x12\x18\x24\x03\x01\x08\x05\x04\x01\x02\x00\x00"
buf_len = len(buf)
count = 0
while (count < 100):
	count = count + 1
	sta.inject(buffer=buf,length=buf_len)
	time.sleep(0.1)


