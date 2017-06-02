#define FORWARD_SPEED       220
#define FORWARD_FAST_SPEED  255
#define FORWARD_TIME        600
#define BACKWARD_SPEED      150
#define BACKWARD_TIME       200
#define TURNING_SPEED       100
#define TURNING_TIME        300
#define TURNING_TIME_MICRO  150


void moveForward(float* movedAngle, float *movedSpace) {
  uint8_t speed = 0;

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  float angle = 0;
  unsigned long prev_time = t0;


  while (millis() - t0 < FORWARD_TIME) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    bool frontObstacle = digitalRead(frontIR) == 0;
    bool rightObstacle = digitalRead(rightIR) == 0;

    if (leftObstacle || frontObstacle || rightObstacle) {
      analogWrite(ENB, 0);
      analogWrite(ENA, 0);
    } else {
      speed += 80;
      analogWrite(ENB, constrain(speed, 0, FORWARD_SPEED));
      analogWrite(ENA, constrain(speed, 0, FORWARD_SPEED));
    }

    angle += getDeltaAngle(&prev_time, millis());


  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle = angle;
  *movedSpace = 0;
}

void moveForwardFast(float* movedAngle, float *movedSpace) {
  uint8_t speed = 0;

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  float angle = 0;
  unsigned long prev_time = t0;

  while (millis() - t0 < FORWARD_TIME) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    bool frontObstacle = digitalRead(frontIR) == 0;
    bool rightObstacle = digitalRead(rightIR) == 0;

    if (leftObstacle || frontObstacle || rightObstacle) {
      analogWrite(ENB, 0);
      analogWrite(ENA, 0);
    } else {
      speed += 2;
      analogWrite(ENB, constrain(speed, 0, FORWARD_FAST_SPEED));
      analogWrite(ENA, constrain(speed, 0, FORWARD_FAST_SPEED));
    }

    angle += getDeltaAngle(&prev_time, millis());

  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle =  angle;
  *movedSpace = 0;
}

void moveBackward(float* movedAngle, float *movedSpace) {
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  analogWrite(ENB, FORWARD_FAST_SPEED);
  analogWrite(ENA, FORWARD_FAST_SPEED);

  delay(BACKWARD_TIME);
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle = 0;
  *movedSpace = 0;
}

void turnLeft(float* movedAngle, float *movedSpace) {
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
      analogWrite(ENB, 0);
      analogWrite(ENA, 0);
    }
    angle += getDeltaAngle(&prev_time, millis());
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  *movedAngle =  angle;
  *movedSpace = 0;
}

void turnLeft(float* movedAngle, float *movedSpace, float targetAngle) {
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

  while (millis() - t0 < TURNING_TIME && abs(angle) < targetAngle) {
    bool leftObstacle  = digitalRead(leftIR) == 0;
    if (leftObstacle) {
      analogWrite(ENB, 0);
      analogWrite(ENA, 0);
    }
    angle += getDeltaAngle(&prev_time, millis());
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  *movedAngle =  angle;
  *movedSpace = 0;
}

void turnLeftMicro(float* movedAngle, float *movedSpace) {
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
      analogWrite(ENB, 0);
      analogWrite(ENA, 0);
    }
    angle += getDeltaAngle(&prev_time, millis());
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle =  angle;
  *movedSpace = 0;
}

void turnRight(float* movedAngle, float *movedSpace) {
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
      analogWrite(ENB, 0);
      analogWrite(ENA, 0);
    }
    angle += getDeltaAngle(&prev_time, millis());

  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle =  angle;
  *movedSpace = 0;
}

void turnRight(float* movedAngle, float *movedSpace, float targetAngle) {
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

  while (millis() - t0 < TURNING_TIME && abs(angle) < targetAngle) {
    bool rightObstacle  = digitalRead(rightIR) == 0;
    if (rightObstacle) {
      analogWrite(ENB, 0);
      analogWrite(ENA, 0);
    }
    angle += getDeltaAngle(&prev_time, millis());

  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
  *movedAngle =  angle;
  *movedSpace = 0;
}

void turnRightMicro(float* movedAngle, float *movedSpace) {

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
      analogWrite(ENB, 0);
      analogWrite(ENA, 0);
    }
    angle += getDeltaAngle(&prev_time, millis());

  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  *movedAngle =  angle;
  *movedSpace = 0;
}

float getDeltaAngle(unsigned long *prev_time, unsigned long curr_time) {
  imu.update(UPDATE_GYRO);
  float sample = imu.calcGyro(imu.gz);
  float delta_time = curr_time - *prev_time;
  *prev_time = curr_time;
  return sample * (delta_time / 1000.0);
}
