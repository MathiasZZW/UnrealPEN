#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
int i=0;

const char* ssid = "Q";
const char* password = "Ab123789";

const char* host = "192.168.123.200"; //需要访问的域名
const int httpsPort = 5000;  // 需要访问的端口
const String url = "/login?data=";   // 需要访问的地址
WiFiClient client;
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password); // 连接WIFI
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

}

void loop() {
  String data="";
   while (Serial.available()>0)
  {
    data += (String)int(Serial.read());
    data+="_";
   }
  i++;

  if(data==""){
   delay(5);
   return;
   }
  client.connect(host, httpsPort);
  String postRequest =(String)("GET ") + url +data
   + " HTTP/1.1\r\n" +
    "Content-Type: text/html;charset=utf-8\r\n" +
    "Host: " + host + "\r\n" +
    "User-Agent: BuildFailureDetectorESP8266\r\n" +
    "Connection: Keep Alive\r\n\r\n";
  
  client.print(postRequest);  // 发送HTTP请求
  Serial.print(data.c_str());
  //delay(3000);
  delay(5);
}
