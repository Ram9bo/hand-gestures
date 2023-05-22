import numpy as np

def detect_direction(all_landmarks):
    detected_directions = []
    # For each hand
    for hand_landmarks in all_landmarks:
        extended_counter = 0
        directions = ["left", "down", "right", "up"]
        # Landmark number
        tips = [4, 8, 12, 16, 20]
        midfinger = [2, 6, 10, 14, 18]
        lower_finger = [2, 5, 9, 13, 17]
        wrist_pos = hand_landmarks[0]
        big_dist = 0
        big_vect = None
        for i, tip in enumerate(tips):
            tip_pos = hand_landmarks[tip]
            midfinger_pos = hand_landmarks[midfinger[i]]
            # Thumb
            if tip == 4:
                # If thumb close to any midfinger, not extended thumb
                thumb_length = np.linalg.norm(tip_pos-midfinger_pos)
                extended_thumb = True
                for j in range(i+1, len(tips)):
                    # Dist thumb tip to midfinger
                    dist1 = np.linalg.norm(tip_pos-hand_landmarks[midfinger[j]])
                    # Dist thumb tip to base of the finger
                    dist2 = np.linalg.norm(tip_pos-hand_landmarks[lower_finger[j]])
                    if dist1 < thumb_length * 0.6 or dist2 < thumb_length * 0.6:
                        extended_thumb = False
                        break
                extended_counter += int(extended_thumb)
            else:
                # Check if vector from wrist to midfinger points
                # in same direction as vector from midfinger to tip
                upper_vect = tip_pos-midfinger_pos
                lower_vect = midfinger_pos - wrist_pos
                extended_counter += int(np.dot(upper_vect, lower_vect) > 0)
            # Detect most extended finger
            vector = tip_pos - wrist_pos
            dist = np.linalg.norm(vector)
            if dist > big_dist:
                big_dist = dist
                big_vect = vector
        # Find direction of most extended finger
        coord = np.argmax(np.abs(big_vect))
        coord = coord + 2 if big_vect[coord] < 0 else coord
        direction = directions[coord]
        detected_directions.append([direction, extended_counter])
    return detected_directions