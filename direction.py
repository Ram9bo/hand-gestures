import numpy as np

def detect_direction(landmarks):
    directions = ["right", "up", "left", "down"]
    tips = [4, 8, 12, 16, 20]
    wrist_pos = landmarks[0]
    big_dist = 0
    big_vect = None
    for tip in tips:
        tip_pos = landmarks[tip]
        vector = tip_pos - wrist_pos
        dist = np.linalg.norm(vector)
        if dist > big_dist:
            big_dist = dist
            big_vect = vector
    coord = np.argmin(big_vect)
    coord = coord + 2 if big_vect[coord] < 0 else coord
    direction = directions[coord]
    return direction
    


