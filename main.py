import cv2
import os
from PIL import Image, ImageEnhance
from cvzone.HandTrackingModule import HandDetector

def  reduceOpc(im, opacity):
    """
    Return an image with reduce opacity
    args:
        im: Image to reduce must Pillow read
        opacity: alpha number
    """
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.65)

dirPath = './img/pieces'
pieceImg = os.listdir(dirPath)

dirPath = './img/pieces'
pieceImg = os.listdir(dirPath)

img1 = cv2.imread('img/pieces/piece_0.png', cv2.IMREAD_UNCHANGED)
img1 = cv2.resize(img1, (150, 150))
ox, oy = 200, 200

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
       print(length)
       
       if length < 60 :
        cursor = lmList[8] 
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h :
          ox,oy = cursor[0] - w //2, cursor[1] - h // 2
    
    try:

      h, w, _ = img1.shape
      img[oy:oy+h, ox:ox+w] = img1
      #img = cvzone.overlayPNG(img, img1, [ox,oy])

    except:
      pass

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()
