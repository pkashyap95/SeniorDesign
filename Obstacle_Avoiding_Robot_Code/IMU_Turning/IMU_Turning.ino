#include <Wire.h>
#include <Adafruit_MotorShield.h> //import your motor shield library
#include <SoftwareSerial.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#define trigPin 8  //define the pins of your sensor
#define echoPin 9

char inChar1; //character to recieve data serially
int dir; //integer to determine direction of the car
int val_1; // integer that holds the actual speed recieved by the car
int recSpeed=0;
int trial=0; //integere variable to check how many characters are sent over bluetooth
int supaspeed; // result of maaping the incoming speed to rpm or analog voltage
int motorSpeed;// the incoming speed from the HeadPi
boolean isRunning;

//import motor shield library
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); //declare the AFMS object
Adafruit_DCMotor *leftMotor = AFMS.getMotor(1);  //leftMotor is in M1 of the motor shield
Adafruit_DCMotor *rightMotor = AFMS.getMotor(2);   //leftMotor is in M2 of the motor shield
//initalizing bluetooth connection
SoftwareSerial mySerial(5, 6);  //RX, TX

void setup(){
  Serial.begin(9600);  //begin serial communitication
  Serial.println("Motor test!"); //Prints on the serial monitor
  Serial.println("Let's get these speeds!"); //Prints on the serial monitor

  //Input for the ultrasonic sensor
  pinMode(trigPin, OUTPUT);// set the trig pin to output (Send sound waves)
  pinMode(echoPin, INPUT);// set the echo pin to input (recieve sound waves)

  AFMS.begin(); // Begins the movemment of the car
  leftMotor->run(BACKWARD); //motors are setup the wrong way BACKWARD makes the car go foward
  rightMotor->run(BACKWARD);

  mySerial.begin(9600); //Begins bluetooth communication

  }

void loop(){  
 long duration, distance; // start the scan
    digitalWrite(trigPin, LOW);  
    delayMicroseconds(2); // delays are required for a succesful sensor operation.
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10); //this delay is required as well!
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = (duration/2) / 29.1;// convert the distance to centimeters.
    if (distance < 30){  
      Serial.print ("Distance From Robot is " );
      Serial.print ( distance);
      Serial.println (); 
       leftMotor->setSpeed(127*(distance/100)); 
       rightMotor->setSpeed(127*(distance/100)*0.95);
       isRunning=true;
       if(distance <10){
          delay(2000);
          leftMotor->run(FORWARD);
          rightMotor->run(FORWARD);
         leftMotor->setSpeed(127); 
         rightMotor->setSpeed(127*.95);
         isRunning=true;
         delay(1500);
       }
     }
    else{
      if(mySerial.available()>=4){ 
        char incomingByte0 = mySerial.read();
        char incomingByte1 = mySerial.read();
        char incomingByte2 = mySerial.read();
        char incomingByte3 = mySerial.read();

        int dir = incomingByte0 - '0';
        int hundreds = incomingByte1 - '0';
        int tens = incomingByte2 - '0';
        int ones = incomingByte3 - '0';
        int motorSpeed= hundreds*100+tens*10+ones;

        if(motorSpeed>0){ //If the speed is greater than 0
          Serial.println("Setting speed");
          //left turning
            if(dir==1){
              Serial.println("Left");
              supaspeed= map(motorSpeed, 0, 435, 0, 255); //the mapping of the values on car speeds to the analog voltages
              leftMotor->setSpeed(supaspeed); //left motor is slowed down
              rightMotor->setSpeed(127*0.95); //right continues
              isRunning=true;
            }
            //straight condition
            if(dir==2){
              Serial.println("Straight");
              leftMotor->run(BACKWARD); //motors are setup the wrong way BACKWARD makes the car go foward
              rightMotor->run(BACKWARD);
              leftMotor->setSpeed(127);
              rightMotor->setSpeed(127*0.95); //right motor is slowed down
              isRunning=true;
            }
          if(dir==3){
            Serial.println("Right");
            supaspeed= map(motorSpeed, 0, 435, 0, 255); //the mapping of the values on car speeds to the analog voltages
            leftMotor->setSpeed(127); //left motor continues
            rightMotor->setSpeed(supaspeed*0.95); //right motor is slowed down
            isRunning=true;
          }//ping of the values on car speeds to the analog voltages
          if(dir==4){
              Serial.println("Reverese");
              leftMotor->run(FORWARD); //motors are setup the wrong way BACKWARD makes the car go foward
              rightMotor->run(FORWARD);
              leftMotor->setSpeed(127);
              rightMotor->setSpeed(127*0.95); //right motor is slowed down
              isRunning=true;
          }
        }
      }
    }
    if(isRunning){
      delay(500);
      leftMotor->setSpeed(0);
      rightMotor->setSpeed(0); //right motor is slowed down
      leftMotor->run(BACKWARD); //motors are setup the wrong way BACKWARD makes the car go foward
      rightMotor->run(BACKWARD);
      isRunning=false;
      Serial.println("Trial reset");
    }
}
