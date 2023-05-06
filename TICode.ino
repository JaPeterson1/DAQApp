#include <Wire.h>
#include <BH1750.h>
#include <Adafruit_GFX.h>
#define ACTectionRange 20;
#define VREF 5.0
const int ACPin = A2;
BH1750 lightMeter;
float readACCurrentValue()
{
  float ACCurrtntValue = 0;
  float peakVoltage = 0;
  float voltageVirtualValue = 0;  //Vrms
  for (int i = 0; i < 5; i++)
  {
    peakVoltage += analogRead(ACPin);   //read peak voltage
    delay(1);
  }
  peakVoltage = peakVoltage / 5;
  voltageVirtualValue = peakVoltage * 0.707;    //change the peak voltage to the Virtual Value of voltage

  / The circuit is amplified by 2 times, so it is divided by 2. /
  voltageVirtualValue = (voltageVirtualValue / 1024 * VREF ) / 2;

  ACCurrtntValue = voltageVirtualValue * ACTectionRange;

  return ACCurrtntValue;
}
void setup() {
  Serial.begin(115200);
  Wire.begin();
  lightMeter.begin();
}
void loop() {
  if (Serial.available()) {
    message = Serial.readStringUntil('\n');
    float lux = lightMeter.readLightLevel();
    float irr = (lux0.0079);
    Serial.print(irr);
    Serial.print(",");
    float sensorValue = analogRead(A0);
    float voltage = (sensorValue / 1023) 5;
    float wind_speed = mapfloat(voltage, 0.4, 2, 0, 32.4);
    Serial.print(wind_speed);
    Serial.print(",");
    float ACCurrentValue = readACCurrentValue();
    Serial.print(ACCurrentValue);
    Serial.print(",");
    Serial.print(ACCurrentValue * 120);
  }
}
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
