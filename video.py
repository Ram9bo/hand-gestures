import cv2

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()
    image = frame