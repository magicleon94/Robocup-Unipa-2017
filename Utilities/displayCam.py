import cv2
import imutils


# cap = cv2.VideoCapture('rtsp://@192.168.1.1/live/ch00_0', cv2.CAP_FFMPEG)
cap = cv2.VideoCapture(0)
while True:
    #frame = cv2.imread('immagini/50cm.jpg', 1)
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    cv2.imshow('img', frame)
    #cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #cv2.destroyAllWindows()

#cap.release()
cv2.destroyAllWindows()
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))

