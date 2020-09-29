#include <Arduino.h>
#include<Servo.h>
#include<Wire.h>
#include<ArduinoJson.h>

Servo frontRight,frontLeft,downRight,downLeft;

#define MIN_PULSE_LENGTH 1000 // Minimum pulse length in µs
}

void front(int value1,int value2);
void down(int value);
void goleft(int value);
void goright(int value);
int reverse(int value);

void setup() {
  Serial.begin(115200);

  frontRight.attach(3,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);
  frontLeft.attach(5,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);
  
  downLeft.attach(6,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);
  downRight.attach(9,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);

  //downRight.attach(9,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);
  //downLeft.attach(9,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);

}


void loop() {

    down(1357);//Ortalarda
  
    if(Serial.available()>0){
        switch (Serial.read())
        {
        case '1':
            front(1650,1350);//ileri
            break;
        case '2':
            turnright(1650);//Sağa
            break;
        case '3':
            turnleft(1350);//Sola
            break;
        }

    }
}

void down(int value){
  downLeft.writeMicroseconds(value);
  downRight.writeMicroseconds(value);
}

void front(int value1,int value2){
  frontLeft.writeMicroseconds(value1);
  frontRight.writeMicroseconds(value2);
}


void goleft(int value){
  frontRight.writeMicroseconds(value);
}

void goright(int value){
  frontLeft.writeMicroseconds(value);
}

void turnleft(int value){
 //frontLeft.writeMicroseconds(value);
 frontRight.writeMicroseconds(value);
 //backRight.writeMicroseconds(value);
}

int reverse(int value){
  int reverseSpeed;
  if(1500<value){
    reverseSpeed=map(value,1500,1900,1500,1100);
    }
   else if(value<1500){
    reverseSpeed=map(value,1500,1100,1500,1900);
    }
    else{
      reverseSpeed =1500;
      }
     return reverseSpeed;
  }

void turnright(int value){
  //frontRight.writeMicroseconds(value);
  frontLeft.writeMicroseconds(value);
  //backLeft.writeMicroseconds(value);
}
