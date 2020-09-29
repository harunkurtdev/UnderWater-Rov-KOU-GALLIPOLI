#include <Arduino.h>
#include<Servo.h>
#include <ArduinoJson.h>

/*
Aracımızıve Kameramızı hareket ettirekcek Servo motor tanımlamalarımız 
*/
Servo frontRight,frontLeft,backLeft,backRight,heightRight,heightLeft,gripperArm,camXPosition,camYPosition;

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

/*FSN-SR04T Mesafe Duration - Distance Hesaplayıcı değişkeni*/

int divider=58;

void setup() {

  Serial.begin(115200);
  //Esc ileri motorları
  frontRight.attach(3,1100,1900);
  frontLeft.attach(4,1100,1900);
  //Esc Geri motorları
  backRight.attach(5,1100,1900);
  backLeft.attach(6,1100,1900);
  //Yükselme alçalma motorları
  heightRight.attach(7,1100,1900);
  heightLeft.attach(8,1100,1900);
  //Gripper Arm
  gripperArm.attach(9,1100,1900);
  //Kamera Servo motorları
  camXPosition.attach(10,1100,1900);
  camYPosition.attach(11,1100,1900);

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
void goleft(int x,int value);
void goright(int x,int value);
void turnright(int x, int value);
void turnleft(int x,int valhe);
void height(int value);
void gripper(int value);
void camPosition(int valueX,int valueY);
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
      gripper(doc["gripper_arm"]);
      camPosition(doc["cam_x_position"],doc["cam_y_position"]);
      
      if (doc["direction"]==1){
        // if(distanceLeft()>25){
        int x;
        x=map(atoi(doc["goLeftSpeed"]),1500,1900,1100,1900); 
         goleft(atoi(doc["frontRightSpeed"]),atoi(doc["goLeftSpeed"]));
        // goleft(1100);
        // Serial.println("Sağa dönüyor");
        //   // Serial.print("Araç sola doğru gitmekte  ");
        // }
        // Serial.print("Araç sola doğru gitmekte  ");
        // doc["goLeftSpeed"].prettyPrintTo(Serial);
        // Serial.println();
      }
      else if(doc["direction"]==2){
        // if(distanceRight()>25){
        // goright(1100);
         int x;
        x=map(atoi(doc["goRightSpeed"]),1500,1900,1100,1900); 
        goright(atoi(doc["frontLeftSpeed"]),atoi(doc["goRightSpeed"]));
        // Serial.println("Sağa dönüyor");
        //   // Serial.print("Araç sağa doğru gitmekte  ");
        // }
        // Serial.print("Araç sağa doğru gitmekte  ");
        // doc["goRightSpeed"].prettyPrintTo(Serial);
        // Serial.println();
      }
      else if(doc["direction"]==3){
        // if(distanceFront()>25){
          front(atoi(doc["frontLeftSpeed"]),atoi(doc["frontRightSpeed"]));
          back(atoi(doc["backSpeed"]));
          // front(1100);
          // Serial.println("ileri gidiyor");
        //   // Serial.println("Araç ileri doğru gitmekte   ");
        // }
        // front(doc["frontSpeed"]);
        // Serial.print("Araç ileri doğru gitmekte   ");
        // doc["frontSpeed"].prettyPrintTo(Serial);
        // Serial.println();
      }
      else if(doc["direction"]==4){
        back(atoi(doc["backSpeed"]));
        // back(1100);
        // Serial.print("Araç geri doğru gitmekte  ");
        // doc["backSpeed"].prettyPrintTo(Serial);
        // Serial.println();
      }
      else if(doc["direction"]==5){
        int x;
        x=map(atoi(doc["turnLeftSpeed"]),1500,1900,1100,1900); 
        turnright(atoi(doc["frontRightSpeed"]),atoi(doc["turnLeftSpeed"]));

        // Serial.print("Araç sağa doğru dönmekte   ");
        // // turnright(1100);
        // doc["turnLeftSpeed"].prettyPrintTo(Serial);
        // Serial.println();
        
      }
      else if(doc["direction"]==6){
        int x;
        x=map(atoi(doc["turnLeftSpeed"]),1500,1900,1100,1900); 

        turnleft(atoi(doc["frontLeftSpeed"]),atoi(doc["turnRightSpeed"]));
        // turnleft(1100);
        // Serial.print("araç sola doğru dönmekte   ");
        // doc["turnRightSpeed"].prettyPrintTo(Serial);
        // Serial.println();
      }
   }
   else{
     //-----------
    //  frontLeft.writeMicroseconds(1100);
    //  frontRight.writeMicroseconds(1100);
    //  //---------
    //  backLeft.writeMicroseconds(1500);
    //  backRight.writeMicroseconds(1500);
    //  //---------
    //  heightLeft.writeMicroseconds(1500);
    //  heightRight.writeMicroseconds(1500);
    //

   }
        
  // frontDistance=distanceFront();
//  downDistance=distanceDown();
//  leftDistance=distanceLeft();
//  rightDistance=distanceRight();
 
  // jsoncreate["distanceFront"]= frontDistance;
//   jsoncreate["distanceDown"]=downDistance;
//   jsoncreate["distanceLeft"]=leftDistance;
//   jsoncreate["distanceRight"]=rightDistance;
  
  // jsoncreate.printTo(Serial);
  // Serial.println();

}

//-------------------------------------Araç hareket kabiliyet ,Kamera ve Gripper Fonksiyon Blokları Bölümü---------------------------------------

void front(int value1,int value2){
  frontLeft.writeMicroseconds(value1);//3. pins
  frontRight.writeMicroseconds(value2);//4.pins
}

void back(int value){
  backLeft.writeMicroseconds(value);
  backRight.writeMicroseconds(value);
}

void goleft(int value1,int value2){
  frontRight.writeMicroseconds(value1);
  backRight.writeMicroseconds(value2);
}

void goright(int value1,int value2){
  frontLeft.writeMicroseconds(value1);
  backLeft.writeMicroseconds(value2);
}

void turnleft(int value1,int value2){
 frontLeft.writeMicroseconds(value1);
 backRight.writeMicroseconds(value2);
}

void turnright(int value1,int value2){
  frontRight.writeMicroseconds(value1);
  backLeft.writeMicroseconds(value2);
}

void height(int value){
  heightRight.writeMicroseconds(value);
  heightLeft.writeMicroseconds(value);
}

void gripper(int value){
  gripperArm.writeMicroseconds(value);
}

void camPosition(int valueX,int valueY){
  camXPosition.writeMicroseconds(valueX);
  camYPosition.writeMicroseconds(valueY);
  // Serial.print("Cam X position : ");
  // Serial.print(valueX);
  // Serial.println();
  // Serial.print("Cam Y position : ");
  // Serial.print(valueY);
  // Serial.println();
}

//------------------------------------ FSN-SR04T Mesafe Sensörleri Fonksiyon Bölgesi--------------------------------

int distanceFront(){

  digitalWrite(trigPinFront, LOW);
  
  delayMicroseconds(2);

 //Sensörümüzün trig pinini 10 mili saniye enerji veri kesiyoruz
  digitalWrite(trigPinFront, HIGH);
  delayMicroseconds(15);
  digitalWrite(trigPinFront, LOW);
  
  // Echo pinimizden okuma işlemi yapmaktayız...
  frontDuration = pulseIn(echoPinFront, HIGH,26000);
  
  // okunan duration bilgisini matematiksel ifade ile cm e çeviriyoruz...
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
