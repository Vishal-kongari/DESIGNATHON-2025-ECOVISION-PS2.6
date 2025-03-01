import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import accuracy_score
import os

# Load the trained model
model_path = "C:/Users/Rammohan/Desktop/vnr_hack/wildlife_species_model.h5"
model = tf.keras.models.load_model(model_path)

# Define test data directory
test_data_dir = "C:/Users/Rammohan/Desktop/vnr_hack/datasets/Testing"  # Change this to your test dataset path

# Image preprocessing (resize to match model input shape)
img_height = 224  # Update according to your model input shape
img_width = 224
batch_size = 32  # Change if needed

# Load test images
test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)  # Normalize if done during training
test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode="categorical",  # Change to "binary" if only 2 classes
    shuffle=False
)

# Predict classes
y_pred = model.predict(test_generator)
y_pred_classes = np.argmax(y_pred, axis=1)  # Convert probabilities to class indices

# Get true labels
y_true = test_generator.classes

# Calculate accuracy
accuracy = accuracy_score(y_true, y_pred_classes)
print(f"Model Accuracy: {accuracy:.4f}")
