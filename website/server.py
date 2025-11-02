#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_from_directory
import pyautogui
from time import sleep
import os

### Desktop Logic ###
ACTIONS = {
    "forward": lambda: press_for("w", 1),
    "backward": lambda: press_for("s", 1),
    "interact": lambda: pyautogui.click(button="right"),
    "shoot": lambda: pyautogui.click(),
    "strafe_left": lambda: pyautogui.press_for("a",1),
    "strafe_right": lambda: pyautogui.press_for("d",1),
    "camera_left": lambda: press_for("left", 1),
    "camera_right": lambda: press_for("right", 1),
}

def press_for(key, duration):
    pyautogui.keyDown(key)
    sleep(duration)
    pyautogui.keyUp(key)

def execute_action(action):
    try:
        print(f"Received action: {action}. Executing...")
        # Execute corresponding desktop action
        func = ACTIONS[action]
        func()

    except TypeError as e:
        print(f"{action} is an invalid action. Not executing... {e}")

    except Exception as e:
        print(f"No message parsed: {e}")


### Website Code ###
app = Flask(__name__)
app.config['VIDEO_FOLDER'] = os.path.join(app.root_path, 'static', 'videos')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/action/<string:action_id>', methods=['POST'])
def action(action_id):
   execute_action(action_id)
   return '', 204

@app.route('/video/<int:video_id>', methods=['GET'])
def video(video_id):
   return send_from_directory(app.config['VIDEO_FOLDER'], f"{video_id}.mp4")

if __name__ == '__main__':
    # For development only
    app.run(host='0.0.0.0', port=8000, debug=True)
