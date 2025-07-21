#ifndef SMS_MODULE_H
#define SMS_MODULE_H

#include <SoftwareSerial.h>

#define SIM800_TX 2
#define SIM800_RX 3

SoftwareSerial sim800(SIM800_RX, SIM800_TX); // RX, TX

void initSIM800L() {
  sim800.begin(9600);
  delay(1000);
}

void sendSMS(String phoneNumber, String message) {
  sim800.println("AT+CMGF=1"); delay(1000); // Set SMS text mode
  sim800.print("AT+CMGS=\""); sim800.print(phoneNumber); sim800.println("\""); delay(1000);
  sim800.print(message); delay(500);
  sim800.write(26);  // ASCII Ctrl+Z to send SMS
  delay(3000);
}

#endif
