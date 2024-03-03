#!/usr/bin/python3
import os
import cv2
from mtcnn import MTCNN


def detect_and_save_faces_mtcnn(image_path, save_directory='./'):
    detector = MTCNN()

    # Read the image
    img = cv2.imread(image_path)

    # Detect faces in the image
    faces = detector.detect_faces(img)

    # Create directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Crop and save each detected face
    for i, face in enumerate(faces):
        x, y, w, h = face['box']
        face_crop = img[y:y+h, x:x+w]  # Crop face region
        save_path = os.path.join(save_directory, f"face_{i}.jpg")
        cv2.imwrite(save_path, face_crop)  # Save cropped face image
        print(f"Face {i+1} cropped and saved successfully at: {save_path}")



# Example usage:
image_path = "../static/2b31e75c-bf6d-4f1e-8066-e191af2c5cd8.jpg"
save_directory = "./"
detect_and_save_faces_mtcnn(image_path, save_directory)
