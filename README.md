# Thanos_Snap
A program that allow AI model to detect your finger snap and hence randomly delete half of your tabs 

Perfectly balanced , as all things should be .

### OVERVIEW & FEATURES

It is a program using real-time AI posture monitoring system built using python , opencv , mediapipe from google, PyAutoGUI , Tkinter
It can detects your finger gesture&snap and hence start randomly deleting half of your tabs .

### How It Works ?
So when you click start , a window will pop up to ask you to input the exact number of tabs you have. 
(yes you have to key in the number , as the developer is too noob/lazy to develope a method of finding the number of tabs using the limited tools he have)
Then program activates the webcam and uses google's mediapipe to track the corrdinate of your fingers . 
It focus on two specific points :  Landmark 4-the tip of the thumb and Landmark 12-the tip of middle finger
It then calculates the distance between thumb and middle finger. A pre-adjusted threshold is to determine whether the distance is close enough to enter the next stage.
In next stage, if the distance suddenly increased too much(more than a pre-adjusted parameter) within certain time (same) , the program confirm it's a snap and excutes deleting process with a system alert sound. 
The deleting process uses pyautoGUI to execute Alt+Tab on your keyboard , this is to switch from the code editor to browser behind it . 
Then followed by Ctrl+1 to jump to the first tab, decide ramdomly whether to close it using Ctrl+w or jump to the next tab using Ctrl+Tab . This process repeats for the number of times you entered previously. ( because it's hard for program to tell whether a complete round of tabs is done or not as they can't see the screen )

### Installation
0: download everything 
1: copy code to whatever IDE you have, enter the following to your terminal 
pip install opencv-python mediapipe pyautogui
2: make sure 'hand_landmarker.task' file is in the same directory as the script.
3: run (make sure your browser is right behind your code editor so Alt+tab switches to it)


Beware this program actually closes your tabs 
