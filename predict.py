import numpy as np
import tensorflow as tf
import cv2,os
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Define the model architecture
def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(300, 300, 3)),
        tf.keras.layers.MaxPooling2D((2,2)),
        tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Conv2D(16, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(6, activation='softmax')
    ])
    return model

# Load the trained model
model_path = 'garbage_classifier_.h5'
model = create_model()
model.load_weights(model_path)

# Function to preprocess the image
def preprocess_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image file at {image_path} does not exist.")
    
    # Load the image
    img = load_img(image_path, target_size=(300, 300))  # Target size should match the input size of the model
    if img is None:
        raise ValueError(f"Failed to load image at {image_path}")
    
    # Convert the image to array
    img_array = img_to_array(img)
    # Expand dimensions to match the input shape of the model (1, 300, 300, 3)
    img_array = np.expand_dims(img_array, axis=0)
    # Normalize the image array
    img_array /= 255.0
    return img_array

# Function to predict the class of the image
def predict_class(image_path):
    try:
        # Preprocess the image
        img_array = preprocess_image(image_path)
        # Predict the class
        predictions = model.predict(img_array)
        # Get the index of the class with the highest probability
        predicted_class_index = np.argmax(predictions[0])
        return predicted_class_index
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return None

if __name__ == '__main__':
    # Path to the new image
    new_image_path = 'data/garbage/swaret.jpg'

    # Predict the class of the new image
    predicted_class = predict_class(new_image_path, model)

    # Mapping class indices to class labels
    class_indices = {'cardboard': 0, 'glass': 1, 'metal': 2, 'paper': 3, 'plastic': 4, 'trash': 5}
    class_labels = {v: k for k, v in class_indices.items()}

    if predicted_class is not None:
        # Get the predicted class label
        predicted_class_label = class_labels.get(predicted_class, "Unknown")
        print(f"The predicted class for the new image is: {predicted_class_label}")
    else:
        print("Prediction failed.")

