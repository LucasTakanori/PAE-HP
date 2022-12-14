
#ifndef Encoder_h
#define Encoder_h

#include "Arduino.h"

class Encoder {

    public:
            Encoder(int encoderA, int encoderB, long deltaT, int ticksPerRev);
            double getSpeed(); //returns speed in deg/seg
            double getDistance(); //return distance rotated in degrees
            void updateCount();
            long getTicks(); //returns ticks counts
    private:
            int _encoderA, _encoderB; // encoder pins
            double _degPerTick; //degrees of output shaft rotation per encoder tick
            volatile long _count, _oldCount, _newCount;
            long _deltaT; // in microseconds
            int _lastSpeed;
            long _totalCount;
};

#endif