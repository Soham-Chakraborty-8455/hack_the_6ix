import cv2
import numpy as np
import Hand_Tracking_Module as ht
import pyautogui
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 700)
cap.set(4, 600)

detector = ht.HandDetector()


def getNumber(fingers):
    s = ""
    for i in fingers:
        s += str(i)

    if (s == "00000"):
        return 0
    elif (s == "01000"):
        return 1
    elif (s == "01100"):
        return "V"
    elif (s == "01110"):
        return 3
    elif (s == "01111"):
        return 4
    elif (s == "11111"):
        return 5
    elif (s == "10000"):
        return 6
    elif (s == "11000"):
        return 7
    elif (s == "11100"):
        return 8
    elif (s == "10111"):
        return 9
    elif (s == "10001"):
        return 10
    elif (s == "11001"):
        time.sleep(2)
        return pyautogui.press("space")
        
    elif (s == "01001"):
        return 30


while (True):
    _, img = cap.read()

    img = cv2.flip(img, 1)
    # Bilateral shift

    img = detector.findHands(img)

    idList = detector.findPosition(img, False)
    tipId = [4, 8, 12, 16, 20]

    if (len(idList) != 0):
        fingers = []
        if (idList[tipId[0]][1] < idList[tipId[0] - 2][1]):
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, len(tipId)):
            if (idList[tipId[id]][2] < idList[tipId[id] - 2][2]):
                fingers.append(1)
            else:
                fingers.append(0)

        cv2.putText(img, str(getNumber(fingers)), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 255), 20)

    cv2.imshow("Result", img)
    cv2.waitKey(1)
