/**
   @example UDPClientSingle.ino
   @brief The UDPClientSingle demo of library WeeESP8266.
   @author Wu Pengfei<pengfei.wu@itead.cc>
   @date 2015.02

   @par Copyright:
   Copyright (c) 2015 ITEAD Intelligent Systems Co., Ltd. \n\n
   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation; either version 2 of
   the License, or (at your option) any later version. \n\n
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
*/

#include "ESP8266.h"
#include <MPU9250_RegisterMap.h>
#include <SparkFunMPU9250-DMP.h>
#define SSID        "ASUS"
#define PASSWORD    "robomiller"
#define HOST_NAME   "192.168.1.234"
#define HOST_PORT   (1931)


#define ENA                 8
#define IN1                 6
#define IN2                 7
#define IN3                 4
#define IN4                 5
#define ENB                 3

#define leftIR              53
#define frontIR             22
#define rightIR             23

float xOffset = -27.0;
float yOffset = 4.0;

ESP8266 wifi(Serial1,115200);
MPU9250_DMP imu;
void setupMPU9250() {
  if (imu.begin() != INV_SUCCESS) {
    while (1) {
      Serial.println("Error");
      if (imu.begin() == INV_SUCCESS) {
        break;
      }
    }
  }
  imu.setSensors(INV_XYZ_GYRO | INV_XYZ_ACCEL | INV_XYZ_COMPASS);
  imu.setLPF(5);
  imu.setSampleRate(10);
  imu.setCompassSampleRate(10);
  imu.setGyroFSR(1000);
  imu.setAccelFSR(2);
}
void setup(void)
{
  Serial.begin(115200);
  Serial.print("setup begin\r\n");

  Serial.print("FW Version:");
  Serial.println(wifi.getVersion().c_str());

  if (wifi.setOprToStation()) {
    Serial.print("to station + softap ok\r\n");
  } else {
    Serial.print("to station + softap err\r\n");
  }

  if (wifi.joinAP(SSID, PASSWORD)) {
    Serial.print("Join AP success\r\n");
    Serial.print("IP: ");
    Serial.println(wifi.getLocalIP().c_str());
  } else {
    Serial.print("Join AP failure\r\n");
  }

  if (wifi.disableMUX()) {
    Serial.print("single ok\r\n");
  } else {
    Serial.print("single err\r\n");
  }

  Serial.print("setup end\r\n");
  setupMPU9250();
  pinMode(leftIR, INPUT);
  pinMode(frontIR, INPUT);
  pinMode(rightIR, INPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

if (wifi.registerUDP(HOST_NAME, HOST_PORT)) {
    Serial.print("register udp ok\r\n");
  } else {
    Serial.print("register udp err\r\n");
  }
  
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  analogWrite(ENB, 200);
  analogWrite(ENA, 200);
}

float getCompassDegrees(){
  imu.update(UPDATE_COMPASS);
  float magX = imu.calcMag(imu.mx)-xOffset; // magX is x-axis magnetic field in uT
  float magY = imu.calcMag(imu.my)-yOffset; // magY is y-axis magnetic field in uT
  
  float heading = atan2(magY, magX);
  float declinationAngle = (2.0 + (53.0 / 60.0)) / (180 / M_PI);
  heading += declinationAngle;

  if (heading < 0)
    heading += 2 * PI;

  if (heading > 2 * PI) 
    heading -= 2 * PI;

  return heading * 180/M_PI;  
}

void loop(void)
{
  uint8_t buffer[128] = {0};
  float sampleY = getCompassDegrees();
  char hello [10];
  dtostrf(sampleY, 2, 2, hello);
  Serial.println(sampleY);
  //wifi.send((const uint8_t*)hello, strlen(hello));
  delay(200);
}

