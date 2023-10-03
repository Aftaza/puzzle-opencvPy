import cv2

class DragImg():
    def __init__(self, path, posOrigin, imgType, name):
        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path
        self.name = name;
        
        # if self.imgType == 'png':
        #     self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        # else:
        self.img = cv2.imread(self.path)
        
        self.img = cv2.resize(self.img, (150, 150))
        
        self.size = self.img.shape[:2]
    
    def update(self, cursor):
        ox, oy = self.posOrigin
        w, h = self.size
        
        # check if cursor in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h :
            self.posOrigin = cursor[0] - w //2, cursor[1] - h // 2
        
        