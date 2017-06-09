#define FORWARD_SPEED       190
#define FORWARD_FAST_SPEED  255
#define FORWARD_TIME        500
#define BACKWARD_SPEED      150
#define BACKWARD_TIME       200
#define TURNING_SPEED       140
#define TURNING_TIME        300
#define TURNING_TIME_MICRO  150
#define ACCEL_X_BIAS        -0.06
#define ACCEL_Y_BIAS        -0.01

void moveForward(float* movedAngle, float *movedSpaceX, float *movedSpaceY) {
  uint8_t speed = 0;

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  float angle = 0;
  float speedX = 0;
  float speedY = 0;
  float deltaSpeedX, deltaSpeedY, deltaAngle;
  unsigned long prev_time = t0;


  while (millis() - t0 < FORWARD_TIME) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    bool frontObstacle = digitalRead(frontIR) == 0;
    bool rightObstacle = digitalRead(rightIR) == 0;

    if (leftObstacle || frontObstacle || rightObstacle) {
      analogWrite(ENB, 0);
      analogWrite(ENA, 0);
      *movedSpaceX = 0.5 * speedX * (FORWARD_TIME - (millis() - prev_time)) / 1000.0;
      *movedSpaceY = 0.5 * speedY * (FORWARD_TIME - (millis() - prev_time)) / 1000.0;
      return;
    } else {
      analogWrite(ENB, FORWARD_SPEED);
      analogWrite(ENA, FORWARD_SPEED);
    }
    getDeltaAll(&prev_time, millis(), &deltaAngle, &deltaSpeedX, &deltaSpeedY);
    speedX += deltaSpeedX;
    speedY += deltaSpeedY;


  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle = angle;
  *movedSpaceX = 0.5 * speedX * FORWARD_TIME / 1000.0;
  *movedSpaceY = 0.5 * speedY * FORWARD_TIME / 1000.0;
}

void moveForwardFast(float* movedAngle, float *movedSpaceX, float *movedSpaceY) {
  uint8_t speed = 0;

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  float angle = 0;
  float speedX = 0;
  float speedY = 0;
  float deltaSpeedX, deltaSpeedY, deltaAngle;
  unsigned long prev_time = t0;


  while (millis() - t0 < FORWARD_TIME) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    bool frontObstacle = digitalRead(frontIR) == 0;
    bool rightObstacle = digitalRead(rightIR) == 0;

    if (leftObstacle || frontObstacle || rightObstacle) {
      break;
    } else {
      speed += 80;
      analogWrite(ENB, constrain(speed, 0, FORWARD_FAST_SPEED));
      analogWrite(ENA, constrain(speed, 0, FORWARD_FAST_SPEED));
    }
    getDeltaAll(&prev_time, millis(), &deltaAngle, &deltaSpeedX, &deltaSpeedY);
    angle += deltaAngle;
    speedX += deltaSpeedX;
    speedY += deltaSpeedY;


  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle = angle;
  *movedSpaceX = 0.5 * speedX * FORWARD_TIME / 1000.0;
  *movedSpaceY = 0.5 * speedY * FORWARD_TIME / 1000.0;
}

void moveBackward(float* movedAngle, float *movedSpaceX, float *movedSpaceY) {
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  unsigned long t0 = millis();
  float angle = 0;
  float speedX = 0;
  float speedY = 0;
  float deltaSpeedX, deltaSpeedY, deltaAngle;
  unsigned long prev_time = t0;

  analogWrite(ENB, BACKWARD_SPEED);
  analogWrite(ENA, BACKWARD_SPEED);

  while (millis() - t0 < BACKWARD_TIME) {
    getDeltaAll(&prev_time, millis(), &deltaAngle, &deltaSpeedX, &deltaSpeedY);
    angle += deltaAngle;
    speedX += deltaSpeedX;
    speedY += deltaSpeedY;
  }

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle = angle;
  *movedSpaceX = 0.5 * speedX * FORWARD_TIME / 1000.0;
  *movedSpaceY = 0.5 * speedY * FORWARD_TIME / 1000.0;

}

void turnLeft(float* movedAngle) {
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  unsigned long t0 = millis();
  unsigned long prev_time = t0;
  float angle = 0;

  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (millis() - t0 < TURNING_TIME) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    if (leftObstacle) {
      break;
    }
    angle += getDeltaAngle(&prev_time, millis());
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  *movedAngle =  angle;

}

void turnLeft(float* movedAngle, float targetAngle) {
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  unsigned long t0 = millis();
  unsigned long prev_time = t0;
  float angle = 0;

  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (angle < targetAngle) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    if (leftObstacle) {
      break;
    }
    angle += getDeltaAngle(&prev_time, millis());
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  *movedAngle =  angle;

}

void turnLeftMicro(float* movedAngle) {
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  unsigned long t0 = millis();
  unsigned long prev_time = t0;
  float angle = 0;

  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (millis() - t0 < TURNING_TIME_MICRO) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    if (leftObstacle) {
      break;
    }
    angle += getDeltaAngle(&prev_time, millis());
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle =  angle;

}

void turnRight(float* movedAngle) {
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  unsigned long prev_time = t0;
  float angle = 0;

  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (millis() - t0 < TURNING_TIME) {
    bool rightObstacle  = digitalRead(rightIR) == 0;
    if (rightObstacle) {
      break;
    }
    angle += getDeltaAngle(&prev_time, millis());

  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle =  angle;

}

void turnRight(float* movedAngle, float targetAngle) {
  targetAngle = -targetAngle;
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  unsigned long prev_time = t0;
  float angle = 0;

  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (1) {
    bool rightObstacle  = digitalRead(rightIR) == 0;
    if (rightObstacle) {
      break;
    }
    angle += getDeltaAngle(&prev_time, millis());
    if (angle < targetAngle) {
      analogWrite(ENA, 0);
      analogWrite(ENB, 0);
      break;
    }
  }

  *movedAngle =  angle;

}

void turnRightMicro(float* movedAngle) {

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);
  unsigned long t0 = millis();
  unsigned long prev_time = t0;
  float angle = 0;

  analogWrite(ENB, TURNING_SPEED);
  analogWrite(ENA, TURNING_SPEED);

  while (millis() - t0 < TURNING_TIME_MICRO) {
    bool rightObstacle  = digitalRead(rightIR) == 0;
    if (rightObstacle) {
      break;
    }
    angle += getDeltaAngle(&prev_time, millis());

  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  *movedAngle =  angle;

}

float getDeltaAngle(unsigned long *prev_time, unsigned long curr_time) {
  imu.update(UPDATE_GYRO);
  *prev_time = curr_time;
  return imu.calcGyro(imu.gz) * ((curr_time - *prev_time) / 1000.0);
}

void getDeltaAll(unsigned long* prev_time, unsigned long curr_time, float *deltaAngle, float *deltaSpeedX, float *deltaSpeedY) {
  //imu.update(UPDATE_GYRO | UPDATE_ACCEL);
  imu.update(UPDATE_ACCEL);
  float sampleY = (imu.calcAccel(imu.ay) - ACCEL_Y_BIAS) * 9.81;
  float sampleX = (imu.calcAccel(imu.ax) - ACCEL_X_BIAS) * 9.81;
  //float sampleAngle = imu.calcGyro(imu.gz);
  float delta_time = (curr_time - *prev_time) / 1000.0;
  *prev_time = curr_time;
  *deltaAngle = 0; //sampleAngle * delta_time;
  *deltaSpeedX = sampleX * delta_time;
  *deltaSpeedY = sampleY * delta_time;
}

