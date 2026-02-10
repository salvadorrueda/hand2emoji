import cv2
import sys
import mediapipe as mp

def main():
    print(f"Python version: {sys.version}")
    
    print(f"MediaPipe version: {mp.__version__}")
    if hasattr(mp, '__file__'):
        print(f"MediaPipe location: {mp.__file__}")
    
    print("Checking mp.solutions...")
    try:
        if not hasattr(mp, 'solutions'):
            print("ERROR: mp.solutions IS MISSING from top level mediapipe module.")
            print("Available attributes in mp:", dir(mp))
            
            # Try explicit import as fallback
            print("Attempting explicit import: import mediapipe.python.solutions")
            import mediapipe.python.solutions as solutions
            mp.solutions = solutions
            print("Explicit import succeeded! mp.solutions patched.")
        
        print(f"mp.solutions detected: {mp.solutions}")
        print(f"mp.solutions.hands detected: {mp.solutions.hands}")
        
    except ImportError as e:
        print(f"ImportError during check: {e}")
    except AttributeError as e:
        print(f"AttributeError during check: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    # Initialize Hand Detector
    detector = None
    try:
        if hasattr(mp, 'solutions') and mp.solutions is not None:
            print("Initializing MediaPipe Hands...")
            mp_hands = mp.solutions.hands
            detector = mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7
            )
            mp_draw = mp.solutions.drawing_utils
            print("MediaPipe Hands initialized successfully.")
        else:
            print("WARNING: mp.solutions unavailable. Hand detection will be skipped.")
    except Exception as e:
        print(f"Error initializing Hand Detector: {e}")

    print("\nInitializing camera...")
    
    # Try index 0 first, then 1 if that fails
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Warning: Could not open camera at index 0. Trying index 1...")
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            print("Error: Could not open camera (tried index 0 and 1).")
            return

    print("Camera opened successfully. Window should appear. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        
        # Hand Detection Logic
        if detector:
            try:
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = detector.process(img_rgb)

                if results.multi_hand_landmarks:
                    for hand_lms in results.multi_hand_landmarks:
                        mp_draw.draw_landmarks(frame, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)
            except Exception as e:
                # Print error once to avoid spamming
                if "detection_error_logged" not in locals():
                    print(f"Error during hand detection: {e}")
                    detection_error_logged = True

        cv2.imshow('Debug Camera', frame)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if detector:
        detector.close()
    cap.release()
    cv2.destroyAllWindows()
    print("Camera closed.")

if __name__ == "__main__":
    main()
