#include <Adafruit_Sensor.h>
#include <DHT.h>

#define DHTPIN 3  // Replace with the actual pin you connected the DHT11 to
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
const int ledPin = 5;  // Replace with the actual pin you connected the LED to
const int buzzerPin = 4;  // Replace with the actual pin you connected the LED to

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);  // Set the baud rate to match your Python script
  dht.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    Serial.println(command);
    if (command == '0'){
        digitalWrite(ledPin, LOW);
    } else if (command == '1') {
      digitalWrite(ledPin, HIGH);  // Turn the LED on
    } else if (command == '2') {
      digitalWrite(buzzerPin, HIGH);
      // delay(1000); 
      // digitalWrite(buzzerPin, LOW);
       // Turn the LED off
      } else if(command == '3') {   
        float humidity = dht.readHumidity();
        float temperature = dht.readTemperature();

        Serial.print("H:");
        Serial.print(humidity);
        Serial.print(",T:");
        Serial.println(temperature);

        delay(2000);  // Adjust delay as needed
      }
    }
}
