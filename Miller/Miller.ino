#include <NewPing.h>

#include <doxygen.h>
#include <ESP8266.h>

#include <MPU9250_RegisterMap.h>
#include <SparkFunMPU9250-DMP.h>

#include <ArduinoJson.h>

#define SSID "ASUS"
#define PASSWORD "robomiller"
#define SERVER_ADDR "192.168.1.234"
#define SERVER_PORT (1931)

#define NOP 0
#define FORWARD 1
#define FORWARD_FAST 2
#define BACKWARD 3
#define TURN_LEFT 4
#define TURN_LEFT_MICRO 5
#define TURN_RIGHT 6
#define TURN_RIGHT_MICRO 7
#define GRAB 10
#define RELEASE 11
#define BACKWARD_LEFT 12
#define BACKWARD_RIGHT 13
#define RIGHT_AND_FORWARD 14
#define LEFT_AND_FORWARD 15
#define LEFT_180_AND_FORWARD 16
#define RIGHT_180_AND_FORWARD 17

#define ENA 3
#define IN1 5
#define IN2 4
#define IN3 7
#define IN4 6
#define ENB 8

#define leftIR 53
#define frontIR 22
#define rightIR 23

#define LEFT_ECHO 10
#define LEFT_TRIGGER 9
#define RIGHT_ECHO A2
#define RIGHT_TRIGGER A1

#define DEBUG_LED_WIFI A8

ESP8266 wifi(Serial1, 115200);
MPU9250_DMP imu;
NewPing leftSonar(LEFT_TRIGGER, LEFT_ECHO, 200);
NewPing rightSonar(RIGHT_TRIGGER, RIGHT_ECHO, 200);

void setupMPU9250()
{
  if (imu.begin() != INV_SUCCESS)
  {
    while (1)
    {
      Serial.println("Error");
      if (imu.begin() == INV_SUCCESS)
      {
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

void joinNetwork()
{
  if (wifi.joinAP(SSID, PASSWORD))
  {
    Serial.print("Join AP success\r\n");
    Serial.print("IP:");
    Serial.println(wifi.getLocalIP().c_str());
    digitalWrite(DEBUG_LED_WIFI, HIGH);
  }
  else
  {
    Serial.print("Join AP failure\r\n");
    digitalWrite(DEBUG_LED_WIFI, LOW);
  }

  if (wifi.disableMUX())
  {
    Serial.print("single ok\r\n");
  }
  else
  {
    Serial.print("single err\r\n");
  }
}

void createTCP()
{

  if (wifi.createTCP(SERVER_ADDR, SERVER_PORT))
  {
    Serial.print("TCP connection successfully created\n");
  }
  else
  {
    Serial.print("Error on creating TCP connection\n");
    delay(1000);
    return;
  }
}

void releaseTCP()
{
  if (wifi.releaseTCP())
  {
    Serial.print("release tcp ok\r\n");
  }
  else
  {
    Serial.print("release tcp err\r\n");
  }
}

void setup()
{
  //wifi.restart();
  // put your setup code here, to run once
  Serial.begin(115200);
  Serial.print("Beginning setup...\n");

  if (wifi.setOprToStation())
  {
    Serial.print("to station ok\r\n");
  }
  else
  {
    Serial.print("to station err\r\n");
  }

  pinMode(leftIR, INPUT);
  pinMode(frontIR, INPUT);
  pinMode(rightIR, INPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(DEBUG_LED_WIFI, OUTPUT);

  setupMPU9250();
  joinNetwork();
}

void askAndExecute(char *data)
{
  uint8_t buffer[10] = {99};

  if (wifi.getIPStatus().equals("STATUS:5"))
  {
    Serial.println("Network error, reconnecting");
    joinNetwork();
    createTCP();
  }

  createTCP();
  wifi.send((const uint8_t *)data, strlen(data));
  uint32_t len = wifi.recv(buffer, sizeof(buffer), 10000);

  int command = atoi((char *)buffer);
  switch (command)
  {

  case FORWARD:
  {
    moveForward();
    break;
  }

  case FORWARD_FAST:
  {
    moveForwardFast();
    break;
  }

  case BACKWARD:
  {
    moveBackward();
    break;
  }

  case TURN_LEFT:
  {
    turnLeft();
    break;
  }

  case TURN_LEFT_MICRO:
  {
    turnLeftMicro();
    break;
  }

  case TURN_RIGHT:
  {
    turnRight();
    break;
  }

  case TURN_RIGHT_MICRO:
  {
    turnRightMicro();
    break;
  }

  case GRAB:
  {
    Serial.println("Lowering my arm");
    break;
  }

  case RELEASE:
  {
    Serial.println("Bringing my arm up");
    break;
  }

  case BACKWARD_LEFT:
  {
    moveBackward();
    turnLeft();
    break;
  }

  case BACKWARD_RIGHT:
  {
    moveBackward();
    turnRight();
    break;
  }

  case LEFT_AND_FORWARD:
  {
    turnLeft();
    moveForward();
  }

  case LEFT_180_AND_FORWARD:
  {
    turnLeft();
    turnLeft();
    moveForward();
  }

  case RIGHT_AND_FORWARD:
  {
    turnRight();
    moveForward();
  }

  case RIGHT_180_AND_FORWARD:
  {
    turnRight();
    turnRight();
    moveForward();
  }

  default:
  {
    switch (command / 1000)
    {
    case TURN_LEFT:
    {
      float targetAngle = command % 1000;
      Serial.print("Turning left of: ");
      Serial.println(targetAngle);
      turnLeft(targetAngle);
      break;
    }
    case TURN_RIGHT:
    {
      float targetAngle = command % 1000;
      Serial.print("Turning right of: ");
      Serial.println(targetAngle);
      turnRight(targetAngle);
      break;
    }
    }
  }
  }
  releaseTCP();
  return;
}

void loop()
{
  uint8_t leftObstacle = digitalRead(leftIR);
  uint8_t frontObstacle = digitalRead(frontIR);
  uint8_t rightObstacle = digitalRead(rightIR);
  float leftDistance = leftSonar.convert_cm(leftSonar.ping_median());
  float rightDistance = rightSonar.convert_cm(rightSonar.ping_median());

  StaticJsonBuffer<200> jsonBuffer;
  JsonObject &root = jsonBuffer.createObject();
  root["leftObstacle"] = leftObstacle;
  root["frontObstacle"] = frontObstacle;
  root["rightObstacle"] = rightObstacle;
  root["leftDistance"] = leftDistance;
  root["rightDistance"] = rightDistance;
  root["degrees"] = getCompassDegrees();

  char msg[512];
  root.printTo(msg, sizeof(msg));
  askAndExecute(msg);
}
