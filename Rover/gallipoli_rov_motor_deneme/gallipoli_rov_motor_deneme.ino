#include <Arduino.h>
#include<Servo.h>
#include<Wire.h>
#include<ArduinoJson.h>

Servo frontRight,frontLeft,backLeft,backRight,downRight,downLeft;
int speed=0;

const int MPU_addr=0x68;
int16_t axis_X,axis_Y,axis_Z;
int minVal=265;
int maxVal=402;
int x;
int y;
double z;


int16_t Acc_rawX, Acc_rawY, Acc_rawZ,Gyr_rawX, Gyr_rawY, Gyr_rawZ;

float Acceleration_angle[2];
float Gyro_angle[2];
float Total_angle[2];

float elapsedTime, timer, timePrev;
int i;
float rad_to_deg = 180/3.141592654;

float PID, pwmLeft, pwmRight, error, previous_error;
float pid_p=0;
float pid_i=0;
float pid_d=0;
/////////////////PID CONSTANTS/////////////////
double kp=3.55;//3.55
double ki=0.005;//0.003
double kd=2.05;//2.05
///////////////////////////////////////////////

double throttle=1300; //motorlara pulse başlangıç değeri

float desired_angle = 0; //dengesinin sabit kalmasını istediğimiz açı bu

int16_t Tmp;

#define MIN_PULSE_LENGTH 1000 // Minimum pulse length in µs
#define MAX_PULSE_LENGTH 2000 // Maximum pulse length in µs

long oldTime=0;
long newTime;


void serialEvent();
void front(int value);
void back(int value);
void goleft(int value);
void goright(int value);
void imuBilgiReturn();
void testEscCalibrete();

void setup() {
  Serial.begin(115200);

  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);


  frontRight.attach(3,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);
  frontLeft.attach(5,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);
  
  backLeft.attach(6,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);
  backRight.attach(9,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);

  //downRight.attach(9,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);
  //downLeft.attach(9,MIN_PULSE_LENGTH,MAX_PULSE_LENGTH);

  testEscCalibrete();

  pinMode(13,OUTPUT);
}


void loop() {
  
  // JsonObject& jsoncreate=jsonBuffer.createObject();

  //  jsoncreate["adin"]="harunlakodla";
  // jsoncreate["soyad"]="Kurt";

  // //data altında bir array olusturmak istersek
  // JsonArray& data =jsoncreate.createNestedArray("data");

  // data.add(44);
  // data.add("Merhaba Nasılsın");

  
  // //jsoncreate.printTo(Serial);
  // // json verisini serial ekranda basmak istersek
  // jsoncreate.prettyPrintTo(Serial);

  newTime=millis();

  // if(100<(newTime-oldTime)<150){
  //   // pidImuReturn();
  //    //imuBilgiReturn();
  // }

  if(Serial.available()>0){
        switch (Serial.read())
        {
        case '1':
            
            Serial.println("motor sola");
            if(speed<2000){
                speed+=100;
            }
            pinMode(13,HIGH);
            goleft(speed);
            break;
        case '2':
            
            Serial.println("motor saga");
             if(speed<2000){
                speed+=100;
            }
            pinMode(13,LOW);
            goright(speed);
            break;
        case '3':
            
            Serial.println("motor motor ileri");
             if(speed<2000){
                speed+=100;
            }
            front(speed);
            break;
        case '4':
          
            Serial.println("motor motor geri");
             if(speed<2000){
                speed+=100;
            }
            back(speed);
            break;
        case '5':
           
            Serial.println("motor motor sağa dön");
             if(speed<2000){
                speed+=100;
            }
            turnright(speed);
            break;
        case '6':
            
            Serial.println("motor motor sağa sola dön");
             if(speed<2000){
                speed+=100;
            }
            turnleft(speed);
            break;
        case '7':
            
            Serial.println("motor yukarıya");
             if(speed<2000){
                speed+=100;
            }
            back(speed);
            break;
        default:
            speed=0;
            frontLeft.writeMicroseconds(MIN_PULSE_LENGTH);
            frontRight.writeMicroseconds(MIN_PULSE_LENGTH);
            
            backLeft.writeMicroseconds(MIN_PULSE_LENGTH);
            backRight.writeMicroseconds(MIN_PULSE_LENGTH);
            Serial.println("hareket yok");
            break;
        }

    }

   oldTime=newTime;
}

void down(int value){
  downLeft.writeMicroseconds(value);
  downRight.writeMicroseconds(value);
}

void front(int value){
  frontLeft.writeMicroseconds(value);
  frontRight.writeMicroseconds(value-200);
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
 //frontLeft.writeMicroseconds(value);
 frontRight.writeMicroseconds(value);
 //backRight.writeMicroseconds(value);
}

