import tensorflow as tf
import numpy as np
import cv2
import os

# ✅ Step 1: Load Model
model = tf.keras.models.load_model("tiger_recognition_model.h5")

# ✅ Step 2: Load Class Labels
train_dir = "C:/Users/Rammohan/Desktop/vnr_hack/py/ds/train"
class_labels = sorted(os.listdir(train_dir))

# ✅ Step 3: Function to Predict Image
def predict_tiger(image_path):
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found!")
        return
    
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Error: Could not read image '{image_path}'. Check file path and format!")
        return
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    img = cv2.resize(img, (224, 224))  # Resize for MobileNetV2
    img = img / 255.0  # Normalize
    img = np.expand_dims(img, axis=0)  # Expand dimensions for model

    prediction = model.predict(img)
    predicted_class = np.argmax(prediction)

    print(f"✅ Recognized Tiger: {class_labels[predicted_class]}")

# ✅ Step 4: Test with an Image
test_image_path = "C:/Users/Rammohan/Desktop/vnr_hack/py/ds/test/Tiger 1/18.jpg"  # Change to your test image
predict_tiger(test_image_path)
