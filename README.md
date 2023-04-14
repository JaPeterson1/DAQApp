# DAQApp
Application used to monitor solar and wind generation at Wichita State University's Project Innovation Hub. 

The hardware consists of the following: 
- A raspberry pi to run the code
- An arduino running three sensors:
  - An analog wind speed sensor
  - A solar intensity sensor
  - A current sensor to measure current on the output (120 V) side. 
- Two Renogy Rover solar charge controllers. 

All data is pushed to a mysql server. 
