import os
import subprocess
import platform
import time
import pyautogui
import pygetwindow as gw
import webbrowser
from urllib.parse import quote
import ctypes
from ctypes import wintypes

pyautogui.FAILSAFE = False


def find_telegram_click_position():
    """Run this to find where to click for Telegram"""
    print("Opening Start menu...")
    pyautogui.press('win')
    time.sleep(6)
    
    print("Typing Apps:telegram...")
    pyautogui.typewrite('Apps:telegram')
    time.sleep(6)
    
    print("\nNOW LOOK AT YOUR SCREEN!")
    print("Move your mouse to where Telegram appears in the search results")
    print("You have 5 seconds...")
    time.sleep(5)
    
    x, y = pyautogui.position()
    print(f"\nTelegram appears at position: x={x}, y={y}")
    print(f"Update the code to use: click_x = {x}, click_y = {y}")
    
    pyautogui.click(x, y)


def open_app(app_name):
    sys = platform.system()
    if sys == "Windows":
        if app_name == "notepad":
            subprocess.Popen("notepad.exe")
        elif app_name == "paint":
            subprocess.Popen("mspaint.exe")
        elif app_name == "spotify":
            # SPOTIFY CODE - DON'T TOUCH
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
            print("\n[DEBUG] Starting Telegram open process...")
            
            # Check if already running in a window
            telegram_windows = []
            for window in gw.getAllWindows():
                if "telegram" in window.title.lower():
                    telegram_windows.append(window)
                    
            if telegram_windows:
                print(f"[INFO] Telegram already running. Found {len(telegram_windows)} window(s)")
                try:
                    telegram_windows[0].activate()
                except:
                    pass
                return True
            
            # NEW: Check taskbar for Telegram
            print("[INFO] Checking taskbar for Telegram...")
            screen_width, screen_height = pyautogui.size()
            taskbar_y = screen_height - 40  # Middle of taskbar
            
            # Try clicking common icon positions in taskbar
            for x_percent in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]:
                x_pos = int(screen_width * x_percent)
                print(f"[DEBUG] Checking taskbar position ({x_pos}, {taskbar_y})...")
                
                


                pyautogui.click(x_pos, taskbar_y)
                time.sleep(2)  # Wait for window to appear
                
                
                for window in gw.getAllWindows():
                    if "telegram" in window.title.lower():
                        print(f"[SUCCESS] Found Telegram at taskbar position {x_pos}")
                        # Give it a moment to fully open
                        time.sleep(1)
                        try:
                            window.activate()
                        except:
                            pass
                        return True
            
            print("[INFO] Telegram not found in taskbar, opening fresh...")
            
            # SIMPLE WINDOWS 11 APPROACH - JUST CLICK!
            print("[INFO] Opening Telegram via Windows 11 Start Menu...")
            try:
                # Press Windows key
                print("[DEBUG] Pressing Windows key...")
                pyautogui.press('win')
                time.sleep(3)
                
                print("[DEBUG] Typing 'Apps:telegram'...")
                pyautogui.typewrite('Apps:telegram', interval=0.1)
                time.sleep(10)  # Wait for search results
                
                
                screen_width, screen_height = pyautogui.size()
                
                click_x = 546  # Fixed position - left side where apps show
                click_y = 348  # First result position
                
                print(f"[DEBUG] Clicking at ({click_x}, {click_y})...")
                pyautogui.click(x=click_x, y=click_y)
                
                # Give it time to open
                print("[INFO] Waiting 15 seconds for Telegram to open...")
                time.sleep(20)
                
                return True
                        
            except Exception as e:
                print(f"[ERROR] Failed: {e}")
                return False
                    
        else:
            print("Unsupported app:", app_name)
            return False
    else:
        print("Platform not supported")
        return False


