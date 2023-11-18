from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import base64

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model(r"E:\cnm\NhanDang\keras_model.h5", compile=False)

# Load the labels
class_names = ["Không có người", "Có người"]



def detection():
    # CAMERA can be 0 or 1 based on default camera of your computer
    camera = cv2.VideoCapture(0)

    while True:
        # Grab the webcamera's image.
        ret, image = camera.read()
        output_image = image.copy()
        
        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        output_image = cv2.resize(output_image, (300, 230), interpolation=cv2.INTER_AREA)

        # Show the image in a window
        retval, buffer = cv2.imencode('.jpg', output_image)
        jpg_as_text = base64.b64encode(buffer)

        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predicts the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        confidence_score = str(np.round(confidence_score * 100))[:-2]
        class_name = 'image too big' if len(jpg_as_text) > 102400 else f'{class_name}'
        

        
        if len(jpg_as_text) > 102400:
            class_name = 'image too big'
            img = cv2.imread('too_big.png')
            img = cv2.resize(img, (300, 230), interpolation=cv2.INTER_AREA)
            retval, buffer = cv2.imencode('.jpg', img)
            jpg_as_text = base64.b64encode(buffer)

        camera.release()
        cv2.destroyAllWindows()
        return jpg_as_text, class_name, confidence_score
