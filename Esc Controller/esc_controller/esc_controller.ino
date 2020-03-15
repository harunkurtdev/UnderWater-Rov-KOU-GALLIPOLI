#include <Servo.h>
Servo ESC0,ESC1,ESC2;     // create servo object to control the ESC
int potValue;  // value from the analog pin
int deger=0;
void setup() {
  // Attach the ESC on pin 9
  ESC0.attach(9);
 // ESC0.attach(10,1000,2000);
 // ESC0.attach(11,1000,2000);// (pin, min pulse width, max pulse width in microseconds) 
  //ESC.attach(10); 
  Serial.begin(9600);
}
void loop() {
    // reads the value of the potentiometer (value between 0 and 1023)
  //Serial.println("Esc ye gönderilecek bilgiyi giriniz");
  if(Serial.available()){

      deger=Serial.parseInt();
      potValue = map(deger, 0, 255, 25, 180);   // scale it to use it with the servo library (value between 0 and 180)
      Serial.println(potValue);
      ESC0.write(180);
      //ESC1.write(deger);
     // ESC2.write(deger);// Send the signal to the ESC
    
    }
  
}
