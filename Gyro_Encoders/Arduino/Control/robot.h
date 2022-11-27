//Different constants used for the robot calculation
#ifndef robot_h
#define robot_h

//delta T used for calculations
const long deltaT = 50000;

//Physical robot constants
const int ticksPerRev = 51200, wheelCirc = 450, wheelDist = 250;

//Encoder pins
#define R_ENCODER_A 3
#define R_ENCODER_B 5
#define L_ENCODER_A 2
#define L_ENCODER_B 4

#endif