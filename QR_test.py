import cv2
import numpy as np
import time
import scipy.signal as signal
import pyautogui
from pylsl import StreamInfo, StreamOutlet

from QRCODE import QRCode


# screen_width, screen_height = pyautogui.size()

# print("Screen Width:", screen_width)
# print("Screen Height:", screen_height)

# parameter
w = 1920
h = 1080

fps = 165

marginX = 400
marginY = 200

size = 300

# load_set = "presets/set1"
load_set = "presets/JustanOrdinarySquare"

# if no load = auto generate
qr1 = QRCode(posX = w//2 - marginX,
             posY = h//2 - marginY,
             frequency = 10,
             size = size,
             fps=fps,
             load = f"{load_set}/qr1")

qr2 = QRCode(posX = w//2 + marginX,
             posY = h//2 - marginY,
             frequency = 10,
             size = size,
             fps=fps,
             load = f"{load_set}/qr2")

qr3 = QRCode(posX = w//2 - marginX,
             posY = h//2 + marginY,
             frequency = 13,
             size = size,
             fps=fps,
             load = f"{load_set}/qr3")

qr4 = QRCode(posX = w//2 + marginX,
             posY = h//2 + marginY,
             frequency = 17,
             size = size,
             fps=fps,
             load = f"{load_set}/qr4")


# save EX.
# qr1.save(r"preset/set1/qr1")


# LSL stream setup
# info = StreamInfo("MyMarkerStream", "Markers", 1, 0, 'int32', 'myuidw43536')
# outlet = StreamOutlet(info)
 
s = -1
color = (0, 0, 255) #red
thickness = 5
prev_s = None


timestamp = time.time()  
timestamp2 = time.time()

while(1):
    
    if (time.time() <= timestamp):
        img = np.zeros((h, w, 3), dtype=np.uint8)
        img[:,:,:] = 255//2
        
        if s != prev_s:
            # Send s value through LSL
            # outlet.push_sample([s])
            prev_s = s
    
        if (time.time() <= timestamp2 and s != -1):
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

                cv2.putText(img, '+', ((w//2)-80,(h//2)+60), cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 255, 255), 6)

            if s == 1:
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
        elif(s != -1):
            timestamp2 += 15
            s = (s +1)%6
        
    else:
        timestamp += 1/fps

    cv2.imshow('Flickering Squares', img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        if (s == -1):
            s = 5
            timestamp2 = time.time()
    elif key == ord('r'):
        s = -1
cv2.destroyAllWindows()
