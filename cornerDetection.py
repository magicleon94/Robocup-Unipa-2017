import cv2
import numpy as np
import imutils

counter_square = 0
counter_triangle = 0
counter_circles = 0


frame = cv2.imread('square_front.jpg',1)
frame = imutils.resize(frame,height=600)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

canny = cv2.Canny(gray, 50, 200)


image, contours, hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")

	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        counter_circles += 1

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    if len(approx)==4 and cv2.contourArea(cnt)>50 and not cv2.isContourConvex(cnt):
        cv2.drawContours(frame, [approx], -1, (0,255,0), 2);
        counter_square+=1
        continue
    if len(approx)==3 and cv2.contourArea(cnt)>50 and not cv2.isContourConvex(cnt):
        cv2.drawContours(frame, [approx], -1, (0,0,255), 3);
        counter_triangle+=1
        continue
    # cv2.drawContours(frame, [approx], -1, (255,0,255), 3);
    print len(approx)

print counter_square, " squares detected"
print counter_triangle, " triangles detected"
print counter_circles, " circles detected"


cv2.imshow('img', frame)
# cv2.imshow('mask', canny)
cv2.waitKey(0)
