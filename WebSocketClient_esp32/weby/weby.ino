
#include <ArduinoWebsockets.h>
#include <WiFi.h>
const int ledPin = 2;
const char* ssid = "Everything is"; //Enter SSID
const char* password = "wtf123wtf"; //Enter Password
const char* websockets_server_host = "192.168.0.103"; //Enter server adress
const uint16_t websockets_server_port = 8000; // Enter server port

using namespace websockets;

WebsocketsClient client;
void setup() {
    Serial.begin(115200);
    pinMode(ledPin, OUTPUT);
    // Connect to wifi
    WiFi.begin(ssid, password);

    // Wait some time to connect to wifi
    for(int i = 0; i < 10 && WiFi.status() != WL_CONNECTED; i++) {
        Serial.print(".");
        delay(1000);
    }

    // Check if connected to wifi
    if(WiFi.status() != WL_CONNECTED) {
        Serial.println("No Wifi!");
        return;
    }

    Serial.println("Connected to Wifi, Connecting to server.");
    // try to connect to Websockets server
    bool connected = client.connect(websockets_server_host, websockets_server_port,"/ws/esp/-ccbBn_fJY2ZiZ2l9YFLeg/");
    if(connected) {
        Serial.println("Connected!");
        client.send("Hello Server");
    } else {
        Serial.println("Not Connected!");
    }
    
    // run callback when messages are received
    client.onMessage([&](WebsocketsMessage message){
        Serial.print("Got Message: ");
        Serial.println(message.data());
        if (String(message.data()) == "True"){digitalWrite(ledPin, HIGH);}
        else{digitalWrite(ledPin, LOW);}
    });
}

void loop() {
    // let the websockets client check for incoming messages
    if(client.available()) {
        client.poll();
    }
    else{
bool connected = client.connect(websockets_server_host, websockets_server_port,"/ws/esp/-ccbBn_fJY2ZiZ2l9YFLeg/");
      
      }
    delay(500);
}
