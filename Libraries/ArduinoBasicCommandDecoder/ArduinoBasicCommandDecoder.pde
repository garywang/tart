#include <Servo.h>
#include <CompactQik2s9v1.h>
#include <NewSoftSerial.h>

#define rxPin 1
#define txPin 0
#define rxPin1 19
#define txPin1 18
#define rxPin2 17
#define txPin2 16
#define rxPin3 15
#define txPin3 14
#define rstPin 5
#define servoChar 'S'
#define analogChar 'A'
#define motorChar 'M'
#define digitalChar 'D'
#define commandLen 6

Servo servo;
NewSoftSerial mySerial[4] = {
    NewSoftSerial(rxPin, txPin),
    NewSoftSerial(rxPin1, txPin1),
    NewSoftSerial(rxPin2, txPin2),
    NewSoftSerial(rxPin3, txPin3)
}
CompactQik2s9v1 mc[4] = {
    CompactQik2s9v1(&mySerial[0], rstPin),
    CompactQik2s9v1(&mySerial[1], rstPin),
    CompactQik2s9v1(&mySerial[2], rstPin),
    CompactQik2s9v1(&mySerial[3], rstPin)
}

void setup()                    
{
  Serial.begin(9600);           // set up Serial library at 9600 bps
  delay(1000); //Wait for it to initialize
  Serial.flush();
  
  for (int i = 0; i < 4; i++)
  {
    mySerial[i].begin(9600);
    mc[i].begin();
    mc[i].getError();
    mc[i].stopBothMotors();
  }
}

void loop()                      
{
  //char command[commandLen-1];
  
    //delay(10);
    
    //Get the mode
    char mode = serialRead();
  
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
      //M[motor number][+/-][val]
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

//----------
void moveServo(){
  int port = getData(2);
  int angle = getData(3);
  servo.attach(port);
  servo.write(angle);
  Serial.println(0);
}
//----------------
void moveMotor(){     
  int controller = getData(1); 
  int num = getData(1);
  char sign = serialRead();
  int val = getData(3);
<<<<<<< HEAD
      
  if (num==0 && sign=='+'){
    motor.motor0Forward(val);
    Serial.println(val);
  }
  else if (num==1 && sign=='+'){
    motor.motor1Forward(val);
    Serial.println(2);
  }
  else if (num==0 && sign=='-'){
    motor.motor0Reverse(val);
    Serial.println(3);
  }
  else if (num==1 && sign=='-'){
    motor.motor1Reverse(val);
    Serial.println(4);
  }
  else {
    Serial.println(val);
  }
 
=======
  
  if (controller >= 0 && controller < 4 && num >= 0 && num < 2) {
      CompactQik2s9v1 m = mc[controller];
          
      if (num==0 && sign=='+'){
        m.motor0Forward(val);
      }
      else if (num==1 && sign=='+'){
        m.motor1Forward(val);
      }
      else if (num==0 && sign=='-'){
        m.motor0Reverse(val);
      }
      else if (num==1 && sign=='-'){
        m.motor1Reverse(val);
      }
      Serial.print(controller);
      Serial.print(num);
      Serial.print(sign);
      Serial.println(val);
  }
  else { // motor does not exist
    Serial.print(controller);
    Serial.print(num);
    Serial.print(val);
  }
}
//---------------
void getAnalog(){
  int port = getData(2);
  int analogData = analogRead(port);

  Serial.println(analogData);
}
//---------------
void getDigital(){
  int port = getData(2);
  int digitalData = digitalRead(port);
  
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
    buffer[received++] = serialRead();
    buffer[received] = '\0';
    if (received >= (sizeof(buffer)-1))
    {
      returnInt = atoi(buffer);
      received = 0;
    }
  }
  
  return returnInt;
}

char serialRead()
{
  char in = -1;
  while (in == -1) in = Serial.read();
  return in;
}
