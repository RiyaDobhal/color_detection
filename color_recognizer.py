import cv2
import pandas as pd
import argparse

#Creating argument parser 
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())

#To set the path of the image
img_path = args['image']

#Opening WebCam 
Webcam = cv2.VideoCapture(0)

#initially setting image_count to 0
image_count = 0

while True:
    ret, frame = Webcam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Live Camera", frame)

    key = cv2.waitKey(1)
    if key%256 == 8:
        # BACKSPACE pressed
        print("Press BACKSPACE to close the Webcam")
        break
    elif key%256 == 32:
        # SPACE pressed
        image_name = "Image_{}.png".format(image_count)
        cv2.imwrite(image_name, frame)
        print("Image Captured")
        image_count += 1

Webcam.release()

cv2.destroyAllWindows()


#Reading the image with opencv
img = cv2.imread(img_path)

#declaration of global variables 
clicked = False
r = g = b = x_position = y_position = 0

#Reading csv file 
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

#function to calculate the distance 
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        distance = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(distance<=minimum):
            minimum = distance
            color_name = csv.loc[i,"color_name"]
    return color_name

#function to get x,y coordinates k
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,x_position,y_position, clicked
        clicked = True
        x_position = x
        y_position = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

while(1):

    cv2.imshow("image",img)
    if (clicked):
   
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #Creating text string to display( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #Displaying text color as black for light color detection
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #Break the loop when user hits 'BACKSPACE' key    
    key = cv2.waitKey(1)
    if key%256 == 8:
        # BACKSPACE pressed
        print("Press BACKSPACE to close the Webcam")
        break
    
cv2.destroyAllWindows()