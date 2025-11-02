import pyautogui
import time 

def press_for(key, duration):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def execute_action(gesture):
    global active
    try:
        print(f"Received gesture: {gesture}")
        # Execute corresponding desktop action
        action = active.get(gesture)
        if action=="comments":
            active = next()
        else:
            action()

    except Exception as e:
        print(f"No message parsed: {e}")

