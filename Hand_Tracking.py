import cv2
import mediapipe as mp
import time

'''https://mediapipe.readthedocs.io/en/latest/solutions/hands.html'''

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap is the object of VideoCapture class in the module cv2

mpHands = mp.solutions.hands
# This initiates the pipelines
hands = mpHands.Hands()
# hands is the object
# Hands is the class

mpDraw = mp.solutions.drawing_utils
# This is the function for drawing
# mpDraw is another object of the solutions.drawing_utils class


# solution is just another kind of module inside the mediapipe libraray which stores the frameworks for various objects

cTime = 0
pTime = 0
# For calculating the frames per second which the camera can identify

while True:
    succes, img = cap.read()
    img = cv2.flip(img, 1)
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    # This method generates the landmarks
    # process is a method

    if (results.multi_hand_landmarks):  # This method checks whether the number of hands are more than 0
        for handlms in results.multi_hand_landmarks:
            # hndlms are the individual hands among the multiple hands
            for id, lm in enumerate(handlms.landmark):
                # handlms are the individual hand and landmark are the array or the three values of that hand
                # handlms.landmark gives the data of each and every landmark
                # The values i.e x , y and z coordinates present in the lm are actually the screen ratio so we multiply it by the height and width to get the pixel value
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # Converting them to int as pixel value cannot be decimal
                print(id, cx, cy)
                # This will give the x and y coordinates of the pixel

                #  Now we will just decorate the fingertips a bit
                if (id == 4 or id == 8 or id == 12 or id == 16 or id == 20):
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    # cx and cy are the coordinates of the centre of the landmarks

            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)
            # landmarks are the 21 2D points described to plot the hand
            # Here if we do draw_landmarks(img , mpHands) then only the dots or the landmarks will be printed

    cTime = time.time()  # This will give the current time
    fps = 1 / (cTime - pTime)
    # As here in the loop only a single frame comes by cap.read thus we write 1 divided by the change in time
    # Thus giving the frames per second value very accuartely
    pTime = cTime
    # previous Time (pTime)  value get replaced by the value of current Time(cTime) thus for the advancement in calculation

    cv2.putText(img, f'FPS : {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
    # (10,70) is the coordinate or the pixel at which this text must be displayed
    # The value 3 represents the thickness and the length of the text

    cv2.imshow("Image", img)
    cv2.waitKey(1)
