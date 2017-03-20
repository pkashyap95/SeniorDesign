#include <Wire.h>
#include <Adafruit_MotorShield.h> //import your motor shield library
#include "utility/Adafruit_MS_PWMServoDriver.h"
#define trigPin 13 // define the pins of your sensor
#define echoPin 12 
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1); // set up motors.
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
 
 
void setup() {
  Serial.begin(9600); // begin serial communitication  
  Serial.println("Motor test!");
   pinMode(trigPin, OUTPUT);// set the trig pin to output (Send sound waves)
  pinMode(echoPin, INPUT);// set the echo pin to input (recieve sound waves)
  AFMS.begin(); 
  myMotor1->setSpeed(155); //set the speed of the motors, between 0-255
  myMotor2->setSpeed(155);  
  myMotor1->run(FORWARD);
  myMotor2->run(FORWARD);
}
 
void loop() {

   long duration, distance; // start the scan
  digitalWrite(trigPin, LOW);  
  delayMicroseconds(2); // delays are required for a succesful sensor operation.
  digitalWrite(trigPin, HIGH);

  delayMicroseconds(10); //this delay is required as well!
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;// convert the distance to centimeters.
  
  if (distance <= 90 && distance > 80)/*if there's an obstacle 25 centimers, ahead, do the following: */ {   
     Serial.println ("Close Obstacle detected!" );
     Serial.println ("Speed is now 135");
     Serial.print ("Distance From Robot is " );
     Serial.print ( distance);
     Serial.print ( " CM!");// print out the distance in centimeters.
     myMotor1->setSpeed(135); 
     myMotor2->setSpeed(135);
   }
   else if (distance <= 80 && distance > 70)/*if there's an obstacle 25 centimers, ahead, do the following: */ {   
       Serial.println ("Close Obstacle detected!" );
       Serial.println ("Speed is now 115");
       Serial.print ("Distance From Robot is " );
       Serial.print ( distance);
       Serial.print ( " CM!");// print out the distance in centimeters.
       myMotor1->setSpeed(115); 
       myMotor2->setSpeed(115);
  }
 else if (distance <= 70 && distance > 60)/*if there's an obstacle 25 centimers, ahead, do the following: */ {   
   Serial.println ("Close Obstacle detected!" );
   Serial.println ("Speed is now 95");
   Serial.print ("Distance From Robot is " );
   Serial.print ( distance);
   Serial.print ( " CM!");// print out the distance in centimeters.
   myMotor1->setSpeed(95); 
   myMotor2->setSpeed(95);
  }
 else if (distance <= 60 && distance > 50)/*if there's an obstacle 25 centimers, ahead, do the following: */ {   
   Serial.println ("Close Obstacle detected!" );
   Serial.println ("Speed is now 70");
   Serial.print ("Distance From Robot is " );
   Serial.print ( distance);
   Serial.print ( " CM!");// print out the distance in centimeters.
   myMotor1->setSpeed(70); 
   myMotor2->setSpeed(70);
  }
  
 else if (distance <= 50 && distance > 40)/*if there's an obstacle 25 centimers, ahead, do the following: */ {   
   Serial.println ("Close Obstacle detected!" );
   Serial.println ("Speed is now 45");
   Serial.print ("Distance From Robot is " );
   Serial.print ( distance);
   Serial.print ( " CM!");// print out the distance in centimeters.
   myMotor1->setSpeed(45); 
   myMotor2->setSpeed(45);
  }
  
 else if (distance <= 40 && distance > 30)/*if there's an obstacle 25 centimers, ahead, do the following: */ {   
   Serial.println ("Close Obstacle detected!" );
   Serial.println ("Speed is now 20");
   Serial.print ("Distance From Robot is " );
   Serial.print ( distance);
   Serial.print ( " CM!");// print out the distance in centimeters.
   myMotor1->setSpeed(20); 
   myMotor2->setSpeed(20);
  }
  
 else if (distance <= 30 && distance >=0)/*if there's an obstacle 25 centimers, ahead, do the following: */ {   
   Serial.println ("Close Obstacle detected!" );
   Serial.println ("Speed is now 0");
   Serial.print ("Distance From Robot is " );
   Serial.print ( distance);
   Serial.print ( " CM!");// print out the distance in centimeters.
   myMotor1->setSpeed(0); 
   myMotor2->setSpeed(0);
  }
  
  else {
   Serial.println ("No obstacle detected. going forward");
   delay (15);
   myMotor1->setSpeed(155); //set the speed of the motors, between 0-255
   myMotor2->setSpeed(155);
   myMotor1->run(BACKWARD); //if there's no obstacle ahead, Go Forward! 
   myMotor2->run(BACKWARD);  
   delay(10);
  }  
}
