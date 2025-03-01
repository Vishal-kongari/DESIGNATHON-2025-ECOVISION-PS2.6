import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Flatten, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import os

# ✅ Step 1: Define dataset paths (Update this to your actual path)
train_dir = "C:/Users/Rammohan/Desktop/vnr_hack/py/ds/train"
val_dir = "C:/Users/Rammohan/Desktop/vnr_hack/py/ds/test"

# ✅ Step 2: Data Augmentation
datagen = ImageDataGenerator(rescale=1./255)

train_dataset = datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='sparse'
)

val_dataset = datagen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='sparse'
)

# ✅ Step 3: Load Pre-trained MobileNetV2
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze pre-trained layers

# ✅ Step 4: Add Custom Layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)  # Prevent overfitting
predictions = Dense(len(train_dataset.class_indices), activation='softmax')(x)

# ✅ Step 5: Compile Model
model = Model(inputs=base_model.input, outputs=predictions)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# ✅ Step 6: Train the Model
print("Training the model...")
model.fit(train_dataset, validation_data=val_dataset, epochs=20)

# ✅ Step 7: Save the Model
model.save("tiger_recognition_model.h5")
print("Model saved as tiger_recognition_model.h5")
