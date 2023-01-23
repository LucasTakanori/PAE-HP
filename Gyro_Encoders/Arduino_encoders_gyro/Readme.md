Since there was not enough time to redo all the Kalman code in c++, we decided to make a small python program, a data logger of the data provided by the Arduino, in order to use Kalman.

The structure of this directory is the following:

- Inside the folder [Arduino](https://github.com/LucasTakanori/PAE-HP/tree/main/Gyro_Encoders/Arduino_encoders_gyro/Arduino/ ) you will find all the programs and libraries used for the Arduino board.

- The program to store all the data comming from Arduino is the following [data_log.py](https://github.com/LucasTakanori/PAE-HP/tree/main/Gyro_Encoders/Arduino_encoders_gyro/data_log.py)

# Install Guide

## Connections 
  
  ### Encoders
  For the encoders, you must connect ground and Vcc.
  Other pins used in the Encoder are  channel A and channel B. We will first talk about the right wheel, channel A must be conected to pin **3** and channel B to pin       **5**,  the connections of the left wheel are the following, channel A to pin **2** and channel B to pint **4**.
    
  ### MPU 6050
  For the MPU, you must also connect the ground and Vcc pins.
  The others ois used are the SDA and SCL pins of the MPU, that must be connected to the respective pins of the Arduino board, in case of the Arduino UNO pins A4 and A5.
  
  The following image represents our connections ina a visual manner.
  
  <img width="600" alt="image" src="https://github.com/LucasTakanori/PAE-HP/blob/main/Gyro_Encoders/Arduino_encoders_gyro/imgs/Connections.png" align="center">

## Using the programs

Having at your disposal an Arduino microcontroller, go to the directory where your projects and libraries are stored, there put all the contents of the following folder [Arduino](https://github.com/LucasTakanori/PAE-HP/tree/main/Gyro_Encoders/Arduino_encoders_gyro/Arduino/ ). Once you have done this, you must open the project **MPU_6050_calibration** upload the project to the Arduino board, run the program, open the serial, once opened send any kay via serial to start, wait until the gyro values are at zero and then press the reset button on the Arduino, the serial will show the optimal offsets. These offsets, technically should be kept stored in the IMU, but if they lose power they are lost, for this reason it is important to replace them in the program **final_robot_main**.
