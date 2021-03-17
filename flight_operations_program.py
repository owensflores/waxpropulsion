"""
Script for operations of Blue Origin wax micropayload experiment. 
Runs on Raspberry Pi in Python
Base code where tagged provided by Z Porter, NanoRacks LLC
Program completed by gowens with Space Enabled, MIT

From nff-sample.py provided by Nanoracks: 

Sample python code for NanoLab payload on the NanoRacks Feather Frame. Program opens
up a serial connection and listens to decode any incoming feather frame packets. Default
values and ports are especially for use on a raspberry pi zero through the UART0 interface.
All code is provided as-is by NanoRacks to help customers develop flight code for their 
Feather Frame payloads as quickly and easily as possible.

Note:
  - Use pip to download the pyserial library (pip install pyserial) if it's missing.
  - For pi zero, a line must be added to /etc/rc.local to run the python script on 
  startup. For example: python /home/pi/nff-sample.py &. The ending & runs the program
  in the background.

last modified by gowens March 13, 2021
"""


import time
import serial
import RPi.GPIO as GPIO


MAXBUFFER = 200
NUMDATAFIELDS = 21

# This is specific to the pi zero. Must have serial enabled and console over serial disabled.
PORTNAME = '/dev/ttyAMA0'

BAUDRATE = 115200
TIMEOUT = 0.02

# assign output pins here
[heaterPin, motorPin] = [1,2] # or whatever we assign
GPIO.setup(chan_list, GPIO.OUT)

# Dictionary to hold all of the current flight information.
FLIGHT_DATA = {'flight_event': 0, 
                'exptime': 0,
                'altitude': 0,
                'gps_altitude': 0,
                'velocity': [0,0,0],
                'acc_magnitude': 0,
                'acceleration': [0,0,0],
                'attitude': [0,0,0],
                'angular_velocity': [0,0,0],
                'warnings': [0,0,0,0]}


""" parse_serial_packet
Parses the incoming serial packet and updates the flight data

Arguments:
    incoming_data = string of serial data.
Returns:
    true or false depending on successful parsing or not.
"""
def parse_serial_packet(incoming_data):
    # Remove leading or trailing white space and separate the fields.
    incoming_data = incoming_data.strip()
    fields = incoming_data.split(',')

    # Ensure that the appropriate number of data fields are present.
    if len(fields) != NUMDATAFIELDS:
        return False
    else:
        index = 0
        for field in fields:
            if index == 0:
                FLIGHT_DATA['flight_event'] = field
            elif index == 1:
                FLIGHT_DATA['exptime'] = float(field)
            elif index == 2:
                FLIGHT_DATA['altitude'] = float(field)
            elif index == 3:
                FLIGHT_DATA['gps_altitude'] = float(field)
            elif index == 4:
                FLIGHT_DATA['velocity'][0] = float(field)
            elif index == 5:
                FLIGHT_DATA['velocity'][1] = float(field)
            elif index == 6:
                FLIGHT_DATA['velocity'][2] = float(field)
            elif index == 7:
                FLIGHT_DATA['acc_magnitude'] = float(field)
            elif index == 8:
                FLIGHT_DATA['acceleration'][0] = float(field)
            elif index == 9:
                FLIGHT_DATA['acceleration'][1] = float(field)
            elif index == 10:
                FLIGHT_DATA['acceleration'][2] = float(field)
            elif index == 11:
                FLIGHT_DATA['attitude'][0] = float(field)
            elif index == 12:
                FLIGHT_DATA['attitude'][1] = float(field)
            elif index == 13:
                FLIGHT_DATA['attitude'][2] = float(field)
            elif index == 14:
                FLIGHT_DATA['angular_velocity'][0] = float(field)
            elif index == 15:
                FLIGHT_DATA['angular_velocity'][1] = float(field)
            elif index == 16:
                FLIGHT_DATA['angular_velocity'][2] = float(field)
            elif index == 17:
                FLIGHT_DATA['warnings'][0] = int(field)
            elif index == 18:
                FLIGHT_DATA['warnings'][1] = int(field)
            elif index == 19:
                FLIGHT_DATA['warnings'][2] = int(field)
            elif index == 20:
                FLIGHT_DATA['warnings'][3] = int(field)
            index = index + 1
        return True


""" Defining helper functions to run the various parts of the experiment: 
heating the wax and melting it, spinning the wax up to cast it, and cooling it

QUESTION: DO THESE LOOPS NEED ESTIMATION? 
"""

def getTempAndRPM():
	# read and output temperature and angular velocity sensor (combined for now, unnecessary though)
	# assumes there will be a readable temperature sensor 
	data = open(device_file, 'r')
    lines = data.readlines()
    data.close()
    return temp,rpm  

def heatUpAndMelt():
	# turn on heater, i.e. send voltage to heater GPIO pin
	meltingPoint = 69 #Celsius; from An Investigation of the Centrifugal Casting of ParaffinWax in the Laboratory and in Microgravity
	while getTempAndSpeed(0) < meltingPoint:
		GPIO.output(heaterPin, GPIO.HIGH) #unclear if this will be PWM, but my guess is yes
		print("heating up")
		return False
	else 
		heaterPin = Low
		print("at temp")
		return True
    

def coolDownAndSpinUp():
	GPIO.output(heaterPin, GPIO.LOW)
	print("cooling down")
	idealRPM = 800 #RPM; from An Investigation of the Centrifugal Casting of ParaffinWax in the Laboratory and in Microgravity
	while getTempAndSpeed(1) <= idealRPM:
		GPIO.output(motorPin, GPIO.HIGH) #this is a motor so will be PWM
    	print("spinning up")
	return True

def shutDown()
	GPIO.output(motorPin, GPIO.LOW) # this is crude at the moment, might look like stepping down slowly? 

""" main

Arguments:
    none
Returns:
    none
"""
def main():
    # Flag to keep track of whether or not the wax has melted
    isWaxMelted = False

    # Flag to keep track of the spinning
    isWaxSpinning = False

    # Flag to keep track of experiment
    experimentRun = False

    # Wait about 5 seconds before starting (probably unnecessary)
    time.sleep(5)

    # Initialize the experiment by starting to heat the wax up

    

    # Open serial connection. Add more robust error handling to this section if
    # desired.
    ser = serial.Serial(port=PORTNAME, baudrate=BAUDRATE, timeout=TIMEOUT)


    # Main loop to continuously read in incoming data and attempt to parse it.
    while not experimentRun: #i.e. run continuously while experiment hasn't been completed 
        # Check for any available data in the input serial buffer according to the polling rate.
        
        # while ser.in_waiting == 0:
        #   time.sleep(0.01)

        # Read in up to the maximum size of data per line.
        data_in = ser.read(MAXBUFFER)

        # Check that some data was received.
        if (len(data_in) == 0):
            continue

        # Check that packet was well formatted.
        if not parse_serial_packet(data_in):
            continue

        if (FLIGHT_DATA['flight_event'] == "F"): # this corresponds with the flight event "seperation"
        	while not isWaxMelted: 
        		isWaxMelted = heatUpAndMelt() # this should run the heat up function and break the loop when the heater has done its thing


		if (FLIGHT_DATA['flight_event'] == "G"): # G is assuming apogee is when we start running the experiment
        	if not isWaxSpinning:
                isWaxSpinning = coolDownAndSpinUp()
 				time.wait() #wait a certain amount of time for casting



if __name__=="__main__":
    main()
