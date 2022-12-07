import cv2
import numpy as np

tests = 0

boardPositions = [[190, 75], [191, 135], [187, 197], [188, 254], [182, 311], [177, 373], [253, 81], [253, 140],
                  [252, 199], [249, 260], [247, 320], [241, 379], [322, 85], [319, 140], [316, 203], [313, 260],
                  [309, 323], [304, 385], [386, 88], [386, 146], [385, 206], [382, 266], [377, 327], [370, 391],
                  [457, 89], [453, 147], [450, 209], [447, 270], [441, 330], [438, 396], [527, 92], [522, 153],
                  [521, 216], [514, 274], [511, 337], [502, 401], [603, 92], [592, 154], [588, 220], [585, 278],
                  [576, 341], [577, 405]]


class Opencv_Function():

    def videoCapture(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        return cap

    def find_Chess(self, img, contourimg, y, h, color):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Blue Red Yellow
        colorHSV = [[108, 0, 0, 120, 255, 255],
                    [3, 100, 60, 10, 255, 255],
                    [18, 120, 130, 40, 210, 255],
                    [30, 10, 0, 70, 255, 120]]

        # Yellow
        y_lower = np.array(colorHSV[color][:3])
        y_upper = np.array(colorHSV[color][3:6])
        y_mask = cv2.inRange(hsv, y_lower, y_upper)

        points_center = self.find_Contour(y_mask, contourimg, y, h)

        return points_center

    def find_Board(self, img, contourimg):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Blue Red Yellow
        colorHSV = [[100, 0, 0, 130, 255, 255],
                    [3, 100, 60, 10, 255, 255],
                    [18, 70, 130, 40, 180, 255],
                    [30, 10, 0, 70, 255, 120]]

        # Yellow
        y_lower = np.array(colorHSV[1][:3])
        y_upper = np.array(colorHSV[1][3:6])
        y_mask = cv2.inRange(hsv, y_lower, y_upper)

        contours, hierarchy = cv2.findContours(y_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area > 10000:
                x, y, w, h = cv2.boundingRect(cnt)
                for i in range(0, 42):
                    cv2.circle(contourimg, (boardPositions[i][0], boardPositions[i][1]), radius=2, color=(0, 0, 255),
                               thickness=-1)

                return x, y, w, h

        return 0, 0, 0, 0

    def find_Contour(self, img, contourimg, y1, h1):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area > 900:
                # print(area)
                cv2.drawContours(contourimg, cnt, -1, (255, 0, 0), 4)
                peri = cv2.arcLength(cnt, True)
                vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)
                x, y, w, h = cv2.boundingRect(vertices)
                contour_point = [x, y, w, h]

                x_center, y_center = self.find_Contour_center(contourimg, peri, contour_point)

                yield x_center, y_center

    def find_Contour_center(self, contourimg, peri, contour_point):
        radius = int((peri / 2) / np.pi)
        x_center = contour_point[0] + radius
        y_center = contour_point[1] + radius
        cv2.circle(contourimg, (contour_point[0] + radius, contour_point[1] + radius), 1, (255, 0, 0), cv2.FILLED)

        return x_center, y_center

    def prepare(self):
        key_bottom = 0
        while key_bottom == 0:
            print("Game Started!")
            cap = self.videoCapture()
            key_bottom = 1
            return 1, cap
