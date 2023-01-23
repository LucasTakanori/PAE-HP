
#include "Arduino.h"
#include <DifferentialDrive.h>
#include <Encoder.h>
#include <math.h>

const double pi = 3.141592;

DifferentialDrive::DifferentialDrive(Encoder *lWheel, Encoder *rWheel, int wheelCirc, int wheelDistance) {

    _leftWheel = lWheel;
    _rightWheel = rWheel;
    _wheelCirc = wheelCirc;
    _wheelDistance = wheelDistance;
    _xPosition = 0.0;
    _yPosition = 0.0;
    _theta = 0.0;
    _degreesPerMilimeter = 360.0 / (double)wheelCirc;
}

void DifferentialDrive::getPosition(double &x, double &y, double &theta) {
    
    x = _xPosition;
    y = _yPosition;
    theta = _theta;
}

void DifferentialDrive::update() {
    _leftWheel->getSpeed();
    _rightWheel->getSpeed();
    updatePosition();
}

void DifferentialDrive::updatePosition() {
    double leftDegrees = -_leftWheel->getDistance();
    double rightDegrees = _rightWheel->getDistance();
    double dLeft = leftDegrees / _degreesPerMilimeter;
    double dRight = rightDegrees / _degreesPerMilimeter;
    double dCenter = (dLeft - dRight)/2.0;
    double phi = (dRight - dLeft) / (4*(double)_wheelDistance);
    _theta += phi;
    if (_theta > 2.0 * M_PI)
        _theta -= 2.0*M_PI;
    if (_theta < 0.0) 
        _theta += 2.0*M_PI;
    _xPosition += dCenter*cos(_theta);
    _yPosition += dCenter*sin(_theta);
}

void DifferentialDrive::resetPosition() {
    _xPosition = 0;
    _yPosition = 0;
    _theta = 0.0;
}
