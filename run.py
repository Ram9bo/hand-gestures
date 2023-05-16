import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe import ImageFormat
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from direction import detect_direction

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green


class Detector:

    def __init__(self):
        self.base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
        self.options = vision.GestureRecognizerOptions(base_options=self.base_options, num_hands=2)
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)
        base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
        options = vision.HandLandmarkerOptions(base_options=base_options,num_hands=2)
        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, image):
        result = self.detector.detect(image)
        landmarks = dict()

        if len(result.hand_landmarks) <= 0:
            return "None", landmarks, image.numpy_view()

        for i in range(21):
            landmark = result.hand_landmarks[0][i]
            landmarks[i] = np.array([landmark.x, landmark.y])

        annotated_image = draw_landmarks_on_image(image.numpy_view(), result, "None")

        return "None", landmarks, annotated_image

    def recognize(self, image):
        result = self.recognizer.recognize(image)
        landmarks = dict()

        top_gesture = None
        if len(result.gestures) > 0:
            top_gesture = result.gestures[0][0]

        if len(result.hand_landmarks) <= 0:
            return top_gesture, landmarks, image.numpy_view()

        for i in range(21):
            landmark = result.hand_landmarks[0][i]
            landmarks[i] = np.array([landmark.x, landmark.y])

        annotated_image = draw_landmarks_on_image(image.numpy_view(), result, top_gesture.category_name)

        return top_gesture.category_name, landmarks, annotated_image



def draw_landmarks_on_image(rgb_image, detection_result, gesture):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)
  if (len(hand_landmarks_list)) == 2:
      print("2 hands")

    #print(len(hand_landmarks_list))

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    # Draw the hand landmarks.
    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
    ])
    #annotated_image = annotated_image.item().numpy_view()
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      hand_landmarks_proto,
      solutions.hands.HAND_CONNECTIONS,
      solutions.drawing_styles.get_default_hand_landmarks_style(),
      solutions.drawing_styles.get_default_hand_connections_style())

    # Get the top left corner of the detected hand's bounding box.
    height, width, _ = annotated_image.shape
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    text_x = int(min(x_coordinates) * width)
    text_y = int(min(y_coordinates) * height) - MARGIN

    for i, l in enumerate(hand_landmarks):
        h_x = int(hand_landmarks[i].x * width)
        h_y = int(hand_landmarks[i].y * height)
        cv2.putText(annotated_image, str(i), (h_x, h_y), cv2.FONT_HERSHEY_DUPLEX, FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    # Draw handedness (left or right hand) on the image.
    cv2.putText(annotated_image, f"{handedness[0].category_name}",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    cv2.putText(annotated_image, str(gesture),
                (text_x, int(text_y - 20 * FONT_SIZE)), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = Detector()

    prev_gesture = None
    prev_direction = None
    while True:
        ret, frame = cap.read()
        image = frame
        frame = mp.Image(image_format=ImageFormat.SRGB, data=frame)
        gesture, landmarks, annotated = detector.detect(frame)
        cv2.imshow("Annotated", annotated)
        cv2.waitKey(1)

        if gesture != prev_gesture:
            print("Gesture", gesture)
            prev_gesture = gesture
        if len(landmarks) > 0:
            direction = detect_direction(landmarks)
            print("Direction", detect_direction(landmarks))
            if prev_direction != direction:
                pass
            prev_direction = direction
