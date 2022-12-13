
#ifndef RobotSerial_h
#define RobotSerial_h

#include <stdio.h>
#include <cstdlib>
#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <string.h>
#include <pthread.h>

using namespace std;

const int commandPacketSize = 4;
const int numPoseVariables = 3;

class RobotSerial {
    public:
            RobotSerial();
            void getPose(int* x, int* y, double* theta);
            void commThreadFunction();

    private:
            int x_, y_;
            double theta_;
            int serialFd_;
            int readPeriod_;
            int numSensor_;
            int sensorPacketSize_;
            int CommandPacketSize_;

            void openSerial();
            void resetController();
            int transmit(char* commandPacket);
            int receive(char* sensorPacket);
            int parseSensorPacket(char* sensorPacket);
};

#endif