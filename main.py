import cv2
from cvzone.HandTrackingModule import HandDetector

W, H = 3, 4

cap = cv2.VideoCapture(0)
cap.set(W, 1200)
cap.set(H, 720)

detector = HandDetector(detectionCon=0.8)

colorR = (255,0,255)

cx, cy, w, h = 100, 100, 200, 200



class DragRect():


    def __init__(self, posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size = size
        self.selected = True

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - w // 2 < cursor[1] < cy + w // 2:
            #colorR = (0, 255, 0)
            self.posCenter = cursor[:2]
            self.selected = True
        else:
            self.selected = False

    def draw(self, img):
        cx, cy = self.posCenter
        w, h = self.size

        cv2.rectangle(img, (cx - w // 2, cy - w // 2), (cx + w // 2, cy + w // 2), colorR, cv2.FILLED)

        return img


rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150,150]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)


    if hands:
        lmList = hands[0]["lmList"]

        l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img, draw=False)

        print(l)

        if l < 52:

            cursor = lmList[8] # index finger tip

            # Call the update here
            for i in range(5):
                rectList[i].update(cursor)

        else:
            colorR = (255,0,255)

    for i in range(5):
        rectList[i].draw(img)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
