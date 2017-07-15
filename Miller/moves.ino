#define FORWARD_SPEED       180
#define FORWARD_FAST_SPEED  240
#define FORWARD_TIME        500
#define BACKWARD_SPEED      150
#define BACKWARD_TIME       200
#define TURNING_SPEED       210
#define TURNING_TIME        250
#define TURNING_TIME_MICRO  150
#define ACCEL_X_BIAS        -0.05
#define ACCEL_Y_BIAS        -0.01

float xOffset = -27.0;
float yOffset = 4.0;
bool down = false;  

void arm_grab(){
  Serial.println("grabbing");
  if (!down){
    for (int i=180; i>=90; i-=5){
      myservo.write(i);
      delay(100);
    }
    down = true;
  }
}

void arm_release(){
  Serial.println("releasing");
  if (down){
    for (int i=90; i<=180; i+=5){
      myservo.write(i);
      delay(100);
    }
    down = false;
  }
}

float getCompassDegrees() {
  imu.update(UPDATE_ACCEL | UPDATE_GYRO | UPDATE_COMPASS);
  float magX = imu.calcMag(imu.mx) - xOffset; // magX is x-axis magnetic field in uT
  float magY = imu.calcMag(imu.my) - yOffset; // magY is y-axis magnetic field in uT

  float heading = atan2(magY, magX);
  float declinationAngle = (2.0 + (53.0 / 60.0)) / (180 / M_PI);
  heading += declinationAngle;

  if (heading < 0)
    heading += 2 * PI;

  if (heading > 2 * PI)
    heading -= 2 * PI;

  return heading * 180 / M_PI;
}

void moveForward() {
  Serial.println("Forward");

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  analogWrite(ENB, FORWARD_SPEED+15);
  analogWrite(ENA, FORWARD_SPEED);

  while (millis() - t0 < FORWARD_TIME) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    bool frontObstacle = digitalRead(frontIR) == 0;
    bool rightObstacle = digitalRead(rightIR) == 0;
    if (leftObstacle || frontObstacle || rightObstacle){
      break;
    }
  }

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

}

void moveForwardFast() {
  uint8_t speed = 0;

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);
  unsigned long t0 = millis();
  analogWrite(ENB, FORWARD_FAST_SPEED+15);
  analogWrite(ENA, FORWARD_FAST_SPEED);
  while (millis() - t0 < FORWARD_TIME) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    bool frontObstacle = digitalRead(frontIR) == 0;
    bool rightObstacle = digitalRead(rightIR) == 0;

    if (leftObstacle || frontObstacle || rightObstacle) {
      break;
    }
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

void moveBackward() {
  Serial.println("Backward");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  unsigned long t0 = millis();
  analogWrite(ENB, BACKWARD_SPEED);
  analogWrite(ENA, BACKWARD_SPEED);

  while (millis() - t0 < BACKWARD_TIME) {
    //pass
  }

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

void turnLeft() {
  Serial.println("Left");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  unsigned long t0 = millis();
  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (millis() - t0 < TURNING_TIME) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    if (leftObstacle) {
      break;
    }
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

void turnLeft(float targetAngle) {
  Serial.println("Left");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);
  float start_angle = getCompassDegrees();

  unsigned long t0 = millis();
  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (abs(getCompassDegrees() - start_angle) < targetAngle) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    if (leftObstacle) {
      break;
    }
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

}

void turnLeftMicro() {
  Serial.println("Left Micro");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  unsigned long t0 = millis();
  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (millis() - t0 < TURNING_TIME_MICRO) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    if (leftObstacle) {
      break;
    }
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

}

void turnRight() {
  Serial.println("Right");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (millis() - t0 < TURNING_TIME) {
    bool rightObstacle  = digitalRead(rightIR) == 0;
    if (rightObstacle) {
      break;
    }

  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

}

void turnRight(float targetAngle) {
  Serial.println("Right");
  targetAngle = -targetAngle;
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  float start_angle = getCompassDegrees();

  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (abs(getCompassDegrees() - start_angle)<targetAngle) {
    bool rightObstacle  = digitalRead(rightIR) == 0;
    if (rightObstacle) {
      break;
    }

  }

  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

}

void turnRightMicro() {
  Serial.println("Right micro");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (millis() - t0 < TURNING_TIME_MICRO) {
    bool rightObstacle  = digitalRead(rightIR) == 0;
    if (rightObstacle) {
      break;
    }

  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);


}

void grab(){
  
}
float getDeltaAngle(unsigned long *prev_time, unsigned long curr_time) {
  imu.update(UPDATE_GYRO);
  long delta_time = curr_time - *prev_time;
  *prev_time = curr_time;
  return imu.calcGyro(imu.gz) * (delta_time / 1000.0);
}

void getDeltaSpace(unsigned long* prev_time, unsigned long curr_time, float *deltaSpeedX, float *deltaSpeedY) {
  //imu.update(UPDATE_GYRO | UPDATE_ACCEL);
  imu.update(UPDATE_ACCEL);
  float sampleY = (imu.calcAccel(imu.ay) - ACCEL_Y_BIAS) * 9.81;
  float sampleX = (imu.calcAccel(imu.ax) - ACCEL_X_BIAS) * 9.81;
  float delta_time = (curr_time - *prev_time) / 1000.0;
  *prev_time = curr_time;
  *deltaSpeedX = sampleX * delta_time;
  *deltaSpeedY = sampleY * delta_time;
}

void switchIRs(){
  if (leftIR != C_leftIR){
    leftIR = C_leftIR;
    frontIR = C_frontIR;
    rightIR = C_rightIR;
    return;
  }
  
  leftIR = C_armLeft;
  frontIR = C_armFront;
  rightIR = C_armRight;
  
}

