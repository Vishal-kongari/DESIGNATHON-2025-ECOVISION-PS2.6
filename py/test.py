import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# ✅ Load Trained Model
model = tf.keras.models.load_model("wildlife_species_model.h5")

# ✅ Define Class Labels
class_labels = {
    0: "African Wild Dog",
    1: "Asian Elephant",
    2: "Banteng",
    3: "Black Rhinoceros",
    4: "Darwins Fox",
    5: "Indri",
    6: "Tasmanian Devil",
    7: "Tiger",
    8: "Verreaux Sifaka",
    9: "Wild Water Buffalo",
    10: "Capybara",
    11: "Common Racoon",
    12: "Domestic Cat"
}

# ✅ Function to preprocess input image
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# ✅ Predict Function
def predict_species(image_path):
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)  # Get predicted index
    species_name = class_labels.get(predicted_class, "Unknown")  # Get species name
    confidence = np.max(predictions) * 100  # Confidence score

    print(f"🔍 Predicted Species: {species_name} ({confidence:.2f}%)")
    return species_name, confidence

# ✅ Run a Prediction
test_image = os.path.join("datasets", "Testing",  "Tiger", "22.jpg")

if os.path.exists(test_image):
    predict_species(test_image)
else:
    print(f"⚠️ Image not found! Check path: {test_image}")