void turnright(int value){
  //frontRight.writeMicroseconds(value);
  frontLeft.writeMicroseconds(value);
  //backLeft.writeMicroseconds(value);
}


void testEscCalibrete()
{
    for (int i = MIN_PULSE_LENGTH; i <= MAX_PULSE_LENGTH; i += 5) {
      
        frontRight.writeMicroseconds(i);
        frontLeft.writeMicroseconds(i);
        backRight.writeMicroseconds(i);
        backLeft.writeMicroseconds(i);
        
        delay(50);
    }
    frontRight.writeMicroseconds(MIN_PULSE_LENGTH);
    frontLeft.writeMicroseconds(MIN_PULSE_LENGTH);
    backRight.writeMicroseconds(MIN_PULSE_LENGTH);
    backLeft.writeMicroseconds(MIN_PULSE_LENGTH);
}

void pidImuReturn(){

  
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& jsoncreate=jsonBuffer.createObject();

  
  
  timePrev = timer;  // önceki zaman gerçek zaman okunmadan önce saklanır
  timer = millis();  // gerçek zamanlı okuma
  elapsedTime = (timer - timePrev) / 1000; 

  Wire.beginTransmission(MPU_addr);//mpu adresini okuyoruz
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,6,true);

  /* 0x3B kaydını istedik. IMU bir brust kayıt gönderecek.
    * Okunacak kayıt miktarı requestFrom işlevinde belirtilir.
    * Bu durumda 6 kayıt talep ediyoruz. Her ivmelenme değeri
    * iki 8 bit kayıt, düşük değerler ve yüksek değerler. Bunun için 6 tanesini talep ediyoruz
    * ve her çiftin toplamını yapın. Bunun için yüksek değerleri sola kaydırıyoruz
    * (<<) 'ı kaydedin ve düşük değerleri eklemek için bir veya (|) işlemi yapın.
    */
  
  /*
  Aşağı daki işlemler de bit kaydırma işlemi yapılmaktadır
  Tmp den sonra ki bitlere geçiş yaptığımız da bize ivmeyi vermektedir.
  ivmenin türevini alarak hız bulununabilir.
  */

  Acc_rawX=Wire.read()<<8|Wire.read(); //each value needs two registres
  Acc_rawY=Wire.read()<<8|Wire.read();
  Acc_rawZ=Wire.read()<<8|Wire.read();
  
  
  // Matematiksel hespalama ile imu bilgileirini açısal bilgilere çeviriyoruz.
  int xAng = map(Acc_rawX,minVal,maxVal,-90,90);
  int yAng = map(Acc_rawY,minVal,maxVal,-90,90);
  int zAng = map(Acc_rawZ,minVal,maxVal,-90,90);
      x= RAD_TO_DEG * (atan2(-yAng, -zAng)+PI);
      y= RAD_TO_DEG * (atan2(-xAng, -zAng)+PI);
      z= RAD_TO_DEG * (atan2(-yAng, -xAng)+PI);

  //  int y_eksenyukari=map(y,0,160,0,160);
  //  int y_eksenasagi=map(y,360,200,0,-160);
  
  // jsoncreate["x_eksen"]=x;
  // jsoncreate["y_eksen_yukari"]=y_eksenyukari;
  // jsoncreate["y_eksen_asagi"]=y_eksenasagi;
  // jsoncreate["z_ekseni"]=z;
  
  //jsoncreate.prettyPrintTo(Serial);
  //jsoncreate.printTo(Serial);
  //Serial.println();
  //Serial.print("{\"x_eksen\":");
  //Serial.print(x);
  //Serial.print("}");
  //Serial.println(); 
 /* /// Euler denklemlerini kullanarak açıları hesaplamanız gereken kısım /// */
    
    /* - Şimdi, "g" birimlerinde ivme değerlerini elde etmek için önce ham
     * 16384.0'da az önce okuduğumuz değerler çünkü MPU6050
     * veri sayfası bize verir. */
    
    /* - Daha sonra 180º'yi PI numarasına bölerek radyanı derece değerine hesaplamalıyız
    * 3.141592654 olup bu değeri rad_to_deg değişkeninde saklar. Sahip olmamak için
    * Her döngüdeki bu değeri hesaplamak için bunu kurulum geçersizliğinden sadece bir kez önce yaptık.
    */

   /* Şimdi Euler formülünü uygulayabiliriz. Atanan arktanjanı hesaplar.
     * pow (a, b), a değerini b gücüne yükseltir. Ve finnaly sqrt işlevi
     * kök kareyi hesaplar. */

