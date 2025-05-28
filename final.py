import time
import cv2
import pytesseract
import numpy as np
import pyautogui
import hbcvt
import serial
import serial.tools.list_ports
import keyboard
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def init_serial(baudrate=9600):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate, timeout=1)
            print(f"[INFO] Connected to Arduino on {port.device}")
            time.sleep(2)  # 아두이노 리셋 대기
            return ser
        except Exception as e:
            print(f"[ERROR] Could not connect to {port.device}: {e}")
    return None


def send_braille_to_arduino(ser, input_text):
    if not input_text:
        print("[WARN] No text to send.")
        return

    braille_list = hbcvt.h2b.text(input_text)

    for text in braille_list:
        text_label = text[0]
        components = text[1]
        print(f"[INFO] Sending character: {text_label}")
        for component in components:
            for pattern in component[1]:
                pattern_str = ''.join(str(bit) for bit in pattern)
                ser.write((pattern_str + '\n').encode())
                print(f"[DEBUG] Sent: {pattern_str}")
                time.sleep(1)

    # Reset pulse
    ser.write(b'reset\n')
    print("[INFO] Reset pulse sent.")


def get_text_with_bounding_boxes(screen):
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (gray.shape[1] // 2, gray.shape[0] // 2))
    config = r'--oem 3 --psm 6'
    results = pytesseract.image_to_data(gray, config=config, output_type=Output.DICT, lang='kor+eng')

    bounding_boxes = []
    for i in range(len(results['text'])):
        if int(results['conf'][i]) > 30:
            x, y, w, h = results['left'][i] * 2, results['top'][i] * 2, results['width'][i] * 2, results['height'][i] * 2
            text = results['text'][i].strip()
            if text:
                bounding_boxes.append((x, y, w, h, text))
    return bounding_boxes


def main():
    ser = init_serial()
    if ser is None:
        print("[FATAL] No Arduino found. Exiting.")
        return

    frame_count = 0
    bounding_boxes = []
    last_pointed_text = ""

    while True:
        screenshot = pyautogui.screenshot()
        screen = np.array(screenshot)
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

        if frame_count % 10 == 0:
            bounding_boxes = get_text_with_bounding_boxes(screen)

        pointed = None
        mouse_x, mouse_y = pyautogui.position()

        for (x, y, w, h, text) in bounding_boxes:
            if x < mouse_x < x + w and y < mouse_y < y + h:
                pointed = text
                break

        if pointed and pointed != last_pointed_text:
            print(f"[INFO] Pointed text: {pointed}")
            send_braille_to_arduino(ser, pointed)
            last_pointed_text = pointed

        if keyboard.is_pressed('q'):
            break

        time.sleep(0.1)
        frame_count += 1

    ser.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
