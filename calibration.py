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

def nothing(x):
    pass

def normalize(img):
    x = img - img.min()
    return 255 / x.max() * x

def update(x):
    hsv_green_lower[0][0][0] = cv2.getTrackbarPos('H_LOW', 'mask')
    hsv_green_lower[0][0][1] = cv2.getTrackbarPos('S_LOW', 'mask')
    hsv_green_lower[0][0][2] = cv2.getTrackbarPos('V_LOW', 'mask')
    hsv_green_upper[0][0][0] = cv2.getTrackbarPos('H_HIGH', 'mask')
    hsv_green_upper[0][0][1] = cv2.getTrackbarPos('S_HIGH', 'mask')
    hsv_green_upper[0][0][2] = cv2.getTrackbarPos('V_HIGH', 'mask')

    print hsv_green_lower, hsv_green_upper

    mask = cv2.inRange(hsv, hsv_green_lower, hsv_green_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



img = cv2.imread('palla.png',1)
img = adjust_gamma(img, gamma=0.6)

green_lower = np.uint8([[[23, 48, 3]]])
green_upper = np.uint8([[[154, 193, 40]]])

hsv_green_lower = cv2.cvtColor(green_lower, cv2.COLOR_BGR2HSV)
hsv_green_upper = cv2.cvtColor(green_upper, cv2.COLOR_BGR2HSV)


frame = imutils.resize(img, width=600)
# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# construct a mask for the color "green", then perform
# a series of dilations and erosions to remove any small
# blobs left in the mask

mask = cv2.inRange(hsv, hsv_green_lower, hsv_green_upper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)

cv2.imshow('mask', mask)
cv2.imshow('img', frame)




cv2.createTrackbar('H_LOW' , 'mask', hsv_green_lower[0][0][0], 255, update)
cv2.createTrackbar('H_HIGH', 'mask', hsv_green_upper[0][0][0], 255, update)

cv2.createTrackbar('S_LOW' , 'mask', hsv_green_lower[0][0][1], 255, update)
cv2.createTrackbar('S_HIGH', 'mask', hsv_green_upper[0][0][1], 255, update)

cv2.createTrackbar('V_LOW' , 'mask', hsv_green_lower[0][0][2], 255, update)
cv2.createTrackbar('V_HIGH', 'mask', hsv_green_upper[0][0][2], 255, update)
cv2.imshow('mask', mask)
cv2.imshow('img', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))


