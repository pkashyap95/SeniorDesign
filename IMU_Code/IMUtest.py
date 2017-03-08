#!/usr/bin/python
import time
import smbus
import math

#For releasing resources at the end of the program
import RPi.GPIO as GPIO

#Defines time
print "time.gmtime() : %s" % time.gmtime()

#To send the values to a CSV File
import csv  

#Please change the file path when working on a different RPi
csvfile = "/home/pi/Desktop/IMU_data/IMUdata" + ".csv"

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

#condition for readings to be made FOREVER, dun dun dun
count=1

#Defines reading from the addresses stored in the IMU
def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

#accelerometer values converted from 2s complement form to normal
time.sleep(0.01)
def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

#Defines x and y rotations and converts from radians to degrees
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
	
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 1)

output = open(csvfile, 'w')
writer = csv.writer(output, lineterminator='\n')

#Sample count starts at 0 and increments in the while loop
sam_count = 0
timecount = time.time()
while count == 1:
	print "gyro data"
	print "---------"

#introduce a delay to derease/control the sampling rate
	time.sleep(0.01)
	gyro_xout = read_word_2c(0x43)
	time.sleep(0.01)
	gyro_yout = read_word_2c(0x45)
	time.sleep(0.01)
	gyro_zout = read_word_2c(0x47)

	print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 65.5)
	print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 65.5)
	print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 65.5)

	print
	print "accelerometer data"
	print "------------------"

	accel_xout = read_word_2c(0x3b)
	accel_yout = read_word_2c(0x3d)
	accel_zout = read_word_2c(0x3f)

	accel_xout_scaled = accel_xout / 16384.0
	accel_yout_scaled = accel_yout / 16384.0
	accel_zout_scaled = accel_zout / 16384.0

	print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
	print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
	print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

	print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	
	gyrox = gyro_xout / 131
	gyroy = gyro_yout / 131
	gyroz = gyro_zout / 131

	xrotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	yrotation = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
	sam_count= sam_count + 1

#Head rotation, roll and sample count
	row = [gyroy, gyroz]	
	writer.writerow(row)
GPIO.cleanup()
fclose(output)
