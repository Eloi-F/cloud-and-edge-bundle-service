import base64
import time
import cv2

from bundle import get_identification

# Initialize the default camera device
cap = cv2.VideoCapture(0)

# Configure camera resolution
cap.set(3, 640)
cap.set(4, 480)


def identification(responses_cloud: list[float]):
    """
    Main object-identification loop.
    """
    while True:
        # Capture a frame from the camera, encode it as jpeg, and convert it to Base64
        _, img = cap.read()
        _, buffer = cv2.imencode(".jpg", img)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        data = {"img": img_base64}

        # Start latency measurement
        t1 = time.time()
        response = get_identification(payload=data)

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

        # End latency measurement
        t2 = time.time()

        print("delay identification [cloud] = ", (t2 - t1) * 1000)

        # Store latency value in milliseconds
        responses_cloud.append((t2 - t1) * 1000)

    # Originally intended latency collection
    # print(responses_cloud)
