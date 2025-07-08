from app_control import test_telegram, send_telegram_message

# Test 1: Can we open Telegram?
print("TEST 1: Opening Telegram")
test_telegram()

# Wait for user confirmation
input("\nPress Enter after you see Telegram open (or if it failed)...")

# Test 2: Send a short message
print("\nTEST 2: Sending short message")
send_telegram_message("Paazi GGITS", "Test message")

# Test 3: Send a long message
print("\nTEST 3: Sending long message")
long_msg = "This is a long test message to check if the clipboard method works properly for messages that are longer than 30 characters."
send_telegram_message("Paazi GGITS", long_msg)