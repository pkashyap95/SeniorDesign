Senior Design: Green Team

---

Our project aims to measure head movement and eye movements which occur at the same time. It then takes these measurements and transmits them to a model car which the user is able to control. 

A camera mounted on the car will stream video to a computer and display what the car sees. The user would be able to change the trajectory of the car with head movements and is able to monitor the changes with the help of software pointers/guides. To avoid any unwanted movements, our system tracks the pupil as a means of making a final decision, where the user has to ‘commit' to the turn or movement. 

Gestures made with the eye are implemented in order to commit specific actions such as controlling the streaming of the data of the head and eye movements.

System Interaction: 





Hardware

  Hardware         	Cost  	Link                  
  RaspberryPi 3    	$35   	http://bit.ly/1OJ7yN2 
  Arduino Uno      	$17.95	http://amzn.to/2qzaCef
  Ultrasonic Sensor	$9.86 	http://amzn.to/2pZ7Vzt
  HC05             	$8.49 	http://amzn.to/2qxj3Gy
  ArduCam          	$14.99	http://amzn.to/2qCsfrB
  MPU 6050         	$5.75 	http://amzn.to/2qzhBE1

EH Tracking

We made use of PyGaze - the open-source toolbox for eye tracking to perform the eye tracking component of our system. The flow chart below explains the exact working of the eye tracking algorithm that we implemented. In addition, to the eye tracking we used an MPU 6050 to perform head tracking (determining the head position).  Comp2.py is the class that actually gets data from the MPU 6050. An instance of the class is created in camtracker.py. 

To run all the above use python 2.7.

Arduino Car Code

The snippet below is essential for Arduino to receive data from the head set. It only receives data when there is 4 bytes available and stores them in order incomingByte0 onwards. It then changes the speed according to values received to execute the various scenarios. 

          if(mySerial.available()>=4){ 
            char incomingByte0 = mySerial.read();
            char incomingByte1 = mySerial.read();
            char incomingByte2 = mySerial.read();
            char incomingByte3 = mySerial.read();

PiStreaming

We used the PiStreaming video demo created by user waveform80. 
