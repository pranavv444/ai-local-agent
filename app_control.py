import os
import subprocess
import platform
import time
import pyautogui
import pygetwindow as gw

def open_app(app_name):
    sys = platform.system()
    if sys == "Windows":
        if app_name == "notepad":
            subprocess.Popen("notepad.exe")
        elif app_name == "paint":
            subprocess.Popen("mspaint.exe")
        elif app_name == "spotify":
            possible = [
                os.path.expandvars(r"%APPDATA%\\Spotify\\Spotify.exe"),
                r"C:\\Users\\hp\\AppData\\Roaming\\Spotify\\Spotify.exe",
                r"C:\\Program Files\\Spotify\\Spotify.exe",
                r"C:\\Program Files (x86)\\Spotify\\Spotify.exe"
            ]
            for path in possible:
                if os.path.exists(path):
                    subprocess.Popen(path)
                    time.sleep(4)  # Give Spotify time to launch
                    return
            print("Spotify not found in default locations.")
        else:
            print("Unsupported app:", app_name)
    else:
        print("Platform not supported")

def play_pause_spotify(max_wait=15):
    """Activate Spotify window and press space; wait for window to appear if needed."""
    waited = 0
    win = None
    while waited < max_wait:
        windows = gw.getWindowsWithTitle("Spotify")
        if windows:
            win = windows[0]
            break
        time.sleep(1)
        waited += 1
    if win:
        win.activate()
        time.sleep(0.6)
        pyautogui.press('space')
        print("Toggled play/pause in Spotify.")
    else:
        print("Spotify window not found after waiting. Please check if Spotify is installed.")

