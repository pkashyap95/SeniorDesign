#include <Wire.h>
#include <Adafruit_MotorShield.h> //import your motor shield library
#include <SoftwareSerial.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#define trigPin 8  //define the pins of your sensor
#define echoPin 9

char inChar1;
int dir;
int val_1;
int recSpeed=0;
int trial=0;
int supaspeed;
int motorSpeed;

//import motor shield library
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);  //set up right motor
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);  //set up left motor
//initalizing bluetooth connection
SoftwareSerial mySerial(3, 4);  //RX, TX

void setup(){
  Serial.begin(9600);  //begin serial communitication
  Serial.println("Motor test!");
  Serial.println("Let's get these angles!");
  //Input for the ultrasonic sensor
//  pinMode(trigPin, OUTPUT);// set the trig pin to output (Send sound waves)
//  pinMode(echoPin, INPUT);// set the echo pin to input (recieve sound waves)
  AFMS.begin(); 
  myMotor1->run(BACKWARD);
  myMotor2->run(BACKWARD);
  mySerial.begin(9600);

  }


void loop(){  
    //supaspeed= map(recSpeed, 0, 435, 0, 255);
    if(mySerial.available()>=0){
      trial++;
      if(trial==1){
        inChar1 = mySerial.read();
        val_1= (inChar1 - '0');
        dir=val_1;
      }
      if(trial==2){
        inChar1 = mySerial.read();
        val_1= (inChar1 - '0');
        motorSpeed=val_1*100;
      }
      if(trial==3){
        inChar1 = mySerial.read();
        val_1= (inChar1 - '0');
        motorSpeed=motorSpeed+val_1*10;
      }
      if(trial==4){
        inChar1 = mySerial.read();
        val_1= (inChar1 - '0');
        motorSpeed=motorSpeed+val_1;
        if(motorSpeed>0){
          if(dir==1){
            Serial.println("The motorspeed is: 1");
            supaspeed= map(motorSpeed, 0, 435, 0, 255);
            Serial.println("The translated speed is: 1");
            myMotor1->setSpeed(supaspeed);
            myMotor2->setSpeed(100);
          }
          if(dir==2){
            myMotor1->setSpeed(100);
            myMotor2->setSpeed(100);

          }
          if(dir==3){
            Serial.println("The motorspeed is: 3");
            supaspeed= map(motorSpeed, 0, 435, 0, 255);
            Serial.println("The translated speed is: 3");
            myMotor1->setSpeed(100);
            myMotor2->setSpeed(supaspeed);
          }
        }
        motorSpeed=0;
      }      
    }
}void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
