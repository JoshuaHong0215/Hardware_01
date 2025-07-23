// 전역 변수
const int trigPin = 9;
const int echoPin = 10;

float duration;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

float getFilteredDistance(int times = 5) {
  float sum = 0;
  for (int i = 0; i < times; i++) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH, 30000); // 30ms timeout
    float d = (duration * 0.0343) / 2;
    sum += d;
    delay(50);  // 센서 간섭 방지
  }
  return sum / times;
}

void loop() {
  float distance = getFilteredDistance(5);
  Serial.println(distance);
  delay(100);
}
