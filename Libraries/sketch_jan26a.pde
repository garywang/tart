void setup()
{
 Serial.begin(9600);
 Serial1.begin(38400);
 Serial1.write(0xaa); 
 delay(100);
 Serial1.write(0x84);
delay(1);
 Serial1.write(0x01);
 delay(1);
 Serial1.write(0x02);
 delay(1);
 Serial1.write(0x55);
 delay(1);
 Serial1.write(0x2a);
 delay(10);
 Serial.write(Serial1.read());
 
}

void loop()
{
 Serial.write(Serial1.read());
 delay(100);
 Serial1.write(0x83);
 delay(1);
 Serial1.write(0x01);
 delay(1);
}
