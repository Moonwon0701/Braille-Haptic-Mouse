#include <Mouse.h>

const int actuatorPins[6] = {3, 4, 5, 6, 7, 8};
const int joystickX = A0;
const int joystickY = A1;
const int lb = 16;
const int rb = 14;
int threshold = 10;

void setup() {
  Serial.begin(9600);
  Mouse.begin();

  for (int i = 0; i < 6; i++) {
    pinMode(actuatorPins[i], OUTPUT);
    digitalWrite(actuatorPins[i], LOW);
  }

  pinMode(lb, INPUT_PULLUP);
  pinMode(rb, INPUT_PULLUP);
}

void loop() {
  // 점자 출력
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line == "reset") {
      for (int i = 0; i < 6; i++) {
        digitalWrite(actuatorPins[i], HIGH);
        delay(100);
        digitalWrite(actuatorPins[i], LOW);
        delay(100);
      }
    } else if (line.length() == 6) {
      for (int i = 0; i < 6; i++) {
        digitalWrite(actuatorPins[i], line.charAt(i) == '1' ? HIGH : LOW);
      }
    }
  }

  // 마우스 제어
  int x = analogRead(joystickX) - 512;
  int y = analogRead(joystickY) - 512;

  int moveX = abs(x) > threshold ? x / 50 : 0;
  int moveY = abs(y) > threshold ? y / 50 : 0;

  if (moveX != 0 || moveY != 0) {
    Mouse.move(moveX, -moveY);
  }

  if (!digitalRead(lb)) {
    Mouse.press(MOUSE_LEFT);
  } else {
    Mouse.release(MOUSE_LEFT);
  }

  if (!digitalRead(rb)) {
    Mouse.press(MOUSE_RIGHT);
  } else {
    Mouse.release(MOUSE_RIGHT);
  }

  delay(10);
}
