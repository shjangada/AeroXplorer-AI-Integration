import boto3
import csv
import json

# Load airline keywords
with open('airline_keywords.json') as f:
    airline_keywords = json.load(f)

# Set up Rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1')
bucket = 'aeroxplorer-rekognition'
image_keys = [
    'imagesCUBE/airplane1.jpg',
    'imagesCUBE/airplane2.jpeg',
    'imagesCUBE/AA-Spirit-STX-3-28-24.jpg',
    'imagesCUBE/model-planes-airplanes-miniatur-wunderland-hamburg-163792.jpeg'
]

# CSV output rows
rows = [("Filename", "Text Detected", "Airline_1", "Airline_2")]

def match_airlines(text_detections):
    detected_airlines = []
    for text in text_detections:
        for keyword, airline in airline_keywords.items():
            if keyword.lower() in text.lower() and airline not in detected_airlines:
                detected_airlines.append(airline)
    return detected_airlines[:2] + [None] * (2 - len(detected_airlines))  # ensure 2 slots

for image_key in image_keys:
    print(f"Processing: {image_key}")
    resp = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': image_key}})
    lines = [text['DetectedText'] for text in resp['TextDetections'] if text['Type'] == 'LINE']
    
    airline_1, airline_2 = match_airlines(lines)
    rows.append((image_key, ", ".join(lines), airline_1, airline_2))

# Save CSV
with open("airline_detection_report.csv", "w", newline="") as f:
    csv.writer(f).writerows(rows)

print("airline_detection_report.csv saved.")
