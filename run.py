import cv2
import mediapipe as mp
from direction import detect_direction

def detect_hands(image, hands):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize the hand landmark model
    mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2)

    # Process the image
    results = mp_hands.process(image_rgb)

    if len(hands) == 1:
        for i, h in enumerate(results.handedness):
            if hands[0] in h[0].display_name:
                filtered_hand_landmarks = results.multi_hand_landmarks[i]
                break
    else:
        filtered_hand_landmarks = results.multi_hand_landmarks

    marks = []
    # Check if landmarks were detected
    if filtered_hand_landmarks:
        for hand_landmarks in filtered_hand_landmarks:
            landmarks = []
            # Draw the landmarks on the image
            mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            for landmark in hand_landmarks.landmark:
                landmarks.append((landmark.x, landmark.y))

            marks.append(landmarks)

    mp_hands.close()
    return image, marks


if __name__ == '__main__':
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
            hands = ["L"]
        elif (hand == "r" or hand == "right"):
            hands = ["R"]
        else:
            raise TypeError("The input received doesn't correspond to a hand")
    else:
        hands = ["L", "R"]

    while True:
        ret, frame = cap.read()
        frame, all_landmarks = detect_hands(frame)
        # Display the image with landmarks
        cv2.imshow('Hand Landmarks', frame)
        cv2.waitKey(1)

        speed = 0
        angle = 0

        if len(all_landmarks) > 0:
            direction = detect_direction(all_landmarks)
            print("Direction", direction)
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
