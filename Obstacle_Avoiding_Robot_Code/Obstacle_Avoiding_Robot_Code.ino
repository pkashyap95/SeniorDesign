#include <Wire.h>
#include <Adafruit_MotorShield.h> //import your motor shield library
#include "utility/Adafruit_MS_PWMServoDriver.h"
#define trigPin 13 // define the pins of your sensor
#define echoPin 12 
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1); // set up right motor
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2); // set up left motor



void setup(){
  Serial.begin(9600); // begin serial communitication  
  Serial.println("Motor test!");
  pinMode(trigPin, OUTPUT);// set the trig pin to output (Send sound waves)
  pinMode(echoPin, INPUT);// set the echo pin to input (recieve sound waves)
  AFMS.begin(); 
  }
  
void loop() {

CarMovement(27);
}


int CarMovement(int angle){
  long duration, STD_distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2); // delays are required for a succesful sensor operation.
  digitalWrite(trigPin, HIGH);

  delayMicroseconds(10); //this delay is required as well!
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  STD_distance = (duration/2) / 29.1;// convert the STD_distance to centimeters.
  
  long A, B, C, D, E;
  A == (angle <= 10 && angle > -10);          //Straight
  B == (angle <= 30 && angle > 10);           //Sharp Right Turn
  C == (angle <= 70 && angle > 30);           //Wide Right Turn
  D == (angle <= -30 && angle > -10);         //Sharp Left Turn
  E == (angle <= -70 && angle > -30);         //Wide Left Turn
   
switch(angle){
  
  case 'B':                                   //10 to 30 degree right turn
  if(STD_distance <= 90 && STD_distance > 60){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(STD_distance*1.65); 
    myMotor2->setSpeed(STD_distance*1.65);
  }
  else if(STD_distance <= 60 && STD_distance > 30){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(STD_distance*1.5); 
    myMotor2->setSpeed(STD_distance*1.5);
    }
  else if(STD_distance <= 30 && STD_distance >= 0){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(0); 
    myMotor2->setSpeed(0);
    }
  else{
    myMotor1->setSpeed((angle*3)+40); 
    myMotor2->setSpeed((angle*4.5)+40);
  }
  break;

  case 'C':                                   //30 to 70 degree right turn
  if(STD_distance <= 90 && STD_distance > 60){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(STD_distance*1.65); 
    myMotor2->setSpeed(STD_distance*1.65);
  }
  else if(STD_distance <= 60 && STD_distance > 30){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(STD_distance*1.5); 
    myMotor2->setSpeed(STD_distance*1.5);
    }
  else if(STD_distance <= 30 && STD_distance >= 0){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(0); 
    myMotor2->setSpeed(0);
    }
  else{
    myMotor1->setSpeed(angle*2); 
    myMotor2->setSpeed(angle*4.5);
  }
  break;

  case 'D':                                   //10 to 30 degree left turn
  if(STD_distance <= 90 && STD_distance > 60){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(STD_distance*1.65); 
    myMotor2->setSpeed(STD_distance*1.65);
  }
  else if(STD_distance <= 60 && STD_distance > 30){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(STD_distance*1.5); 
    myMotor2->setSpeed(STD_distance*1.5);
    }
  else if(STD_distance <= 30 && STD_distance >= 0){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(0); 
    myMotor2->setSpeed(0);
    }
  else{
    myMotor1->setSpeed((angle*3)+40); 
    myMotor2->setSpeed((angle*4.5)+40);
  }
  break;

  case 'E':                                   //30 to 70 degree left turn
  if(STD_distance <= 90 && STD_distance > 60){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(STD_distance*1.65); 
    myMotor2->setSpeed(STD_distance*1.65);
  }
  else if(STD_distance <= 60 && STD_distance > 30){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(STD_distance*1.5); 
    myMotor2->setSpeed(STD_distance*1.5);
    }
  else if(STD_distance <= 30 && STD_distance >= 0){
    Serial.print("There's an obstacle: " + String(STD_distance) + "away");
    myMotor1->setSpeed(0); 
    myMotor2->setSpeed(0);
    }
  else{
    myMotor1->setSpeed(angle*4.5); 
    myMotor2->setSpeed(angle*2);
  }
  break;
  
  default :                                    //Straight
  
  if(STD_distance <= 90 && STD_distance > 60){
    myMotor1->setSpeed(STD_distance*1.65); 
    myMotor2->setSpeed(STD_distance*1.65);
  }
  else if(STD_distance <= 60 && STD_distance > 30){
    myMotor1->setSpeed(STD_distance*1.5); 
    myMotor2->setSpeed(STD_distance*1.5);
    }
  else if(STD_distance <= 30 && STD_distance >= 0){
    myMotor1->setSpeed(0); 
    myMotor2->setSpeed(0);
    }
  else{
    myMotor1->setSpeed(155); 
    myMotor2->setSpeed(155);
    myMotor1->run(BACKWARD);
    myMotor2->run(BACKWARD);
    }
  }
 }
