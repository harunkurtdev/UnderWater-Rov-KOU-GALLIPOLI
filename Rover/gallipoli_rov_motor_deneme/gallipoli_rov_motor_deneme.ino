#include <Arduino.h>
#include<Servo.h>
#include <ArduinoJson.h>

/*
Aracımızıve Kameramızı hareket ettirekcek Servo motor tanımlamalarımız 
*/
Servo frontRight,frontLeft,backLeft,backRight,heightRight,heightLeft,gripperArm,camXPosition,camYPosition;
//PWM Value
#define MAX_PWM 1900
#define MIN_PWM 1100
#define STABIL_PWM 1500


/*Mesafe sensörlerinin değişkenleri*/
long frontDuration,downDuration,leftDuration,rightDuration;
/*Mesafe Sensörlerinin uzunluklarının değişkenleri*/
int frontDistance,downDistance,leftDistance,rightDistance;

/*FSN-SR04T Trig ve Echo Pinleri*/
#define trigPinFront 23
#define trigPinDown 27
#define trigPinLeft 31
#define trigPinRight 35

#define echoPinFront 25
#define echoPinDown 29
#define echoPinLeft 33
#define echoPinRight 37

//Mesafe 
#define MAX_DISTANCE 450

/*FSN-SR04T Mesafe Duration - Distance Hesaplayıcı değişkeni*/
int divider=58;

void setup() {

  Serial.begin(115200);
  //Esc ileri motorları
  frontRight.attach(3,MIN_PWM,MAX_PWM);
  frontLeft.attach(4,MIN_PWM,MAX_PWM);
  //Esc Geri motorları
  backRight.attach(5,MIN_PWM,MAX_PWM);
  backLeft.attach(6,MIN_PWM,MAX_PWM);
  //Yükselme alçalma motorları
  heightRight.attach(7,MIN_PWM,MAX_PWM);
  heightLeft.attach(8,MIN_PWM,MAX_PWM);
  //Gripper Arm
  gripperArm.attach(9,MIN_PWM,MAX_PWM);
  //Kamera Servo motorları
  camXPosition.attach(10,MIN_PWM,MAX_PWM);
  camYPosition.attach(11,MIN_PWM,MAX_PWM);

  //--------Front Dictance Pins-----
  pinMode(trigPinFront, OUTPUT);
  pinMode(echoPinFront, INPUT_PULLUP);
  //---------Down Distance Pins------
  pinMode(trigPinDown, OUTPUT);
  pinMode(echoPinDown, INPUT_PULLUP);
  //---------Left Distance Pins------
  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT_PULLUP);
  //-------Right Distance Pins------
  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT_PULLUP);

}

//Aracımızın ve kameramızın hareket kabiliyetini sağlayacak fonksiyonlarımız...
void front(int value);
void back(int value);
void goleft(int value);
void goright(int value);
void turnright(int value);
void turnleft(int value);
void height(int value);
void gripper(int value);
void krameyer(int value);
void camPosition(int value);
//
int distanceFront(); 
int distanceDown();
int distanceLeft();
int distanceRight();


void loop() {

  StaticJsonBuffer<512> jsonBuffer;
  JsonObject& jsoncreate=jsonBuffer.createObject();
  // frontDistance,downDistance,leftDistance,rightDistance
 
  // jsoncreate.prettyPrintTo(Serial);
  
   if ( Serial.available()>0){


    String  payload;
    payload = Serial.readStringUntil('\n');

    // Serial.println("verimiz"+payload);
    // DynamicJsonBuffer json;
    // StaticJsonBuffer<512> json;
    JsonObject& doc = jsonBuffer.parseObject(payload);

    // Serial.print("giden veri");
    // doc.printTo(Serial);
    // Serial.println(payload);
    //  doc.prettyPrintTo(Serial);
      
      height(atoi(doc["robotHeightSpeed"]));
      gripper(atoi(doc["gripper_arm"]));
      camPosition(atoi(doc["cam_y_position"]));
      krameyer(atoi(doc["cam_x_position"]));

      if (doc["direction"]==1){
         goleft(atoi(doc["goLeftSpeed"]));
         goright(atoi(doc["goRightSpeed"]));
      }
      else if(doc["direction"]==2){
        goright(atoi(doc["goRightSpeed"]));
        goleft(atoi(doc["goLeftSpeed"]));
      }
      else if(doc["direction"]==3){
        front(atoi(doc["frontSpeed"]));
        back(atoi(doc["backSpeed"]));
      }
      else if(doc["direction"]==4){
        front(atoi(doc["frontSpeed"]));
        back(atoi(doc["backSpeed"]));
      }
      else if(doc["direction"]==5){
        turnright(atoi(doc["turnLeftSpeed"]));
        turnleft(atoi(doc["turnRightSpeed"]));
      }
      else if(doc["direction"]==6){
        turnright(atoi(doc["turnLeftSpeed"]));
        turnleft(atoi(doc["turnRightSpeed"]));
      }
   
   else if(doc["direction"]==0){
     //-----------
     frontLeft.writeMicroseconds(STABIL_PWM);
     frontRight.writeMicroseconds(STABIL_PWM);
     //---------
     backLeft.writeMicroseconds(STABIL_PWM);
     backRight.writeMicroseconds(STABIL_PWM);
    //  //---------
    //  heightLeft.writeMicroseconds(STABIL_PWM);
    //  heightRight.writeMicroseconds(STABIL_PWM);
    //

   }else{
    /*
    Tüm Durumlar oluşmadı ise
    */      
   }
   
  }else{
    /*
    Veri Gelmiyorsa Mesafe sensör bilgilerini bas
    */
    frontDistance=distanceFront();
    downDistance=distanceDown();
    leftDistance=distanceLeft();
    rightDistance=distanceRight();
    jsoncreate["distanceFront"]= frontDistance;
    jsoncreate["distanceDown"]=downDistance;
    jsoncreate["distanceLeft"]=leftDistance;
    jsoncreate["distanceRight"]=rightDistance;
    jsoncreate.printTo(Serial);
    Serial.println();
  }
        
}

