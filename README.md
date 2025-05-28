# Braille Mouse Project

This project combines an Arduino-based joystick mouse with a Python OCR system to detect on-screen text and convert it into braille signals via serial communication.

## Features

- **Joystick Mouse Control**  
  Arduino reads joystick inputs and sends HID mouse signals (move, click).

- **Text Detection via OCR**  
  Python captures the screen, uses Tesseract OCR to detect Korean/English text, and identifies the word under the cursor.

- **Braille Conversion and Output**  
  Detected words are converted to braille patterns and sent to Arduino to activate a 6-dot braille actuator.

---

## Getting Started

### Requirements

- Arduino board with HID support (e.g., Leonardo, Micro, Pro Micro)
- Joystick module (connected to analog pins)
- 6-pin braille actuator
- Python 3.x
- Tesseract OCR installed (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe` on Windows)


```bash
pip install -r requirements.txt
