
class Relay_Controller:
	def __init__(self, combus, kwargs = {}):
		self.__dict__.update(kwargs)
		self.renew_replace_interface(combus)

	def test_comms(self):
		command = self.wrap_in_api([254, 33])
		return self.process_control_command_return(self.send_command(command, 4))

	def set_relay_bank_status(self, status, bank = 1):
		command = self.wrap_in_api([254, 140, status, bank])
		return self.process_control_command_return(self.send_command(command, 4))

	def toggle_relay_by_index(self, relay):
		lsb = relay-1 & 255
		msb = relay >> 8
		command = self.wrap_in_api([254, 47, lsb, msb, 1])
		return self.process_control_command_return(self.send_command(command, 4))

	def turn_on_relay_by_index(self, relay):
		lsb = relay-1 & 255
		msb = relay >> 8
		command = self.wrap_in_api([254,48,lsb,msb])
		return self.process_control_command_return(self.send_command(command, 4))

	def turn_off_relay_by_index(self, relay):
		lsb = relay-1 & 255
		msb = relay >> 8
		command = self.wrap_in_api([254,47,lsb,msb])
		return self.process_control_command_return(self.send_command(command, 4))

	def fusion_turn_on_relay_by_index(self, relay):
		lsb = relay-1 & 255
		msb = relay >> 8
		command = self.wrap_in_api([254,148,lsb,msb])
		return self.process_control_command_return(self.send_command(command, 4))

	def fusion_turn_off_relay_by_index(self, relay):
		lsb = relay-1 & 255
		msb = relay >> 8
		command = self.wrap_in_api([254,147,lsb,msb])
		return self.process_control_command_return(self.send_command(command, 4))

	def turn_off_relay_group(self, relay, bank, group_size):
		command = self.wrap_in_api([254, 99+relay, bank, group_size-1])
		return self.process_control_command_return(self.send_command(command, 4))

	def turn_on_relay_group(self, relay, bank, group_size):
		command = self.wrap_in_api([254, 107+relay, bank, group_size-1])
		return self.process_control_command_return(self.send_command(command, 4))

	def turn_on_relay_by_bank(self, relay, bank = 1):
		command = self.wrap_in_api([254, 107+relay, bank])
		return self.process_control_command_return(self.send_command(command, 4))

	def turn_off_relay_by_bank(self, relay, bank = 1):
		command = self.wrap_in_api([254, 99+relay, bank])
		return self.process_control_command_return(self.send_command(command, 4))

	def turn_on_relay_flasher(self, flasher, speed=1):
		command = self.wrap_in_api([254, 45, flasher, speed])
		return self.process_control_command_return(self.send_command(command, 4))

	def turn_off_relay_flasher(self, flasher):
		command = self.wrap_in_api([254, 45, flasher, 0])
		return self.process_control_command_return(self.send_command(command, 4))

	def set_flasher_speed(self, speed):
		command = self.wrap_in_api([254, 45, 0, speed])
		return self.process_control_command_return(self.send_command(command, 4))

	def start_relay_timer(self, timer, hours, minutes, seconds, relay):
		command = self.wrap_in_api([254, 50, 49+timer, hours, minutes, seconds, relay-1])
		return self.process_control_command_return(self.send_command(command, 4))

	def get_relay_bank_status(self, bank = 1):
		command = self.wrap_in_api([254,124, bank])
		return self.process_read_command_return(self.send_command(command, 4))

	def get_relay_status_by_index(self, relay):
		lsb = relay-1 & 255
		msb = relay >> 8
		command = self.wrap_in_api([254, 44, lsb, msb])
		return self.process_read_command_return(self.send_command(command, 4))

	def get_relay_status_by_index_fusion(self, relay):
		lsb = relay-1 & 255
		msb = relay >> 8
		command = self.wrap_in_api([254, 144, lsb, msb])
		return self.process_read_command_return(self.send_command(command, 4))

	def read_single_ad8(self, channel):
	#TODO read back single integer
		command = self.wrap_in_api([254, 149+channel])
		return self.translate_ad(self.process_read_command_return(self.send_command(command, 4)), 8)

	def read_all_ad8(self):
		command = self.wrap_in_api([254, 166])
		return self.translate_ad(self.process_read_command_return(self.send_command(command, 11)), 8)

	def read_single_ad10(self, channel):
		command = self.wrap_in_api([254, 157+channel])
		return self.translate_ad(self.process_read_command_return(self.send_command(command, 5)), 10)

	def read_all_ad10(self):
		command = self.wrap_in_api([254, 167])
		return self.translate_ad(self.process_read_command_return(self.send_command(command, 19)), 10)

	def get_relay_status_by_bank(self, relay, bank = 1):
		command = self.wrap_in_api([254,115+relay, bank])
		return self.process_read_command_return(self.send_command(command, 4))

	def convert_data(self, data):
		command_string = ''
		for character in data:
			command_string += chr(character)
		return command_string

	def add_checksum(self, data):
		data.append(int(sum(data) & 255))
		return data

	# def wrap_in_api(self, data):
	# 	bytes_in_packet = len(data)
	# 	data.insert(0, bytes_in_packet)
	# 	data.insert(0, 170)
	# 	data = self.add_checksum(data)
	# 	# futzing with thier code. moving to hex.decode
	# 	# print data
	# 	hexData = ''
	# 	for byte in data:
	# 		hexData += '{:02X}'.format(byte)
	# 	# print hexData
	# 	# create payload
	# 	payload = hexData.decode('hex')
	# 	return payload
	def wrap_in_api(self, data):
		bytes_in_packet = len(data)
		data.insert(0, bytes_in_packet)
		data.insert(0, 170)
		data = self.add_checksum(data)
		return data

	def send_command(self, command, bytes_back):
