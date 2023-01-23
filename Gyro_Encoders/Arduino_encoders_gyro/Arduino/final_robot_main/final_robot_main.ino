#include <DifferentialDrive.h>
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


Encoder rEncoder(R_ENCODER_A, R_ENCODER_B, deltaT, ticksPerRev);

Encoder lEncoder(L_ENCODER_A, L_ENCODER_B, deltaT, ticksPerRev);

DifferentialDrive robot(&lEncoder, &rEncoder, wheelCirc, wheelDist);

double x, y;
double theta;
unsigned long currentTime;

void setup() {
  Serial.begin(57600); //Start serial with Raspberry Pi
  Serial.setTimeout(100);

  //start timer and hardware interrupts
  Timer1.initialize(deltaT);
  Timer1.attachInterrupt(adjust);
  attachInterrupt(0, readLEncoder, RISING);
  attachInterrupt(1, readREncoder, RISING);
  //gyro initialization
  Wire.begin();           //Iniciando I2C  
  sensor.initialize();    //Iniciando el sensor

  if (sensor.testConnection()) Serial.println("Sensor intialized");
  else Serial.println("Error initializing sensor");
  sensor.setXAccelOffset(-337);
  sensor.setYAccelOffset(344);
  sensor.setZAccelOffset(1451);
  sensor.setXGyroOffset(24);
  sensor.setYGyroOffset(38);
  sensor.setZGyroOffset(36);
  sensor.setDLPFMode(MPU6050_DLPF_BW_5);
  tiempo_prev=millis();
  //initialize state Variables
  currentTime = millis();
}

void loop() {  
  if (millis() - tiempo_prev > 11) { //input.length()>0 millis() - currentTime > 111
    //currentTime=millis();
    //sendPacket();
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
    Serial.print(millis());Serial.print(",");
    sendPacket();
    //Serial.print(w_l);Serial.print(",");
    //Serial.print(w_r);Serial.print(",");
    Serial.print(gz_esc);Serial.print(",");
    Serial.println(girosc_ang_z);
  }
    

}

// assembles a packet to send it to Raspberry Pi
// sends values as ints broken into 2 byte pairs, least significant byte first
void sendPacket() {
  robot.getPosition(x, y, theta);
  float yaw = theta * 180.0 / M_PI;
  int sendX = (int)x;
  int sendY = (int)y;

  if (true) {
    //Serial.print("X: ");
    Serial.print(sendX);
    Serial.print(",");
    //Serial.print("Y: ");
    Serial.print(sendY);
    Serial.print(",");
    //Serial.print("Yaw ");
    Serial.print(yaw);
    Serial.print(",");
  }

}

void readLEncoder() {
  lEncoder.updateCount();
}

void readREncoder() {
  rEncoder.updateCount();
}

void adjust() {
  robot.update();
  lEncoder.getSpeed();
  rEncoder.getSpeed();
  
}




