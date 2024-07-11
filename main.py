import numpy as np
from cvzone.HandTrackingModule import HandDetector
from enum import Enum
from Objects import *


class DrawStyle(Enum):
    SOLID = 0
    TRANSPARENT = 1

W, H = 3, 4

Transperency = True

cap = cv2.VideoCapture(0)
cap.set(W, 1200)
cap.set(H, 720)

detector = HandDetector(detectionCon=0.8)


cx, cy, w, h = 100, 100, 200, 200


def isRecSelected(recList):
    for rec in recList:
        if rec.selected: return True
    return False


addrect = AddRect([100,100])
AddRect.rectList.append(DragRect([150,150]))


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=False)



    if hands:
        lmList = hands[0]["lmList"]

        l, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])

        print(l)

        if l < 52:

            cursor = lmList[8] # index finger tip

            addrect.update(cursor)

            # Call the update here
            for i in range(len(AddRect.rectList)):
                if AddRect.rectList[i].selected or not isRecSelected(AddRect.rectList):
                    AddRect.rectList[i].update(cursor)



        else:
            colorR = (255, 182, 56)



    if Transperency:
        imgNew = np.zeros_like(img, np.uint8)
        for i in range(len(AddRect.rectList)):
            AddRect.rectList[i].draw(imgNew, cornerRect=True)
        addrect.draw(imgNew)
        out = img.copy()
        alpha = 0.5
        mask = imgNew.astype(bool)
        out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
        img = out
    else:
        addrect.draw(img)
        for i in range(len(AddRect.rectList)):
            AddRect.rectList[i].draw(img, cornerRect=True)



    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("t"):
        Transperency = not Transperency

    if key == ord("q"):
        break
