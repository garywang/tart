#include <Servo.h>
#include <CompactQik2s9v1.h>
#include <NewSoftSerial.h>

#define rxPin 19
#define txPin 18
#define rstPin 5
#define servoChar 'S'
#define analogChar 'A'
#define motorChar 'M'
#define digitalChar 'D'
#define commandLen 6

Servo servo;
NewSoftSerial mySerial = NewSoftSerial(rxPin, txPin);
CompactQik2s9v1 motor = CompactQik2s9v1(&mySerial, rstPin);

void setup()                    
{
  Serial.begin(9600);           // set up Serial library at 9600 bps
  delay(1000); //Wait for it to initialize
  Serial.flush();
  
  mySerial.begin(9600);
  motor.begin();
  motor.stopBothMotors();
  
}

void loop()                      
{
  //char command[commandLen-1];
  
  if (Serial.available()>0){
    delay(10);
    
    //Get the mode
    char mode = Serial.read();
  
    switch (mode){
      
      //If it's a servo command: 
      //S[port][angle]
      case servoChar:
        moveServo();
        break;
    
      //If it's an analog data request:
      //A[port]
      case analogChar:
        getAnalog();
        break;
    
      //If it's a motor command:
      //M[motor number][val]
      case motorChar:
        moveMotor();
        break;
    
      //If it's a digital data request:
      //D[port]
      case digitalChar:
        getDigital();
        break;
    }
  }
  
}

//----------
void moveServo(){
  int port = getData(2);
  int angle = getData(3);
  servo.attach(port);
  servo.write(angle);
  Serial.println("000000");
  delay(10);
}
//----------------
void moveMotor(){      
  int num = getData(1);
  int val = getData(3);
      
  if (num==0){
    if (val > 200) {
      motor.motor0Reverse(val-200);
    }
    else {
      motor.motor0Forward(val);
    }
  }
  else if (num==1){
    if (val > 200) {
      motor.motor1Reverse(val-200);
    }
    else {
      motor.motor1Forward(val);
    }
  }
  Serial.println(000010);
  delay(10);
}
//---------------
void getAnalog(){
  int port = getData(2);
  int analogData = analogRead(port);
  Serial.println(analogData);
  delay(10);
}
//---------------
void getDigital(){
  int port = getData(2);
  int digitalData = digitalRead(port);
  Serial.println(digitalData);
  delay(10);
}
//----------------
int getData(int len)
//Collects data of the appropriate length and turns it into an integer
{
  char buffer[len+1];
  int received = 0, returnInt;
  
  for (int i = 0; i<len; i++)
  {
    buffer[received++] = Serial.read();
    buffer[received] = '\0';
    if (received >= (sizeof(buffer)-1))
    {
      returnInt = atoi(buffer);
      received = 0;
    }
  }
  
  return returnInt;
}
