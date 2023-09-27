import cv2
import numpy as np
import math
import mediapipe as mp
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
while True:
    success, img = cap.read()
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx, cy = int (lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])

        if lmList:
            x1,y1 = lmList[4][1], lmList[4][2]
            x2,y2 = lmList[8][1], lmList[8][2]
            cv2.circle(img, (x1,y1), 10, (0,255,0), cv2.FILLED)
            cv2.circle(img, (x2,y2), 10, (0,255,0), cv2.FILLED)
            cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 3)

            length = math.hypot(x2-x1, y2-y1)
            if length < 50:
                z1 = (x1+x2)//2
                z2 = (y1+y2)//2
                cv2.circle(img, (z1,z2), 15, (255,0,0), cv2.FILLED)

        volRange = volume.GetVolumeRange()
        minVol = volRange [0]
        maxVol = volRange [1]
        vol = np.interp(length, [50,300],[minVol, maxVol])
        volBar = np.interp(length, [50,300], [400,150])
        volume.SetMasterVolumeLevel(vol,None)
        cv2.rectangle(img, (50,150), (85,400), (0,255,0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85,400), (255,0,0), cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    