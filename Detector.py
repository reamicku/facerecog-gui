import cv2
from time import time
from PIL import Image
from tkinter import messagebox

def main_app(name, timeout = 8):
    face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(f"./data/classifiers/{name}_classifier.xml")
    cap = cv2.VideoCapture(0)
    pred = False
    start_time = time()
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h,x:x+w]
            id,confidence = recognizer.predict(roi_gray)
            confidence = 100 - int(confidence)
            if confidence > 50:
                pred = True
                text = 'Rozpoznano: '+ name.upper()
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
            else:   
                pred = False
                text = "Nieznana twarz"
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)
        cv2.imshow("image", frame)

        elapsed_time = time() - start_time
        if elapsed_time >= timeout:
            print(pred)
            if pred:
                messagebox.showinfo('Gratulacje', 'Zostałeś rozpoznany.')
            else:
                messagebox.showerror('Uwaga', 'Ponów próbę.')
            break

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
