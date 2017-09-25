
class Relay_Controller:
	def __init__(self, combus, kwargs = {}):
		self.__dict__.update(kwargs)
		self.renew_replace_interface(combus)
		
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
	
	def turn_on_relay_flasher(self, flasher):
		command = self.wrap_in_api([254, 45, flasher, 1])
		return self.process_control_command_return(self.send_command(command, 4))
		
	def turn_off_relay_flasher(self, flasher):
		command = self.wrap_in_api([254, 45, flasher, 0])
		return self.process_control_command_return(self.send_command(command, 4))
		
	def set_flasher_speed(self, speed):
		command = self.wrap_in_api([254, 45, 0, 5])
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

	def wrap_in_api(self, data):
		bytes_in_packet = len(data)
		data.insert(0, bytes_in_packet)
		data.insert(0, 170)
		data = self.add_checksum(data)
		return data
		
	def send_command(self, command, bytes_back):
		command = self.convert_data(command)
		if self.combus_type == 'serial':
			self.combus.write(command)
			return self.combus.read(bytes_back)
		else:
			self.combus.send(command)
			return self.combus.recv(bytes_back)
		
	def process_control_command_return(self, data):
		handshake = self.check_handshake(data)
		bytes_back = self.check_bytes_back(data)
		checksum = self.check_checksum(data)
		if handshake and bytes_back and checksum:
			return True
		else:
			return False
	
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
