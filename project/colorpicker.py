import cv2
import numpy as np

boardPositions = [[190, 75], [191, 135], [187, 197], [188, 254], [182, 311], [177, 373], [253, 81], [253, 140], [252, 199], [249, 260], [247, 320], [241, 379], [322, 85], [319, 140], [316, 203], [313, 260], [309, 323], [304, 385], [386, 88], [386, 146], [385, 206], [382, 266], [377, 327], [370, 391], [457, 89], [453, 147], [450, 209], [447, 270], [441, 330], [438, 396], [527, 92], [522, 153], [521, 216], [514, 274], [511, 337], [502, 401], [603, 92], [592, 154], [588, 220], [585, 278], [576, 341], [577, 405]]


cap = cv2.VideoCapture(2)
def mouseRGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse left button down condition
        colorsB = image[y, x, 0]
        colorsG = image[y, x, 1]
        colorsR = image[y, x, 2]
        colors = image[y, x]
        print("Red: ", colorsR)
        print("Green: ", colorsG)
        print("Blue: ", colorsB)
        print("BRG Format: ", colors)
        print("Coordinates of pixel: X: ", x, "Y: ", y)


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
    colorHSV = [[108, 0, 0, 120, 255, 255],
                [3, 100, 60, 10, 255, 255],
                [18, 120, 130, 40, 210, 255],
                [30,10,0,70,255,120]]
    y_lower = np.array(colorHSV[0][:3])
    y_upper = np.array(colorHSV[0][3:6])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(image, y_lower, y_upper)
    mask = cv2.bitwise_not(mask)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    for i in range(0, 42):
        cv2.circle(frame, (boardPositions[i][0], boardPositions[i][1]), radius=2, color=(0, 0, 255), thickness=-1)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('mouseRGB', res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
# if esc pressed, finish.
cv2.destroyAllWindows()