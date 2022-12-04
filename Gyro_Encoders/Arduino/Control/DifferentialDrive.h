#ifndef DifferentialDrive_h
#define DifferentialDrive_h

#include "Arduino.h"
#include <Encoder.h>
#include <math.h>

class DifferentialDrive {
    public:
            DifferentialDrive(Encoder*, Encoder*, int, int);
            void getPosition(double &x, double &y, double &theta);
            void updatePosition();
            void resetPosition();
            void update();

    private:
            int _wheelCirc;
            int _wheelDistance;
            double _xPosition, _yPosition, _theta;
            double _degreesPerMilimeter;
            Encoder *_leftWheel;
            Encoder *_rightWheel;
};

#endif