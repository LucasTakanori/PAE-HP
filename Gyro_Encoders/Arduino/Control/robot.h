//Different constants used for the robot calculation
#ifndef robot_h
#define robot_h

//delta T used for calculations
const long deltaT = 50000;

//Physical robot constants
const int ticksPerRev = 51200, wheelCirc = 768, wheelDist = 287;

//Encoder pins
#define R_ENCODER_A 3 //defined as Arduino digital pin interrupt
#define R_ENCODER_B 5
#define L_ENCODER_A 2 //defined as Arduino digital pin interrupt
#define L_ENCODER_B 4

#endif
