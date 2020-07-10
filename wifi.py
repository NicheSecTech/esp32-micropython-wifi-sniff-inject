import ubinascii
import network


## USAGE
# >>> import wifi

## Define a new packet class
# >>> new_packet = wifi.packet()
## Updates the packet data (structure defined below)
# >>> new_packet.update(raw_packet)

## PACKET TYPES
# https://en.wikipedia.org/wiki/802.11_Frame_Types

WIFI_TYPES = ["MANAGEMENT","CONTROL","DATA","EXTENSION"]
WIFI_SUBTYPES = [["ASSOCIATION_REQUEST","ASSOCIATION_RESPONSE","REASSOCIATION_REQUEST","REASSOCIATION_RESPONSE","PROBE_REQUEST","PROBE_RESPONSE","TIMING_ADVERTISEMENT","RESERVED1","BEACON","ATIM","DISASSOCIATION","AUTHENTICATION","DEAUTHENTICATION","ACTION","NACK","RESERVED2"],["RESERVED1","RESERVED2","TRIGGER","RESERVED3","REPORT_POLL","NDP_ANNOUNCEMENT","CONTROL_FRAME_EXTENSION","CONTROL_WRAPPER","BLOCK_ACK_REQUEST","BLOCK_ACK","PS_POLL","RTS","CTS","ACK","CF_END","CF_END_ACK"],["DATA","DATA_CF_ACK","DATA_CF_POLL","DATA_CF_ACK_POLL","NULL","CF_ACK","CF_POLL","CF_ACK_POLL","QOS_DATA","QOS_DATA_CF_ACK","QOS_DATA_CF_POLL","QOS_DATA_CF_ACK_POLL","QOS_NULL","QOS_RESERVED1","QOS_CF_POLL","QOS_CF_ACK_POLL"],["DMG_BEACON"]]

TYPE_MANAGEMENT = const(0)
TYPE_MANAGEMENT_ASSOCIATION_REQUEST = const(0)
TYPE_MANAGEMENT_ASSOCIATION_RESPONSE = const(1)
TYPE_MANAGEMENT_REASSOCIATION_REQUEST = const(2)
TYPE_MANAGEMENT_REASSOCIATION_RESPONSE = const(3)
TYPE_MANAGEMENT_PROBE_REQUEST = const(4)
TYPE_MANAGEMENT_PROBE_RESPONSE = const(5)
TYPE_MANAGEMENT_TIMING_ADVERTISEMENT = const(6)
TYPE_MANAGEMENT_RESERVED1 = const(7)
TYPE_MANAGEMENT_BEACON = const(8)
TYPE_MANAGEMENT_ATIM = const(9)
TYPE_MANAGEMENT_DISASSOCIATION = const(10)
TYPE_MANAGEMENT_AUTHENTICATION = const(11)
TYPE_MANAGEMENT_DEAUTHENTICATION = const(12)
TYPE_MANAGEMENT_ACTION = const(13)
TYPE_MANAGEMENT_NACK = const(14)
TYPE_MANAGEMENT_RESERVED2 = const(15)

TYPE_CONTROL = const(1)
TYPE_CONTROL_RESERVED1 = const(0)
TYPE_CONTROL_RESERVED2 = const(1)
TYPE_CONTROL_TRIGGER = const(2)
TYPE_CONTROL_RESERVED3 = const(3)
TYPE_CONTROL_REPORT_POLL = const(4)
TYPE_CONTROL_NDP_ANNOUNCEMENT = const(5)
TYPE_CONTROL_CONTROL_FRAME_EXTENSION = const(6)
TYPE_CONTROL_CONTROL_WRAPPER = const(7)
TYPE_CONTROL_BLOCK_ACK_REQUEST = const(8) #(BAR)
TYPE_CONTROL_BLOCK_ACK = const(9) #(BA)
TYPE_CONTROL_PS_POLL = const(10)
TYPE_CONTROL_RTS = const(11)
TYPE_CONTROL_CTS = const(12)
TYPE_CONTROL_ACK = const(13)
TYPE_CONTROL_CF_END = const(14)
TYPE_CONTROL_CF_END_ACK = const(15)

TYPE_DATA = const(2)
TYPE_DATA_DATA  = const(0)
TYPE_DATA_DATA_CF_ACK  = const(1)
TYPE_DATA_DATA_CF_POLL  = const(2)
TYPE_DATA_DATA_CF_ACK_POLL  = const(3)			
TYPE_DATA_NULL  = const(4)						# (no data)
TYPE_DATA_CF_ACK  = const(5)					# (no data)
TYPE_DATA_CF_POLL  = const(6)					# (no data)
TYPE_DATA_CF_ACK_POLL  = const(7)				# (no data)
TYPE_DATA_QOS_DATA  = const(8)
TYPE_DATA_QOS_DATA_CF_ACK  = const(9)
TYPE_DATA_QOS_DATA_CF_POLL  = const(10)
TYPE_DATA_QOS_DATA_CF_ACK_POLL  = const(11)	
TYPE_DATA_QOS_NULL  = const(12)				# (no data)
TYPE_DATA_QOS_RESERVED1  = const(13)			# Reserved
TYPE_DATA_QOS_CF_POLL  = const(14)				# (no data)
TYPE_DATA_QOS_CF_ACK_POLL  = const(15)			# (no data)

