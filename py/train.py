import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight

# ✅ Dataset Paths
base_dir = os.path.join(os.getcwd(), "datasets")
train_dir = os.path.join(base_dir, "Training")
val_dir = os.path.join(base_dir, "Validation")
test_dir = os.path.join(base_dir, "Testing")

# ✅ Ensure Dataset Exists
for path in [train_dir, val_dir, test_dir]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"⚠️ Dataset directory '{path}' not found! Check paths.")

# ✅ Image Augmentation & Preprocessing
image_size = (224, 224)
batch_size = 32

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=40,
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.3,
    zoom_range=0.3,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest'
)

val_test_datagen = ImageDataGenerator(rescale=1.0 / 255)

# ✅ Load Dataset
train_data = train_datagen.flow_from_directory(
    train_dir, target_size=image_size, batch_size=batch_size, class_mode="categorical"
)

val_data = val_test_datagen.flow_from_directory(
    val_dir, target_size=image_size, batch_size=batch_size, class_mode="categorical"
)

test_data = val_test_datagen.flow_from_directory(
    test_dir, target_size=image_size, batch_size=batch_size, class_mode="categorical", shuffle=False
)

# ✅ Extract Species Names
class_labels = {v: k for k, v in train_data.class_indices.items()}
print(f"🔍 Class Labels: {class_labels}")

# ✅ Compute Class Weights for Imbalanced Data
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(train_data.classes),
    y=train_data.classes
)
class_weight_dict = dict(enumerate(class_weights))

# ✅ Load Pretrained MobileNetV2 Model
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze pretrained layers

# ✅ Build Model
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(512, activation="relu"),
    Dropout(0.5),
    Dense(len(class_labels), activation="softmax")  # Output layer for species classification
])

# ✅ Compile Model
model.compile(optimizer=Adam(learning_rate=0.0001), loss="categorical_crossentropy", metrics=["accuracy"])

# ✅ Training Callbacks
early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, verbose=1)

# ✅ Train Model
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=50,  # Increased epochs for better training
    class_weight=class_weight_dict,  # Handle imbalanced classes
    callbacks=[early_stop, reduce_lr]
)

# ✅ Save Model
model.save("wildlife_species_model.h5")
print("✅ Model Saved Successfully!")

# ✅ Evaluate Model
test_loss, test_acc = model.evaluate(test_data)
print(f"📊 Test Accuracy: {test_acc * 100:.2f}%")
