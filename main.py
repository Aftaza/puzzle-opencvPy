import cv2
import os
from cvzone.HandTrackingModule import HandDetector
from DragImg import DragImg

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.65)

dirPath = './img/pieces'
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
        xPos = 50 + temp * 200
        temp += 1
    else:
        yPos = 100
        xPos = 50 + x * 200
    
    listImg.append(DragImg(f'{dirPath}/{pathPiece}', [xPos,yPos], imgType))

# img1 = cv2.imread('img/pieces/piece_0.png', cv2.IMREAD_UNCHANGED)
# img1 = cv2.resize(img1, (150, 150))
# ox, oy = 200, 200

# img = Image.open("img/pieces/piece_0.png")
# img.show()
# img = reduceOpc(img, 0.8)
# img.show()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands :
        lmList = hands[0]['lmList']

        length, info, img  = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        
        if length < 50 :
            cursor = lmList[8]
            
            for imgObject in listImg:
                if imgObject.draged == True:
                    imgObject.update(cursor)
    
    
    try:
        for imgObject in listImg:
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            # draw for PNG images
            img[oy:oy+h, ox:ox+w] = imgObject.img
    except:
      pass

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()
