import numpy as np
from PIL import Image
import os, cv2

def train_classifer(name):
    path = os.path.join(os.getcwd()+"/data/capture/"+name+"/")

    faces = []
    ids = []
    labels = []
    pictures = {}

    for root,dirs,files in os.walk(path):
        pictures = files

    for pic in pictures :
        imgpath = path+pic
        img = Image.open(imgpath).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(pic.split(name)[0])
        faces.append(imageNp)
        ids.append(id)
    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    print("./data/classifiers/"+name+"_classifier.xml")
    clf.write("./data/classifiers/"+name+"_classifier.xml")
