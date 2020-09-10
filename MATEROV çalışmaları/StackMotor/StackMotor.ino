//Code to send the values to the ROV for a different motor controller we were using
//Similar to the other program but values are written to the motors differently

int size = 6;
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMSbot(0x60);
Adafruit_MotorShield AFMStop(0x61);
Adafruit_DCMotor *motors[6] = {AFMSbot.getMotor(1), AFMSbot.getMotor(2), AFMSbot.getMotor(3), AFMSbot.getMotor(4), AFMStop.getMotor(1), AFMStop.getMotor(2)};
String msg = "";
String msgCurr = "";
int val[] = {0, 0, 0, 0, 0, 0};
int lastVal[] = {0, 0, 0, 0, 0, 0};

void setup() {
  Serial.begin(9600);
  AFMSbot.begin();
  AFMStop.begin();
  for (int i = 0; i < size; i++) {
    motors[i] -> setSpeed(0);
    motors[i] -> run(FORWARD);
    motors[i] -> run(RELEASE);
  }
}

void loop() {
  if (Serial.available()) {
    process();

  }
  for (int i = 0; i < size; i++) {
    if (lastVal[i] != val[i]) {
      setMotor(i, val[i]);
      lastVal[i] = val[i];
    }
  }
}

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

void setMotor(int index, int speed) {
  motors[index] -> setSpeed(abs(speed));
  if (speed < 0) {
    motors[index] -> run(BACKWARD);
  } else {
    motors[index] -> run(FORWARD);
  }
}
