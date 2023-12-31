import cv2
import os
from cvzone.HandTrackingModule import HandDetector
from DragImg import DragImg
from boxPiece import BoxPiece

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.65)

def check(listImg): 
    for eli in listImg :
        for elj in  listImg :
            if eli == elj : continue

            oxi, oyi = eli.posOrigin
            oxj, oyj = elj.posOrigin

            if oxi == oxj and oyi==oyj : return False

    return True

def is_piece_in_box(self, imgObject, box):
        ox, oy = imgObject.posOrigin
        x1, y1 = box[0]
        x2, y2 = box[1]
        
        return (x1-10 <= ox <= x2+10) and (y1-10 <= oy <= y2+10)

dirPath = './img/pieceOH'
piecePath = os.listdir(dirPath)
listImg = []
temp = 0
for x, pathPiece in enumerate(piecePath):

    if 'png' in pathPiece:
        imgType = 'png'
    else:
        imgType = 'jpg'
    
    if x > 5:
        yPos = 300
        xPos = 350 + temp * 200
        temp += 1
    else:
        yPos = 100
        xPos = 50 + x * 200
    
    listImg.append(DragImg(f'{dirPath}/{pathPiece}', [xPos,yPos], imgType))

listBox = BoxPiece(9, (150,150), cap.read()[1].shape[:2] )

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    
    for box in listBox.boxes:
        cv2.rectangle(img, box[0], box[1], (0,255, 0), 3)

    if hands :
        lmList = hands[0]['lmList']

        length, info, img  = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        
        if length < 20 :
            cursor = lmList[8]
            
            for imgObject in listImg:
                oxOld, oyOld = imgObject.posOrigin
                imgObject.update(cursor) 
                
                if check (listImg) == False: imgObject.posOrigin = [oxOld, oyOld]

    try:
        for imgObject in listImg:
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            # draw for PNG images
            img[oy:oy+h, ox:ox+w] = imgObject.img
    except:
      pass

    # cv2.rectangle(img, (400, 100), (850, 550), (0, 255, 0), 5)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()
