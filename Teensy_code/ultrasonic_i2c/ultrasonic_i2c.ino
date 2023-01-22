#include <Wire.h>
#define trigpin 2
#define echopin1 3
#define echopin2 6

#define freq 60

int distance = 0;
int distance2 = 0;
int min_trigger = (1000000 / freq); // micros // 100hz
unsigned long current_millis = 0;
unsigned long current_millis2 = 0;
unsigned long previous_millis = 0;
unsigned long previous_millis2 = 0;
bool previous_state = 0;
bool previous_state2 = 0;
unsigned long timeout = 16000;
// byte arr[2] = {0,0};

void setup()
{
  Wire.begin(32);               // join i2c bus with address #32
  Wire.onRequest(requestEvent); // register event
  // Serial.begin(9600);           // start serial for output
  pinMode(trigpin, OUTPUT);
  pinMode(echopin1, INPUT);
  pinMode(echopin2, INPUT);
  digitalWrite(trigpin, LOW);
  Serial.begin(9600);
}

void loop()
{
  if (previous_state == 0 && previous_state2 == 0 && (micros() - previous_millis) > min_trigger && (micros() - previous_millis2) > min_trigger)
  {
    digitalWrite(trigpin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigpin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigpin, LOW);
    previous_millis = micros();
    previous_millis2 = micros();
  }

  if (previous_state2 == 0 && digitalRead(echopin2))
  {
    previous_state2 = 1;
    current_millis2 = micros();
  }
  else if (previous_state2 == 1 && (micros() - current_millis2 > timeout))
  {
    previous_state2 = 0;
    previous_millis2 = micros();
    // Serial.print("distance2 Exceded: ");
    // Serial.println(distance2);
    distance2 = 255;
  }
  else if (previous_state2 == 1 && !digitalRead(echopin2))
  {
    previous_state2 = 0;
    previous_millis2 = current_millis2;
    current_millis2 = micros();
    distance2 = (current_millis2 - previous_millis2) * 0.033 / 2;
    distance2 = constrain(distance2, 0, 255);
    // Serial.print("distance2 : ");
    // Serial.println(distance2);
  }

  if (previous_state == 0 && digitalRead(echopin1))
  {
    previous_state = 1;
    current_millis = micros();
  }
  else if (previous_state == 1 && (micros() - current_millis > timeout))
  {
    previous_state = 0;
    previous_millis = micros();
    // Serial.print("distance Exceded: ");
    // Serial.println(distance);
    distance = 255;
  }
  else if (previous_state == 1 && !digitalRead(echopin1))
  {
    previous_state = 0;
    previous_millis = current_millis;
    current_millis = micros();
    distance = (current_millis - previous_millis) * 0.033 / 2;
    distance = constrain(distance, 0, 255);
    // Serial.print("distance : ");
    // Serial.println(distance);
  }
  // Serial.println(distance);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void requestEvent()
{
  if (distance > 240 && distance2 > 240)
    Wire.write(byte(255));
  else if (distance > 240)
    Wire.write(byte(distance2));
  else if (distance2 > 240)
    Wire.write(byte(distance));
  else
    Wire.write(byte((distance + distance2) / 2));
}
