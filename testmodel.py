import cv2
import time

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Trainer.yml") 

name_list = ["", "Martin"]  

imgBackground = cv2.imread("whitebackground.jpg")

while True:
    ret, frame = video.read()

  
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    
    faces = facedetect.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        
        serial, conf = recognizer.predict(gray[y:y+h, x:x+w])
        if 0 <= serial < len(name_list) and conf < 60:  
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  
            cv2.rectangle(frame, (x, y-40), (x+w, y), (0, 255, 0), -1)
            cv2.putText(frame, name_list[serial], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)  
            cv2.rectangle(frame, (x, y-40), (x+w, y), (0, 0, 255), -1)
            cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    frame = cv2.resize(frame, (640, 480))
    if imgBackground is not None:
        imgBackground[162:162 + 480, 55:55 + 640] = frame
        cv2.imshow("Frame", imgBackground)
    else:
        cv2.imshow("Frame", frame)

    k = cv2.waitKey(1)

    
    if k == ord('q'):
        break
    elif k == ord('o') and conf < 60: 
        cv2.imwrite("captured_face.jpg", frame[y:y+h, x:x+w])  
        time.sleep(2)  

video.release()
cv2.destroyAllWindows()