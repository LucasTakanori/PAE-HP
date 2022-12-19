//Different constants used for the robot calculation
#ifndef robot_h
#define robot_h

//delta T used for calculations, is defined in microseconds
const long deltaT = 100000;

//Physical robot constants, ticksPerRev depends on how we read channel A, only rise -> 51200, change-> 102400
const int ticksPerRev = 51200, wheelCirc = 768, wheelDist = 287;

//Encoder pins
#define R_ENCODER_A 3 //defined as Arduino digital pin interrupt
#define R_ENCODER_B 5
#define L_ENCODER_A 2 //defined as Arduino digital pin interrupt
#define L_ENCODER_B 4

#endif
