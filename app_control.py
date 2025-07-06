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
            # DON'T TOUCH THIS - IT'S WORKING FINE
            possible = [
                os.path.expandvars(r"%APPDATA%\\Spotify\\Spotify.exe"),
                r"C:\\Users\\hp\\AppData\\Roaming\\Spotify\\Spotify.exe",
                r"C:\\Program Files\\Spotify\\Spotify.exe",
                r"C:\\Program Files (x86)\\Spotify\\Spotify.exe"
            ]
            for path in possible:
                if os.path.exists(path):
                    subprocess.Popen(path)
                    time.sleep(4)
                    return True
            print("Spotify not found in default locations.")
            return False
        elif app_name == "telegram":
            # Check if already running
            for window in gw.getAllWindows():
                if "telegram" in window.title.lower():
                    print("[INFO] Telegram is already running.")
                    return True
            
            # Open using Windows Search
            print("[INFO] Opening Telegram using Windows Search...")
            try:
                # Press Windows key
                pyautogui.press('win')
                time.sleep(2)  # Wait for start menu
                
                # Type telegram
                pyautogui.typewrite('telegram', interval=0.1)
                time.sleep(2)  # Wait for search results
                
                # Press Enter to open first result
                pyautogui.press('enter')
                print("[INFO] Telegram launch command sent. Waiting 10 seconds...")
                time.sleep(10)  # Wait for Telegram to open
                return True
            except Exception as e:
                print(f"[ERROR] Failed to open Telegram via search: {e}")
                return False
        else:
            print("Unsupported app:", app_name)
            return False
    else:
        print("Platform not supported")
        return False

def play_pause_spotify(max_wait=15):
    # DON'T TOUCH THIS FUNCTION - IT'S WORKING
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
        try:
            win.activate()
            time.sleep(1)
            pyautogui.press('space')
            print("Toggled play/pause in Spotify.")
        except Exception as e:
            print(f"Error controlling Spotify: {e}")
    else:
        print("Spotify window not found after waiting.")

def send_telegram_message(contact: str, message: str, max_wait=40):
    """
    Open Telegram via Windows Search and send message
    """
    print(f"\n[AGENT] Starting Telegram message process...")
    print(f"[AGENT] Contact: '{contact}'")
    print(f"[AGENT] Message: '{message[:50]}...'")
    
    # Step 1: Open Telegram using Windows Search
    app_opened = open_app("telegram")
    if not app_opened:
        print("[ERROR] Cannot open Telegram. Aborting.")
        return False
    
    # Step 2: Wait for window
    print("[INFO] Waiting for Telegram window...")
    waited = 0
    win = None
    while waited < max_wait:
        try:
            for window in gw.getAllWindows():
                if "telegram" in window.title.lower():
                    win = window
                    break
            if win:
                break
        except Exception:
            pass
        
        time.sleep(2)
        waited += 2
        if waited % 10 == 0:
            print(f"[INFO] Still waiting... {waited}/{max_wait} seconds")
    
    if not win:
        print("[ERROR] Telegram window not found after waiting.")
        return False
    
    print(f"[SUCCESS] Found Telegram window: '{win.title}'")
    
    # Step 3: Focus window
    print("[INFO] Focusing Telegram window...")
    for attempt in range(3):
        try:
            if win.isMinimized:
                win.restore()
            win.activate()
            time.sleep(2)
            if win.isActive:
                print("[SUCCESS] Window is active")
                break
        except Exception as e:
            print(f"[WARN] Attempt {attempt+1} to focus failed: {e}")
            time.sleep(2)
    
    # Step 4: Search for contact
    contact_clean = contact.strip().replace('"', '')
    print(f"[INFO] Searching for contact: '{contact_clean}'")
    
    try:
        # Clear any dialogs
        pyautogui.press('escape')
        time.sleep(1)
        
        # Open search
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(2)
        
        # Clear and type contact
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.typewrite(contact_clean, interval=0.1)
        time.sleep(3)
        
        # Select contact
        pyautogui.press('enter')
        time.sleep(2)
        print("[SUCCESS] Contact selected")
        
    except Exception as e:
        print(f"[ERROR] Failed to search contact: {e}")
        return False
    
    # Step 5: Send message
    print("[INFO] Sending message...")
    try:
        # Click message area
        pyautogui.click(win.width // 2, win.height - 100)
        time.sleep(1)
        
        # Type message
        if len(message) > 50:
            try:
                import pyperclip
                pyperclip.copy(message)
                pyautogui.hotkey('ctrl', 'v')
            except:
                pyautogui.typewrite(message, interval=0.05)
        else:
            pyautogui.typewrite(message, interval=0.05)
        
        time.sleep(1)
        pyautogui.press('enter')
        print("[SUCCESS] Message sent!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")
        return False