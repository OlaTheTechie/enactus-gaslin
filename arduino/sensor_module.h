#ifndef SENSOR_MODULE_H
#define SENSOR_MODULE_H

#define MQ6_PIN A0
#define GAS_THRESHOLD 300

void initSensor() {
  pinMode(MQ6_PIN, INPUT);
}

int readGasLevel() {
  return analogRead(MQ6_PIN);
}

#endif
