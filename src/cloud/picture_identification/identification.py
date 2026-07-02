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
import os
from ultralytics import YOLO

MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "./yolo26x.pt")

model = YOLO(MODEL_PATH)


def identification(img_base64):
    """
    Detect objects on camera flow using YOLO.
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

    results = model(source=img)

    detections = []
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy().astype(int)
        confs = result.boxes.conf.cpu().numpy()

        names = result.names

        for box, class_id, conf in zip(boxes, class_ids, confs):
            x1, y1, x2, y2 = box

            detections.append(
                {
                    "classId": names[class_id],
                    "confidence": round(float(conf), 3),
                    "box": {
                        "x": int(x1),
                        "y": int(y1),
                        "width": int(x2 - x1),
                        "height": int(y2 - y1),
                    },
                }
            )
    return detections
