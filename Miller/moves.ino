#define FORWARD_SPEED       100
#define FORWARD_FAST_SPEED  255
#define FORWARD_TIME        300
#define BACKWARD_SPEED      80
#define BACKWARD_TIME       200
#define TURNING_SPEED       100
#define TURNING_TIME        200
#define TURNING_TIME_MICRO  100


void moveForward(){

  analogWrite(ENB,0);
  analogWrite(ENA,0);

  digitalWrite(IN3,0);
  digitalWrite(IN4,1);
  digitalWrite(IN1,1);
  digitalWrite(IN2,0);

  long t0 = millis();

  analogWrite(ENB,FORWARD_SPEED);
  analogWrite(ENA,FORWARD_SPEED);

  while (millis()-t0<FORWARD_TIME){
    bool leftObstacle  = digitalRead(leftIR)==0;
    bool frontObstacle = digitalRead(frontIR)==0;
    bool rightObstacle = digitalRead(rightIR)==0;
    if (leftObstacle || frontObstacle || rightObstacle){
        analogWrite(ENB,0);
        analogWrite(ENA,0);
    }
  }
  analogWrite(ENB,0);
  analogWrite(ENA,0);
}

void moveForwardFast(){
  analogWrite(ENB,0);
  analogWrite(ENA,0);

  digitalWrite(IN3,0);
  digitalWrite(IN4,1);
  digitalWrite(IN1,1);
  digitalWrite(IN2,0);

  long t0 = millis();

  analogWrite(ENB,FORWARD_FAST_SPEED);
  analogWrite(ENA,FORWARD_FAST_SPEED);

  while (millis()-t0<FORWARD_TIME){
    bool leftObstacle  = digitalRead(leftIR)==0;
    bool frontObstacle = digitalRead(frontIR)==0;
    bool rightObstacle = digitalRead(rightIR)==0;
    if (leftObstacle || frontObstacle || rightObstacle){
        analogWrite(ENB,0);
        analogWrite(ENA,0);
    }
  }
  analogWrite(ENB,0);
  analogWrite(ENA,0);
}

void moveBackward(){
  analogWrite(ENB,0);
  analogWrite(ENA,0);

  digitalWrite(IN3,1);
  digitalWrite(IN4,0);
  digitalWrite(IN1,0);
  digitalWrite(IN2,1);

  analogWrite(ENB,FORWARD_FAST_SPEED);
  analogWrite(ENA,FORWARD_FAST_SPEED);

  delay(BACKWARD_TIME);
  analogWrite(ENB,0);
  analogWrite(ENA,0);
}

void turnLeft(){
  analogWrite(ENB,0);
  analogWrite(ENA,0);

  digitalWrite(IN3,1);
  digitalWrite(IN4,0);
  digitalWrite(IN1,1);
  digitalWrite(IN2,0);

  long t0 = millis();

  analogWrite(ENB,TURNING_SPEED);
  analogWrite(ENA,TURNING_SPEED);

  while (millis()-t0<TURNING_TIME){
    bool leftObstacle  = digitalRead(leftIR)==0;
    if (leftObstacle){
        analogWrite(ENB,0);
        analogWrite(ENA,0);
    }
  }
  analogWrite(ENB,0);
  analogWrite(ENA,0);
}

void turnLeftMicro(){
  analogWrite(ENB,0);
  analogWrite(ENA,0);

  digitalWrite(IN3,1);
  digitalWrite(IN4,0);
  digitalWrite(IN1,1);
  digitalWrite(IN2,0);

  long t0 = millis();

  analogWrite(ENB,TURNING_SPEED);
  analogWrite(ENA,TURNING_SPEED);

  while (millis()-t0<TURNING_TIME_MICRO){
    bool leftObstacle  = digitalRead(leftIR)==0;
    if (leftObstacle){
        analogWrite(ENB,0);
        analogWrite(ENA,0);
    }
  }
  analogWrite(ENB,0);
  analogWrite(ENA,0);
}

void turnRight(){
  analogWrite(ENB,0);
  analogWrite(ENA,0);

  digitalWrite(IN3,0);
  digitalWrite(IN4,1);
  digitalWrite(IN1,0);
  digitalWrite(IN2,1);

  long t0 = millis();
  
  analogWrite(ENB,TURNING_SPEED);
  analogWrite(ENA,TURNING_SPEED);

  while (millis()-t0<TURNING_TIME){
    bool rightObstacle  = digitalRead(rightIR)==0;
    if (rightObstacle){
        analogWrite(ENB,0);
        analogWrite(ENA,0);
    }
  }
  analogWrite(ENB,0);
  analogWrite(ENA,0);
}

void turnRightMicro(){
  analogWrite(ENB,0);
  analogWrite(ENA,0);

  digitalWrite(IN3,0);
  digitalWrite(IN4,1);
  digitalWrite(IN1,0);
  digitalWrite(IN2,1);

  long t0 = millis();

  analogWrite(ENB,TURNING_SPEED);
  analogWrite(ENA,TURNING_SPEED);

  while (millis()-t0<TURNING_TIME_MICRO){
    bool rightObstacle  = digitalRead(rightIR)==0;
    if (rightObstacle){
        analogWrite(ENB,0);
        analogWrite(ENA,0);
    }
  }
  analogWrite(ENB,0);
  analogWrite(ENA,0);
}
