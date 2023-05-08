# DAQApp
Application Used to Monitor Solar and Wind Power Generation Produced by Wichita State University's Project Innovation Hub Shipping Container Annex. 

The hardware consists of the following: 
- A Raspberry Pi to run the code
- An Arduino reading data from three sensors:
  - An analog wind speed sensor
  - A solar intensity sensor
  - A current sensor to measure AC current on the output (120 V) side
- Two Renogy Rover Solar Charge Controllers

All data is pushed to a mysql server. 
