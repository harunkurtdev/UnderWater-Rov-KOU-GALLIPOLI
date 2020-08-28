#include <Servo.h>
Servo ESC0,ESC1,ESC2;     // create servo object to control the ESC
int potValue;  // value from the analog pin
int deger=0;
void setup() {
  // Attach the ESC on pin 9
  ESC0.attach(3,1000,2000);
 // ESC0.attach(10,1000,2000);
 // ESC0.attach(11,1000,2000);// (pin, min pulse width, max pulse width in microseconds) 
  //ESC.attach(10); 
}
void loop() {
    // reads the value of the potentiometer (value between 0 and 1023)
  //Serial.println("Esc ye gönderilecek bilgiyi giriniz");
  ESC0.writeMicroseconds(2000);
  
}
