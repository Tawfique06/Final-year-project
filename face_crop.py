#!/usr/bin/python3
import os
import cv2
from mtcnn import MTCNN


def crop_face(image_path, save_directory='./static'):
    """Face detection using Multi-task Cascaded Convolutional Network-MTCCN"""

    detector = MTCNN()

    img = cv2.imread(image_path)
    faces = detector.detect_faces(img)

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for i, face in enumerate(faces):
        x, y, w, h = face['box']
        face_crop = img[y:y+h, x:x+w]  # Crop face region
        save_path = os.path.join(save_directory, f"face_{i}.jpg")
        cv2.imwrite(save_path, face_crop)  # Save cropped face image
        print(f"Face {i+1} cropped and saved successfully at: {save_path}")
        