//-------------------------------------Araç hareket kabiliyet ,Kamera ve Gripper Fonksiyon Blokları Bölümü---------------------------------------

void front(int value){
  frontLeft.writeMicroseconds(value);//3. pins
  frontRight.writeMicroseconds(value);//4.pins
}

void back(int value){
  backLeft.writeMicroseconds(value);
  backRight.writeMicroseconds(value);
}

void goleft(int value){
  frontRight.writeMicroseconds(value);
  backRight.writeMicroseconds(value);
}

void goright(int value){
  frontLeft.writeMicroseconds(value);
  backLeft.writeMicroseconds(value);
}

void turnleft(int value){
 frontLeft.writeMicroseconds(value);
 backRight.writeMicroseconds(value);
}

void turnright(int value){
  frontRight.writeMicroseconds(value);
  backLeft.writeMicroseconds(value);
}

void height(int value){
  heightRight.writeMicroseconds(value);
  heightLeft.writeMicroseconds(value);
}

void krameyer(int value){
camXPosition.writeMicroseconds(value);
}

void gripper(int value){
  gripperArm.writeMicroseconds(value);
  // gripperArm.write(value);
}

void  camPosition(int value){
  camYPosition.writeMicroseconds(value);
}

//------------------------------------ FSN-SR04T Mesafe Sensörleri Fonksiyon Bölgesi--------------------------------

int distanceFront(){

  digitalWrite(trigPinFront, LOW);
  delayMicroseconds(2);
//  //Sensörümüzün trig pinini 10 mili saniye enerji veri kesiyoruz
  digitalWrite(trigPinFront, HIGH);
  delayMicroseconds(20);
  digitalWrite(trigPinFront, LOW);
//   // Echo pinimizden okuma işlemi yapmaktayız...
  frontDuration = pulseIn(echoPinFront, HIGH,26000);
  
//   // okunan duration bilgisini matematiksel ifade ile cm e çeviriyoruz...
  frontDistance = frontDuration/58;
  return frontDistance;
}

int distanceDown(){

  digitalWrite(trigPinDown, LOW);
  
  delayMicroseconds(2);
 //Sensörümüzün trig pinini 10 mili saniye enerji veri kesiyoruz
  digitalWrite(trigPinDown, HIGH);
  delayMicroseconds(20);
  digitalWrite(trigPinDown, LOW);
  // Echo pinimizden okuma işlemi yapmaktayız...
  downDuration = pulseIn(echoPinDown, HIGH,26000);
  // okunan duration bilgisini matematiksel ifade ile cm e çeviriyoruz...
  downDistance = downDuration/divider;
  return downDistance;
}

int distanceLeft(){

  digitalWrite(trigPinLeft, LOW);
  
  delayMicroseconds(2);

 //Sensörümüzün trig pinini 10 mili saniye enerji veri kesiyoruz
  digitalWrite(trigPinLeft, HIGH);
  delayMicroseconds(20);
  digitalWrite(trigPinLeft, LOW);
  
  // Echo pinimizden okuma işlemi yapmaktayız...
  leftDuration = pulseIn(echoPinLeft, HIGH,26000);
  
  // okunan duration bilgisini matematiksel ifade ile cm e çeviriyoruz...
  leftDistance = leftDuration/divider;

  return leftDistance;
}

int distanceRight(){

  digitalWrite(trigPinRight, LOW);
  
  delayMicroseconds(2);

 //Sensörümüzün trig pinini 10 mili saniye enerji veri kesiyoruz
  digitalWrite(trigPinRight, HIGH);
  delayMicroseconds(20);
  digitalWrite(trigPinRight, LOW);
  
  // Echo pinimizden okuma işlemi yapmaktayız...
  rightDuration = pulseIn(echoPinRight, HIGH,26000);
  
  // okunan duration bilgisini matematiksel ifade ile cm e çeviriyoruz...
  rightDistance = rightDuration/divider;

  return rightDistance;
}
