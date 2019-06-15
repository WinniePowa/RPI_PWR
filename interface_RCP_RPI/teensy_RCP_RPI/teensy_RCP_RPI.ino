#include <Encoder.h>

Encoder iris(11,12);
Encoder univ(10,9) ;
bool mode = false;
void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
pinMode(13,OUTPUT);
digitalWrite(13,LOW);
}

void loop() {
  if(Serial.available())
  {
    Serial.read();
    mode = ! mode;
    digitalWrite(13,mode);
    //Serial.print("2");
//   //if(Serial.read() == '1' )
     sendToPc();
    }
//sendToPc();
//delay(200);
}
  // put your main code here, to run repeatedly:
void sendToPc()
{
 
  Serial.print(125);
  Serial.print(" ");
  Serial.print(iris.read());
  Serial.print(" ");
  Serial.print(univ.read());

  iris.write(0);
  univ.write(0);
}
