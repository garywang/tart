#include <Servo.h>
#include <CompactQik2s9v1.h>
#include <NewSoftSerial.h>

#define rxPin 19
#define txPin 18
#define rstPin 5
#define servoChar 'S'
#define analogChar 'A'
#define motorForwardChar 'M'
#define motorReverseChar 'R'
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
      case motorForwardChar:
        moveMotor(1);
        break;
      
      case motorReverseChar:
        moveMotor(-1);
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
  Serial.println("");
}
//----------------
void moveMotor(int dir){      
  int num = getData(1);
  int val = getData(3);
      
  if (num==0 && dir==1){
    motor.motor0Forward(val);
  }
  else if (num==1 && dir==1){
    motor.motor1Forward(val);
  }
  else if (num==0 && dir==-1){
    motor.motor0Reverse(val);
  }
  else if (num==1 && dir==-1){
    motor.motor1Reverse(val);
  }
  Serial.println("");
}
//---------------
void getAnalog(){
  int port = getData(2);
  int analogData = analogRead(port);

  Serial.print("A ");
  Serial.print(port);
  Serial.print(" ");
  Serial.println(analogData);
}
//---------------
void getDigital(){
  int port = getData(2);
  int digitalData = digitalRead(port);
  
  Serial.print("D ");
  Serial.print(port);
  Serial.print(" ");
  Serial.println(digitalData);
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
