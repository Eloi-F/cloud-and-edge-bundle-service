from io import BytesIO
import base64
from PIL import Image
import logging

logger = logging.getLogger(__name__)
IMG_SIZE = 640


def crop_with_padding(img_b64: str):
    """
    Resize endpoint logic. Transform input image to
    IMG_SIZE x IMG_SIZE dimensions.
    :param img_b64:
    :return:
    """

    logger.debug("Resizing input image...")

    # Decode base64 image
    image_data = base64.b64decode(img_b64)
    image = Image.open(BytesIO(image_data)).convert("RGB")

    # Resize given image
    ratio = min(IMG_SIZE / image.width, IMG_SIZE / image.height)
    new_width = round(image.width * ratio)
    new_height = round(image.height * ratio)

    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (IMG_SIZE, IMG_SIZE), (114, 114, 114))

    x = (IMG_SIZE - new_width) // 2
    y = (IMG_SIZE - new_height) // 2

    canvas.paste(image, (x, y))

    output = BytesIO()
    canvas.save(output, format="JPEG")

    # Encode in base64 resized image
    resized_b64 = base64.b64encode(output.getvalue()).decode("utf-8")

    logger.debug(f"Successfully resized input image to {IMG_SIZE}x{IMG_SIZE}.")
    return resized_b64
