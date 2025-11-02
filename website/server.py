#!/usr/bin/env python3
from flask import Flask, send_from_directory, make_response
import pyautogui
from time import sleep
import os

### Desktop Logic ###
MOUSE_HOLD_TIME = 0.1
KEY_HOLD_TIME = 0.3
TURN_HOLD_TIME = 0.1

ACTIONS = {
    "forward": lambda: press_for("w"),
    "backward": lambda: press_for("s"),
    "interact": lambda: mouse_click("right"),
    "shoot": lambda: mouse_click("left"),
    "strafe_left": lambda: pyautogui.press_for("a"),
    "strafe_right": lambda: pyautogui.press_for("d"),
    "camera_left": lambda: press_for("left", TURN_HOLD_TIME),
    "camera_right": lambda: press_for("right", TURN_HOLD_TIME),
}

class ActionException(Exception):
    pass

def mouse_click(button):
    pyautogui.mouseUp(button=button)
    sleep(MOUSE_HOLD_TIME)
    pyautogui.mouseDown(button=button)

def press_for(key, duration=KEY_HOLD_TIME):
    pyautogui.keyDown(key)
    sleep(duration)
    pyautogui.keyUp(key)

def execute_action(action):
    try:
        print(f"Received action: {action}. Executing...")
        # Execute corresponding desktop action
        func = ACTIONS[action]
        func()

    except KeyError as e:
        print(f"{action} action not recognised... {e}")
        raise ActionException(f"{action} action not recognised... {e}")

### Website Code ###
app = Flask(__name__)
app.config['VIDEO_FOLDER'] = os.path.join(app.root_path, 'static', 'videos')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/action/<string:action_id>', methods=['POST'])
def action(action_id):
    try:
        execute_action(action_id)
        return '', 204
    except ActionException:
        return make_response(f"Unable to run action {action_id}", 500)

@app.route('/video/<int:video_id>', methods=['GET'])
def video(video_id):
    return send_from_directory(app.config['VIDEO_FOLDER'], f"{video_id}.mp4")

if __name__ == '__main__':
    # For development only
    app.run(host='0.0.0.0', port=8000, debug=True)
