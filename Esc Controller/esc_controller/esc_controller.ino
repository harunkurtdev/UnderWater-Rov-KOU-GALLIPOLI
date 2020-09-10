 #include <Servo.h>
Servo ESC0,ESC1,ESC2,ESC3,ESC4,ESC5;     // create servo object to control the ESC
int potValue,escValue;  // value from the analog pin
int deger=0;

void setup() {
  // Attach the ESC on pin 9
  ESC0.attach(3,1000,2000);
  Serial.begin(9600);
  ESC1.attach(4,1000,2000);
  ESC2.attach(5,1000,2000);// (pin, min pulse width, max pulse width in microseconds) 
  ESC3.attach(6,1000,2000);// (pin, min pulse width, max pulse width in microseconds) 
  ESC4.attach(7,1000,2000);// (pin, min pulse width, max pulse width in microseconds) 
  ESC5.attach(8,1000,2000);// (pin, min pulse width, max pulse width in microseconds) 
  
}
void loop() {
    // reads the value of the potentiometer (value between 0 and 1023)
  //Serial.println("Esc ye gönderilecek bilgiyi giriniz");
  potValue=analogRead(1);
  
  escValue=map(potValue,0,1023,1100,1900);
  Serial.println(escValue);
  ESC0.writeMicroseconds(escValue);
  ESC1.writeMicroseconds(escValue);
  ESC2.writeMicroseconds(escValue);
  ESC3.writeMicroseconds(escValue);
  ESC4.writeMicroseconds(escValue);
  ESC5.writeMicroseconds(escValue);
}
