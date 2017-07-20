#define FORWARD_SPEED 190
#define FORWARD_FAST_SPEED 220
#define FORWARD_TIME 800
#define BACKWARD_SPEED 190
#define BACKWARD_TIME 250
#define TURNING_SPEED 230
#define TURNING_TIME 230
#define TURNING_TIME_MICRO 100
#define ACCEL_X_BIAS -0.05
#define ACCEL_Y_BIAS -0.01
#define A_BALANCE +30
#define B_BALANCE -23

float xOffset = -27.0;
float yOffset = 4.0;
bool down = false;

void arm_grab()
{
  Serial.println("grabbing");
  if (!down)
  {
    for (int i = 180; i >= 90; i -= 5)
    {
      myservo.write(i);
      delay(100);
    }
    down = true;
  }
}

void arm_release()
{
  Serial.println("releasing");
  if (down)
  {
    for (int i = 90; i <= 180; i += 5)
    {
      myservo.write(i);
      delay(100);
    }
    down = false;
  }
}

float getCompassDegrees()
{
  imu.update(UPDATE_COMPASS);
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

void moveForward()
{
  Serial.println("Forward");

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  analogWrite(ENB, constrain(FORWARD_SPEED + B_BALANCE,0,255));
  analogWrite(ENA, constrain(FORWARD_SPEED + A_BALANCE,0,255));

  while (millis() - t0 < FORWARD_TIME)
  {
    bool leftObstacle = digitalRead(LEFT_IR) == 0;
    bool frontObstacle = digitalRead(FRONT_IR) == 0;
    bool rightObstacle = digitalRead(RIGHT_IR) == 0;
    bool leftArmObstacle = digitalRead(ARMLEFT_IR) == 0;
    bool rightArmObstacle = digitalRead(ARMRIGHT_IR) == 0;
    if (leftObstacle || frontObstacle || rightObstacle || ((rightArmObstacle || leftArmObstacle) && down))
    {
      break;
    }
  }

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

void moveForwardFast()
{
  uint8_t speed = 0;

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);
  unsigned long t0 = millis();
  analogWrite(ENB, constrain(FORWARD_FAST_SPEED + B_BALANCE,0,255));
  analogWrite(ENA, constrain(FORWARD_FAST_SPEED + A_BALANCE,0,255));
  while (millis() - t0 < FORWARD_TIME)
  {
    bool leftObstacle = digitalRead(LEFT_IR) == 0;
    bool frontObstacle = digitalRead(FRONT_IR) == 0;
    bool rightObstacle = digitalRead(RIGHT_IR) == 0;
    bool leftArmObstacle = digitalRead(ARMLEFT_IR) == 0;
    bool rightArmObstacle = digitalRead(ARMRIGHT_IR) == 0;
    if (leftObstacle || frontObstacle || rightObstacle || ((rightArmObstacle || leftArmObstacle) && down))
    {
      break;
    }
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

void moveBackward()
{
  Serial.println("Backward");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  unsigned long t0 = millis();
  analogWrite(ENB, constrain(BACKWARD_SPEED + B_BALANCE,0,255));
  analogWrite(ENA, constrain(BACKWARD_SPEED + A_BALANCE,0,255));

  while (millis() - t0 < BACKWARD_TIME)
  {
    //pass
  }

  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

void turnLeft()
{
  Serial.println("Left");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  unsigned long t0 = millis();
  analogWrite(ENB, constrain(TURNING_SPEED + B_BALANCE,0,255));
  analogWrite(ENA, constrain(TURNING_SPEED + A_BALANCE,0,255));

  while (millis() - t0 < TURNING_TIME)
  {
    bool leftObstacle = digitalRead(LEFT_IR) == 0;
    bool leftArmObstacle = digitalRead(ARMLEFT_IR) == 0;
    if (leftObstacle || (leftArmObstacle && down))
    {
      break;
    }
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

void turnLeft(float targetAngle)
{
  Serial.println("Left");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);
  float start_angle = getCompassDegrees();

  unsigned long t0 = millis();
  analogWrite(ENB, constrain(TURNING_SPEED + B_BALANCE,0,255));
  analogWrite(ENA, constrain(TURNING_SPEED + A_BALANCE,0,255));

  while (abs(getCompassDegrees() - start_angle) < targetAngle)
  {
    bool leftObstacle = digitalRead(LEFT_IR) == 0;
    bool leftArmObstacle = digitalRead(ARMLEFT_IR) == 0;
    if (leftObstacle || (leftArmObstacle && down))
    {
      break;
    }
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

void turnLeftMicro()
{
  Serial.println("Left Micro");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 0);
  digitalWrite(IN4, 1);
  digitalWrite(IN1, 0);
  digitalWrite(IN2, 1);

  unsigned long t0 = millis();
  analogWrite(ENB, constrain(TURNING_SPEED + B_BALANCE,0,255));
  analogWrite(ENA, constrain(TURNING_SPEED + A_BALANCE,0,255));

  while (millis() - t0 < TURNING_TIME_MICRO)
  {
    bool leftObstacle = digitalRead(LEFT_IR) == 0;
    bool leftArmObstacle = digitalRead(ARMLEFT_IR) == 0;
    if (leftObstacle || (leftArmObstacle && down))
    {
      break;
    }
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

void turnRight()
{
  Serial.println("Right");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  analogWrite(ENB, constrain(TURNING_SPEED + B_BALANCE,0,255));
  analogWrite(ENA, constrain(TURNING_SPEED + A_BALANCE,0,255));

  while (millis() - t0 < TURNING_TIME)
  {
    bool rightObstacle = digitalRead(RIGHT_IR) == 0;
    bool rightArmObstacle = digitalRead(ARMRIGHT_IR) == 0;
    if (rightObstacle || (rightArmObstacle && down))
    {
      break;
    }
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

void turnRight(float targetAngle)
{
  Serial.println("Right");
  targetAngle = -targetAngle;
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  float start_angle = getCompassDegrees();

  analogWrite(ENB, constrain(TURNING_SPEED + B_BALANCE,0,255));
  analogWrite(ENA, constrain(TURNING_SPEED + A_BALANCE,0,255));

  while (abs(getCompassDegrees() - start_angle) < targetAngle)
  {
    bool rightObstacle = digitalRead(RIGHT_IR) == 0;
    bool rightArmObstacle = digitalRead(ARMRIGHT_IR) == 0;
    if (rightObstacle || (rightArmObstacle && down))
    {
      break;
    }
  }

  analogWrite(ENB, constrain(TURNING_SPEED + B_BALANCE,0,255));
  analogWrite(ENA, constrain(TURNING_SPEED + A_BALANCE,0,255));
}

void turnRightMicro()
{
  Serial.println("Right micro");
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);

  digitalWrite(IN3, 1);
  digitalWrite(IN4, 0);
  digitalWrite(IN1, 1);
  digitalWrite(IN2, 0);

  unsigned long t0 = millis();
  analogWrite(ENB, constrain(TURNING_SPEED + B_BALANCE,0,255));
  analogWrite(ENA, constrain(TURNING_SPEED + A_BALANCE,0,255));

  while (millis() - t0 < TURNING_TIME_MICRO)
  {
    bool rightObstacle = digitalRead(RIGHT_IR) == 0;
    bool rightArmObstacle = digitalRead(ARMRIGHT_IR) == 0;
    if (rightObstacle || (rightArmObstacle && down))
    {
      break;
    }
  }
  analogWrite(ENB, 0);
  analogWrite(ENA, 0);
}

float getDeltaAngle(unsigned long *prev_time, unsigned long curr_time)
{
  imu.update(UPDATE_GYRO);
  long delta_time = curr_time - *prev_time;
  *prev_time = curr_time;
  return imu.calcGyro(imu.gz) * (delta_time / 1000.0);
}

void getDeltaSpace(unsigned long *prev_time, unsigned long curr_time, float *deltaSpeedX, float *deltaSpeedY)
{
  //imu.update(UPDATE_GYRO | UPDATE_ACCEL);
  imu.update(UPDATE_ACCEL);
  float sampleY = (imu.calcAccel(imu.ay) - ACCEL_Y_BIAS) * 9.81;
  float sampleX = (imu.calcAccel(imu.ax) - ACCEL_X_BIAS) * 9.81;
  float delta_time = (curr_time - *prev_time) / 1000.0;
  *prev_time = curr_time;
  *deltaSpeedX = sampleX * delta_time;
  *deltaSpeedY = sampleY * delta_time;
}

void switchIRs()
{
  if (FRONT_IR == C_FRONT_IR)
  {
    FRONT_IR = ARMFRONT_IR;
  }
  else
  {
    FRONT_IR = C_FRONT_IR;
  }
}
