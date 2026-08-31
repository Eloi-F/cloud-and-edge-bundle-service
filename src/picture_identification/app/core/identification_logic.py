import base64

import cv2
import numpy as np
from ultralytics import YOLO

from src.models.schemas import BoundingBox, Detection

from src.picture_identification.app.core.config import MODEL_PATH
import logging

logger = logging.getLogger(__name__)

model = YOLO(MODEL_PATH)


def identify_objects(img_base64: str) -> list[Detection]:
    """
    Detect objects on an image using YOLO.
    """

    try:
        logger.debug("Starting identifying objects.")
        img_bytes = base64.b64decode(img_base64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return []

    except Exception:
        return []

    results = model(source=img)

    detections: list[Detection] = []

    for result in results:
        logger.debug("Object detected.")
        boxes = result.boxes.xyxy.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy().astype(int)
        confs = result.boxes.conf.cpu().numpy()

        for box, class_id, conf in zip(boxes, class_ids, confs):
            x1, y1, x2, y2 = box

            detections.append(
                Detection(
                    class_id=result.names[class_id],
                    confidence=round(float(conf), 3),
                    box=BoundingBox(
                        x=int(x1),
                        y=int(y1),
                        width=int(x2 - x1),
                        height=int(y2 - y1),
                    ),
                )
            )

    logger.debug("Finished identifying objects.")
    return detections
