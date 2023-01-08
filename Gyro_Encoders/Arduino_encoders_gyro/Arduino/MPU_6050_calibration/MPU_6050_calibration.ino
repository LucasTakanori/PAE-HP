// The librarys used are from Jeff Rowberg
// library MPU6050.h needs I2Cdev.h, I2Cdev.h needs Wire.h
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

// The address of the MPU6050 can be 0x68 or 0x69, depends 
// of AD0. If not specified, 0x68 
MPU6050 sensor;

// RAW values from accelerometer and gyro x,y,z axis
int ax, ay, az;
int gx, gy, gz;

//Parameters used for the low pass filter
long f_ax,f_ay, f_az;
int p_ax, p_ay, p_az;
long f_gx,f_gy, f_gz;
int p_gx, p_gy, p_gz;
int counter=0;

//Offsets values
int ax_o,ay_o,az_o;
int gx_o,gy_o,gz_o;

int rate;

void setup() {
  Serial.begin(9600);   //Initialize serial port
  Wire.begin();           //initialize I2C  
  sensor.initialize();    //Initialize sensor

  if (sensor.testConnection()) Serial.println("Sensor Initialized");
  sensor.setDLPFMode(MPU6050_DLPF_BW_5);
  
  // Reading last offsets
  
  
  ax_o=sensor.getXAccelOffset();
  ay_o=sensor.getYAccelOffset();
  az_o=sensor.getZAccelOffset();
  gx_o=sensor.getXGyroOffset();
  gy_o=sensor.getYGyroOffset();
  gz_o=sensor.getZGyroOffset();

  rate = sensor.getRate();
  
  Serial.println("Offsets:");
  Serial.print(ax_o); Serial.print("\t"); 
  Serial.print(ay_o); Serial.print("\t"); 
  Serial.print(az_o); Serial.print("\t"); 
  Serial.print(gx_o); Serial.print("\t"); 
  Serial.print(gy_o); Serial.print("\t");
  Serial.print(gz_o); Serial.print("\t");
  Serial.println("\n Send a character to start calibration \n");  
  // Waits for a character to be sent
  while (true){if (Serial.available()) break;}  
  Serial.println("Calibrating, do not move the IMU");  
  
}

void loop() {
  // Reading the raw values for the gyro and accelerometer
  //sensor.getAcceleration(&ax, &ay, &az);
  //sensor.getRotation(&gx, &gy, &gz);
  sensor.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  

  // Readings filter
  f_ax = f_ax-(f_ax>>5)+ax;
  p_ax = f_ax>>5;

  f_ay = f_ay-(f_ay>>5)+ay;
  p_ay = f_ay>>5;

  f_az = f_az-(f_az>>5)+az;
  p_az = f_az>>5;

  f_gx = f_gx-(f_gx>>3)+gx;
  p_gx = f_gx>>3;

  f_gy = f_gy-(f_gy>>3)+gy;
  p_gy = f_gy>>3;

  f_gz = f_gz-(f_gz>>3)+gz;
  p_gz = f_gz>>3;

  //Correcting the values every 100 samples
  if (counter==100){
    Serial.print(p_ax); Serial.print("\t");
    Serial.print(p_ay); Serial.print("\t");
    Serial.print(p_az); Serial.print("\t");
    Serial.print(p_gx); Serial.print("\t");
    Serial.print(p_gy); Serial.print("\t");
    Serial.println(p_gz);

    //Acceleromter calibration
    if (p_ax>0) ax_o--;
    else {ax_o++;}
    if (p_ay>0) ay_o--;
    else {ay_o++;}
    if (p_az-16384>0) az_o--;
    else {az_o++;}
    
    sensor.setXAccelOffset(ax_o);
    sensor.setYAccelOffset(ay_o);
    sensor.setZAccelOffset(az_o);

    //Gyroscope calibration we want 0º/s 
    if (p_gx>0) gx_o--;
    else {gx_o++;}
    if (p_gy>0) gy_o--;
    else {gy_o++;}
    if (p_gz>0) gz_o--;
    else {gz_o++;}
    
    sensor.setXGyroOffset(gx_o);
    sensor.setYGyroOffset(gy_o);
    sensor.setZGyroOffset(gz_o);    

    counter=0;
  }
  counter++;
}
