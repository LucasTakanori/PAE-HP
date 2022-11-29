#include "RobotSerial.h"
#include <pthread.h>

using namespace std;

RobotSerial robot;
pthread_t commThread;

void* threadFunction(void* args) {
    robot.commThreadFunction();
    return 0;
}

void getPose() {

    int x, y;
    double theta;
    robot.getPose(&x, &y, &theta);
    cout << "New pose: " << endl;
    cout << "       x = " << x << endl;
    cout << "       y = " << y << endl;
    cout << "   theta = " << theta << endl;
}

int main() {
    pthread_create(&commThread, NULL, threadFunction, NULL);
    while (true){
        usleep(500000);
        getPose();
    }
    
}