def play_pause_spotify(max_wait=15):
    # SPOTIFY FUNCTION - DON'T TOUCH
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
    Send message via Telegram using Start Menu to open
    """
    print(f"\n{'='*50}")
    print(f"[AGENT] TELEGRAM MESSAGE AUTOMATION STARTING")
    print(f"[AGENT] Contact: '{contact}'")
    print(f"[AGENT] Message: '{message}'")  # Added to debug
    print(f"[AGENT] Message length: {len(message)} characters")
    print(f"{'='*50}\n")

    print("[STEP 1] Opening Telegram via Start Menu...")
    app_opened = open_app("telegram")

    if not app_opened:
        print("\n[ERROR] Cannot open Telegram")
        return False

    print("\n[STEP 2] Looking for Telegram window...")
    telegram_win = None
    attempts = 0

    while attempts < 14:  
        all_windows = gw.getAllWindows()

        for window in all_windows:
            if "telegram" in window.title.lower():
                telegram_win = window
                print(f"[SUCCESS] Found: '{window.title}'")
                break

        if telegram_win:
            break

        attempts += 1
        print(f"[DEBUG] Attempt {attempts}/10 - Waiting for Telegram...")
        time.sleep(5)  

    if not telegram_win:
        print("\n[ERROR] Telegram window not found")
        return False

    print("\n[STEP 3] Focusing Telegram window...")
    try:
        if telegram_win.isMinimized:
            telegram_win.restore()
            time.sleep(2)
        telegram_win.activate()
        time.sleep(5)  # INCREASED

        window_x = telegram_win.left + (telegram_win.width // 2)
        window_y = telegram_win.top + (telegram_win.height // 2)
        pyautogui.click(window_x, window_y)
        time.sleep(2)

        print("[SUCCESS] Window focused")
    except Exception as e:
        print(f"[WARN] Focus error: {e}")

    print(f"\n[STEP 4] Searching for contact: '{contact}'")
    try:
        # Clear any existing dialogs
        pyautogui.press('escape')
        time.sleep(1)
        pyautogui.press('escape')
        time.sleep(1)

        # Open search
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(3)  # INCREASED

        # Clear search box THOROUGHLY
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.press('delete')
        time.sleep(1)
        pyautogui.press('backspace')  # Extra clear
        time.sleep(1)

        # Type ONLY contact name
        print(f"[DEBUG] Typing ONLY contact name: '{contact}'")
        pyautogui.typewrite(contact, interval=0.2)  # Type only contact
        time.sleep(5)  # Wait for search results

        
        pyautogui.press('enter')
        time.sleep(5)  # INCREASED wait after selecting

        print("[SUCCESS] Contact selected")
    except Exception as e:
        print(f"[ERROR] Contact search failed: {e}")
        return False

    



    print(f"\n[STEP 5] Sending message: '{message}'")
    try:


        msg_x = telegram_win.left + (telegram_win.width // 2)
        msg_y = telegram_win.top + telegram_win.height - 100



        for i in range(3):
            pyautogui.click(msg_x, msg_y)
            time.sleep(1)

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.press('delete')
        time.sleep(1)

        # Type the message
        if len(message) > 30:
            print("[DEBUG] Using clipboard for long message")
            try:
                import pyperclip
                pyperclip.copy(message)
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1)
                print("[DEBUG] Message pasted")
            except Exception as e:
                print(f"[WARN] Clipboard failed: {e}, typing instead...")
                pyautogui.typewrite(message, interval=0.1)
        else:
            print(f"[DEBUG] Typing short message: '{message}'")
            pyautogui.typewrite(message, interval=0.1)

        time.sleep(2)  # Wait before sending

        

        print("[DEBUG] Pressing Enter to send...")
        pyautogui.press('enter')
        time.sleep(2)

        print("\n[SUCCESS] MESSAGE SENT SUCCESSFULLY!")
        print(f"{'='*50}\n")
        return True

    except Exception as e:
        print(f"\n[ERROR] Message sending failed: {e}")
        return False


# Test function
def test_telegram():
    """Test if we can open Telegram"""
    print("Testing Telegram opening...")
    success = open_app("telegram")
    if success:
        print("✓ Telegram test passed!")
    else:
        print("✗ Telegram test failed!")
    return success


# Optional: Debug function to test search clicking
def debug_telegram_search():
    """Debug function to test the search and click process"""
    print("Debug: Testing Telegram search...")
    pyautogui.press('win')
    time.sleep(5)
    pyautogui.typewrite('telegram', interval=0.2)
    time.sleep(5)

    screenshot = pyautogui.screenshot()
    screenshot.save('telegram_search_debug.png')
    print("Screenshot saved as 'telegram_search_debug.png'")

    screen_width, screen_height = pyautogui.size()
    search_result_x = int(screen_width * 0.15)
    search_result_y = int(screen_height * 0.25)
    print(f"Clicking at ({search_result_x}, {search_result_y})...")
    pyautogui.click(x=search_result_x, y=search_result_y)
def system_control(command: str, value: str = None):
    """Control system functions like volume, brightness, shutdown"""
    try:
        if command == "volume":
            if value == "up":
                print("[INFO] Increasing volume...")
                pyautogui.press('volumeup')
                return True
            elif value == "down":
                print("[INFO] Decreasing volume...")
                pyautogui.press('volumedown')
                return True
            elif value == "mute":
                print("[INFO] Toggling mute...")
                pyautogui.press('volumemute')
                return True
                
        elif command == "brightness":
            
            if value == "up":
                print("[INFO] Increasing brightness...")
                # Windows 10/11 shortcut
                pyautogui.hotkey('win', 'a')  # Open action center
                time.sleep(2)
                pyautogui.click(1800, 950)  # Adjust for your screen
                pyautogui.press('escape')
                return True
            elif value == "down":
                print("[INFO] Decreasing brightness...")
                pyautogui.hotkey('win', 'a')
                time.sleep(2)
                pyautogui.click(1700, 950)  
                pyautogui.press('escape')
                return True
                
        elif command == "lock":
            print("[INFO] Locking screen...")
            pyautogui.hotkey('win', 'l')
            return True
            
        elif command == "shutdown":
            if value:
                print(f"[INFO] Scheduling shutdown in {value} seconds...")
                os.system(f"shutdown /s /t {value}")
            else:
                print("[INFO] Shutting down immediately...")
                os.system("shutdown /s /t 0")
            return True
            
        elif command == "restart":
            if value:
                print(f"[INFO] Scheduling restart in {value} seconds...")
                os.system(f"shutdown /r /t {value}")
            else:
                print("[INFO] Restarting immediately...")
                os.system("shutdown /r /t 0")
            return True
            
        elif command == "cancel_shutdown":
            print("[INFO] Cancelling shutdown/restart...")
            os.system("shutdown /a")
            return True
            
    except Exception as e:
        print(f"[ERROR] System control failed: {e}")
        return False
def browser_control(action: str, query: str = None):
    """Control browser - search, open websites, play youtube"""
    try:
        if action == "google":
            if query:
                print(f"[INFO] Searching Google for: {query}")
                search_url = f"https://www.google.com/search?q={quote(query)}"
                webbrowser.open(search_url)
                return True
            else:
                print("[ERROR] No search query provided")
                return False
                
        elif action == "youtube":
            if query:
                print(f"[INFO] Searching YouTube for: {query}")
                youtube_url = f"https://www.youtube.com/results?search_query={quote(query)}"
                webbrowser.open(youtube_url)
                # Wait and click first video
                time.sleep(5)
                pyautogui.click(700, 350)  # Adjust coordinates for first video
                return True
            else:
                print("[ERROR] No video query provided")
                return False
                
        elif action == "website":
            if query:
                print(f"[INFO] Opening website: {query}")
                if not query.startswith(('http://', 'https://')):
                    query = 'https://' + query
                webbrowser.open(query)
                return True
            else:
                print("[ERROR] No website provided")
                return False
                
    except Exception as e:
        print(f"[ERROR] Browser control failed: {e}")
        return False