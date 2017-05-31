#include <doxygen.h>
#include <ESP8266.h>

#include <ArduinoJson.h>

#define SSID            "Robot Wifi"
#define PASSWORD        "robomiller"
#define SERVER_ADDR     "192.168.1.83"
#define SERVER_PORT     (1931)

#define FORWARD             0
#define FORWARD_FAST        1
#define BACKWARD            2
#define TURN_LEFT           3
#define TURN_LEFT_MICRO     4
#define TURN_RIGHT          5
#define TURN_RIGHT_MICRO    6
#define GRAB                10
#define RELEASE             11
#define BACKWARD_LEFT       12
#define BACKWARD_RIGHT      13

#define ENA                 7
#define IN1                 4
#define IN2                 3
#define IN3                 6
#define IN4                 5
#define ENB                 2

#define leftIR              53
#define frontIR             22
#define rightIR             23

#define DEBUG_LED_WIFI      A0

ESP8266 wifi(Serial1,115200);

void joinNetwork(){
  if (wifi.joinAP(SSID, PASSWORD)) {
    Serial.print("Join AP success\r\n");
    Serial.print("IP:");
    Serial.println( wifi.getLocalIP().c_str());
    digitalWrite(DEBUG_LED_WIFI,HIGH);
  } else {
    Serial.print("Join AP failure\r\n");
    digitalWrite(DEBUG_LED_WIFI,LOW);

  }

  if (wifi.disableMUX()) {
    Serial.print("single ok\r\n");
  } else {
    Serial.print("single err\r\n");
  }
}

void createTCP(){

  if (wifi.createTCP(SERVER_ADDR,SERVER_PORT)){
    Serial.print("TCP connection successfully created\n");
  }else{
    Serial.print("Error on creating TCP connection\n");
    delay(1000);
    return;
    /*
     * if wifi.getNowConnectAp().equals("No AP"){
     *  joinNetwork();
     * }
     */
  }

}

void releaseTCP(){
  if (wifi.releaseTCP()) {
        Serial.print("release tcp ok\r\n");
  } else {
        Serial.print("release tcp err\r\n");
  }
}
void setup() {
  wifi.restart();
  // put your setup code here, to run once
  Serial.begin(115200);
  Serial.print("Beginning setup...\n");

  if (wifi.setOprToStation()) {
    Serial.print("to station ok\r\n");
  } else {
    Serial.print("to station err\r\n");
  }

  pinMode(leftIR,INPUT);
  pinMode(frontIR,INPUT);
  pinMode(rightIR,INPUT);
  pinMode(ENA,OUTPUT);
  pinMode(ENB,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  pinMode(DEBUG_LED_WIFI,OUTPUT);

  joinNetwork();
}

void askAndExecute(char* data){
  uint8_t buffer[10] = {99};

  if (wifi.getIPStatus().equals("STATUS:5")){
    Serial.println("Network error, reconnecting");
    joinNetwork();
    createTCP();
  }

  createTCP();
  wifi.send((const uint8_t*)data,strlen(data));
  uint32_t len = wifi.recv(buffer,sizeof(buffer),10000);

  int command = atoi((char*)buffer);

  switch(command){
    case FORWARD:{
        Serial.println("Moving forward");
        moveForward();
        break;
    }
    case FORWARD_FAST:{
        Serial.println("Moving forward faaaaast");
        moveForwardFast();
        break;
    }
    case BACKWARD:{
        Serial.println("Moving backward");

        moveBackward();

        break;
    }
    case TURN_LEFT:{
        Serial.println("Turning left");

        turnLeft();

        break;
    }
    case TURN_LEFT_MICRO:{
        Serial.println("Turning left a bit");
        turnLeftMicro();
        break;
    }
    case TURN_RIGHT:{
        Serial.println("Turning right");
        turnRight();

        break;

    }
    case TURN_RIGHT_MICRO:{
        Serial.println("Turning right a bit");

        turnRightMicro();

        break;

    }
    case GRAB:{
      Serial.println("Lowering my arm");
      break;
    }
    case RELEASE:{
      Serial.println("Bringing my arm up");
      break;
    }

    case BACKWARD_LEFT:{
      Serial.println("Going back and turning left");
      moveBackward();
      turnLeft();
    }

    case BACKWARD_RIGHT:{
      Serial.println("Going back and turning right");
      moveBackward();
      turnRight();
    }

  }
  releaseTCP();
  return;
}

void loop() {
  uint8_t leftObstacle  = digitalRead(leftIR);
  uint8_t frontObstacle = digitalRead(frontIR);
  uint8_t rightObstacle = digitalRead(rightIR);

  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  root["leftObstacle"]  = leftObstacle;
  root["frontObstacle"] = frontObstacle;
  root["rightObstacle"] = rightObstacle;

  char msg[256];
  root.printTo(msg,sizeof(msg));
  askAndExecute(msg);

}
