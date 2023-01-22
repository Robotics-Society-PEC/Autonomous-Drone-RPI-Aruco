#include <Wire.h> 
#define trigpin 2
#define echopin 3

int distance = 0;
int min_trigger = 100;
unsigned long current_millis = 0;
unsigned long previous_millis = 0;
bool previous_state = 0;
unsigned long timeout = 16000;
//byte arr[2] = {0,0};

void setup() 
{ 
  Wire.begin(32);                // join i2c bus with address #32
  Wire.onRequest(requestEvent); // register event 
  //Serial.begin(9600);           // start serial for output 
  pinMode(trigpin , OUTPUT);
  pinMode(echopin , INPUT);
  digitalWrite(trigpin,LOW);
  Serial.begin(9600);
} 

void loop() {
  if(previous_state == 0 && (millis() - previous_millis) > min_trigger){
    digitalWrite(trigpin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigpin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigpin, LOW);
  }

  if(previous_state == 0 && digitalRead(echopin)){
    previous_state = 1;
    current_millis = micros();
  }

//  if( previous_state == 1 && digitalRead(echopin) && (micros() - current_millis >timeout) )
  if( previous_state == 1  && (micros() - current_millis >timeout) )
  {
    previous_state = 0;
    previous_millis = micros();
    //Serial.print("distance errorrrrrrrrrrrrrr: ");
    //Serial.println(distance);
    distance = 255;
  }
  if(previous_state == 1 && !digitalRead(echopin)){
    previous_state = 0;
    previous_millis = current_millis;
    current_millis = micros();
    distance = (current_millis - previous_millis) * 0.033 / 2;
    distance = constrain(distance , 0 , 255);
    //Serial.print("distance : ");
    //Serial.println(distance);
  }
  //Serial.println(distance);
} 

// function that executes whenever data is received from master 
// this function is registered as an event, see setup() 
void requestEvent() 
{
  Wire.write(byte(distance));
}
