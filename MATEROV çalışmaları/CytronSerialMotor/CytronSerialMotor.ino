//Initialize the variables necessary
int dirPin[] = {2, 4, 7, 8, 12, 13};
int s = 6;
int pvmPin[] = {3, 5, 6, 9, 10, 11};
double t = 0;
int amp = 250;
int val[] = {0, 0, 0, 0, 0, 0};
int lastVal[] = {0, 0, 0, 0, 0, 0};
String msg = "";
String msgCurr = "";
//Setup the motors
void setup() {
  for (int x = 0; x < s; x++) {
    pinMode(dirPin[x], OUTPUT);
  }

  for (int x = 0; x < s; x++) {
    pinMode(pvmPin[x], OUTPUT);
  }
  Serial.begin(9600);
}
//Read input from python and send it to the motors
void loop() {
  if (Serial.available()) {
    process();
    //delay(50);
  }
  for (int i = 0; i < s; i++) {
    if (val[i] == lastVal[i]) {
      continue;
    }
    int pvr = val[i];
    digitalWrite(dirPin[i], (pvr > 0) ? HIGH : LOW);
    analogWrite(pvmPin[i], abs(pvr));
    lastVal[i] = val[i];
  }
}
//Read input from python and convert it to motor values. Sample Input: 125,125,125,125,-125,-125;
void process() {
  char chrIn = Serial.read();
  msg += chrIn;
  if (msg.indexOf(";") > 0) {
    msgCurr = msg.substring(0, msg.indexOf(";"));
    msg = msg.substring(msg.indexOf(";") + 3);
  }
  if (msgCurr != "") {
    int i = 0;
    while (msgCurr.indexOf(",") != -1) {
      val[i++] = msgCurr.substring(0, msgCurr.indexOf(",")).toInt();
      msgCurr = msgCurr.substring(msgCurr.indexOf(",") + 1);
    }
    val[i++] = msgCurr.substring(0, msgCurr.indexOf(";")).toInt();
    msgCurr = "";
  }
}
