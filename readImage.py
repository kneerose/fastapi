from io import BytesIO
from PIL import Image
# from tensorflow.keras.applications.imagenet_utils import decode_predictions
def read_image(image_encoded):
    pil_image = Image.open(BytesIO(image_encoded))
    print(pil_image);
    return pil_image