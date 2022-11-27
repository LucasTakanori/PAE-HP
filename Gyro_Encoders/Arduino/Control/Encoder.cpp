
#include "Encoder.h"
#include "Arduino.h"


Encoder::Encoder(int encoderA, int encoderB, long deltaT, int ticksPerRev) {
    
    _encoderA = encoderA;
    _encoderB = encoderB;
    _count = 0;
    _oldCount = 0;
    _newCount = 0;
    _totalCount = 0;
    _lastSpeed = 0;
    _deltaT = deltaT;
    _degPerTick = 360.0 / (double)ticksPerRev;
    pinMode(_encoderA, INPUT);
    pinMode(_encoderB, INPUT);
}

int Encoder::getSpeed() {
    _oldCount = _newCount;
    _newCount = _count;
    
    int difference = _newCount - _oldCount;

    _totalCount += difference;
    int degPerSec;

    if (difference < 65000 && difference > -65000) {
        double deltaTinSec = 1000000 / _deltaT;
        double ticksPerSec = (double)difference*(double)deltaTinSec;
        degPerSec = ticksPerSec * _degPerTick;
        _lastSpeed = degPerSec;
    } 
    else {
        degPerSec = _lastSpeed;
    }
    return degPerSec;
}

int Encoder::getDistance(){
    int distance = _degPerTick * _totalCount;
    _totalCount = 0;
    return distance;
}

void Encoder::updateCount() {
    if(digitalRead(_encoderA) == HIGH) {
        if(digitalRead(_encoderB) == LOW)
            _count++;
        else
            _count--;
    }
    else{
        if(digitalRead(_encoderB) == LOW)
            _count--;
        else
            _count++;
    }
}