import cv2
import numpy as np
import imutils

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)



def update(x):
    hsv_green_lower[0] = cv2.getTrackbarPos('H_LOW', 'mask')
    hsv_green_lower[1] = cv2.getTrackbarPos('S_LOW', 'mask')
    hsv_green_lower[2] = cv2.getTrackbarPos('V_LOW', 'mask')
    hsv_green_upper[0] = cv2.getTrackbarPos('H_HIGH', 'mask')
    hsv_green_upper[1] = cv2.getTrackbarPos('S_HIGH', 'mask')
    hsv_green_upper[2] = cv2.getTrackbarPos('V_HIGH', 'mask')

    print hsv_green_lower, hsv_green_upper

    mask = cv2.inRange(hsv, hsv_green_lower, hsv_green_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

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



img = cv2.imread('palla.png',1)
img = adjust_gamma(img, gamma=0.6)



hsv_green_lower = np.array([38, 66, 39])
hsv_green_upper = np.array([74, 158, 78])

first_time = True

#hsv_green_lower = cv2.cvtColor(hsv_green_lower, cv2.COLOR_BGR2HSV)
#hsv_green_upper = cv2.cvtColor(hsv_green_upper, cv2.COLOR_BGR2HSV)


frame = imutils.resize(img, width=600)
# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
# a series of dilations and erosions to remove any small
# blobs left in the mask

mask = cv2.inRange(hsv, hsv_green_lower, hsv_green_upper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)

#cv2.imshow('mask', mask)
#cv2.imshow('img', frame)
cv2.namedWindow('mask')
cv2.namedWindow('img')



if first_time:
    first_time = False
    cv2.createTrackbar('H_LOW' , 'mask', hsv_green_lower[0], 255, update)
    cv2.createTrackbar('H_HIGH', 'mask', hsv_green_upper[0], 255, update)

    cv2.createTrackbar('S_LOW' , 'mask', hsv_green_lower[1], 255, update)
    cv2.createTrackbar('S_HIGH', 'mask', hsv_green_upper[1], 255, update)

    cv2.createTrackbar('V_LOW' , 'mask', hsv_green_lower[2], 255, update)
    cv2.createTrackbar('V_HIGH', 'mask', hsv_green_upper[2], 255, update)



cv2.imshow('mask', mask)
cv2.imshow('img', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
