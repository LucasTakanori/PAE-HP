// The librarys MPU6050.h, I2Cdev.h and Wire.h are from Jeff Rowberg
// library MPU6050.h needs I2Cdev.h, I2Cdev.h needs Wire.h

//#include <DifferentialDrive.h>
#include <Encoder.h>
#include <robot.h>

#include <TimerOne.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#include <Wire.h>

MPU6050 sensor;

#define ARDUINO_ADDRESS 0x6 //check I2C adddress

int gx, gy, gz;
int ax, ay, az;
long tiempo_prev, dt;

float girosc_ang_z=0, girosc_ang_y;
float girosc_ang_z_prev, girosc_ang_y_prev;
float gz_esc;
double w_l, w_r;

bool commandReceived;   // true if command packet has been received

Encoder rEncoder(R_ENCODER_A, R_ENCODER_B, deltaT, ticksPerRev);

Encoder lEncoder(L_ENCODER_A, L_ENCODER_B, deltaT, ticksPerRev);

//DifferentialDrive robot(&lEncoder, &rEncoder, wheelCirc, wheelDist);

double x, y;
double theta;
int still;
unsigned long lastCommandTime, currentTime;

void setup() {
  Serial.begin(57600); //Start serial with Raspberry Pi
  Serial.setTimeout(100);

  //start timer and hardware interrupts
  //Timer1.initialize(deltaT); //Used when we where tracking the odometry in the Arduino
  //Timer1.attachInterrupt(adjust);
  attachInterrupt(0, readLEncoder, RISING);
  attachInterrupt(1, readREncoder, RISING);
  //gyro initialization
  Wire.begin();           //Initialize I2C  
  sensor.initialize();    //Initialize sensor

  if (sensor.testConnection()) Serial.println("Sensor intialized");
  else Serial.println("Error initializing sensor");
  //Sensor offset obtained through MPU_6050_calibration
  sensor.setXAccelOffset(-303);
  sensor.setYAccelOffset(342);
  sensor.setZAccelOffset(1459);
  sensor.setXGyroOffset(26);
  sensor.setYGyroOffset(36);
  sensor.setZGyroOffset(34);
  sensor.setDLPFMode(MPU6050_DLPF_BW_5);
  tiempo_prev=millis();
  //initialize state Variables
  commandReceived = false;
  lastCommandTime = millis();
  currentTime = millis();
}

void loop() {
  
  if (millis() - tiempo_prev > 111) { 

    //sensor.getRotation(&gx, &gy, &gz);
    sensor.getMotion6(&ax, &ay, &az,&gx, &gy, &gz);
    w_l = (-1)*lEncoder.getSpeed();
    w_r = (rEncoder.getSpeed());
  
    //Calcular los angulos rotacion:
  
    dt = millis()-tiempo_prev;
    tiempo_prev=millis();

    gz_esc = gz/131.0;
    girosc_ang_z = (gz_esc)*dt/1000.0 + girosc_ang_z_prev;
    girosc_ang_z_prev=girosc_ang_z;
    //Send via serial the current time of arduino [ms]
    //                                    left wheel angular velocity []
    //                                    right wheel angular velocity
    //                                    gyroscope angular velocity from Z axis
    //                                    angle obtained through the integration
    //Intended to be read by a Python program, that will store the data in a CSV file
    Serial.print(millis());Serial.print(",");
    Serial.print(w_l);Serial.print(",");
    Serial.print(w_r);Serial.print(",");
    Serial.print(gz_esc);Serial.print(",");
    Serial.println(girosc_ang_z);
  }
    

}

// assembles a packet to send it to Raspberry Pi
// sends values as ints broken into 2 byte pairs, least significant byte first
//Function created to communicate with the Raspberry PI, fixing the length of the message
void sendPacket() {
  //robot.getPosition(x, y, theta);
  byte buffer[9];
  float yaw = theta * 180.0 / M_PI;
  int sendX = (int)x;
  int sendY = (int)y;
  uint32_t sendTheta = (uint32_t)(yaw*1000);
  buffer[0] = (sendX & 0xFF);
  buffer[1] = ((sendX >> 8) & 0xFF);
  buffer[2] = (sendY & 0xFF);
  buffer[3] = ((sendY >> 8) & 0xFF);
  buffer[4] = (sendTheta & 0xFF);
  buffer[5] = ((sendTheta >> 8) & 0xFF);
  buffer[6] = ((sendTheta >> 16) & 0xFF);
  buffer[7] = ((sendTheta >> 24) & 0xFF);
  buffer[8] = (still & 0xFF);
  //Serial.write(buffer, 9);
  //Serial.println();
  if (false) { //DEbug purposes
    Serial.print("X: ");
    Serial.print(sendX);
    Serial.print("\t");
    Serial.print("Y: ");
    Serial.print(sendY);
    Serial.print("\t");
    Serial.print("Yaw no decimal: ");
    Serial.println(sendTheta);
  }

}

void readLEncoder() {
  lEncoder.updateCount();
}

void readREncoder() {
  rEncoder.updateCount();
}

void adjust() {
  //robot.update();
  //Returns the angular velocity of each wheel.
  lEncoder.getSpeed(); 
  rEncoder.getSpeed();
  
}




