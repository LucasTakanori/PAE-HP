
#ifndef Encoder_h
#define Encoder_h

#include "Arduino.h"

class Encoder {

    public:
            Encoder(int encoderA, int encoderB, long deltaT, int ticksPerRev);
            int getSpeed();
            int getDistance();
            void updateCount();
    private:
            int _encoderA, _encoderB; // encoder pins
            double _degPerTick;
            volatile long _count, _oldCount, _newCount;
            long _deltaT; // in microseconds
            int _lastSpeed;
            int _totalCount;
};

#endif