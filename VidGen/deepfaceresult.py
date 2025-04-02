import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import cv2 # type: ignore
#cv video işlemede kullanılan kütüphane
import numpy as np
from deepface import DeepFace # type: ignore
#cv den aldığımız frameleri incelemek icin kullanacağımız kütüpane


class DeepFaceResults:
    def __init__(self):
        # def init clası oluşturuken kullandığımız temel yapı 
        #self classsın icinde değişkeni kullanabilmemizisağlayan şeydir
        self.path = ""
        self.frames = []
        DeepFace.build_model("VGG-Face")
       

    def start(self, path, progress_signal):
        self.path = path
        return self.detected_frames(progress_signal)


    def detected_frames(self, progress_signal):
        vidObj = cv2.VideoCapture(self.path)
        success = True


        while success:
            success, frame = vidObj.read()
            #videocapture fonksiyonu ile aldığımız değişkeni read fonksiyonu ile framelere ayırıyoruz
            if success:
                frame = cv2.resize(frame, (224, 224))
                self.frames.append(frame)
                #read ile aldığımız frameleri frames dizisine kaydetmeye yarar
        number_of_frames = len(self.frames)

        
        for idx, frame in enumerate(self.frames):
            percent = int(((idx + 1) / number_of_frames) * 100)
            progress_signal.emit(percent)  

            if not self.tensorflow_model(frame):
                return "Fake"
        return "Real"

    def tensorflow_model(self, frame):
        if not isinstance(frame, np.ndarray):
            return False
        
        temp_path = "temp_frame.jpg"
        cv2.imwrite(temp_path, frame)
        #framesin içinden aldığımız frameleri temp pathe göndererek işncelememiz icin saklıyor

        analysis = DeepFace.extract_faces(
            temp_path,
            detector_backend='opencv',
            anti_spoofing=True,
            enforce_detection=False,
        )
        

        for i, face in enumerate(analysis):
            print(face)
            if not face['is_real']:
                return False

        return True


# Driver Code
if __name__ == "__main__":
    deep_face = DeepFaceResults() 
    deep_face.start()
