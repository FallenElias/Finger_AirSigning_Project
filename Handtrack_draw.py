import cv2
import mediapipe as mp
import numpy as np

# Set up video capture from default camera
cap = cv2.VideoCapture(0)

# Set up MediaPipe hand detection
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Initialize list of finger positions
finger_positions = []
drawing_started = False
drawing_points = []
drawing_lists = []

# Main loop for video capture and hand detection
while True:
    # Capture a frame from the camera
    success, image = cap.read()
    image = cv2.flip(image, 1)

    # Convert the color space of the image from BGR to RGB
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Use MediaPipe to detect hand landmarks in the image
    results = hands.process(imageRGB)

    # Check if any hands were detected in the image
    if results.multi_hand_landmarks:
        # Loop through all detected hands
        for handLms in results.multi_hand_landmarks:
            # Loop through all the landmarks of the current hand
            for id, lm in enumerate(handLms.landmark):
                # Get the pixel coordinates of the landmark
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                
                # If the current landmark is the tip of the index finger
                if id == 8:
                    # Add its position to the list
                    finger_positions.append((cx, cy))

                    # If the finger is up and drawing has not yet started, start a new drawing list
                    if not drawing_started:
                        drawing_started = True
                        drawing_points = []
                        drawing_lists.append(drawing_points)
                    # If the finger is up and drawing has already started, add the position to the current drawing list
                    else:
                        drawing_points.append((cx, cy))

                    cv2.circle(image, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                else:
                    drawing_started = False

            # Draw the landmarks and connections on the image using MediaPipe
            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

    # Draw all the completed drawings on the image
    for points in drawing_lists:
        if len(points) > 0:
            curve = np.array(points)
            cv2.polylines(image, [curve], False, (255, 0, 0), 3)

    # Display the image on the screen
    cv2.imshow("Output", image)

    # Check for the Esc key to stop the program
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
