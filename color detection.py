import cv2
import numpy as np
import time

# Start the camera
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(1) #cap1 slow one *for me*
sens = 10
settings = np.zeros((250,250,3), np.uint8)
prev_frame_time = 0 # frame time to calculate fps
new_frame_time = 0 # frame time to calculate fps
fps = 0
colorU = np.array([0, 0, 0]) # vars to fix a bug
colorL = np.array([0, 0, 0]) # vars to fix a bug

# [[[ 0  0  0]]

#  [[10 10 10]]

#  [[ 8  8  8]]]
# [[[20 20 20]]

#  [[30 30 30]]

#  [[28 28 28]]]#unknown


# [[[234 234 234]]

#  [[244 244 244]]

#  [[242 242 242]]]
# [[[254 254 254]]

#  [[  8   8   8]]

#  [[  6   6   6]]] # only sun light

# [[[215 215 215]]

#  [[214 214 214]]

#  [[170 170 170]]]
# [[[255 255 255]]

#  [[254 254 254]]

#  [[210 210 210]]] #really good white

# lower_bound = (230, 230 ,230)
# upper_bound = (255, 255, 255) #white
# lower_bound = (0, 7 ,10)
# upper_bound = (20, 27, 30)# cool but not so good black?
# lower_bound = (0, 5 ,5)
# upper_bound = (21, 33, 48)# cool and good black?
# lower_bound = (0, 150, 0)
# upper_bound = (100, 255, 100)#test maybe
lower_bound = (2, 4, 4)
upper_bound = (22, 24, 24)#12,14,14 night vision

def on_mouse_click(event, x, y, flags, param):
    # If the left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the color of the pixel at (x, y)
        global color
        color = frame[y, x]

        # Set the lower and upper bounds for the mask
        global lower_bound
        global upper_bound

        #lower check for a glitch where if 0 it would go to 245
        for x in range(3):
            if(color[x] - sens <= 0):
                colorL[x] = color[x]
            else:
                colorL[x] = color[x] - sens
        lower_bound = colorL
        
        #upper check for a glitch where if 255 it would go to 10
        for x in range(3):
            if(color[x] + sens >= 255):
                colorU[x] = color[x]
            else:
                colorU[x] = color[x] + sens
        upper_bound = colorU

        # change background color
        settings[:]=(color[0], color[1], color[2])
        cv2.putText(settings, "Sens: " + str(sens), (25, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) , 1, cv2.LINE_AA)
        cv2.line(settings, (0, 125), (252, 125), (0, 255, 0), 2)
        cv2.putText(settings, "Sens Up", (100, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) , 1, cv2.LINE_AA)
        cv2.putText(settings, "Sens Down", (100, 175), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) , 1, cv2.LINE_AA)


def changeSens(event, x, y, flags, param):
    global sens, color, upper_bound, lower_bound
    if event == cv2.EVENT_LBUTTONDOWN:
        if(y <= 125):
            sens += 1
        else:
            sens -= 1

        #lower
        for x in range(3):
            if(color[x] - sens <= 0):
                colorL[x] = color[x]
            else:
                colorL[x] = color[x] - sens
        lower_bound = colorL
        
        #upper
        for x in range(3):
            if(color[x] + sens >= 255):
                colorU[x] = color[x]
            else:
                colorU[x] = color[x] + sens
        upper_bound = colorU
    # change background color
    settings[:]=(color[0], color[1], color[2])
    cv2.putText(settings, "Sens: " + str(sens), (25, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) , 1, cv2.LINE_AA)
    cv2.line(settings, (0, 125), (252, 125), (0, 255, 0), 2)
    cv2.putText(settings, "Sens Up", (100, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) , 1, cv2.LINE_AA)
    cv2.putText(settings, "Sens Down", (100, 175), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) , 1, cv2.LINE_AA)

def Disp_fps():
    global prev_frame_time
    new_frame_time = time.time()
    fps = str(int(1 / (new_frame_time - prev_frame_time)))
    prev_frame_time = new_frame_time
    
    cv2.putText(frame, fps, (0, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0) , 2, cv2.LINE_AA)
    cv2.putText(mask, fps, (0, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0) , 2, cv2.LINE_AA)

cv2.namedWindow("Camera")
cv2.namedWindow("Settings")

cv2.setMouseCallback('Camera', on_mouse_click)
cv2.setMouseCallback('Settings', changeSens)

# Loop until the user closes the window
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # retM, frame1 = cap1.read() # use for camera 2 at the same time

    # Create a mask for the green colors
    mask = cv2.inRange(frame, lower_bound, upper_bound)
    # mask1 = cv2.inRange(rgb1, lower_bound, upper_bound)
    colorFilter = cv2.bitwise_and(frame, frame, mask=mask)

    # uncomment to flip
    # frameF = cv2.flip(frame, 1) 
    # maskF = cv2.flip(mask, 1) 
    
    Disp_fps()

    # Display the resulting frame 
    cv2.imshow('Camera', frame) # To flip uncomment above and add F to these
    cv2.imshow("Mask", mask)
    cv2.imshow("Settings", settings)
    cv2.imshow("Color filter", colorFilter)
    # cv2.imshow("Camera1", frame1) # use for camera 2 displays
    # cv2.imshow("Mask1", mask1) # use for camera 2 displays

    # Check if the user pressed 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()