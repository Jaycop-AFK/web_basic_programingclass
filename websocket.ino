#include <WiFi.h>
#include <WebSocketsServer.h>

const char* ssid = "iPhone";
const char* password = "987654321";

// Create a WebSocket server on port 81
WebSocketsServer webSocket = WebSocketsServer(81);

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Start the WebSocket server
  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);

  Serial.println(WiFi.localIP());
}

void loop() {
  // Listen for WebSocket events
  webSocket.loop();
}

// Handle incoming WebSocket events
void onWebSocketEvent(uint8_t client_num, WStype_t type, uint8_t * payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.printf("Client %u disconnected\n", client_num);
      break;
    case WStype_CONNECTED: {
      IPAddress ip = webSocket.remoteIP(client_num);
      Serial.printf("Client %u connected from %s\n", client_num, ip.toString().c_str());
      break;
    }
    case WStype_TEXT:
      // When a message is received from the client
      Serial.printf("Client %u sent: %s\n", client_num, payload);
      
      // If the message is "hello", do something
      if (strcmp((const char*)payload, "hello") == 0) {
        Serial.println("Received 'hello' from client!");
      }
      break;
  }
}
