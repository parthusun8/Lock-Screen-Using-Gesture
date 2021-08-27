import ctypes
import math
import cv2
import handtrackingmodule as htm
import time

################################
wCam, hCam = 640, 480
################################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
detector = htm.handDetector(detect_con=0.7)

while True:
    success, img = cap.read()
    img = detector.find_Hands(img)
    Landmark_list = detector.locateHands(img, draw=False)
    label = detector.get_label(img)
    if len(Landmark_list) != 0:
        # print(Landmark_list[4], Landmark_list[8])
        x1, y1 = Landmark_list[4][1], Landmark_list[4][2]
        x2, y2 = Landmark_list[8][1], Landmark_list[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 7, (204, 255, 229), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (204, 255, 229), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (204, 255, 229), 2)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        if length < 50:
            ctypes.windll.user32.LockWorkStation()

        x3, y3 = Landmark_list[0][1], Landmark_list[0][2]
        cv2.putText(img, str(label), (x3, y3 + 20), cv2.QT_FONT_NORMAL,
                    0.5, (0, 255, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
