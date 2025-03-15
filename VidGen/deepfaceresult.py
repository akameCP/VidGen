
import cv2
import numpy as np
from deepface import DeepFace
from tensorflow.keras.applications.xception import Xception


class DeepFaceResults:
    def __init__(self):
        self.path = ""
        self.frames = []
        self.model = Xception(weights='imagenet')

    def start(self, path, progress_signal):
        self.path = path
        return self.detected_frames(progress_signal)

    def detected_frames(self, progress_signal):
        vidObj = cv2.VideoCapture(self.path)
        success = True

        while success:
            success, frame = vidObj.read()
            if success:
                self.frames.append(frame)

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

        analysis = DeepFace.extract_faces(
            temp_path,
            anti_spoofing=True,
            enforce_detection=False
        )

        for i, face in enumerate(analysis):
            if not face['is_real']:
                return False

        return True


# Driver Code
if __name__ == "__main__":
    deep_face = DeepFaceResults() 
    deep_face.start() 