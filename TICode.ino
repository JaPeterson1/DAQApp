#include <Wire.h>
#include <BH1750.h>
#include <Adafruit_GFX.h>
#define ACTectionRange 20;
#define VREF 5.0
const int ACPin = A2;
const int windSensorPin = A0;
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

  //The circuit is amplified by 2 times, so it is divided by 2.
  voltageVirtualValue = (voltageVirtualValue / 1024 * VREF ) / 2;

  ACCurrtntValue = voltageVirtualValue * ACTectionRange;

  return ACCurrtntValue;
}
void setup() {
  Serial.begin(9600);
  //Serial.setTimeout(100);
  Wire.begin();
  lightMeter.begin();
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

float map_range(float x, float in_min, float in_max, float out_min, float out_max) {
  float in_range = in_max - in_min;
  float in_delta = x - in_min;
  float mapped = 0;
  if (in_range != 0) {
    mapped = in_delta / in_range;
  } else if (in_delta != 0) {
    mapped = in_delta;
  } else {
    mapped = 0.5;
  }
  mapped *= out_max - out_min;
  mapped += out_min;
  if (out_min <= out_max) {
    return max(min(mapped, out_max), out_min);
  }
  return min(max(mapped, out_max), out_min);
}
void loop() {
  float lux = lightMeter.readLightLevel();
  float irr = (lux * 0.0079);
  float sensorValue = analogRead(windSensorPin);
  float voltage = sensorValue * (5 / 1023.0);
  float wind_speed = map_range(voltage, .4, 2, 0, 32.4);
  float ACCurrentValue = readACCurrentValue();

  if (Serial.available() > 0) {
    Serial.readStringUntil("\n");
    Serial.print(irr);
    Serial.print(",");
    Serial.print(wind_speed);
    Serial.print(",");
    Serial.print(ACCurrentValue * 120);
    Serial.print("\n");
  }
}
