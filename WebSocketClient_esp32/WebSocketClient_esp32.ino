#include <WiFi.h>
#include <WebSocketClient.h>
#include <ArduinoJson.h> 
const char* ssid     = "Everything is";
const char* password = "wtf123wtf";
 
char path[] = "ws/esp/-ccbBn_fJY2ZiZ2l9YFLeg/";
char host[] = "192.168.0.113";
 
WebSocketClient webSocketClient;
WiFiClient client;
 
void setup() {
  Serial.begin(115200);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
 
  delay(5000);
 
  if (client.connect(host, 8000)) {
    Serial.println("Connected");
  } else {
    Serial.println("Connection failed.");
  }
 
  webSocketClient.path = path;
  webSocketClient.host = host;
  if (webSocketClient.handshake(client)) {
    Serial.println("Handshake successful");
  } else {
    Serial.println("Handshake failed.");
  }
 
}
 
void loop() {
  String data;
 
  if (client.connected()) {
    StaticJsonDocument<256> doc;
    doc["type"] = "current_statue";
    doc["time"] = 1351824120;
    String jsonStr;
    serializeJson(doc, jsonStr);
    webSocketClient.sendData(jsonStr);
    
    webSocketClient.getData(data);
    if (data.length() > 0) {
      Serial.print("Received data: ");
      Serial.println(data);
    }
 
  } else {
    Serial.println("Client disconnected.");
  }
 
  delay(3000);
 
}
