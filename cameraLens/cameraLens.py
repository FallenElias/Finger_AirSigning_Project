# %%
#run on airwriting venv py 3.9.16 prooved
# All imports
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import mediapipe as mp
import imutils


# %%
mphands = mp.solutions.hands
hands = mphands.Hands()
mp_drawing = mp.solutions.drawing_utils

# %%
def find_marker(image, finger_positions):
    result = hands.process(image)
    hand_landmarks = result.multi_hand_landmarks
    box = None

    if hand_landmarks:
        for handLMs in hand_landmarks:
            x_max = 0
            y_max = 0
            x_min = float('inf')
            y_min = float('inf')

            for id, lm in enumerate(handLMs.landmark):
                if id == 8 :
                    # Get the pixel coordinates of the landmark
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    finger_positions.append((cx, cy))

                x, y = int(lm.x * image.shape[1]), int(lm.y * image.shape[0])
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
            # compute the center and size of the bounding box
            center_x = (x_min + x_max) // 2
            center_y = (y_min + y_max) // 2
            width = x_max - x_min
            height = y_max - y_min
            angle = 0  # the angle is always 0 for an upright bounding box
            box = ((center_x, center_y), (width, height), angle)

            mp_drawing.draw_landmarks(image, handLMs, mphands.HAND_CONNECTIONS)
            
    return box

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth


# %%
def draw_signature(image, finger_positions) :
    curve = []
    for i in finger_positions :
        if i != "stop" :
            curve.append(i)
        elif len(curve) > 0:
            curve = np.array(curve)
            cv2.polylines(image, [curve], False, (255, 0, 0), 3)
            curve = []


# %%

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 24.0
# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 5.0
# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length

# %%
finger_positions = []
compteur = 0
start = False
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use appropriate codec for your system
out = cv2.VideoWriter("output.mp4", fourcc, 30.0, (640, 480))
hand = cv2.imread( "main.png")
alpha = 0.1
beta = ( 1.0 - alpha )
height, width, _ = hand.shape

for i in range(height):
    for j in range(width):
        # hand[i, j] is the RGB pixel at position (i, j)
        # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
        if hand[i, j].sum() == 0:
            hand[i, j] = [255, 255, 255]

while True:
	ret, frame = cap.read()
	if ret:
		frame = cv2.flip(frame, 1)

		if start :
			marker = find_marker(frame, finger_positions)
			if marker :
				inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])   

				if inches/12 > 4 :
					dot_color = (0, 0, 255)  # red
					finger_positions.pop()
					compteur +=1
				else :
					dot_color = (0, 255, 0)  # green
					compteur = 0
				
				# Draw a circle at the dot location with the desired color and radius
				dot_radius = 20
				cv2.circle(frame, (30, 30), dot_radius, dot_color, -1)
			
				# draw a bounding box around the image and display it
				box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
				box = np.int0(box)
				#cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
				#cv2.putText(frame, "%.2fft" % (inches / 12),
				#	(frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
				#	2.0, (0, 255, 0), 3)
				
			else :
				compteur += 1 

			finger_positions.append("stop")
			draw_signature(frame, finger_positions)
			
			if compteur <= 5 :
				finger_positions.pop()
			else :
				compteur = 0
			out.write(frame)
		
		else :
			result = hands.process(frame)
			hand_landmarks = result.multi_hand_landmarks
			if hand_landmarks:
				for handLMs in hand_landmarks:
					mp_drawing.draw_landmarks(frame, handLMs, mphands.HAND_CONNECTIONS)
			
			src1 = cv2.resize(hand, (frame.shape[1], frame.shape[0]))
			frame = cv2.addWeighted(src1, alpha, frame, beta, 0.0)

		cv2.imshow("image", frame)

		if cv2.waitKey(1) & 0xFF == ord(' '):
			marker = find_marker(frame, [])	
			if marker :
				start = True
				focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
			
		# Exit recording if 'q' is pressed
		if cv2.waitKey(1) & 0xFF == ord('q'):
			signature = np.zeros((480, 640, 3), dtype=np.uint8)
			signature.fill(255)

			# Draw the lines connecting the coordinates
			finger_positions.append("stop")
			draw_signature(signature, finger_positions)

			# Display the signature
			cv2.imwrite("drawing.png", signature)
			cv2.imshow("Drawing", signature)
			cv2.waitKey(0)

			break
	else:
		break

out.release() 
cap.release()
cv2.destroyAllWindows()


