
import os
import sys
import subprocess
import time



import tkinter as tk
from tkinter import simpledialog


def get_initial_count():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    res = simpledialog.askinteger("Thanos's preparations", "How many targets are there in the universe(Tabs)?",
                                  parent=root, minvalue=1, maxvalue=100)
    root.destroy()
    return res


target_tabs = get_initial_count()


if not target_tabs:
    print("Nothing is entered")
    sys.exit()


import mediapipe as mp
import cv2
import math
import pyautogui
import winsound
import random




pyautogui.FAILSAFE = True




current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'hand_landmarker.task')


BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)


prev_dist = 0
last_snap_time = 0
ready_timer = 0
cap = cv2.VideoCapture(0)


print(f"Targeted :{target_tabs} Tabs")
print(" make sure your chrome is right behind VS Code(or whatever platform you use for program) (just make sure use Alt+Tab can jump there)")


with HandLandmarker.create_from_options(options) as landmarker:
    print("V")
   
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
       
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        result = landmarker.detect_for_video(mp_image, int(time.time()*1000))
       
        cv2.putText(frame, f"Target: {target_tabs} Tabs", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)


        if result.hand_landmarks:
            pts = result.hand_landmarks[0]
            dist = math.hypot(pts[4].x - pts[12].x, pts[4].y - pts[12].y)
            current_time = time.time()
           
            cv2.circle(frame, (int(pts[4].x*w), int(pts[4].y*h)), 6, (0, 255, 0), -1)
            cv2.circle(frame, (int(pts[12].x*w), int(pts[12].y*h)), 6, (0, 255, 0), -1)


            if dist < 0.05:
                ready_timer = current_time
                cv2.putText(frame, "READY", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)
            elif (current_time - ready_timer < 0.5) and (dist - prev_dist > 0.08):
                if current_time - last_snap_time > 3.0:
                    print(" !!!SNAP!!! ")
                    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
                   


                    pyautogui.hotkey('alt', 'tab')
                    time.sleep(0.6)
                   
                    kill_indices = random.sample(range(target_tabs), target_tabs // 2)
                    kill_indices.sort()
                   
                    pyautogui.hotkey('ctrl', '1')
                    time.sleep(0.4)
                   
                    for i in range(target_tabs):
                        if i in kill_indices:
                            pyautogui.keyDown('ctrl')
                            pyautogui.press('w')
                            pyautogui.keyUp('ctrl')
                            print(f"[{i+1}] 抹除")
                        else:
                            pyautogui.keyDown('ctrl')
                            pyautogui.press('tab')
                            pyautogui.keyUp('ctrl')
                            print(f"[{i+1}] left")
                        time.sleep(0.25)
                   
                    print(f"Mission accomplished: The universe has reached equilibrium.")
                    last_snap_time = current_time
                    break
           
            prev_dist = dist
       
        cv2.imshow('THANOS ULTIMATE', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break


cap.release()
cv2.destroyAllWindows()

