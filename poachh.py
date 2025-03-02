from ultralytics import YOLO
import cv2

# Load the advanced YOLOv8 model (pre-trained on COCO dataset)
model = YOLO("yolov8x.pt")  # "yolov8x.pt" is more accurate than "yolov8n.pt"

# List of relevant objects for detection
dangerous_objects = ["person", "gun", "rifle", "knife", "vehicle"]
weapons = ["gun", "rifle", "knife"]
animals_of_interest = ["elephant", "tiger", "deer"]  # Add more animals as needed

def detect_poaching_activity(image_path):
    # Load image
    img = cv2.imread(image_path)

    # Run YOLO detection
    results = model(image_path)

    # Initialize variables
    detected_objects = []
    poacher_detected = False
    weapon_detected = False
    animal_detected = False
    person_count = 0
    weapon_count = 0
    animal_count = 0
    weapons_found = []
    detected_animals = []

    # Process results
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])  # Get class ID
            conf = float(box.conf[0])  # Get confidence score
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates

            # Get class name
            class_name = model.names[cls]

            # Debug: Print out detected class names
            # print(f"Detected class: {class_name} with confidence: {conf:.2f}")

            # Check if object is relevant
            if class_name in dangerous_objects:
                detected_objects.append(class_name)

                # Count persons
                if class_name == "person":
                    person_count += 1
                    poacher_detected = True
                    # Draw bounding box for persons (blue color)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red for weapons
                    cv2.putText(img, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


                # Count weapons (guns, rifles, knives)
                if class_name in weapons:
                    weapon_count += 1
                    weapon_detected = True
                    weapons_found.append(class_name)
                    # Draw bounding box for weapons (red color)
                    # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red for weapons
                    # cv2.putText(img, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                # Detect animals (for example: elephants, tigers, deer)
            if class_name in animals_of_interest:
                animal_count += 1
                detected_animals.append(class_name)
                animal_detected = True
                # Draw bounding box for animals (green color)
                # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green for animals
                # cv2.putText(img, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


                # # Draw bounding box with label
                # color = (0, 0, 255) if class_name in weapons else (255, 0, 0)  # Red for weapons, Blue for others
                # cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                # cv2.putText(img, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Save the output image
    output_path = "poacher_detected.jpg"
    cv2.imwrite(output_path, img)

    # Generate AI-generated textual report based on detections
    if poacher_detected: 
        if weapon_detected and poacher_detected and animal_detected:
            description = "🚨 **Critical Alert**: Armed poachers have been detected in close proximity to wildlife! Immediate intervention is required to prevent harm to endangered animals. Authorities must respond urgently to safeguard the animals."
        elif weapon_detected and poacher_detected:
            description = "⚠️ Armed poachers have been detected in the forest. They may pose a serious threat to the wildlife. Immediate action is necessary."
        elif animal_detected:
            description = "🚨 **Critical Alert**: Humans spotted near wildlife in a potentially dangerous area. Immediate action is required to protect the animals from possible poaching."
        else:
            description = "👀 Unauthorized individuals detected in a restricted area. Possible poaching attempt detected."
    else:
        if animal_detected:
            description = "✅ No poaching activity detected, but **animals are present** in the area. Authorities should monitor to ensure their safety."
        else:
            description = "✅ No suspicious activity detected. The area appears safe."

    return output_path, description, detected_objects, person_count, weapons_found, weapon_count, animal_count, detected_animals

# Example usage
output_image, detection_report, detected_items, num_persons, detected_weapons, weapon_count, animals_num, detected_animal_list = detect_poaching_activity("noWeapon.png")

# Print AI-generated report
print(f"Detection Report: {detection_report}")
print(f"Number of Persons Detected: {num_persons}")
print(f"Number of Weapons Detected: {weapon_count}")
print(f"Number of Animals Detected: {animals_num}")
print(f"Animals Detected: {detected_animal_list}")
print(f"Processed Image Saved As: {output_image}")
