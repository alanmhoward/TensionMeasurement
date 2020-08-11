/*
This sketch has been modified for use with the adafruit V2 motor shield
to be used as a controller for a solenoid valve dispensing gas in short bursts

The Arduino waits for the character 'g' to be sent over the serial port
and then opens the valve for a short period
*/

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// We are connected to M1
Adafruit_DCMotor *myMotor = AFMS.getMotor(1);
// Could also connect to e.g. port M2
//Adafruit_DCMotor *myOtherMotor = AFMS.getMotor(2);

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Solenoid valve control");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  // In our case the direction sets the polarity (we want 'forward')
  // and start with the voltage off (speed == 0)
  myMotor->setSpeed(0);
  myMotor->run(FORWARD);
  // turn on motor
  myMotor->run(RELEASE);
}

void loop() {

  // Wait for serial input (stay in while loop unitl there is something in the serial buffer)
  // Note that a new line character will be taken as input (can give double firing)
  // Expect an integer value to be passed (e.g. echo '20' > /dev/ttyACM0)
  while(Serial.available() == 0) { }  // 
  int time = Serial.parseInt();
  
  
  delay(50);
  
  
  // Now open the valve
  if (time>0){
    
    Serial.print("Gas on!\n");
    myMotor->run(FORWARD)
    ;
  
    myMotor->setSpeed(255);  
    
    
    delay(time);  // Wait so many ms
    
    myMotor->setSpeed(0);    // and close the valve again
    
    
  }
  
}
