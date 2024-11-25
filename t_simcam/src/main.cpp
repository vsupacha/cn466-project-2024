#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <PubSubClient.h>

#include <Arduino.h>
#include <cam_dev.h>

static bool status = false;

// WiFi credentials
const char* ssid = "KT";
const char* password = "1234567890";

// MQTT server credentials
const char* mqttServer = "mqtt.eclipseprojects.io";
const int mqttPort = 1883;
const char* mqttTopic = "TU/CN466/tsimcam/room422";

// Brightness threshold
const uint64_t BRIGHTNESS_THRESHOLD = 100; // Adjust this value based on your requirements

// WiFi and MQTT clients
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// State tracking
bool isBright = false; // Tracks whether the last state was bright

void connectToWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

void checkWiFiConnection() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected! Reconnecting...");
    connectToWiFi();
  }
}

void connectToMQTT() {
  Serial.print("Connecting to MQTT...");
  while (!mqttClient.connected()) {
    if (mqttClient.connect("ArduinoClient")) {
      Serial.println("connected");
    } else {
      Serial.print("failed with state ");
      Serial.println(mqttClient.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(2000);

  // Initialize camera
  status = cam_dev_init();
  
  // Connect to WiFi
  connectToWiFi();
  
  // Setup MQTT
  mqttClient.setServer(mqttServer, mqttPort);
  connectToMQTT();
}

void loop() {
  static uint8_t buf[160 * 120 * 2] = {0};
  uint64_t sum_color = 0;

  // Ensure WiFi connection
  checkWiFiConnection();

  // Ensure the MQTT connection is active
  if (!mqttClient.connected()) {
    connectToMQTT();
  }
  mqttClient.loop();

  // Capture image data from the camera
  int buf_sz = cam_dev_snapshot(buf);
  for (int i = 0; i < buf_sz; i++) {
    sum_color += buf[i];
  }

  sum_color /= buf_sz;

  // Display the current brightness value
  Serial.printf("Current Bright Value: %llu\n", sum_color);

  // Determine status based on brightness threshold
  int status = (sum_color > BRIGHTNESS_THRESHOLD) ? 1 : 0;

  // Check for state transition
  if (status == 1 && !isBright) { // Transition from OFF to ON
    isBright = true;

    // Send MQTT message with status = 1
    char message[100];
    snprintf(message, sizeof(message),
             "{\n"
             "  \"timestamp\": %lu,\n"
             "  \"status\": 1\n"
             "}",
             millis());

    mqttClient.publish(mqttTopic, message);

    // Debug message
    Serial.printf("Transition to ON detected. Timestamp: %lu, Status: 1\n", millis());
  } else if (status == 0 && isBright) { // Transition from ON to OFF
    isBright = false;

    // Send MQTT message with status = 0
    char message[100];
    snprintf(message, sizeof(message),
             "{\n"
             "  \"timestamp\": %lu,\n"
             "  \"status\": 0\n"
             "}",
             millis());

    mqttClient.publish(mqttTopic, message);

    // Debug message
    Serial.printf("Transition to OFF detected. Timestamp: %lu, Status: 0\n", millis());
  }

  delay(1000);
}
