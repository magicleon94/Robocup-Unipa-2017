import cv2
import numpy as np



frame = cv2.imread('landmarks', 1)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

corners = cv2.goodFeaturesToTrack(gray,25,0.1,10)
corners = np.int0(corners)

try:
    cv2.drawContours(frame, contours, 3, (0,0,255),4)
except:
    pass
for i in circles[0,:]:
    cv2.circle(frame, (i[0],i[1]), i[2], (0,255,0),4)
cv2.imshow('img', frame)
cv2.imshow('mask', thresh
           )
#cv2.destroyAllWindows()
cv2.waitKey(0)

cv2.destroyAllWindows()
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
