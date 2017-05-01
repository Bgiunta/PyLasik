import cv2
import os
import maestro


HAAR2_CASCADE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xmls', 'haarcascade_frontalface_default.xml')
cascadeFFace = cv2.CascadeClassifier(HAAR2_CASCADE_PATH)
sCon = maestro.Controller()
sCon.runScriptSub(0)


def detect_faces(image):
    faces = []
    face = cascadeFFace.detectMultiScale(image, 1.3, 5, minSize=(40,40), maxSize=(100,100))
    if face != []:
        for (x,y,w,h) in face:
            faces.append((x,y,w,h))
    return faces

def track(x,y,w,h,cw,ch):
    sCon.stopScript()
    sCon.setAccel(0, 0)
    sCon.setAccel(1, 0)
    sCon.setSpeed(0, 0)
    sCon.setSpeed(1, 0)
    z = 1
    t = 1
    if cw - (x+(w/2)) > 175 or (x+(w/2)) - cw > 175:
        z = 2
    if ch - (y+(h/2)) > 175 or (y+(h/2)) - ch > 175:
        t = 2
    if x+(w/2) < cw:
        sCon.setTarget(0, sCon.getPosition(0) - (cw - (x+(w/2)))*z)
    elif x+(w/2) > cw:
        sCon.setTarget(0, sCon.getPosition(0) + ((x+(w/2)) - cw)*z)
    if y+h/2 < ch:
        sCon.setTarget(1, sCon.getPosition(1) - (ch - (y+(h/2)))*t)
    elif y+h/2 > ch:
        sCon.setTarget(1, sCon.getPosition(1) + ((y+(h/2)) - ch)*t)



if __name__ == "__main__":
    capture = cv2.VideoCapture(0)

    capture.set(3,640)
    capture.set(4,480)
    capture.set(11,1)

    faces = []
    uppers = []
    frameC = 0
    i = 0
    ret, image = capture.read()
    ih, iw = image.shape[:2]
    cw = iw / 2
    ch = ih / 2

    while True:
        ret, image = capture.read()

        #draw dot in center
        ih, iw = image.shape[:2]
        cv2.circle(image, (iw/2, ih/2), 3, (0,0, 255), -1)

        #flip image vertically
        image = cv2.flip(image, 1)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if i%2==0:
            faces = detect_faces(gray)
        big = 0
        temp = 0
        tempw = 0
        temph = 0

        if faces != []:
            for (x,y,w,h) in faces:
                temp = w*h
                if temp > big:
                    tempw = w
                    temph = h
                    big = temp
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
            frameC = i
            #tracking
            track(x,y,w,h,cw,ch)
        if i - frameC > 40 and sCon.getMovingState() == False:
            sCon.runScriptSub(0)

        cv2.imshow("video", image)
        if cv2.waitKey(33) == 27:
            capture.release()
            #sCon.stopScript()
            exit()
        i += 1

