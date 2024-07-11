import cv2
import cvzone

colorR = (255, 182, 56)

class Box:

    def __init__(self, posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size = size
        self.selected = True

    def _update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            # colorR = (0, 255, 0)
            self.posCenter = cursor[:2]
            self.selected = True
        else:
            self.selected = False

        return self.selected

    def draw(self, img, cornerRect=False):
        cx, cy = self.posCenter
        w, h = self.size

        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)

        if cornerRect:
            cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h),20, rt=0, colorC=(182, 255, 56))
        return img

class DragRect(Box):


    def __init__(self, posCenter, size=[200,200]):
        super().__init__(posCenter, size)

    def update(self, cursor):
        if self._update(cursor): self.posCenter = cursor[:2]



class AddRect(Box):
    rectList = []

    def __init__(self, posCenter, size=[50, 50]):
        self.posCenter = posCenter
        self.size = size
        self.selected = False

    def update(self, cursor):
        if self._update(cursor): AddRect.rectList.append(DragRect([150, 150]))


