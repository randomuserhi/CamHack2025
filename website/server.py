#!/usr/bin/env python3
from flask import Flask, request, jsonify
import pyautogui
from time import sleep 

### Desktop Logic ###
# Maps from received gestures to desktop actions
GESTURE_ACTIONS = {
    "up": lambda: press_for("w", 1),                  # scroll to move forward
    "down": lambda: press_for("s", 1),                # scroll to move back 
    "tap": lambda: pyautogui.click(button="right"),   # interact
    "double_tap": lambda: pyautogui.click(),          # like to shoot 
    "like": lambda: pyautogui.click(),                # alternative shoot input
    "share": lambda: pyautogui.press_for("a",1),      # move left
    "save": lambda: pyautogui.press_for("d",1),       # move right
    "comments": "comments" 
}

COMMENT_ACTIONS = {
    "left": lambda: press_for("left", 1),              # scroll to look left
    "right": lambda: press_for("right", 1),            # scroll to look right
    "exit": "comments"
}

actions = [GESTURE_ACTIONS, COMMENT_ACTIONS]
list_item = 0
def next():
    global list_item                      #allows list_item to be overwritten from within function
    print("Switching Active Action Dict")
    item = actions[list_item]
    list_item = (list_item+1)%len(actions)
    return item 
active = next()

def press_for(key, duration):
    pyautogui.keyDown(key)
    sleep(duration)
    pyautogui.keyUp(key)

def execute_action(gesture):
    global active
    try:
        print(f"Received gesture: {gesture}. Executing...")
        # Execute corresponding desktop action
        if gesture=="comments":
            active = next()
        else:
            action = active.get(gesture)
            action()

    except TypeError as e:
        print(f"{gesture} is an invalid action. Not executing... {e}")

    except Exception as e:
        print(f"No message parsed: {e}")


### Website Code ###
app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/swipe', methods=['POST'])
def swipe():
    direction = request.args.get('direction')
    if not direction:
        return jsonify({"error": "'direction' parameter is required"}), 400

    execute_action(direction)

    return '', 204

@app.route('/tap', methods=['POST'])
def tap():
    double = request.args.get('double')

    if double is None:
        execute_action("tap")
    else:
        execute_action("double_tap")

    return '', 204

@app.route('/button/<string:button_id>', methods=['POST'])
def button(button_id):

   execute_action(button_id)
   return '', 204

if __name__ == '__main__':
    # For development only
    app.run(host='0.0.0.0', port=8000, debug=True)



