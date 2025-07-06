import os
import subprocess
import platform
import time
import pyautogui
import pygetwindow as gw

# Disable pyautogui failsafe for testing
pyautogui.FAILSAFE = False


def find_telegram_in_search():
    """Helper function to find and click Telegram in search results"""
    try:
        # Get screen dimensions for better positioning
        screen_width, screen_height = pyautogui.size()

        # Calculate position for first search result
        # Typically appears in the left panel of Start menu
        search_result_x = int(screen_width * 0.15)  # 15% from left
        search_result_y = int(screen_height * 0.25)  # 25% from top

        print(f"[DEBUG] Clicking on search result at ({search_result_x}, {search_result_y})...")
        pyautogui.click(x=search_result_x, y=search_result_y)
        return True

    except Exception as e:
        print(f"[ERROR] Could not click search result: {e}")
        return False


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

            # Check if already running
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

            # WINDOWS 11 SPECIFIC APPROACH
            print("[INFO] Opening Telegram via Windows 11 Start Menu...")
            try:
                # Press Windows key
                print("[DEBUG] Pressing Windows key...")
                pyautogui.press('win')
                time.sleep(5)  # Windows 11 needs more time for Start menu

                # Type telegram
                print("[DEBUG] Typing 'telegram'...")
                pyautogui.typewrite('telegram', interval=0.1)
                time.sleep(5)  # Wait for Windows 11 search to complete

                # In Windows 11, we need to ensure the result is selected
                print("[DEBUG] Selecting first result with Tab...")
                # This selects the first result in Windows 11
                pyautogui.press('tab')
                time.sleep(1)

                # Now press Enter
                print("[DEBUG] Pressing Enter to launch...")
                pyautogui.press('enter')

                # Wait for Telegram to open
                print("[INFO] Waiting 20 seconds for Telegram to open...")
                time.sleep(20)

                print("[SUCCESS] Telegram should be open now")
                return True

            except Exception as e:
                print(f"[ERROR] Failed to open Telegram: {e}")

                # Windows 11 Alternative: Try clicking in the search results area
                try:
                    print("\n[FALLBACK] Trying click method for Windows 11...")
                    pyautogui.press('win')
                    time.sleep(5)
                    pyautogui.typewrite('telegram', interval=0.1)
                    time.sleep(5)

                    # In Windows 11, results appear in center of screen
                    screen_width, screen_height = pyautogui.size()
                    # Click on the first result (usually in the center-left area)
                    click_x = int(screen_width * 0.3)  # 30% from left
                    click_y = int(screen_height * 0.4)  # 40% from top

                    print(f"[DEBUG] Clicking at ({click_x}, {click_y})...")
                    pyautogui.click(x=click_x, y=click_y)

                    time.sleep(20)
                    return True

                except Exception as e2:
                    print(f"[ERROR] Click method also failed: {e2}")
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

    # Step 1: Ensure Telegram is open (using Start Menu method)
    print("[STEP 1] Opening Telegram via Start Menu...")
    app_opened = open_app("telegram")

    if not app_opened:
        print("\n[ERROR] Cannot open Telegram")
        return False

    # Step 2: Find Telegram window with MORE ATTEMPTS
    print("\n[STEP 2] Looking for Telegram window...")
    telegram_win = None
    attempts = 0

    while attempts < 10:  # INCREASED attempts
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
        time.sleep(5)  # INCREASED wait time

    if not telegram_win:
        print("\n[ERROR] Telegram window not found")
        return False

    # Step 3: Focus the window with extra time
    print("\n[STEP 3] Focusing Telegram window...")
    try:
        if telegram_win.isMinimized:
            telegram_win.restore()
            time.sleep(2)
        telegram_win.activate()
        time.sleep(5)  # INCREASED

        # Click in the middle of the window to ensure focus
        window_x = telegram_win.left + (telegram_win.width // 2)
        window_y = telegram_win.top + (telegram_win.height // 2)
        pyautogui.click(window_x, window_y)
        time.sleep(2)

        print("[SUCCESS] Window focused")
    except Exception as e:
        print(f"[WARN] Focus error: {e}")

    # Step 4: Search for contact with more delays
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

        # Select the contact
        pyautogui.press('enter')
        time.sleep(5)  # INCREASED wait after selecting

        print("[SUCCESS] Contact selected")
    except Exception as e:
        print(f"[ERROR] Contact search failed: {e}")
        return False

    # Step 5: Send the message with better handling
    print(f"\n[STEP 5] Sending message: '{message}'")
    try:
        # Click in message area - try multiple positions
        msg_x = telegram_win.left + (telegram_win.width // 2)
        msg_y = telegram_win.top + telegram_win.height - 100

        # Try clicking multiple times to ensure focus
        for i in range(3):
            pyautogui.click(msg_x, msg_y)
            time.sleep(1)

        # Clear any existing text
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

        # Send the message
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

    # Take screenshot to see what's happening
    screenshot = pyautogui.screenshot()
    screenshot.save('telegram_search_debug.png')
    print("Screenshot saved as 'telegram_search_debug.png'")

    # Try clicking
    screen_width, screen_height = pyautogui.size()
    search_result_x = int(screen_width * 0.15)
    search_result_y = int(screen_height * 0.25)
    print(f"Clicking at ({search_result_x}, {search_result_y})...")
    pyautogui.click(x=search_result_x, y=search_result_y)