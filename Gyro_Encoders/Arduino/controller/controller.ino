#include <DifferentialDrive.h>
#include <Encoder.h>
#include <robot.h>

#include <TimerOne.h>
#include <Wire.h>

#define ARDUINO_ADDRESS 0x6 //check I2C adddress

const uint8_t trig = 1; // constant for triggering updates
bool commandReceived;   // true if command packet has been received

Encoder rEncoder(R_ENCODER_A, R_ENCODER_B, deltaT, ticksPerRev);

Encoder lEncoder(L_ENCODER_A, L_ENCODER_B, deltaT, ticksPerRev);

DifferentialDrive robot(&lEncoder, &rEncoder, wheelCirc, wheelDist);

double x, y;
double theta;
unsigned long lastCommandTime, currentTime;
int still;

void setup() {
  Serial.begin(9600); //Start serial with Raspberry Pi
  //Serial.setTimeout(100);

  //start timer and hardware interrupts
  Timer1.initialize(deltaT);
  Timer1.attachInterrupt(adjust);
  attachInterrupt(0, readLEncoder, CHANGE);
  attachInterrupt(1, readREncoder, CHANGE);

  //initialize state Variables
  commandReceived = false;
  lastCommandTime = millis();
  currentTime = millis();
  still = 1;
}

void loop() {
  //check if a command packet is available to read
  //readCommandPacket();
  //sendPacket();

  currentTime=millis();

  if (Serial.available()<=0) {
    if (currentTime - lastCommandTime > 1000) {
    //Serial.println("Command not recieved for 1 second");
      sendPacket();
      still=1;
      lastCommandTime = millis();
    }
  }

}


// assembles a packet to send it to Raspberry Pi
// sends values as ints broken into 2 byte pairs, least significant byte first
void sendPacket() {
  robot.getPosition(x, y, theta);
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
  //Serial.println(theta);
  Serial.write(buffer, 9);
  // Serial.println(sendTheta);
}

void readLEncoder() {
  lEncoder.updateCount();
  still = 0;
}

void readREncoder() {
  rEncoder.updateCount();
  still = 0;
}

void adjust() {
  robot.update();
}




