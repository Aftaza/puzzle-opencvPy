import cv2

class BoxPiece:
    def __init__(self, sumBoxes:int, sizes:tuple, frame):
        # get from parameters and initialize class variables
        self.sumBoxes = sumBoxes
        self.sizes = sizes
        self.frame = frame
        self.centers = []
        self.boxes = []
        
        height, width = self.frame
        w, h = self.sizes
        
        start = (width // 2 - w, height // 2 - h)
        
        # calculate center and  coordinates of boxes
        for box in range(self.sumBoxes):
            if box < 3:
                for up in range(3):
                    center = (start[0] + w * up, start[1])
                    boxny = ((center[0] - w // 2, center[1] - h // 2), (center[0] + w // 2, center[1] + h // 2))
                    self.centers.append(center)
                    self.boxes.append(boxny)
            elif box >= 3 and box < 6:
                for up in range(3):
                    center = (start[0] + w * up, start[1] + h)
                    boxny = ((center[0] - w // 2, center[1] - h // 2), (center[0] + w // 2, center[1] + h // 2))
                    self.centers.append(center)
                    self.boxes.append(boxny)
            elif box < self.sumBoxes:
                for up in range(3):
                    center = (start[0] + w * up, start[1] + (h*2))
                    boxny = ((center[0] - w // 2, center[1] - h // 2), (center[0] + w // 2, center[1] + h // 2))
                    self.centers.append(center)
                    self.boxes.append(boxny)