import cv2
import time
from hand_detector import HandDetector
from gesture_classifier import GestureClassifier
from emoji_overlay import EmojiOverlay

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    # Initialize hand detector
    detector = HandDetector(detection_con=0.7, max_hands=1)
    classifier = GestureClassifier()
    overlay = EmojiOverlay()
    
    p_time = 0
    c_time = 0

    print("Starting hand2emoji... Press 'q' to exit.")

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            break

        # Flip image for mirror effect
        img = cv2.flip(img, 1)

        # Find hands
        img = detector.find_hands(img)
        lm_list = detector.find_position(img, draw=False)

        if len(lm_list) != 0:
            gesture = classifier.get_gesture(lm_list)
            
            # Draw gesture name
            cv2.putText(img, gesture, (10, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

            # Overlay emoji
            emoji_img = overlay.get_emoji_image(gesture)
            if emoji_img is not None:
                # Use wrist or center of palm as anchor? 
                # Wrist is ID 0. Middle finger MCP is ID 9. 9 is a good center approximation.
                cx, cy = lm_list[9][1], lm_list[9][2]
                img = overlay.overlay_emoji(img, emoji_img, cx, cy)

        # Calculate FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("hand2emoji", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
