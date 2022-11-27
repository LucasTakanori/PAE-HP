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

int translational;
double angular;

void setup() {
  Serial.begin(9600); //Start serial with Raspberry Pi
  Serial.setTimeout(100);

  //start timer and hardware interrupts
  Timer1.initialize(deltaT);
  Timer1.attachInterrupt(adjust);
  attachInterrupt(0, readLEncoder, CHANGE);
  attachInterrupt(1, readREncoder, CHANGE);

  //initialize state Variables
  commandReceived = false;
  lastCommandTime = millis();
  currentTime = millis();
  translational = 0;
  angular = 0.0;
}

void loop() {
  //check if a command oacket is available to read
  readCommandPacket();

  currentTime=millis();

  if (currentTime - lastCommandTime > 1000) {
    Serial.println("Command not recieved for 1 second");
    lastCommandTime = millis();
  }

}

//tries to read command packet from Raspberry Pi
void readCommandPacket() {
  byte buffer[4];
  int result = Serial.readBytes((char*)buffer, 4);

  if (result == 4) { //correct number of bytes recieved
    int commands[2];

    //assemble 16bit ints from the recieved bytes in the buffer
    for (int i=0; i < 2; i++) {
      int firstByte = buffer[2*i];
      int secondByte = buffer[(2*i) + 1];
      commands[i] = (secondByte << 8) | firstByte;
    }
    translational = commands[0];
    angular = (double)commands[1] / 1000.0; //Convert recieved int to double 

    commandReceived = true;
    lastCommandTime = millis();
  }
  else if (result > 0) {
    Serial.println("Incomplete command");
  }

}

// assembles a packet to send it to Raspberry Pi
// sends values as ints broken into 2 byte pairs, least significant byte first
void sendPacket() {
  robot.getPosition(x, y, theta);
  byte buffer[22];
  int sendX = (int)x;
  int sendY = (int)y;
  int sendTheta = (int)(theta*1000.0);
  buffer[16] = (byte)(sendX & 0xFF);
  buffer[17] = (byte)((sendX >> 8) & 0xFF);
  buffer[18] = (byte)(sendY & 0xFF);
  buffer[19] = (byte)((sendY >> 8) & 0xFF);
  buffer[20] = (byte)(sendTheta & 0xFF);
  buffer[21] = (byte)((sendTheta >> 8) & 0xFF);
  Serial.write(buffer, 22);
}

void readLEncoder() {
  lEncoder.updateCount();
}

void readREncoder() {
  rEncoder.updateCount();
}

void adjust() {
  robot.updatePosition();
}




