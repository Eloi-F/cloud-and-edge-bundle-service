import base64
import cv2

from src.common.local.bundle import get_identification_seq, get_identification_parallel

# Initialize the default camera device
cap = cv2.VideoCapture(0)

# Configure camera resolution
cap.set(3, 640)
cap.set(4, 480)


def identification(cycle: int = 100, parallel_exec: bool = False):
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
        # Capture a frame from the camera, encode it as jpeg, and convert it to Base64
        _, img = cap.read()
        _, buffer = cv2.imencode(".jpg", img)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        data = {"img": img_base64}

        if parallel_exec:
            response = get_identification_parallel(payload=data)
        else:
            response = get_identification_seq(payload=data)

        box = response["box"]
        classId = response["classId"]

        # Draw bounding box around detected object
        cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)

        # Display detected class label
        cv2.putText(
            img,
            classId,
            (box[0] + 10, box[1] + 30),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 0),
            1,
        )

        # Display annotated frame
        cv2.imshow("Output", img)
        cv2.waitKey(1)

        if not parallel_exec:
            return
