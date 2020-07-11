import machine
machine.freq(240000000)
import _thread
import network
import usocket as socket
import utime as time
import wifi

channel = 1

@micropython.native
def read_wifi_packets():
	global channel
	beacon_list = []
	### Listen on UDP port 20001 for wifi packets from the lwIP network stack on core 0.
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(("127.0.0.1", 20001))
	### Use the packet class
	packet = wifi.packet()
	while (True):
		try:
			### Read the wifi packet from the UDP socket.
			temp_packet = sock.recv(4096)
			### Optimization
			mv = memoryview(temp_packet)
			### Update the packet
			packet.update(mv)

			### Print detailed packet info (EXTRA VERBOSE)
			# packet.print_packet()

			# ### Example to print PROBE REQUESTS
			if (packet.fc_type == wifi.TYPE_MANAGEMENT) and (packet.fc_sub == wifi.TYPE_MANAGEMENT_PROBE_REQUEST):
				tags = packet.decode_tags()
				packet_src = wifi.raw_to_hex(packet.addr2).decode('utf-8')
				packet_dst = wifi.raw_to_hex(packet.addr1).decode('utf-8')
				packet_bssid = wifi.raw_to_hex(packet.addr3).decode('utf-8')
				try:
					# probe_len = int(packet.body[1]) + 2
					# probe_ssid = bytes(packet.body[2:probe_len]).decode('utf-8')
					probe_ssid = tags[0][0].decode('utf-8')
					print("[%d] PROBE REQUEST: %s > %s  %s '%s'" % (channel,packet_src,packet_dst,packet_bssid,probe_ssid))
				except:
					pass

			# ### Example to print PROBE RESPONSE
			if (packet.fc_type == wifi.TYPE_MANAGEMENT) and (packet.fc_sub == wifi.TYPE_MANAGEMENT_PROBE_RESPONSE):
				packet_src = wifi.raw_to_hex(packet.addr2).decode('utf-8')
				packet_dst = wifi.raw_to_hex(packet.addr1).decode('utf-8')
				packet_bssid = wifi.raw_to_hex(packet.addr3).decode('utf-8')
				try:
					# probe_len = int(packet.body[1]) + 2
					probe_ssid = tags[0][0].decode('utf-8')
					# probe_ssid = bytes(packet.body[2:probe_len]).decode('utf-8')
					print("[%d] PROBE RESPONSE: %s > %s  %s '%s'" % (channel,packet_src,packet_dst,packet_bssid,probe_ssid))
				except:
					pass

			# ### Example to print BEACONS
			if (packet.fc_type == wifi.TYPE_MANAGEMENT) and (packet.fc_sub == wifi.TYPE_MANAGEMENT_BEACON):
				tags = packet.decode_tags()
				essid = tags[0][0].decode('utf-8')
				beacon_chan = ord(tags[3][0].decode('utf-8'))
				packet_src = wifi.raw_to_hex(packet.addr2).decode('utf-8')
				packet_dst = wifi.raw_to_hex(packet.addr1).decode('utf-8')
				packet_bssid = wifi.raw_to_hex(packet.addr3).decode('utf-8')
				check_entry = (beacon_chan,packet_src,essid)
				if check_entry not in beacon_list:
					beacon_list.append(check_entry)
					print("[%d] BEACON: %s '%s'" % (check_entry[0],check_entry[1],check_entry[2]))

		except Exception as error:
			print("ERROR %s\n%s" % (error,temp_packet))



print("Starting UDP listener thread to recieve wifi packets...")
_thread.start_new_thread(read_wifi_packets, ())

print("Starting the sniffer....")
sta = network.WLAN(network.STA_IF)
sta.active(False)
sta.sniffer(ch=channel)

## Uncomment below to do channel hopping
while (True):
	for channel in range(1,12):
		sta.sniffer(ch=channel)
		time.sleep(3)
