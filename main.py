import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.65)

img1 = cv2.imread('img/pieces/piece_0.png')
img1 = cv2.resize(img1, (150, 150))
ox, oy = 200, 200

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    
    h, w, _ = img1.shape
    img[oy:oy+h, ox:ox+w] = img1
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()