TYPE_EXTENSION  = const(3)
TYPE_EXTENSION_DMG_BEACON  = const(0)


def raw_to_hex(mac):
	output = ubinascii.hexlify(mac,":")
	return output

def hex_to_raw(mac):
	new_mac = mac.replace(":","")
	output = ubinascii.unhexlify(new_mac)
	return output

@micropython.native
def get_my_mac():
	mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
	return mac

class packet:
	@micropython.native
	def __init__(self,packet=None):
		# FRAME CONTROL
		self.size = None
		self.fc_ver = None
		self.fc_type = None
		self.fc_sub = None
		self.fc_tods = None
		self.fc_fromds = None
		self.fc_frag = None
		self.fc_retry = None
		self.fc_pwmg = None
		self.fc_moredata = None
		self.fc_wep = None
		self.fc_order = None
		self.header = None
		# HEADER
		self.duration =  None
		self.addr1 =  None
		self.addr2 =  None
		self.addr3 =  None
		self.seq =    None
		self.addr4 =  None
		self.body =   None
		self.crc =    None
		if (packet != None):
			self.update(packet)

	@micropython.native
	def decode_tags(self):
		tags = self.body
		tags_dict = {}
		pos = 12
		pos_len = len(tags)
		dtags = bytes(bytearray(tags))
		while pos < pos_len:
			tag_number = int(dtags[pos])
			tag_length = int(dtags[(pos+1)])
			tag_data = dtags[(pos+2):(pos+2+tag_length)]
			pos = pos + 2 + tag_length
			if tag_number not in tags_dict.keys():
				tags_dict[tag_number] = []
			tags_dict[tag_number].append(tag_data)
		return tags_dict

	@micropython.native
	def update(self,packet):
		# FRAME CONTROL
		self.size = len(packet)
		self.fc_ver =    (((packet[0]) & 0b00000011) >> 0)
		self.fc_type =   (((packet[0]) & 0b00001100) >> 2)
		self.fc_sub =    (((packet[0]) & 0b11110000) >> 4)
		self.fc_tods = 	 (((packet[1]) & 0b10000000) >> 7)
		self.fc_fromds = (((packet[1]) & 0b01000000) >> 6)
		self.fc_frag =   (((packet[1]) & 0b00100000) >> 5)
		self.fc_retry =  (((packet[1]) & 0b00010000) >> 4)
		self.fc_pwmg =   (((packet[1]) & 0b00001000) >> 3)
		self.fc_more =   (((packet[1]) & 0b00000100) >> 2)
		self.fc_wep =    (((packet[1]) & 0b00000010) >> 1)
		self.fc_order =  (((packet[1]) & 0b00000001) >> 0)

		# HEADER
		self.duration =  packet[2:3]
		self.addr1 =     packet[4:10]
		self.addr2 =     packet[10:16]
		self.addr3 =     packet[16:22]
		self.seq =       packet[22:23]
		# self.addr4 =     packet[24:30]
		self.body =      packet[24:-4]
		self.crc =       packet[-4:]

	def print_summary(self):
		try:
			ptype = WIFI_TYPES[int(self.fc_type)]
		except:
			ptype = int(self.fc_type)
		try:
			stype = WIFI_SUBTYPES[int(self.fc_type)][int(self.fc_sub)]
		except:
			stype = int(self.fc_sub)
		print("%d %s %s %s %s %s" % (self.size,ptype,stype,raw_to_hex(self.addr1),raw_to_hex(self.addr2),raw_to_hex(self.addr3)))

	def print_packet(self):
		print("self.fc_ver: %d" % self.fc_ver)
		print("self.fc_type: %d" % self.fc_type)
		print("self.fc_sub: %d" % self.fc_sub)
		print("self.fc_tods: %d" % self.fc_tods)
		print("self.fc_fromds: %d" % self.fc_fromds)
		print("self.fc_frag: %d" % self.fc_frag)
		print("self.fc_retry: %d" % self.fc_retry)
		print("self.fc_pwmg: %d" % self.fc_pwmg)
		print("self.fc_more: %d" % self.fc_more)
		print("self.fc_wep: %d" % self.fc_wep)
		print("self.fc_order: %d" % self.fc_order)
		print("self.duration: %s" % raw_to_hex(self.duration))
		print("self.addr1: %s" % raw_to_hex(self.addr1))
		print("self.addr2: %s" % raw_to_hex(self.addr2))
		print("self.addr3: %s" % raw_to_hex(self.addr3))
		print("self.seq: %s" % raw_to_hex(self.seq))
		# print("self.addr4: %s" % raw_to_hex(self.addr4))
		print("self.body(hex): %s" % raw_to_hex(self.body))
		print("self.crc: %s" % raw_to_hex(self.crc))
