#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include<stdlib.h>
#include<stdio.h>

const char* ssid = "Q_1";
const char* password = "Ab123789";

int keyPin1 = 4;
int keyPin2 = 5;

unsigned int localPort = 8888; 
WiFiUDP Udp;
void setup() 
{
    delay(1000);
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    
  }
  pinMode(keyPin1, INPUT);
  pinMode(keyPin2, INPUT);
    Udp.begin(localPort);
    //Udp.beginPacket("255.255.255.255", localPort);
}
void Send(const char ch[])
{
   Udp.beginPacket("255.255.255.255", localPort);
   Udp.write(ch);
   Udp.endPacket();
}
void loop() 
{
  String data="";
  int tempd;
   while (Serial.available()>0)
  {     
    data+=int(Serial.read());
    data+=int("_");
  }
  
//  char * datap;
//  data.toCharArray(datap,data.length());
  if(data!="")
  {
    data+=digitalRead(keyPin1);
  data+=int("_");
  data+=digitalRead(keyPin2);
  data+=int("_");
    Send(data.c_str());
  }
  
  delay(5);
}
