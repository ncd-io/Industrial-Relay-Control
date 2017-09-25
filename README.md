# ProXR-Fusion-Taralist

## What This Library is For

>This library is for any ProXR, Fusion, or Taralist board and any Relay Expansion Board that can be connected to them.
>This does not include UXP Expansion boards with things such as ADC, Contact Closure, or Potentiometers.
>Below are some links to pertinent products:
>Fusion https://store.ncd.io/?fwp_main_facet=ncd-industrial&fwp_product_type=relay-controllers&fwp_series=fusion
>ProXR https://store.ncd.io/?fwp_main_facet=ncd-industrial&fwp_product_type=relay-controllers&fwp_series=proxr
>Taralist https://store.ncd.io/?fwp_main_facet=ncd-industrial&fwp_product_type=relay-controllers&fwp_series=taralist

## About This Library

>This library acts a translation layer to save you from having to learn the API and command structure to control your boards.
>Simply use methods like turn_on_relay_by_index and you won't have to do any bit or byte calculations to determine the correct command.

### What This Library Does

>Allows you to use serial ports or TCP/IP sockets interchangeably with just a simple Communication object declaration
>Allows multiple ways to control relays based on what works best for you and your application with no bit manipulation or direct byte writes
>Allows you to easily get ADC/Sensor Readings in bulk or in singular at 8 or 10 bit resolution.
>On, off, and toggle commands.
>Control Relays by bank or index
>Timers and Flashers supported

### What This Library Doesn't Do

>This library does not create, maintain, or close any communication ports or sockets.
>These communication buses will be maintained by you in your application to allow you to keep it open or only open it as your applciation needs.
>This library does not read out real world values of your sensors based on your ADC readings.
>Sensors require a particular equation or table to get accurate readings so incorporating all of them would be impossible.
>This library does not release computer control for those series that have alternative automation capabilities such as Fusion and Taralist

## About the Code

### Instantiation

>This library has class called Relay_Controller that can be instantiated by simply calling it and passing it a Communication Bus.
>This bus can either be a serial port or a TCP/IP socket.
>You should view the examples to get a better idea of how this works.

### Methods

#### Control Methods
toggle_relay_by_index(relay)
>This command accepts an integer value for the Relay Number (1-512) and inverses the current state of that relay.

turn_on_relay_by_index(relay)
>This command accepts an integer value for the Relay Number (1-512) and turns on that relay.

turn_off_relay_by_index(relay)
>This command accepts an integer value for the Relay Number (1-512) and turns off that relay.

turn_on_relay_by_index(relay)
>This command accepts an integer value for the Relay Number (1-512) and turns on that relay.

##### Advanced
start_relay_timer(timer, hours, minutes, seconds, relay)
>Relay timers are a very powerful and somewhat complex component of our Industrial Relay Controllers
>This command will allow you to tell a command to be on for a certain amount of time and then shut off.
>Argument one is the number of the timer (1-16).
>Argument two is time in hours (0-255)
>Argument three is time in minutes (0-255)
>Argument four is time in seconds (0-255)
>Argument five is the target relay (1-256)

turn_on_relay_by_bank(relay, bank)
>This method turns on a relay (1-8) in a specified bank of 8 relays.

turn_off_relay_by_bank(relay, bank)
>This method turns off a relay (1-8) in a specified bank of 8 relays. 

turn_off_relay_group(relay, bank, group_size)
>This command accepts an integer from 1 to 8 for the relay argument.
>The bank argument will be an integer to target a particular bank of 8 relays.
>The group_size argument is an integer for how many relays after the relay argument should be turned off.
>turn_off_relay_group(3, 1, 2) would turn off relays 3, 4, and 5. turn_off_relay_group(3, 1, 4) would turn off relays 3, 4, 5, 6 and 7. 

turn_on_relay_group(relay, bank, group_size)
>This command accepts an integer from 1 to 8 for the relay argument.
>The bank argument will be an integer to target a particular bank of 8 relays.
>The group_size argument is an integer for how many relays after the relay argument should be turned off.
>turn_ofn_relay_group(3, 1, 2) would turn on relays 3, 4, and 5. turn_on_relay_group(3, 1, 4) would turn on relays 3, 4, 5, 6 and 7. 

set_relay_bank_status(status, bank)
>This method accepts a value from 0 to 255 for status and an integer for the bank.
>Bank 1 will include the first 8 relays.
>A status of 255 will turn on all relays and is 8 bits all set to 1: 11111111. 
>A status of 3 is the first 2 bits set to 1 and will turn on the first two relays.
>This is the most flexible relay command, but also the hardest to use due to account for existing relay states and bit manipulation.

##### Miscellaneous Control Methods
turn_on_relay_flasher(relay)
>Activates a flasher on the relay passed in (1-256). The frequency of the flash can be set with set_flasher_speed.

turn_off_relay_flasher(relay)
>Deactivates a flasher on the relay passed in (1-256). The frequency of the flash can be set with set_flasher_speed.

set_flasher_speed(speed)
>Set the speed at which flashers flash. 0 is the fastest and 255 is the slowest.

#### Monitoring Methods
##### Relay Monitoring
get_relay_bank_status(bank)
>Returns an integer representation of the byte value of the bank's relay status'.
>255 means all relays are on. 0 means all relays are off. 9 means relays 1 and 4 are on.

get_relay_status_by_index(relay)
>Returns the status of a single relay. The relay argument is an integer from 1-512.

get_relay_status_by_bank(relay, bank)
>Returns the status of a specific relay in a specific bank. The relay argument will be an integer from 1-8.

##### ADC Monitoring
read_single_ad8(channel)
>Returns the value of an ADC reading in a 1 byte integer (0-255). The integer will be in an array i.e. [255]

read_all_ad8()
>Returns the value of all 8 channels of ADC in an array. item[0] is channel 1 item[1] is channel 2 etc.
>The reading will be from 0 to 255.

read_single_ad10(channel)
>Returns the value of an ADC reading in a 10 bit integer (0-1023). The integer will be in an array i.e. [784]

read_all_ad10()
>Returns the value of all 8 channels of ADC in an array. item[0] is channel 1 item[1] is channel 2 etc.
>The reading will be from 0 to 1023.

#### Utility Methods
renew_replace_interface(combus)
>This method updates the combus the device is using.
>Useful if there is a change, reboot, or any other reason you need to renegotiate a serial port or TCP socket.
>combus will be your serial port or TCP socket object.

wrap_in_api(data)
>This method simply takes an integer array such as [254, 108, 1] and wraps it into an API.

send_command(command, bytes_back)
>If you find yourself needing to use a command that isn't supported by this library you can use this method.
>In conjunction with wrap_in_api it is relatively easy to send commands.

process_control_command_return(data)
>Just checks the API packet from the device to make sure its a proper data packet and returns a boolean.

process_read_command_return(data)
>Checks the data packet to ensure quality communications and returns either the payload of the packet or False if failed.
