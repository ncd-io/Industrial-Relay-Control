#import the pyserial module
import socket
import ncd_industrial_relay


#set up your socket with the desired settings.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#instantiate the board object and pass it the network socket
board1 = ncd_industrial_relay.Relay_Controller(sock)
#connect the socket using desired IP and Port
IP_ADDRESS = "192.168.1.37"
PORT = 2101
sock.connect((IP_ADDRESS, PORT))
sock.settimeout(.5)

#pass these methods a number between 1 and 512 to set the current status of the relay
print board1.turn_on_relay_by_index(1)
print board1.turn_on_relay_by_index(2)
print board1.turn_off_relay_by_index(1)
print board1.turn_off_relay_by_index(2)

#pass these methods a number between 1 and 512 to get the current status of the relay
print board1.get_relay_status_by_index(1)
print board1.get_relay_status_by_index(2)

#close the interface, not necessary here but you may need to in your application
sock.close()

#you can renew or replace your communication interface with new settings if desired.
#serial_port = serial.Serial('COM27', baudrate=115200, bytesize=8, stopbits=1, timeout=.5)
#you can update this serial port by using the following method and passing the new combus
#this would allow you to switch between two interfaces on a fusion board for instance.
#Could be used if the network interface goes down and you need to communicate to it via a USB port.
#board1.renew_replace_interface(serial_port)

#sockets require you to re-instantiate the connection as the OS wipes the connection data on close.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP_ADDRESS, PORT))
sock.settimeout(.5)

board1.renew_replace_interface(sock)

#set the status of a bank, 255 is all relays on, 3 is relay one and two etc. The value is based on an 8 bit value so 3 = 00000011 = relays one and two will be on.
#the first arg is the relay value. The second arg is the bank number.
print board1.set_relay_bank_status(3, 1)

#get a relay status value for the board in a byte value The value is based on an 8 bit value so 3 = 00000011 = relays one and two are on.
#The argument is the relay bank
print board1.get_relay_bank_status(1)

#control relays by number and by bank. The first argument is the relay number from 1-8. The second argument is the bank number.
print board1.turn_on_relay_by_bank(2, 1)
print board1.turn_off_relay_by_bank(2, 1)

#monitor relay by number and by bank. The first argument is the relay number from 1-8. The second argument is the bank number.
print board1.get_relay_status_by_bank(1, 1)

#get the adc reading of one input in 8 bits resolution. Pass it the number of the ADC (1-8).
#This method returns an array with one item in it.
try:
	print board1.read_single_ad8(1)
except:
	print 'The ADC read command failed due to a socket timeout. Most likely your board does not have AD Inputs'
#get the adc reading of all ADC inputs in 8 bit resolution. This method returns an array of values indexed by their number-1.
#read_all_ad8[0] will be ADC 1 etc.
try:
	print board1.read_all_ad8()
except:
	print 'The ADC read command failed due to a socket timeout. Most likely your board does not have AD Inputs'
#get the adc reading of one input in 10 bits resolution. Pass it the number of the ADC (1-8).
#This method returns an array with one item in it.
try:
	print board1.read_single_ad10(1)
except:
	print 'The ADC read command failed due to a socket timeout. Most likely your board does not have AD Inputs'
	
#get the adc reading of all ADC inputs in 10 bit resolution. This method returns an array of values indexed by their number-1.
#read_all_ad10[0] will be ADC 1 etc.
try:
	print board1.read_all_ad10()
except:
	print 'The ADC read command failed due to a socket timeout. Most likely your board does not have AD Inputs'

#relay group commands allow you to easily control multiple relays simultaneously.
#Argument one is the first relay number (1-8). Argument two is the bank number. Argument three is the number of subsequent relays to control in desired bank.
print board1.turn_on_relay_group(1, 1, 7)
print board1.turn_off_relay_group(1, 1, 7)

#toggle a relay by index. Pass a relay number from 1 to 512
print board1.toggle_relay_by_index(1)
print board1.toggle_relay_by_index(1)

#configure flasher speed
print board1.set_flasher_speed(5)

#tell relay to begin flashing. The argument passed is the number of the relay you would like to flash.
print board1.turn_on_relay_flasher(1)
print board1.turn_off_relay_flasher(1)

#tell a relay timer to start.
#Argument one is the number of the timer (1-16).
#Argument two is time in hours
#Argument three is time in minutes
#Argument four is time in seconds
#Argument five is the target relay (1-256)
print board1.start_relay_timer(1, 0, 0, 5, 1)

#close the socket after we are done with it. Its good practice to close a TCP socket when you are no longer using it.
#no one wants to walk over to a board and unplug it if comms get stuck open on one end and not the other.
sock.close()
