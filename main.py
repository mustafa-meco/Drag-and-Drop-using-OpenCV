import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from enum import Enum

class DrawStyle(Enum):
    SOLID = 0
    TRANSPARENT = 1

W, H = 3, 4

Transperency = True

cap = cv2.VideoCapture(0)
cap.set(W, 1200)
cap.set(H, 720)

detector = HandDetector(detectionCon=0.8)

colorR = (255, 182, 56)

cx, cy, w, h = 100, 100, 200, 200

rectList = []

class DragRect():


    def __init__(self, posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size = size
        self.selected = True



    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            #colorR = (0, 255, 0)
            self.posCenter = cursor[:2]
            self.selected = True
        else:
            self.selected = False

    def draw(self, img, cornerRect=False):
        # if drawStyle == DrawStyle.SOLID:
            cx, cy = self.posCenter
            w, h = self.size

            cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)

            if cornerRect:
                cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h),20, rt=0, colorC=(182, 255, 56))
            return img

        # elif drawStyle == DrawStyle.TRANSPARENT:
        #     cx, cy = self.posCenter
        #     w, h = self.size
        #
        #     cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        #
        #     if cornerRect:
        #         cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)
        #
        #     return out


class AddRect():
    def __init__(self, posCenter, size=[50, 50]):
        self.posCenter = posCenter
        self.size = size
        self.selected = False

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2 and not self.selected:
            rectList.append(DragRect([150, 150]))
            self.selected = True
        else:
            self.selected = False

    def draw(self, img, cornerRect=False):
        # if drawStyle == DrawStyle.SOLID:
            cx, cy = self.posCenter
            w, h = self.size

            cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), (182, 255, 56), cv2.FILLED)

            if cornerRect:
                cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h),20, rt=0, colorC=(182, 255, 56))
            return img


def isRecSelected(recList):
    for rec in recList:
        if rec.selected: return True
    return False


addrect = AddRect([100,100])
rectList.append(DragRect([150,150]))


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
            for i in range(len(rectList)):
                if rectList[i].selected or not isRecSelected(rectList):
                    rectList[i].update(cursor)



        else:
            colorR = (255, 182, 56)



    if Transperency:
        imgNew = np.zeros_like(img, np.uint8)
        for i in range(len(rectList)):
            rectList[i].draw(imgNew, cornerRect=True)
        addrect.draw(imgNew)
        out = img.copy()
        alpha = 0.5
        mask = imgNew.astype(bool)
        out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
        img = out
    else:
        addrect.draw(img)
        for i in range(len(rectList)):
            rectList[i].draw(img, cornerRect=True)



    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("t"):
        Transperency = not Transperency

    if key == ord("q"):
        break
