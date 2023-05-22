import cv2
import mediapipe as mp
from direction import detect_direction
import numpy as np
from ps_connect import send_command
import paramiko

def detect_hands(image, hands):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize the hand landmark model
    mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2)

    # Process the image
    results = mp_hands.process(image_rgb)

    marks = []
    # Check if landmarks were detected
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[i].classification[0].label
            if handedness not in hands:
                continue
            landmarks = []
            # Draw the landmarks on the image
            mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            for landmark in hand_landmarks.landmark:
                landmarks.append(np.array([landmark.x, landmark.y]))

            marks.append(landmarks)

    mp_hands.close()
    return image, marks


if __name__=='__main__':
    hostname = "192.168.101.252"
    username = 'pi'
    password = 'raspberry'
    dir_path = '/home/pi/picar-4wd/final_project/control.py'
    command = 'python3 ' + dir_path
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname,username=username,password=password)
    except paramiko.AuthenticationException:
        print("Failed to connect to %s due to wrong username/password" %hostname)
        exit(1)
    except Exception as e:
        print(e)    
        exit(2)
        

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    prev_gesture = None
    prev_direction = None
    print("Type how many hands you want to use for gesture control: (1 / 2)")
    num_hands = input()
    if num_hands == "1":
        print("Type which hand you want to use for gesture control: (L / R)")
        hand = input().lower()
        if (hand == "l" or hand == "left"):
            hands = ["Right"]
        elif (hand == "r" or hand == "right"):
            hands = ["Left"]
        else:
            raise TypeError("The input received doesn't correspond to a hand")
    else:
        hands = ["Left", "Right"]

    prev_speed = 0
    prev_angle = 0
    while True:
        ret, frame = cap.read()
        frame, all_landmarks = detect_hands(frame, hands)
        # Display the image with landmarks
        cv2.imshow('Hand Landmarks', frame)
        cv2.waitKey(1)

        speed = 0
        angle = 0
        if len(all_landmarks) > 0:
            direction = detect_direction(all_landmarks)
            for hand_command in direction:
                direction = hand_command[0]
                fingers = hand_command[1]
                if direction == "up":
                    speed += fingers
                elif direction == "down":
                    speed -= fingers
                elif direction == "right":
                    angle += fingers
                elif direction == "left":
                    angle -= fingers
        speed = np.clip(speed, -5, 5)
        angle = np.clip(angle, -5, 5)
        
        if speed != prev_speed or angle != prev_angle:
            send_command(speed, angle, ssh, command)
        prev_speed = speed
        prev_angle = angle

                    
