import cv2
import numpy as np
import time
import scipy.signal as signal


class Square:
    def __init__(self, posStart , posEnd, color, posX,posY,size) -> None:
        self.size = size//10

        self.posX = posX - self.size * 5
        self.posY = posY - self.size * 5


        self.color = color
        
        self.margin = 3
        self.gray = 255//2
        

        self.posStart = posStart
        self.posEnd = posEnd
    
    def flick(self, img,f):
        cv2.rectangle(img, (self.posX + self.size*self.posStart[0] + self.margin, self.posY + self.size*self.posStart[1] + self.margin), 
                    (self.posX + self.size*self.posEnd[0] - self.margin, self.posY + self.size*self.posEnd[1]- self.margin), 
                    (255-np.absolute(255*self.color - 255*f ), 255-np.absolute(255*self.color - 255*f ), 255-np.absolute(255*self.color - 255*f )),
                      -1)
class QRCode:
    def __init__(self,posX,posY,frequency,size) -> None:
        self.size = size
        self.fps = 165
        self.period = 1 / self.fps

        self.posX = posX
        self.posY = posY

        self.square = []

        self._frequencyArray = [self.frequencyApprox(frequency) , self.frequencyApprox(frequency*2)]
        
        
        self._counter = 0


        # random square 1
        matrix = np.zeros((10, 10))

        values = [0,1, 2]
        probabilities = [0.55, 0.225, 0.225]

        indices = np.random.choice(len(values), size=matrix.size, p = probabilities)

        matrix.flat[:] = [values[i] for i in indices]


        matrix[0:3,0:3] = 0
        matrix[0:3,7:10] = 0
        matrix[7:10,7:10] = 0

        for i in range(10):
                        for j in range(10):
                            if matrix[i,j] == 0:
                                pass
                            else:
                                self.add_square((i,j), (i+1,j+1),matrix[i,j] - 1)
        
        # random square 2
        matrix = np.zeros((10, 10))

        values = [0,1, 2]
        probabilities = [0.55, 0.225, 0.225]


        indices = np.random.choice(len(values), size=matrix.size, p = probabilities)

        matrix.flat[:] = [values[i] for i in indices]


        matrix[0:3,0:3] = 0
        matrix[0:3,6:10] = 0
        matrix[6:10,6:10] = 0

        white = matrix.copy()
        black = matrix.copy()

        for i in range(10-1):
            for j in range(10-1):
                if matrix[i,j] == 0:
                    pass
                elif white[i,j] == 1:
                    self.add_square((i,j), (i+2,j+2),0)
                    if j <= 1: white[i:i+2,j:j+2] = 0
                    else : white[i:i+2,j-2:j+2] = 0

                elif black[i,j] == 2:
                    self.add_square((i,j), (i+2,j+2),1)
                    if j <= 1: black[i:i+2,j:j+2] = 0
                    else : black[i:i+2,j-2:j+2] = 0
                                
 
        sq = np.array(self.square)
        np.random.shuffle(sq)
        self.square = sq.tolist()


        # init random color of main pattern
        r1 = np.random.randint(2)
        self.add_square((0,0), (3,3),r1)
        self.add_square((1,1), (2,2),not r1) 

        r2 = np.random.randint(2)
        self.add_square((7,7), (10,10), r2) 
        self.add_square((8,8), (9,9),not r2) 
        
        r3 = np.random.randint(2)
        self.add_square((0,7), (3,10),r3)
        self.add_square((1,8), (2,9),not r3) 

    def frequencyApprox(self, frequency):
        y = signal.square(2*np.pi*frequency*(np.arange(0,self.fps)/ self.fps))
        return (y+1)/2


    def add_square(self,pos1 , pos2, color):
        self.square.append(Square(pos1 , pos2, color, self.posX ,self.posY, self.size))

    def flick(self,img):
        for s in self.square:
            s.flick(img,self._frequencyArray[0][self._counter])
        self._counter = (self._counter + 1)%self.fps
    
w = 1920
h = 1080
marginX = 400
marginY = 250

size = 250

qr1 = QRCode(posX = w//2 - marginX,
             posY = h//2 - marginY,
             frequency = 7,
             size = size)

qr2 = QRCode(posX = w//2 + marginX,
             posY = h//2 - marginY,
             frequency = 10,
             size = size)

qr3 = QRCode(posX = w//2 - marginX,
             posY = h//2 + marginY,
             frequency = 13,
             size = size)

qr4 = QRCode(posX = w//2 + marginX,
             posY = h//2 + marginY,
             frequency = 17,
             size = size)


timestamp = time.time()  
timestamp2 = time.time()

s = 3
while(1):
    if (time.time() <= timestamp):
 
        img = np.zeros((1080, 1920, 3), dtype=np.uint8) + 255//2

    
        

        if (time.time() <= timestamp2):
            if(s<4):
                qr1.flick(img)
                qr2.flick(img)
                qr3.flick(img)
                qr4.flick(img)
            if s == 0:
                color = (0, 0, 255)
                thickness = 5

                start_point =(w//2 - marginX - size//2 - 10, h//2 - marginY - size//2 - 10)
                end_point =(w//2 - marginX + size//2 + 10, h//2 - marginY + size//2 + 10)
                
                cv2.rectangle(img, start_point, end_point, color, thickness)
            elif s == 1:
                color = (0, 0, 255)
                thickness = 5

                start_point =(w//2 + marginX - size//2 - 10, h//2 - marginY - size//2 - 10)
                end_point =(w//2 + marginX + size//2 + 10, h//2 - marginY + size//2 + 10)
                
                cv2.rectangle(img, start_point, end_point, color, thickness)
            elif s == 2:
                color = (0, 0, 255)
                thickness = 5

                start_point =(w//2 - marginX - size//2 - 10, h//2 + marginY - size//2 - 10)
                end_point =(w//2 - marginX + size//2 + 10, h//2 + marginY + size//2 + 10)
                
                cv2.rectangle(img, start_point, end_point, color, thickness)
            elif s == 3:
                color = (0, 0, 255)
                thickness = 5

                start_point =(w//2 + marginX - size//2 - 10, h//2 + marginY - size//2 - 10)
                end_point =(w//2 + marginX + size//2 + 10, h//2 + marginY + size//2 + 10)
                
                cv2.rectangle(img, start_point, end_point, color, thickness)
        else:
            if s == 4:
                timestamp2 += 3
            else:
                timestamp2 += 6
            s = (s +1)%5
            


        
    else:
        timestamp += 1/165

    
    cv2.imshow('Flickering Squares', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
