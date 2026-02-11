class GestureClassifier:
    def __init__(self):
        self.tip_ids = [4, 8, 12, 16, 20]

    def get_gesture(self, lm_list):
        if len(lm_list) == 0:
            return None

        fingers = []

        # Thumb
        # specific logic for thumb (checking x coordinate might be needed depending on hand side, 
        # but for simplicity let's check if tip is to the left or right of IP joint)
        # Assuming right hand for now: thumb tip x < thumb ip x implies open
        # But to be generic, let's just check relative to the palm center or similar? 
        # Actually, for thumb, checking if tip is 'outside' the hand is better.
        # Simple heuristic: if tip.x < ip.x (for right hand)
        
        # Let's verify which hand it is or just use a simple heuristic for now.
        # Heuristic: Thumb tip is to the left/right of the MCP?
        # A simpler check: 
        if lm_list[self.tip_ids[0]][1] < lm_list[self.tip_ids[0] - 1][1]: # Check X coordinate
             fingers.append(1)
        else:
             fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]: # Check Y coordinate (up is lower value)
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = fingers.count(1)

        if total_fingers == 5:
            return "Open Hand"
        elif total_fingers == 0:
            return "Fist"
        elif fingers == [0, 1, 1, 0, 0] or fingers == [1, 1, 1, 0, 0]: # Victory (sometimes thumb is out)
            return "Victory"
        elif fingers == [1, 0, 0, 0, 0]: # Thumbs Up (strictly)
            return "Thumbs Up"
        elif fingers == [0, 1, 0, 0, 0] or fingers == [1, 1, 0, 0, 0]: # Pointing
            return "Pointing"
        elif fingers == [0, 0, 1, 0, 0]: # Middle Finger
            return "Middle Finger"
        else:
            return "Unknown"
