#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

const int gasPin = 7;
const int ledPin = 8; 

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(ledPin, OUTPUT);
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  int ledState = digitalRead(ledPin);
  int gasValue = digitalRead(gasPin);
  // Đọc dữ liệu từ Serial và xử lý
  if (Serial.available()) {
    char data = Serial.read();
    if (data == 'L') {
      if (Serial.available()) {
        char stateChar = Serial.read();
        if (stateChar == '0') {
          digitalWrite(ledPin, LOW); // Tắt đèn LED
        } else if (stateChar == '1') {
          digitalWrite(ledPin, HIGH); // Bật đèn LED
        } else {
          digitalWrite(ledPin, LOW);
        }
    }
    }else {
      return;
    }
  }
  // Gửi dữ liệu nhiệt độ, độ ẩm và giá trị khí gas qua cổng Serial
  Serial.print("T:");
  Serial.print(temperature);
  Serial.print(",H:");
  Serial.print(humidity);
  Serial.print(",G:");
  Serial.println(gasValue);
  delay(16000);
}



