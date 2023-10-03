import cv2
import os
from cvzone.HandTrackingModule import HandDetector
from DragImg import DragImg


def is_object_inside_box(imgObject, box):
    h, w = imgObject.size
    ox, oy = imgObject.posOrigin
    x1, y1 = box[0]
    x2, y2 = box[1]
    #print(h,w);
    # print(ox,oy);
    # print(imgObject.path);
    # print(x1,y1);
    # print(x2,y2);
    # print("gdddddddd");
    return (x1-10 <= ox <= x2+10) and (y1-10 <= oy <= y2+10) 


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.65)

dirPath = './img/imageonline'
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
    
    listImg.append(DragImg(f'{dirPath}/{pathPiece}', [xPos,yPos], imgType, pathPiece))

# img1 = cv2.imread('img/pieces/piece_0.png', cv2.IMREAD_UNCHANGED)
# img1 = cv2.resize(img1, (150, 150))
# ox, oy = 200, 200
# cv2.imshow("image 1", listImg[1].img)
# img = Image.open("img/pieces/piece_0.png")
# img.show()
# img = reduceOpc(img, 0.8)
# img.show()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1);
    ans = 0;
    hands, img = detector.findHands(img, flipType=False)
    #print(hands);
    if hands :
        lmList = hands[0]['lmList']

        length, info, img  = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        
        if length < 50 :
            cursor = lmList[8]
            
            for imgObject in listImg:
                imgObject.update(cursor)  

    try:
        for imgObject in listImg:
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            # draw for PNG images
            img[oy:oy+h, ox:ox+w] = imgObject.img
    except:
      pass

    height, width, _ = img.shape

# Define box sizes (width, height)
    box_size = (150, 150)

    # Define center coordinates for the four boxes
    center1 = (width // 2, height // 2)
    center2 = (width // 2 + 150, height // 2)
    center3 = (width // 2, height // 2 +150)
    center4 = (width // 2 +150, height // 2 +150)

    # Calculate top-left and bottom-right coordinates
    box1 = ((center1[0] - box_size[0]//2, center1[1] - box_size[1]//2), 
            (center1[0] + box_size[0]//2, center1[1] + box_size[1]//2))

    box2 = ((center2[0] - box_size[0]//2, center2[1] - box_size[1]//2), 
            (center2[0] + box_size[0]//2, center2[1] + box_size[1]//2))

    box3 = ((center3[0] - box_size[0]//2, center3[1] - box_size[1]//2), 
            (center3[0] + box_size[0]//2, center3[1] + box_size[1]//2))

    box4 = ((center4[0] - box_size[0]//2, center4[1] - box_size[1]//2), 
            (center4[0] + box_size[0]//2, center4[1] + box_size[1]//2))

    # Define the color and thickness of the border
    color = (0, 255, 0)  # Green color
    thickness = 3

    # Draw the rectangles
    cv2.rectangle(img, box1[0], box1[1], color, thickness)
    cv2.rectangle(img, box2[0], box2[1], color, thickness)
    cv2.rectangle(img, box3[0], box3[1], color, thickness)
    cv2.rectangle(img, box4[0], box4[1], color, thickness)

   

    if is_object_inside_box(listImg[0], box1) :
        ans |= (1 << 0)
        #print("0")
    if is_object_inside_box(listImg[1], box2) :
        ans |= (1 << 1)
        #print("1");
    if is_object_inside_box(listImg[2], box3) :
        ans |= (1 << 2)
        #print("2");
    if is_object_inside_box(listImg[3], box4) :
        ans |= (1 << 3)
        #print("3");q

    print(ans)
    if ans == 15 :
        print("Berhasil bang");


    

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()
