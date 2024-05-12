import cv2
import numpy as np
import time
import scipy.signal as signal
import pyautogui
from pylsl import StreamInfo, StreamOutlet

class Square:
    """
     Represents a canvas that contains 10x10 blocks of squares.

    """

    def __init__(self, start_block: int, end_block: int, color: int, pixel_x: int, pixel_y: int, block_size: int,
                 margin : int = 3,
                 background_color: list = (255, 255, 255)) -> None:
        """
        Initializes a Square object.

        Args:
            start_block: The starting block of the square (lower left corner), represented as coordinates (0, 0) to (9, 9).
            end_block: The ending block of the square (upper right corner), represented as coordinates (0, 0) to (9, 9).
            color: An integer representing the color of the square (0 for black, 1 for white).
            pixel_x: The x-coordinate position of the canvas in pixels.
            pixel_y: The y-coordinate position of the canvas in pixels.
            block_size: The size of the square's block.
            margin:
            background_color: 

        """
        self.block_size = block_size // 10
        self.pixel_x = pixel_x - self.block_size * 5
        self.pixel_y = pixel_y - self.block_size * 5
        self.color = color
        self.margin = margin
        self.background_color = np.array(background_color)
        self.start_block = start_block
        self.end_block = end_block
    
    def flick(self, img, flicker_state) -> None:
        """
        Draw the square on an image.

        Args:
            img: The image to draw the square on.
            flicker_state: A variable indicating the state of flickering, where 0 represents the off state and 1 represents the on state. This variable controls whether the square is flickering on or off.

        """

        # if color black, flick 
        if self.color == 0:
            cv2.rectangle(img = img, 
                          pt1 = (self.pixel_x + self.block_size * self.start_block[0] + self.margin, self.pixel_y + self.block_size * self.start_block[1] + self.margin), 
                          pt2 = (self.pixel_x + self.block_size * self.end_block[0] - self.margin, self.pixel_y + self.block_size * self.end_block[1] - self.margin), 
                          color = self.background_color * flicker_state,
                          thickness = -1)
        # if color white, just showing
        else:
            cv2.rectangle(img = img, 
                          pt1 = (self.pixel_x + self.block_size * self.start_block[0] + self.margin, self.pixel_y + self.block_size * self.start_block[1] + self.margin), 
                          pt2 = (self.pixel_x + self.block_size * self.end_block[0] - self.margin, self.pixel_y + self.block_size * self.end_block[1] - self.margin), 
                          color = (255,255,255),
                          thickness = -1)

class QRCode:
    def __init__(self,posX,posY,frequency,size,fps) -> None:
        self.size = size
        self.fps = fps
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


# screen_width, screen_height = pyautogui.size()

# print("Screen Width:", screen_width)
# print("Screen Height:", screen_height)

# parameter
w = 3840
h = 2160

fps = 60

marginX = 1000
marginY = 600

size = 600

qr1 = QRCode(posX = w//2 - marginX,
             posY = h//2 - marginY,
             frequency = 10,
             size = size,
             fps=fps)

qr2 = QRCode(posX = w//2 + marginX,
             posY = h//2 - marginY,
             frequency = 10,
             size = size,
             fps=fps)

qr3 = QRCode(posX = w//2 - marginX,
             posY = h//2 + marginY,
             frequency = 13,
             size = size,
             fps=fps)

qr4 = QRCode(posX = w//2 + marginX,
             posY = h//2 + marginY,
             frequency = 17,
             size = size,
             fps=fps)

# LSL stream setup
info = StreamInfo("MyMarkerStream", "Markers", 1, 0, 'int32', 'myuidw43536')
outlet = StreamOutlet(info)
 
timestamp = time.time()  
timestamp2 = time.time()

s = 6
color = (0, 0, 255) #red
thickness = 5
prev_s = None


while(1):
    if (time.time() <= timestamp):
        
        if s != prev_s:
            # Send s value through LSL
            outlet.push_sample([s])
            prev_s = s

        img = np.zeros((h, w, 3), dtype=np.uint8)
        img[:,:,:] = 255//2
    
        if (time.time() <= timestamp2):
            # print(s)
            if(s<5):
                qr1.flick(img)
                qr2.flick(img)
                qr3.flick(img)
                qr4.flick(img)

            if s == 0:
                start_point =(w//2 - size//2 - 10, h//2 - size//2 - 10)
                end_point =(w//2 + size//2 + 10, h//2 + size//2 + 10)
                
                cv2.rectangle(img, start_point, end_point, color, thickness)
                center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)

                cv2.putText(img, '+', ((3840//2)-80,(2160//2)+60), cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 255, 255), 6)
            elif s == 1:
                start_point =(w//2 - marginX - size//2 - 10, h//2 - marginY - size//2 - 10)
                end_point =(w//2 - marginX + size//2 + 10, h//2 - marginY + size//2 + 10)
                
                cv2.rectangle(img, start_point, end_point, color, thickness)
            elif s == 2:
                start_point =(w//2 + marginX - size//2 - 10, h//2 - marginY - size//2 - 10)
                end_point =(w//2 + marginX + size//2 + 10, h//2 - marginY + size//2 + 10)
                
                cv2.rectangle(img, start_point, end_point, color, thickness)
            elif s == 3:
                start_point =(w//2 - marginX - size//2 - 10, h//2 + marginY - size//2 - 10)
                end_point =(w//2 - marginX + size//2 + 10, h//2 + marginY + size//2 + 10)
                
                cv2.rectangle(img, start_point, end_point, color, thickness)
            elif s == 4:
                start_point =(w//2 + marginX - size//2 - 10, h//2 + marginY - size//2 - 10)
                end_point =(w//2 + marginX + size//2 + 10, h//2 + marginY + size//2 + 10)
                
                cv2.rectangle(img, start_point, end_point, color, thickness)

        else:
            timestamp2 += 20
            s = (s +1)%7

    else:
        timestamp += 1/fps

    cv2.imshow('Flickering Squares', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