# 		The following line is causing problems and has been commented out until further study.
# 		command = self.convert_data(command)
		if self.combus_type == 'serial':
			self.combus.write(command)
			return self.combus.read(bytes_back)
		else:
			# print command
			# print bytearray(command)
			self.combus.send(bytearray(command))
			return self.combus.recv(32)

	def process_control_command_return(self, data):
		# print(data).encode('hex');
		handshake = self.check_handshake(data)
		bytes_back = self.check_bytes_back(data)
		checksum = self.check_checksum(data)
		if handshake and bytes_back and checksum:
			return [True, self.hex_to_decimal(data)]
		else:
			return [False, 0]

	def process_read_command_return(self, data):
		handshake = self.check_handshake(data)
		bytes_back = self.check_bytes_back(data)
		checksum = self.check_checksum(data)
		if handshake and bytes_back and checksum:
			return self.get_payload(data)
		else:
			return False

	def get_payload(self, data):
		payload = []
		for byte in range(2, len(data)-1):
			payload.append(ord(data[byte:byte+1]))
		return payload


	def check_handshake(self, data):
		return ord(data[:1]) == 170

	def check_bytes_back(self, data):
		return ord(data[1:2]) == (len(data)-3)

	def check_checksum(self,data):
		dlength = len(data)
		dsum = 0
		for byte in range(0, dlength-1):
			dsum += (ord(data[byte:byte+1]))
		return dsum & 255 == ord(data[dlength-1:dlength])

	def split_by_byte(self, data):
		return list(map(''.join, list(zip(*[iter(data)]*2))))

	def hex_to_decimal(self, data):
		# bytes = self.split_by_byte(data.decode('unicode'))
		# print(int.from_bytes(data, "big"))
		# for i in data:
		# 	print data.get
		dataArray = [x for x in data]
		# for idx in bytes:
		# 	dataArray.append(int(idx, 16))
		# print(dataArray)
		return dataArray


	def translate_ad(self, data, resolution):
		read_array = []
		if resolution == 10:
			for index in range(0, len(data), 2):
				read_array.append(((data[index] & 3) << 8) + data[index+1])
			return read_array
		elif resolution == 8:
			return data
		return False

	def renew_replace_interface(self, combus):
		self.combus = combus
		if 'serial' in str(type(self.combus)):
			self.combus_type = 'serial'
		else:
			self.combus_type = 'socket'

	def reactor_read_timers(self):
		command = self.wrap_in_api([254, 55, 3, 136, 16])
		result, seconds = self.process_control_command_return(self.send_command(command, 16))
		command = self.wrap_in_api([254, 55, 3, 120, 16])
		result, minutes = self.process_control_command_return(self.send_command(command, 16))
		command = self.wrap_in_api([254, 55, 3, 104, 16])
		result, hours = self.process_control_command_return(self.send_command(command, 16))
		return self.hex_to_decimal(seconds), self.hex_to_decimal(minutes), self.hex_to_decimal(hours)


	def reactor_send_event(self, event):
		command = self.wrap_in_api([233, 108, int(event)])
		result, data = self.process_control_command_return(self.send_command(command, 4))
		return self.hex_to_decimal(data)

	def reactor_trigger_timer(self, timer):
		timer = int(timer) + 48
		return self.reactor_send_event(timer)

	def reactor_cancel_timer(self, timer):
		timer = int(timer) + 64
		return self.reactor_send_event(timer)

	def reactor_set_timer_seconds(self, timer, seconds = 0):
		timer = int(timer) + 135
		command = self.wrap_in_api([254, 56, 3, timer, seconds])
		return self.process_control_command_return(self.send_command(command, 4))

	def reactor_set_timer_minutes(self, timer, minutes = 0):
		timer = int(timer) + 119
		command = self.wrap_in_api([254, 56, 3, timer, minutes])
		return self.process_control_command_return(self.send_command(command, 4))

	def reactor_set_timer_hours(self, timer, hours = 0):
		timer = int(timer) + 103
		command = self.wrap_in_api([254, 56, 3, timer, hours])
		return self.process_control_command_return(self.send_command(command, 4))
	# Timer info from reactor
	# 170 5 254 56 3 104 24 104 - hours 103 + timer
	# 170 5 254 56 3 120 98 194 - minutes 119 +timer
	#                           - seconds 135 + timer

	# def reactor_set_timer(self, what, timer, seconds = 0, minutes = 0, hours = 0):
	# case = {
	#   'seconds': lambda x: x * 5,
	#   'minutes': lambda x: x + 7,
	#   'hours': lambda x: x - 2
	# 	'all': lambda x: x + 12
	# }[value](x)
	# 	timer = int(timer) + 135
	# 	command = self.wrap_in_api([254, 56, 3, timer, seconds])
	# 	return self.process_control_command_return(self.send_command(command, 4))

	def reactor_read_timers_remaining(self):
		command = self.wrap_in_api([233, 106, 3])
		return self.process_control_command_return(self.send_command(command, 32))

	def lantronix_read_amps(self):
		command = self.wrap_in_api([188, 50, 10, 84, 146, 106, 1, 1, 6, 0, 0, 4, 85, 19])
		return self.process_control_command_return(self.send_command(command, 32))
