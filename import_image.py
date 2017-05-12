import cv2
import numpy as np
import imutils

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

img = cv2.imread('palla.png',1)
img = adjust_gamma(img, gamma=0.6)

#green_lower = np.array([23, 48, 3])
#green_upper = np.array([154, 193, 40])


#hsv_green_lower = cv2.cvtColor(green_lower,cv2.COLOR_BGR2HSV)
#hsv_green_upper = cv2.cvtColor(green_upper,cv2.COLOR_BGR2HSV)

hsv_lower = np.uint8([[[61, 42, 28]]])
hsv_upper = np.uint8([[[240, 131, 103]]])

frame = imutils.resize(img, width=600)
# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# construct a mask for the color "green", then perform
# a series of dilations and erosions to remove any small
# blobs left in the mask

mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)


# find contours in the mask and initialize the current
# (x, y) center of the ball
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
center = None

# only proceed if at least one contour was found
if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # only proceed if the radius meets a minimum size
    if radius > 10:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, (int(x), int(y)), int(radius),
                   (0, 255, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)


cv2.imshow('mask', mask)
cv2.imshow('img', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