//     /*---X---*/
//      Acceleration_angle[0] = atan((Acc_rawY/16384.0)/sqrt(pow((Acc_rawX/16384.0),2) + pow((Acc_rawZ/16384.0),2)))*rad_to_deg;
//      /*---Y---*/
//      Acceleration_angle[1] = atan(-1*(Acc_rawX/16384.0)/sqrt(pow((Acc_rawY/16384.0),2) + pow((Acc_rawZ/16384.0),2)))*rad_to_deg;

//    /* Şimdi Gyro verilerini Acc verileriyle aynı şekilde okuyoruz. Adresi
//     * gyro verileri 0x43'te başlar. Eğer kayıt haritasına bakarsak bu adresleri görebiliriz
//     * MPU6050'nin. Bu durumda sadece 4 değer talep ediyoruz. Gyro'yu istemiyorum
//     * Z ekseni (YAW). */

//    Wire.beginTransmission(MPU_addr);
//    Wire.write(0x43); //Gyro verileri ilk adres
//    Wire.endTransmission(false);
//    Wire.requestFrom(MPU_addr,4,true); //Sadece 4 kayıt istiyorz
   
//    Gyr_rawX=Wire.read()<<8|Wire.read(); 
//    Gyr_rawY=Wire.read()<<8|Wire.read();

//    /* Şimdi jiroskop verilerini derece /saniye cinsinden elde edebilmek için önce bölmemiz gerekiyor
//    ham değeri 131 olarak verir çünkü veri sayfasının bize verdiği değer */

//   /*---X---*/
//    Gyro_angle[0] = Gyr_rawX/131.0; 
//    /*---Y---*/
//    Gyro_angle[1] = Gyr_rawY/131.0;

//    /* Şimdi derece elde etmek için dereceyi / saniyeyi çarpmamız gerekiyor
//    * elapsedTime değerine göre değer. */
//    /* Son olarak ivmeyi eklediğimiz son filtreyi uygulayabiliriz
//    * açıları ve tabiatı etkileyen kısım 0.98 ile çarpılır */

//    /*---X axis angle---*/
//    Total_angle[0] = 0.98 *(Total_angle[0] + Gyro_angle[0]*elapsedTime) + 0.02*Acceleration_angle[0];
//    /*---Y axis angle---*/
//    Total_angle[1] = 0.98 *(Total_angle[1] + Gyro_angle[1]*elapsedTime) + 0.02*Acceleration_angle[1];

//   /*///////////////////////////P I D///////////////////////////////////*/

//   /* Bakiye için sadece bir eksen kullanacağımızı unutmayın. X açısını seçtim
//   ile PID uygulamak. Bu, IMU'nun x ekseninin aşağıdakilere paralel olması gerektiği anlamına gelir:
//   denge */
//   /* Önce istenen açı ile
//    * ölçülen gerçek açı */

//   error = Total_angle[1] - desired_angle;

//   /* Sonra PID'nin oransal değeri sadece oransal bir sabittir
// * hatayla çarpılır */

//   pid_p = kp*error;

//   /* İntegral kısım, yalnızca
//   istenen konuma ayarlayabiliriz ancak hatayı hassas bir şekilde ayarlamak istiyoruz. Yani en
//   neden -3 ve 3 derece arasında bir hata için if if işlemi yaptım.
//   Entegre etmek için önceki integral değerini sadece
//   hata integral sabiti ile çarpılır. Bu entegre olacak (artacak)
//   0 noktasına ulaşana kadar her bir döngü değeri */

//   if(-3 <error <3)
//   {
//     pid_i = pid_i+(ki*error);  
//   }

//   pid_d = kd*((error - previous_error)/elapsedTime);

//   PID = pid_p + pid_i + pid_d;

//   /* PWM sinyalinin minimum değerinin 1000us ve maksimum 2000 olduğunu biliyoruz.
//   bize PID değerinin -1000 ve 1000'den fazla salınabileceğini söylüyor çünkü
//   2000us değerinde sybstract yapabileceğimiz maksimum değer 1000 ve
//   PWM sihnal için 1000us değerine sahibiz, ekleyebileceğimiz maksimum değer 1000
//   maksimum 2000us */

//   if(PID < -1000)
//   {
//     PID=-1000;
//   }
//   if(PID > 1000)
//   {
//     PID=1000;
//   }

//   /* Son olarak PWM genişliğini hesaplıyoruz. İstenen gaz kelebeğini ve PID değerini */

//   pwmLeft = throttle + PID;
//   pwmRight = throttle - PID;

//   /* Bir kez daha, PWM değerlerini eşleştirerek min.
//     ve maks. değerler. Evet, zaten PID değerlerini eşleştirdik. Ancak, örneğin,
//     1300 gaz değeri, maksimum PID değerini toplarsak 2300us olur ve
//     ESC'yi bozacak. */

