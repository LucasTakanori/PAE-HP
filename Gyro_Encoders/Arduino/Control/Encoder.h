
#ifndef Encoder_h
#define Encoder_h

#include "Arduino.h"

class Encoder {

    public:
            Encoder(int encoderA, int encoderB, long deltaT, int ticksPerRev);
            int getSpeed(); //returns speed in deg/seg
            int getDistance(); //return distance rotated in degrees
            void updateCount();
            int getTicks(); //returns ticks counts
    private:
            int _encoderA, _encoderB; // encoder pins
            double _degPerTick; //degrees of output shaft rotation per encoder tick
            volatile long _count, _oldCount, _newCount;
            long _deltaT; // in microseconds
            int _lastSpeed;
            int _totalCount;
};

#endif