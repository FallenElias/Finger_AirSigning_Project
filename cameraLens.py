import cv2
import tkinter as tk
from PIL import ImageTk, Image
import mediapipe as mp
import imutils
import numpy as np



class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.begin = False

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(max_num_hands= 1, min_detection_confidence = 0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        # initialize the known distance from the camera to the object, which
        # in this case is 24 inches
        self.KNOWN_DISTANCE = 24.0
        # initialize the known object width, which in this case, the piece of
        # paper is 12 inches wide
        self.KNOWN_WIDTH = 5.0
        # load the furst image that contains an object that is KNOWN TO BE 2 feet
        # from our camera, then find the paper marker in the image, and initialize
        # the focal length
        self.finger_positions = []
        self.compteur = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use appropriate codec for your system
        self.out = cv2.VideoWriter("output.mp4", self.fourcc, 30.0, (640, 480))
        self.hand = cv2.imread( "main.png")
        self.alpha = 0.1
        self.beta = ( 1.0 - self.alpha )
        self.height, width, _ = self.hand.shape
        self.frame = 0
        self.curve = []
        self.saving = False

        # Création d'un Canvas pour afficher la vidéo
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        # Création des boutons "Démarrer" et "Recommencer"
        self.btn_start = tk.Button(window, text="Start", width=15, command=self.start)
        self.btn_start.pack(side="left", padx=10, pady=10)

        self.btn_save = tk.Button(window, text="Save", width=15, command=self.save)
        self.btn_save.pack(side="right", padx=10, pady=10)

        self.btn_reset = tk.Button(window, text="Reload", width=15, command=self.reset)
        self.btn_reset.pack(side="left", padx=10, pady=10)

        # Initialisation de la capture vidéo
        self.cap = cv2.VideoCapture(0)

        for i in range(self.height):
            for j in range(width):
		        # hand[i, j] is the RGB pixel at position (i, j)
		        # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
                if self.hand[i, j].sum() == 0:
                    self.hand[i, j] = [255, 255, 255]

        # Initialisation de l'image pour affichage dans le Canvas
        self.image = None

        # Affichage initial de la vidéo
        self.update()

        self.window.mainloop()

    def find_marker(self, finger_positions):
        result = self.hands.process(self.frame)
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
                        h, w, c = self.frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        finger_positions.append((cx, cy))

                    x, y = int(lm.x * self.frame.shape[1]), int(lm.y * self.frame.shape[0])
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

                self.mp_drawing.draw_landmarks(self.frame, handLMs, self.mphands.HAND_CONNECTIONS)
                
        return box

    def distance_to_camera(self, perWidth):
        # compute and return the distance from the maker to the camera
        return (self.KNOWN_WIDTH * self.focalLength) / perWidth


    # %%
    def draw_signature(self, image) :
        for i in self.finger_positions :
            if i != "stop" :
                self.curve.append(i)
            elif len(self.curve) > 0:
                self.curve = np.array(self.curve)
                cv2.polylines(image, [self.curve], False, (255, 0, 0), 3)
                self.curve = []


    def update(self):
        # Lecture de l'image de la vidéo
        if not self.saving:
            ret, self.frame = self.cap.read()

            if ret:
                self.frame = cv2.flip(self.frame, 1)

                if self.begin :
                    marker = self.find_marker(self.finger_positions)
                    if marker :
                        inches = self.distance_to_camera(marker[1][0])   

                        if inches/12 > 4 :
                            dot_color = (0, 0, 255)  # red
                            self.finger_positions.pop()
                            self.compteur +=1
                        else :
                            dot_color = (0, 255, 0)  # green
                            self.compteur = 0
                        
                        # Draw a circle at the dot location with the desired color and radius
                        dot_radius = 20
                        cv2.circle(self.frame, (30, 30), dot_radius, dot_color, -1)
                    
                        # draw a bounding box around the image and display it
                        box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
                        box = np.int0(box)
                        #cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
                        #cv2.putText(frame, "%.2fft" % (inches / 12),
                        #	(frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                        #	2.0, (0, 255, 0), 3)
                        
                    else :
                        self.compteur += 1 

                    self.finger_positions.append("stop")
                    self.draw_signature(self.frame)
                    
                    if self.compteur <= 5 :
                        self.finger_positions.pop()
                    else :
                        self.compteur = 0
                    self.out.write(self.frame)
                
                else :
                    result = self.hands.process(self.frame)
                    hand_landmarks = result.multi_hand_landmarks
                    if hand_landmarks:
                        for handLMs in hand_landmarks:
                            self.mp_drawing.draw_landmarks(self.frame, handLMs, self.mphands.HAND_CONNECTIONS)

                    src1 = cv2.resize(self.hand, (self.frame.shape[1], self.frame.shape[0]))
                    self.frame = cv2.addWeighted(src1, self.alpha, self.frame, self.beta, 0.0)

                # Conversion de l'image pour affichage dans le Canvas
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                self.image = ImageTk.PhotoImage(image)

                # Affichage de l'image dans le Canvas
                self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        else:
            # Conversion de l'image pour affichage dans le Canvas
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            self.image = ImageTk.PhotoImage(image)

            # Affichage de l'image dans le Canvas
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        # Mise à jour de la vidéo toutes les 15ms
        self.window.after(10, self.update)

    def start(self):
        # Démarrage de la capture vidéo
        marker = self.find_marker([])

        if marker :
            self.begin = True
            self.focalLength = (marker[1][0] * self.KNOWN_DISTANCE) / self.KNOWN_WIDTH

    def reset(self):
        # Reset de la capture vidéo
        self.finger_positions = []

    def save(self):
        signature = np.zeros((480, 640, 3), dtype=np.uint8)
        signature.fill(255)

        # Draw the lines connecting the coordinates
        self.finger_positions.append("stop")
        self.draw_signature(signature)
        self.frame = signature
        self.saving = True

        self.btn_start.destroy()
        self.btn_save.destroy()
        self.btn_reset.destroy()

        # Créer un nouveau bouton "Confirm"
        self.btn_confirm = tk.Button(window, text="Confirm", width=15, command=self.confirm)
        self.btn_confirm.pack(side="left", padx=10, pady=10)

        # Créer un nouveau bouton "Restart"
        self.btn_restart = tk.Button(window, text="Restart", width=15, command=self.restart)
        self.btn_restart.pack(side="left", padx=10, pady=10)

    def confirm(self):
        # Display the signature
        cv2.imwrite("drawing.png", self.frame)
        self.window.destroy()

    def restart(self):
        self.begin = False

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

        # initialize the known distance from the camera to the object, which
        # in this case is 24 inches
        self.KNOWN_DISTANCE = 24.0
        # initialize the known object width, which in this case, the piece of
        # paper is 12 inches wide
        self.KNOWN_WIDTH = 5.0
        # load the furst image that contains an object that is KNOWN TO BE 2 feet
        # from our camera, then find the paper marker in the image, and initialize
        # the focal length
        self.finger_positions = []
        self.compteur = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use appropriate codec for your system
        self.out = cv2.VideoWriter("output.mp4", self.fourcc, 30.0, (640, 480))
        self.hand = cv2.imread( "main.png")
        self.alpha = 0.1
        self.beta = ( 1.0 - self.alpha )
        self.height, width, _ = self.hand.shape
        self.frame = 0
        self.curve = []
        self.saving = False

        # Création des boutons "Démarrer" et "Recommencer"
        self.btn_start = tk.Button(window, text="Start", width=15, command=self.start)
        self.btn_start.pack(side="left", padx=10, pady=10)

        self.btn_save = tk.Button(window, text="Save", width=15, command=self.save)
        self.btn_save.pack(side="right", padx=10, pady=10)

        self.btn_reset = tk.Button(window, text="Reload", width=15, command=self.reset)
        self.btn_reset.pack(side="left", padx=10, pady=10)

        # Initialisation de la capture vidéo
        self.cap = cv2.VideoCapture(0)

        for i in range(self.height):
            for j in range(width):
		        # hand[i, j] is the RGB pixel at position (i, j)
		        # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
                if self.hand[i, j].sum() == 0:
                    self.hand[i, j] = [255, 255, 255]

        # Initialisation de l'image pour affichage dans le Canvas
        self.image = None
        self.btn_restart.destroy()
        self.btn_confirm.destroy()



window = tk.Tk()
app = App(window, "Ma fenêtre")
