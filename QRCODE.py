import cv2
import numpy as np
import scipy.signal as signal
import json
import os
import shutil

class Square:
    """
     Represents a canvas that contains 10x10 blocks of squares.

    """

    def __init__(self, start_block : int = None, end_block: int = None, color: int = None, pixel_x: int = None, pixel_y: int = None, block_size: int = None,
                 margin : int = 3,
                 background_color: list = (255, 255, 255),
                 load=None) -> None:
        """
        Initializes a Square object.

        Args:
            start_block: The starting block of the square (lower left corner), represented as coordinates (0, 0) to (9, 9).
            end_block: The ending block of the square (upper right corner), represented as coordinates (0, 0) to (9, 9).
            color: An integer representing the color of the square (0 for black, 1 for white).
            pixel_x: The x-coordinate position of the canvas in pixels.
            pixel_y: The y-coordinate position of the canvas in pixels.
            block_size: The size of the square's block.
            margin: Margin size.
            background_color: Background color.
            load: A filename to load the parameters from a JSON file.

        """


        if load:
            with open(load, 'r') as json_file:
                square_data = json.load(json_file)
            
            self.start_block = tuple(square_data['start_block'])
            self.end_block = tuple(square_data['end_block'])
            self.color = square_data['color']
            self.pixel_x = square_data['pixel_x']
            self.pixel_y = square_data['pixel_y']
            self.block_size = square_data['block_size']
            self.margin = square_data['margin']
            self.background_color = np.array(square_data['background_color'])
            

        else : 
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
            
    def save(self, filename: str) -> None:
        """
        Save the square parameters to a JSON file.

        Args:
            filename: The name of the file to save the parameters.
        """
        square_data = {
            'start_block': self.start_block,
            'end_block': self.end_block,
            'color': self.color,
            'pixel_x': self.pixel_x,
            'pixel_y': self.pixel_y,
            'block_size': self.block_size,
            'margin': self.margin,
            'background_color': self.background_color.tolist()
        }
        
        with open(filename, 'w') as json_file:
            json.dump(square_data, json_file, indent=4)


class QRCode:
    def __init__(self,posX,posY,frequency,size,fps,load = None) -> None:

        self.size = size
        self.fps = fps
        self.period = 1 / self.fps

        self.posX = posX
        self.posY = posY

        self.square = []

        self._frequencyArray = [self.frequencyApprox(frequency) , self.frequencyApprox(frequency*2)]
        
        
        self._counter = 0
        if load:
            # Load combined data from the main JSON file
            input_path = load + ".json"
            with open(input_path, 'r') as infile:
                combined_data = json.load(infile)

            for i, data in enumerate(combined_data):
                with open(f"{i}.json", 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                self.square.append(Square(load=f"{i}.json"))

                os.remove(f"{i}.json")
        else:
            self.generate()
            


    def generate(self):
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


    def save(self, filename: str):
        if not os.path.exists(filename):
            os.makedirs(filename)

        combined_data = []

        for i, item in enumerate(self.square):
            filepath = os.path.join(filename, f"{i}.json")
            item.save(filepath)

            with open(filepath, 'r') as file:
                data = json.load(file)
                combined_data.append(data)
            os.remove(filepath)
        

        shutil.rmtree(filename)

        output_path = filename + ".json"
        with open(output_path, 'w') as outfile:
            json.dump(combined_data, outfile, indent=4)

        
            

    def frequencyApprox(self, frequency):
        y = signal.square(2*np.pi*frequency*(np.arange(0,self.fps)/ self.fps))
        return (y+1)/2


    def add_square(self,pos1 , pos2, color):
        self.square.append(Square(pos1 , pos2, color, self.posX ,self.posY, self.size))

    def flick(self,img):
        for s in self.square:
            s.flick(img,self._frequencyArray[0][self._counter])
        self._counter = (self._counter + 1)%self.fps