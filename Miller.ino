#include <ArduinoJson.h>

#include <doxygen.h>
#include <ESP8266.h>

#define SSID            "Leon Wireless"
#define PASSWORD        "cipollamarrone123"
#define SERVER_ADDR     "192.168.1.83"
#define SERVER_PORT     (1934)

#define FORWARD             0
#define FORWARD_FAST        1
#define BACKWARD            2
#define TURN_LEFT           3
#define TURN_LEFT_MICRO     4
#define TURN_RIGHT          5
#define TURN_RIGHT_MICRO    6
#define GRAB                10
#define RELEASE             11

#define ENA               2
#define IN1               3
#define IN2               4
#define IN3               5
#define IN4               6
#define ENB               7

#define leftIR            A0
#define frontIR           A1
#define rightIR           A2

ESP8266 wifi(Serial1,115200);


void setup() {
  // put your setup code here, to run once
  Serial.begin(115200);
  Serial.print("Beginning setup...\n");

  if (wifi.setOprToStationSoftAP()) {
    Serial.print("to station + softap ok\r\n");
  } else {
    Serial.print("to station + softap err\r\n");
  }

  if (wifi.joinAP(SSID, PASSWORD)) {
    Serial.print("Join AP success\r\n");
    Serial.print("IP:");
    Serial.println( wifi.getLocalIP().c_str());
  } else {
    Serial.print("Join AP failure\r\n");
  }

  if (wifi.disableMUX()) {
    Serial.print("single ok\r\n");
  } else {
    Serial.print("single err\r\n");
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
}

void askAndExecute(char* data){
  uint8_t buffer[10] = {0};

  //establishing connection
  if (wifi.createTCP(SERVER_ADDR,SERVER_PORT)){
    Serial.print("TCP connection successfully created\n");
  }else{
    //Serial.print("Error on creating TCP connection\n");
    return;
  }

  //connection established

  
  wifi.send((const uint8_t*)data,strlen(data));

  uint32_t len = wifi.recv(buffer,sizeof(buffer),10000);
  Serial.print("Received:");
  Serial.println((char*)buffer);
  int command = atoi((char*)buffer);

  switch(command){
    case FORWARD:{
      Serial.println("Moving forward");
      break;
    }
    case FORWARD_FAST:{
      Serial.println("Moving forward faaaaast");
      break;
    }
    case BACKWARD:{
      Serial.println("Moving backward");
      break;
    }
    case TURN_LEFT:{
      Serial.println("Turning left");
      break;
    }
    case TURN_LEFT_MICRO:{
      Serial.println("Turning left a bit");
      break;
    }
    case TURN_RIGHT:{
      Serial.println("Turning right");
      break;
    }
    case TURN_RIGHT_MICRO:{
      Serial.println("Turning right a bit");
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
  }
  
  if (wifi.releaseTCP()) {
        Serial.print("release tcp ok\r\n");
  } else {
        Serial.print("release tcp err\r\n");
  }
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
