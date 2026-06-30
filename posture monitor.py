import cv2
import mediapipe as mp
import time
import winsound  


BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="D:\GITHUB1_MONITOR\pose_landmarker_lite.task"),
    running_mode=VisionRunningMode.VIDEO
)


bad_posture_start_time = 0  
last_alert_time = 0        


with PoseLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0)
    print("Launched Succesfully")
    print("Note: Holding a bad posture for more than 1 second will trigger an alert.")


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break


        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
       
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        timestamp = int(time.time() * 1000)
        result = landmarker.detect_for_video(mp_image, timestamp)


        if result.pose_landmarks:
            for landmarks in result.pose_landmarks:
                ear_y = (landmarks[7].y + landmarks[8].y) / 2
                sho_y = (landmarks[11].y + landmarks[12].y) / 2
                diff = sho_y - ear_y


                ''' due to difference in the position of camera (mine is on the keyboard)
one should adjust the number until this program works smoothly. Expecially the choioce of
< or > sybol , as due to the angle of my camera i use > instead of < for convience .
(for camera on top of the scree, i recommand using < instead .)
                '''
                if diff > 0.50:
                    if bad_posture_start_time == 0:
                        bad_posture_start_time = time.time()
                   
                    current_time = time.time()
                    if (current_time - bad_posture_start_time > 1.0) and (current_time - last_alert_time > 3.0):
                        winsound.Beep(800, 500)
                        last_alert_time = current_time
                       
                    status = "Bad"
                    color = (0, 0, 255) 
                else:
                    bad_posture_start_time = 0
                    status = "Good"
                    color = (0, 255, 0) 


                cv2.putText(frame, f"{status} | Dist: {diff:.2f}", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
               
                for idx in [7, 8, 11, 12]:
                    cx, cy = int(landmarks[idx].x * w), int(landmarks[idx].y * h)
                    cv2.circle(frame, (cx, cy), 6, color, -1)


        cv2.imshow('Posture Guard V1.0 (Sound)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break


    cap.release()
    cv2.destroyAllWindows()
