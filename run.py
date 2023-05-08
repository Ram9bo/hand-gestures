import cv2
import mediapipe as mp
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from direction import detect_direction
from mediapipe import ImageFormat
import time
import PIL

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green


class Detector:

    def __init__(self):
        self.base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
        self.options = vision.GestureRecognizerOptions(base_options=self.base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)

    def detect(self, image):
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

        annotated_image = draw_landmarks_on_image(image, result)

        return top_gesture.category_name, landmarks, annotated_image



def draw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    # Draw the hand landmarks.
    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
    ])
    annotated_image = annotated_image.item().numpy_view()
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

    # Draw handedness (left or right hand) on the image.
    cv2.putText(annotated_image, f"{handedness[0].category_name}",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image

if __name__ == '__main__':
    vid = cv2.VideoCapture(0)
    detector = Detector()

    while True:
        ret, frame = vid.read()
        image = frame
        frame = mp.Image(image_format=ImageFormat.SRGB, data=frame)
        gesture, landmarks, annotated = detector.detect(frame)
        annotated = PIL.Image.fromarray(np.uint8(annotated))
        annotated.show()

        print("Gesture", gesture)
        if len(landmarks) > 0:
            print("Direction", detect_direction(landmarks))
        else:
            print(landmarks)
