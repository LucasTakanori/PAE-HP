#include "RobotSerial.h"

RobotSerial::RobotSerial() {

    x_ = 0;
    y_ = 0;
    theta_ = 0.0;
    serialFd_ = -1;
    readPeriod_ = 250000;
    numSensor_ = 0;
    sensorPacketSize_ = (numSensor_ + numPoseVariables);

    resetController();
    openSerial();

}

void RobotSerial::getPose(int *x, int *y, double *theta) {
    *x = x_;
    *y = y_;
    *theta = theta_;
}

void RobotSerial::openSerial() {
    serialFd_ = open("/dev/ttyACM0", O_RDWR);

    if (serialFd_ == -1) {
        cerr << "Error, unable to open uart" << endl;
        exit(-1);
    }

    struct termios options;
    tcgetattr(serialFd_, &options);
    options.c_lflag = B9600 | CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    options.c_cc[VMIN] = sensorPacketSize_;
    options.c_cc[VTIME] = 0;
    tcsetattr(serialFd_, TCSANOW, &options);
    usleep(250000);
    tcflush(serialFd_, TCIOFLUSH);
}

void RobotSerial::resetController() {
    //TO-DO
}

int RobotSerial::receive(char* sensorPacket) {
    memset(sensorPacket, '\0', sensorPacketSize_);

    int rxBytes;
    if(serialFd_ != -1) {
        rxBytes = read(serialFd_, sensorPacket, sensorPacketSize_);
    }
    return rxBytes;

}

int RobotSerial::parseSensorPacket(char* sensorPacket) {
    int16_t firstByte;
    int16_t secondByte;
    int16_t inValues[numSensor_ + numPoseVariables];
    for (int i = 0; i < (numSensor_ + numPoseVariables); i++){
        firstByte = sensorPacket[2*i];
        secondByte = sensorPacket[(2*i)+1];
        inValues[i]= (secondByte << 8) | firstByte;
    }

    x_ = inValues[numSensor_ + numPoseVariables - 3];
    y_ = inValues[numSensor_ + numPoseVariables - 2];
    theta_ = ((double)inValues[numSensor_ + numPoseVariables - 1]) / 1000.0;

    return (numSensor_ + numPoseVariables);
}

void RobotSerial::commThreadFunction() {
        while(true) {
            //char commandPacket[commandPacketSize];
            char sensorPacket[sensorPacketSize_];
            int receiveResult = receive(sensorPacket);
            if (receiveResult < 1) {
                cerr << "sensor packet not received" << endl;
            }
            else if (receiveResult < sensorPacketSize_) {
                cerr << "incomplete sensor packet" << endl;
            }
            else {
                parseSensorPacket(sensorPacket);
            }
            usleep(readPeriod_);
        }
}