import cv2
import numpy as np
import pandas as pd
import argparse

# Creating argument parser to take image path from command line and open the image using opencv
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']
img = cv2.imread(img_path)

# declaring global variables and initializing them for later use
clicked = False
r = g = b = xpos = ypos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"] #this is a list of string
csv = pd.read_csv('colors.csv', names=index, header=None) #reads the colors dataset
# and assigns names to its columns from the previous list of strings
#We will be using a dataset that contains RGB values with their corresponding names


# function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000 #just initializng the variable
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"])) #[i, 'R'] gives value of ith row of 'R' column from dataset
        if (d <= minimum): #this just finds the minimum value of d and the color name for that value
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# function to get x,y coordinates of mouse double click and get the RGB values of clicked pixel
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked #global variables
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x] #gets the RGB value of the pixel clicked and outputs it in the given order
        b = int(b)
        g = int(g)
        r = int(r)


#mouse callback event
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while (1):

    cv2.imshow("image", img)
    if (clicked):

        # cv2.rectangle creates a rectangle to show text of color name
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText writes the color name and rgb values from getColorName and displays it in the triangle
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if (r + g + b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
