import os
import numpy as np
import tensorflow as tf
import spacy
import pdfplumber
import requests
from bs4 import BeautifulSoup
import hashlib
import csv
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from twilio.rest import Client
from src.summary import summarize_text, extract_text_from_pdf, scrape_wikipedia
import shutil
from pathlib import Path
import cv2
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles  # Import StaticFiles
from fastapi import FastAPI, File, UploadFile, Form
import cv2
import numpy as np
import shutil
from pathlib import Path
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles  # Import StaticFiles








app = FastAPI()

# ✅ Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load Models
species_model = tf.keras.models.load_model("C:/Users/Rammohan/Desktop/vnr_hack/wildlife_species_model.h5")
tiger_model = tf.keras.models.load_model("C:/Users/Rammohan/Desktop/vnr_hack/py/tiger_recognition_model.h5")

# ✅ Class Labels
class_labels = {
    0: "African Wild Dog",
    1: "Asian Elephant",
    2: "Banteng",
    3: "Black Rhinoceros",
    4: "Darwin's Fox",
    5: "Indri",
    6: "Tasmanian Devil",
    7: "Tiger",
    8: "Verreaux's Sifaka",
    9: "Wild Water Buffalo",
    10: "Capybara",
}

tiger_labels = {
    0: "Tiger 1",
    1: "Tiger 2",
    2: "Tiger 3",
    3: "Tiger 4",
}

# ✅ Twilio Credentials
TWILIO_ACCOUNT_SID = "ACb001d3862e83788e4549013ee01a16d5"
TWILIO_AUTH_TOKEN = "74367227b8474a6b2a61b13d3f683218"
TWILIO_PHONE_NUMBER = "+19592144242"
OWNER_PHONE_NUMBER = "+918919363969"

# ✅ Tracking Detections
processed_tigers = set()  # Stores names of unique tigers detected
tiger_count = 0  # Tracks total unique tiger count
species_count = {}  # Tracks count for other species

# ✅ CSV File Path
CSV_FILE = "C:/Users/Rammohan/Desktop/vnr_hack/bio_guardian/src/detections.csv"

# ✅ Create CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Filename", "Species", "Confidence (%)", "Latitude", "Longitude", "Count"])

def send_sms(species, confidence, latitude, longitude, count):
    """Sends an SMS with species details & live location."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message_body = (
        f"🔍 Wildlife Alert!\n"
        f"🐾 Species Detected: {species}\n"
        f"📊 Confidence: {confidence:.2f}%\n"
        f"📍 Location: https://www.google.com/maps?q={latitude},{longitude}\n"
        f"📸 Count: {count}"
    )

    message = client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=OWNER_PHONE_NUMBER
    )

    print("✅ SMS Sent:", message.sid)

def preprocess_image(image_path):
    """Preprocess image before prediction."""
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def log_to_csv(filename, species, confidence, latitude, longitude, count):
    """Logs detection data to a CSV file."""
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([filename, species, confidence, latitude, longitude, count])
        




UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload/")
async def predict_species(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
): 
    global tiger_count
    
        
  

    try:
        # ✅ Extract filename
        
        print(f"Received file: {file.filename}, Location: {latitude}, {longitude}")

        # Save file
        file_path  = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())


        # ✅ Save uploaded file temporarily
        

        # ✅ Predict Species
        img_array = preprocess_image(file_path)
        predictions = species_model.predict(img_array)
        predicted_class = int(np.argmax(predictions))  
        species_name = class_labels.get(predicted_class, "Unknown")  
        confidence = float(np.max(predictions)) * 100  
      
        # ✅ Remove temporary file
        os.remove(file_path)
        

        # ✅ If species is "Tiger", identify individual tiger
        tiger_name = None
        if species_name == "Tiger":
            tiger_predictions = tiger_model.predict(img_array)
            tiger_name = tiger_labels.get(int(np.argmax(tiger_predictions)), "Unknown")


            # ✅ If new tiger, increase count
            if tiger_name not in processed_tigers:
                processed_tigers.add(tiger_name)
                tiger_count += 1  # Increment only for new tigers

            count = tiger_count  # Always return current tiger count

            # ✅ Log and Notify
            
            #log_to_csv(image_name, tiger_name, confidence, latitude, longitude, count)
            print(tiger_name, confidence, latitude, longitude, count)
            send_sms(tiger_name, confidence, latitude, longitude, count)
            
            return {
                "species": "Tiger",
                "tiger_name": tiger_name,
                "confidence": round(confidence, 2)-10,
                "latitude": latitude,
                "longitude": longitude,
                "count": count
            }
            

        # ✅ If Not a Tiger, Increment Count Normally
        species_count[species_name] = species_count.get(species_name, 0) + 1

        # ✅ Log and Notify
        #log_to_csv(image_name, species_name, confidence, latitude, longitude, species_count[species_name])
        send_sms(species_name, confidence, latitude, longitude, species_count[species_name])
        print(species_name, confidence, latitude, longitude, species_count[species_name])

        return {
            "species": species_name,
            "confidence": round(confidence, 2)-10,
            "latitude": latitude,
            "longitude": longitude,
            "count": species_count[species_name]
        }

    except Exception as e:
        return {"error": str(e)}


    
@app.post("/summarize_text/")
async def summarize_text_api(text: str = Form(...)):
    """Summarizes plain text input"""
    summary = summarize_text(text)
    return {"summary": summary}

@app.post("/summarize_pdf/")
async def summarize_pdf_api(file: UploadFile = File(...)):
    """Handles PDF summarization"""
    try:
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        pdf_text = extract_text_from_pdf(file_path)
        os.remove(file_path)

        if not pdf_text:
            return {"error": "No text found in the PDF."}

        summary = summarize_text(pdf_text)
        return {"summary": summary}

    except Exception as e:
        return {"error": str(e)}

@app.post("/wikipedia_summary/")
async def wikipedia_summary_api(keywords: str = Form(...)):
    """Fetches Wikipedia summaries"""
    keyword_list = [kw.strip() for kw in keywords.split(',')]
    summary = scrape_wikipedia(keyword_list)
    return {"summary": summary}

UPLOAD_DIR_SPECIES = Path("uploads_species")


UPLOAD_DIR_SPECIES.mkdir(exist_ok=True)

# Serve static files
app.mount("/uploads_species", StaticFiles(directory=UPLOAD_DIR_SPECIES), name="uploads_sepcies")

@app.post("/analyze")
async def analyze_forest_change(past: UploadFile = File(...), recent: UploadFile = File(...)):
    past_path = UPLOAD_DIR_SPECIES / past.filename
    recent_path = UPLOAD_DIR_SPECIES/ recent.filename
    output_filename = "change_detected.jpg"
    output_path =UPLOAD_DIR_SPECIES / output_filename
    
    with past_path.open("wb") as buffer:
        shutil.copyfileobj(past.file, buffer)
    with recent_path.open("wb") as buffer:
        shutil.copyfileobj(recent.file, buffer)
    
    output_file, report = detect_and_analyze_forest_changes(str(past_path), str(recent_path), str(output_path))
    
    return JSONResponse(content={"report": report, "processed_image": f"/uploads_species/{output_filename}"})

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
    🌍 Environmental Change Analysis  :
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


