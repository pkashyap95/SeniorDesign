#!/usr/bin/python
import smbus
import math
import time
import csv
import serial


class IMU_Reader:
        accel_scaled_z=0
        gyro_scaled_x=0
        gyro_scaled_y=0
        gyro_scaled_z=0
        gyro_offset_x=0
        gyro_offset_y=0
        gyro_offset_z=0
        gyro_total_x=0
        gyro_total_y=0
        gyro_total_z=0
        get_x_rotation=0
        get_y_rotation=0
        get_z_rotation=0
        last_x=0
        last_y=0
        last_z=0
        sample=0
        now=time.time()
        

        
	def __init__(self):
	       # Power management registers
	        self.power_mgmt_1 = 0x6b
	        self.power_mgmt_2 = 0x6c
		# sensitivity of the sensors
		self.gyro_scale = 131.0
		self.accel_scale = 16384.0
		self.address = 0x68  # This is the address value read via the i2cdetect command
		    # raise SerialException("could not open port %s: %s" % (self._port, msg))
                self.bluetoothSerial = serial.Serial("/dev/rfcomm1", baudrate=9600)
		# or bus = smbus.SMBus(1) for Revision 2 boards
		self.bus = smbus.SMBus(1)
		# Now wake the 6050 up as it starts in sleep mode
		self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)
		self.K = 0.98
		self.K1 = 1 - self.K
		self.time_diff = 0.01


	def goStraight(self):
		self.bluetoothSerial.write(str(2004))
	
#        def goBack(self):
#		self.bluetoothSerial.write(str(4004))


	def backward(self,accel_scaled_z):
		if(accel_z_scaled <= 3):		
			self.bluetoothSerial.write(str(4000+172))
	
 	def leftTurn(self,gyro_total_y):
        	angle = -(gyro_total_y)
        	# 360*Vl/2*pi*angle
        	r = ((360) * 172) / (2 * 3.14 * angle)
        	# Vl(R+wheeltowheel)/R
        	#print (172 * (r + 142) / r)
        	# print 'left'
		self.bluetoothSerial.write(str(1000 + 172 * (r + 142) / r))
		

	def rightTurn(self,gyro_total_y):
		angle = (gyro_total_y)
		# 360*Vr/2*pi*angle
		r = ((360) * 172) / (2 * 3.14 * angle)
		#Vr(R+wheeltowheel)/R
		#print (172 * (r + 142) / r)
		self.bluetoothSerial.write(str(3000 + 172 * (r + 142) / r))

		
	def twos_compliment(self,val):
		if (val >= 0x8000):
			return -((65535 - val) + 1)
		else:
			return val

	def readAll(self):
		raw_gyro_data = self.bus.read_i2c_block_data(self.address, 0x43, 6)
		raw_accel_data = self.bus.read_i2c_block_data(self.address, 0x3b, 6)
		gyro_scaled_x = self.twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.gyro_scale
		gyro_scaled_y = self.twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.gyro_scale
		gyro_scaled_z = self.twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.gyro_scale
		accel_scaled_x = self.twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / self.accel_scale
		accel_scaled_y = self.twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / self.accel_scale
		accel_scaled_z = self.twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / self.accel_scale
		return (
		    gyro_scaled_x,
		    gyro_scaled_y,
		    gyro_scaled_z,
		    accel_scaled_x,
		    accel_scaled_y,
		    accel_scaled_z)

	def dist(self, a, b):
		return math.sqrt((a * a) + (b * b))

	def get_y_rotation(self,x, y, z):
		radians = math.atan2(x, self.dist(y, z))
		return -math.degrees(radians)

	def get_x_rotation(self,x, y, z):
		radians = math.atan2(y, self.dist(x, z))
		return math.degrees(radians)

        def startReading(self):
		time.sleep(self.time_diff - 0.005)
		(gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = self.readAll()
		self.gyro_scaled_x -= self.gyro_offset_x
		self.gyro_scaled_y -= self.gyro_offset_y
		self.gyro_scaled_z -= self.gyro_offset_z
		gyro_x_delta = (gyro_scaled_x * self.time_diff)
		gyro_y_delta = (gyro_scaled_y * self.time_diff)
		gyro_z_delta = (gyro_scaled_z * self.time_diff)
		self.gyro_total_x += gyro_x_delta
		self.gyro_total_y += gyro_y_delta
		self.gyro_total_z += gyro_z_delta
		rotation_x = self.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
		rotation_y = self.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
		last_x = self.K * (self.last_x + gyro_x_delta) + (self.K1 * rotation_x)
		last_y = self.K * (self.last_y + gyro_y_delta) + (self.K1 * rotation_y)
		self.sample = self.sample + 1
		return [self.sample, rotation_x, self.gyro_total_x, last_x, rotation_y, self.gyro_total_y, last_y, self.gyro_total_z, self.accel_scaled_z]


	def intialRead(self):
		(gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = self.readAll()
		self.last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
		self.last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
		self.gyro_offset_x = gyro_scaled_x
		self.gyro_offset_y = gyro_scaled_y
		self.gyro_total_x = (last_x) - self.gyro_offset_x
		self.gyro_total_y = (last_y) - self.gyro_offset_y
		self.sample=1