//    //Sağ
//   if(pwmRight < 1000)
//   {
//     pwmRight= 1000;
//   }
//   if(pwmRight > 2000)
//   {
//     pwmRight=2000;
//   }
//   //Sol
//   if(pwmLeft < 1000)
//   {
//     pwmLeft= 1000;
//   }
//   if(pwmLeft > 2000)
//   {
//     pwmLeft=2000;
//   }
 

//   Serial.print("Pwm Left");
//   Serial.println(pwmLeft);
  
//   Serial.print("Pwm Right");
//   Serial.println(pwmRight);

//   /* Son olarak servo fonksiyonunu kullanarak hesaplanan PWM darbeleri oluşturuyoruz
//   her darbe için genişlik */


  if(x<=10){
  frontRight.writeMicroseconds(1000);
  frontLeft.writeMicroseconds(1000);
  Serial.println(x);
  }
  else if(10<x<20)
  {
  frontRight.writeMicroseconds(1000);
  frontLeft.writeMicroseconds(1000);
  
  }else if(20<=x<25)
  {
  frontRight.writeMicroseconds(1000);
  frontLeft.writeMicroseconds(1000);
  }
  

  
  

  //Bu bölüm motorlarımıza giden pid bölgesidir.
  //motorlar ters yönde bağlanmış ise
  //frontRight.writeMicroseconds(pwmRight);
  //frontLeft.writeMicroseconds(pwmLeft);

  previous_error = error;// önce ki hata.

}


void imuBilgiReturn(){
  //Milis bilgileri koyulmalı.
  
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& jsoncreate=jsonBuffer.createObject();

  Wire.beginTransmission(MPU_addr);//mpu adresini okuyoruz
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,6,true);

  /* 0x3B kaydını istedik. IMU bir brust kayıt gönderecek.
    * Okunacak kayıt miktarı requestFrom işlevinde belirtilir.
    * Bu durumda 6 kayıt talep ediyoruz. Her ivmelenme değeri
    * iki 8 bit kayıt, düşük değerler ve yüksek değerler. Bunun için 6 tanesini talep ediyoruz
    * ve her çiftin toplamını yapın. Bunun için yüksek değerleri sola kaydırıyoruz
    * (<<) 'ı kaydedin ve düşük değerleri eklemek için bir veya (|) işlemi yapın.
    */
  
  /*
  Aşağı daki işlemler de bit kaydırma işlemi yapılmaktadır
  Tmp den sonra ki bitlere geçiş yaptığımız da bize ivmeyi vermektedir.
  ivmenin türevini alarak hız bulununabilir.
  */
  
  axis_X=Wire.read()<<8|Wire.read();
  axis_Y=Wire.read()<<8|Wire.read();
  axis_Z=Wire.read()<<8|Wire.read();
  //Tmp=Wire.read()<<8|Wire.read(); // Sıcaklık bilgisi kaydırma işlemi yapmadan önce requestFrom içinde ki
  // bit kaydırma sayısını 8 yapmalısın...
    
    // Matematiksel hespalama ile imu bilgileirini açısal bilgilere çeviriyoruz.
    int xAng = map(axis_X,minVal,maxVal,-90,90);
    int yAng = map(axis_Y,minVal,maxVal,-90,90);
    int zAng = map(axis_Z,minVal,maxVal,-90,90);
       x= RAD_TO_DEG * (atan2(-yAng, -zAng)+PI);
       y= RAD_TO_DEG * (atan2(-xAng, -zAng)+PI);
       z= RAD_TO_DEG * (atan2(-yAng, -xAng)+PI);

      int y_eksenyukari=map(y,0,160,0,160);
      int y_eksenasagi=map(y,360,200,0,-160);

  jsoncreate["x_eksen"]=x;
  jsoncreate["y_eksen"]=y;
  jsoncreate["y_eksen_yukari"]=y_eksenyukari;
  jsoncreate["y_eksen_asagi"]=y_eksenasagi;
  jsoncreate["z_ekseni"]=z;

  //jsoncreate.prettyPrintTo(Serial);
  jsoncreate.printTo(Serial);
  Serial.println();
  //Serial.print("{\"x_eksen\":");
  //Serial.print(x);
  //Serial.print("}");
  //Serial.println(); 

      //Serial.println(Tmp/340.00+36.53);
     
     //Serial.println(x);//x ekseni mpu bilgilerini verir
     
     //Serial.println(y);// y ekseni mpu bilgilerini verir
     
     //Serial.println(y_eksenyukari);//

     //Serial.println(y_eksenasagi);
}
