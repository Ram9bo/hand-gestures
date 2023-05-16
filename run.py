import cv2
import mediapipe as mp


def detect_hands(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize the hand landmark model
    mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2)

    # Process the image
    results = mp_hands.process(image_rgb)

    marks = []
    # Check if landmarks were detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
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

    while True:
        ret, frame = cap.read()
        frame, marks = detect_hands(frame)
        # Display the image with landmarks
        cv2.imshow('Hand Landmarks', frame)
        cv2.waitKey(1)
