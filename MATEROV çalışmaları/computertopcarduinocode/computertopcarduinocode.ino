
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(11,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(13,OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) // if receiver buffer is full
  {
    char chrIn = Serial.read();
    Serial.println(chrIn);
    switch(chrIn)
    {
      case '0': digitalWrite(11,LOW);
        break;
      case '1': digitalWrite(11,HIGH);
        break;
      case '2': digitalWrite(10,LOW);
        break;
      case '3': digitalWrite(10,HIGH);
        break;
      case '4': digitalWrite(13,LOW);
        break;
      case '5': digitalWrite(13,HIGH);
        break;
      default: break;
    }
  }
}
