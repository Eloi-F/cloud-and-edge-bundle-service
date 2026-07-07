import base64
import threading
import cv2

from core.bundle import get_identification_seq, get_identification_parallel

# Initialize the default camera device
cap = cv2.VideoCapture(0)

# Configure camera resolution
cap.set(3, 640)
cap.set(4, 480)


def identification(
    stop_event: threading.Event,
    cycle: int = 100,
    parallel_exec: bool = False,
):
    """
    Captures camera frames and sends them to the identification service.

    Each frame is encoded as JPEG, converted to Base64, and sent to either the
    sequential or parallel identification endpoint. The returned bounding box
    and class label are drawn on the frame before displaying it.

    In sequential mode, the function processes a single frame and returns.
    In parallel mode, it repeats the process for the specified number of cycles.

    :param cycle: Number of iterations in parallel mode.
    :param parallel_exec: Selects the parallel or sequential endpoint.
    """
    for _ in range(cycle):
        if stop_event.is_set():
            break

        # Capture a frame from the camera, encode it as jpeg, and convert it to Base64
        _, img = cap.read()
        _, buffer = cv2.imencode(".jpg", img)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        data = {"img": img_base64}

        if parallel_exec:
            detections = get_identification_parallel(payload=data)
        else:
            detections = get_identification_seq(payload=data)

        for element in detections:
            box_dict = element["box"]

            pt1 = (box_dict["x"], box_dict["y"])
            pt2 = (
                box_dict["x"] + box_dict["width"],
                box_dict["y"] + box_dict["height"],
            )

            cv2.rectangle(img, pt1, pt2, color=(0, 255, 0), thickness=2)

            label = f"{element['classId']} ({element['confidence']})"

            cv2.putText(
                img,
                label,
                (pt1[0], pt1[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        # Display annotated frame
        cv2.imshow("Output", img)
        cv2.waitKey(1)

        if not parallel_exec:
            return
