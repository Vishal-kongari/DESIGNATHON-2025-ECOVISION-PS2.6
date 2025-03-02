import cv2
import numpy as np

def detect_and_analyze_forest_changes(old_image_path, new_image_path, output_path):
    old_img = cv2.imread(old_image_path, cv2.IMREAD_COLOR)
    new_img = cv2.imread(new_image_path, cv2.IMREAD_COLOR)
    new_img = cv2.resize(new_img, (old_img.shape[1], old_img.shape[0]))

    old_gray = cv2.cvtColor(old_img, cv2.COLOR_BGR2GRAY)
    new_gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(old_gray, new_gray)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5,5), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    new_img[processed == 255] = [0, 0, 255]
    cv2.imwrite(output_path, new_img)

    old_hsv = cv2.cvtColor(old_img, cv2.COLOR_BGR2HSV)
    new_hsv = cv2.cvtColor(new_img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 50, 50])
    upper_green = np.array([90, 255, 255])
    old_green_mask = cv2.inRange(old_hsv, lower_green, upper_green)
    new_green_mask = cv2.inRange(new_hsv, lower_green, upper_green)

    old_green_pct = np.sum(old_green_mask > 0) / old_green_mask.size * 100
    new_green_pct = np.sum(new_green_mask > 0) / new_green_mask.size * 100
    vegetation_change = new_green_pct - old_green_pct
    change_type = "increase" if vegetation_change > 0 else "decrease"

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(processed, connectivity=8)
    deforestation_regions = num_labels - 1

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    old_water_mask = cv2.inRange(old_hsv, lower_blue, upper_blue)
    new_water_mask = cv2.inRange(new_hsv, lower_blue, upper_blue)
    old_water_pct = np.sum(old_water_mask > 0) / old_water_mask.size * 100
    new_water_pct = np.sum(new_water_mask > 0) / new_water_mask.size * 100

    lower_gray = np.array([0, 0, 50])
    upper_gray = np.array([180, 50, 200])
    old_urban_mask = cv2.inRange(old_hsv, lower_gray, upper_gray)
    new_urban_mask = cv2.inRange(new_hsv, lower_gray, upper_gray)
    old_urban_pct = np.sum(old_urban_mask > 0) / old_urban_mask.size * 100
    new_urban_pct = np.sum(new_urban_mask > 0) / new_urban_mask.size * 100
    urban_growth = new_urban_pct - old_urban_pct

    lower_burnt = np.array([0, 0, 0])
    upper_burnt = np.array([50, 50, 50])
    old_burnt_mask = cv2.inRange(old_hsv, lower_burnt, upper_burnt)
    new_burnt_mask = cv2.inRange(new_hsv, lower_burnt, upper_burnt)
    old_burnt_pct = np.sum(old_burnt_mask > 0) / old_burnt_mask.size * 100
    new_burnt_pct = np.sum(new_burnt_mask > 0) / new_burnt_mask.size * 100
    burnt_change = new_burnt_pct - old_burnt_pct

    lower_soil = np.array([10, 50, 50])
    upper_soil = np.array([30, 255, 255])
    old_soil_mask = cv2.inRange(old_hsv, lower_soil, upper_soil)
    new_soil_mask = cv2.inRange(new_hsv, lower_soil, upper_soil)
    old_soil_pct = np.sum(old_soil_mask > 0) / old_soil_mask.size * 100
    new_soil_pct = np.sum(new_soil_mask > 0) / new_soil_mask.size * 100
    soil_change = new_soil_pct - old_soil_pct

    report = f"""
    🌍 Environmental Change Analysis:
    -------------------------------------
    📊 Initial Vegetation Cover: {old_green_pct:.2f}%
    📈 Current Vegetation Cover: {new_green_pct:.2f}%
    🔍 Change in Vegetation: {abs(vegetation_change):.2f}% ({change_type})
    🛑 Observation: {'🚨 Deforestation detected!' if vegetation_change < 0 else '✅ Reforestation detected.'}
    
    🔥 Burnt Areas: {old_burnt_pct:.2f}% → {new_burnt_pct:.2f}% (Change: {burnt_change:.2f}%)
    🌊 Water Bodies: {old_water_pct:.2f}% → {new_water_pct:.2f}% (Change: {new_water_pct - old_water_pct:.2f}%)
    🏙️ Urban Growth: {old_urban_pct:.2f}% → {new_urban_pct:.2f}% (Change: {urban_growth:.2f}%)
    🏜️ Soil Exposure: {old_soil_pct:.2f}% → {new_soil_pct:.2f}% (Change: {soil_change:.2f}%)
    🛑 Deforestation Hotspots Identified: {deforestation_regions}
    """
    return output_path, report

output_image, analysis_report = detect_and_analyze_forest_changes("src/past.png", "src/recent.png", "change_detected.jpg")
print(analysis_report)
print(f"Processed Image Saved As: {output_image}")
