"""
Identification Service implementation
=====================================

This service initializes the model used for computer vision as
well as the vocabulary set of potentially detected objects.

It provides endpoint function to perform object detection on
an image.
"""

import base64
import numpy as np
import cv2

# Initializing classNames values
classFile = 'coco.names' #Common Objects in Context dataset
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# Build and configure model (SSD Mobilenet V3)
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'
net = cv2.dnn_DetectionModel(weightsPath,configPath)

net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5)) # Normalizing pixel values
net.setInputSwapRB(True) # OpenCV uses BGR by default

def identification(img_base64):
    """
    Detect objects on camera flow using cv2.
    :param img_base64: camera feed
    :return: array of detected objects
    """
    # Decode image to cv2 expected format
    try:
        img_bytes = base64.b64decode(img_base64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            print("Failed to decode image from base64 input")
            return []
    except Exception as e:
        print(f"Image decoding error: {e}")
        return []

    # Detect objects on image
    # classIds contains detected classes (0 or 1)
    # confs contains the associated confidence score for each class
    # bbox contains the part of the image for each detected object
    classIds, confs, bbox = net.detect(img, confThreshold=0.6)

    # return array with all detected objects
    detections = []
    for classId, conf, box in zip(classIds.flatten(),
                                  confs.flatten(),
                                  bbox):
        detections.append({
            "classId": classNames[classId - 1],
            "confidence": round(float(conf), 3),
            "box": {
                "x": int(box[0]),
                "y": int(box[1]),
                "width": int(box[2]),
                "height": int(box[3])
            }
        })
    return detections
