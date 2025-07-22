import serial
import math
import time

# Set up UART
ser = serial.Serial('/dev/ttyUSB1', 1000000) #1Mbps baud rate

# 64-point sine wave
sine_wave = [
    int(128 + 100 * math.sin(2 * math.pi * i / 128))
    for i in range(128)
]

# Interleave I and Q
iq_stream = [val for pair in zip(sine_wave, sine_wave) for val in pair]  # I=Q here; you can change Q separately

# Continuously send interleaved data
for i in range(0, 500):
	for val in iq_stream:
		ser.write(bytes([val]))
        	#delay can be given if required. Runs at max efficiency without delay.

ser.close()
