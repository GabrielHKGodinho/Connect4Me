import cv2
import numpy as np

boardPositions = list()

cap = cv2.VideoCapture(2)
def mouseRGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
        colorsB = image[y, x, 0]
        colorsG = image[y, x, 1]
        colorsR = image[y, x, 2]
        colors = image[y, x]
        boardPositions.append([x,y])
        print("Red: ", colorsR)
        print("Green: ", colorsG)
        print("Blue: ", colorsB)
        print("BRG Format: ", colors)
        print("Coordinates of pixel: X: ", x, "Y: ", y)
    if event == cv2.EVENT_RBUTTONDOWN:
        print(boardPositions)


# Read an image, a window and bind the function to window
# image = cv2.imread("./teste.jpg")
# image = cv2.resize(image, (900, 450))
# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.namedWindow('mouseRGB')
cv2.setMouseCallback('mouseRGB', mouseRGB)

# Do until esc pressed
while (1):
    _, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Blue Red Yellow
    colorHSV = [[100, 0, 0, 130, 255, 255],
                [3, 100, 60, 10, 255, 255],
                [18, 70, 130, 40, 180, 255],
                [30,10,0,70,255,120]]
    y_lower = np.array(colorHSV[2][:3])
    y_upper = np.array(colorHSV[2][3:6])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(image, y_lower, y_upper)
    mask = cv2.bitwise_not(mask)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('mouseRGB', res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
# if esc pressed, finish.
cv2.destroyAllWindows()