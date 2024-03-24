import subprocess
import os
import json
from PIL import Image
import pandas as pd
import numpy as np
import re

# Setup source and destination directories
source_directory = "C:\\Users\\ur4me\\Tests Image Dataset\\Tests Image Dataset"  # Update this path to where your DNG files are stored
jpg_directory = "C:\\Users\\ur4me\\Tests Image Dataset\\Extract JPG"  # Update this path to where you want the JPGs saved
metadata_directory = "C:\\Users\\ur4me\\Tests Image Dataset\\Metadata"  # Update this path to where you want the JPGs saved

def extract_jpg_with_orientation(filename):
    if filename.lower().endswith(".dng"):
        # Construct the full file paths
        source_file = os.path.join(source_directory, filename)
        output_file = os.path.join(jpg_directory, filename.lower().replace(".dng", ".jpg"))
        
        # Commands for ExifTool
        cmd_extract = [
            "C:\\Users\\ur4me\\Downloads\\exiftool-12.80\\exiftool.exe",
            "-b",
            "-PreviewImage",
            source_file,
        ]
        
        cmd_orientation = [
            "C:\\Users\\ur4me\\Downloads\\exiftool-12.80\\exiftool.exe",
            "-TagsFromFile",
            source_file,
            "-Orientation",
            output_file,
        ]

        try:
            # Extract the preview image
            with open(output_file, "wb") as outfile:
                result_extract = subprocess.run(cmd_extract, stdout=outfile, stderr=subprocess.PIPE)
            
            # Adjust orientation of the extracted JPG
            if "Error" not in result_extract.stderr.decode():
                result_orientation = subprocess.run(cmd_orientation, stderr=subprocess.PIPE)
                
                # If the operation was successful, check for and delete the backup file
                backup_file = output_file + "_original"
                if os.path.exists(backup_file):
                    os.remove(backup_file)
                    print(f"Removed backup file: {backup_file}")
                
                print(f"Extracted and adjusted JPG for {filename}")
            else:
                print("Extract stderr:", result_extract.stderr.decode())

        except subprocess.CalledProcessError as e:
            print(f"Error processing {filename}: {e}")

def extract_and_cache_metadata(filename):
    source_file = os.path.join(source_directory, filename)
    metadata_file = os.path.join(metadata_directory, filename + '.json')
    
    if os.path.exists(metadata_file):
        print(f"Metadata for {filename} already cached.")
        return
    
    cmd = ["C:\\Users\\ur4me\\Downloads\\exiftool-12.80\\exiftool.exe", "-j", source_file]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        metadata = result.stdout
        with open(metadata_file, 'w') as f:
            f.write(metadata)
        print(f"Metadata for {filename} extracted and cached.")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting metadata for {filename}: {e}")
    except FileNotFoundError:
        print(f"File not found: {source_file}. Ensure the path to Exiftool and the image files are correct.")

def create_hsv_histogram(paths):
    image_path, histogram_path = paths  # Unpack the tuple
    
    # Load the image
    image = Image.open(image_path)
    # Convert to HSV
    hsv_image = image.convert('HSV')
    
    # Extract H, S, V channels and calculate histograms
    h, s, v = np.array(hsv_image).T
    hist_h = np.histogram(h, bins=256, range=(0, 256))[0]
    hist_s = np.histogram(s, bins=256, range=(0, 256))[0]
    hist_v = np.histogram(v, bins=256, range=(0, 256))[0]
    
    # Prepare histogram data for JSON
    histogram_data = {'H': hist_h.tolist(), 'S': hist_s.tolist(), 'V': hist_v.tolist()}
    
    # Save histogram data as JSON
    with open(histogram_path, 'w') as outfile:
        json.dump(histogram_data, outfile)
    
    print(f"Histogram saved for {image_path}")

def roman_to_arabic(roman):
    roman_numerals = {'I': 1, 'IV': 4, 'V': 5, 'IX': 9, 'X': 10}
    i = 0
    num = 0
    while i < len(roman):
        if i+1<len(roman) and roman[i:i+2] in roman_numerals:
            num += roman_numerals[roman[i:i+2]]
            i += 2
        else:
            num += roman_numerals[roman[i]]
            i += 1
    return num

def extract_lens_features(row):
    lens = row['LensModel'] if pd.notnull(row['LensModel']) else ""
    features = {
        'LensType': None,
        'FocalLength': None,
        'MaxAperture': None,
        'Professional': None,  # This will now directly capture the letter next to MaxAperture value
        'Version': 0,  # Default to 0
        'AutofocusType': None
    }
    
    lens_type_pattern = re.compile(r'^(EF|EF-S|EF-M|RF)', re.IGNORECASE)
    focal_length_pattern = re.compile(r'(\d+)mm', re.IGNORECASE)
    # Updated to capture the character immediately following the aperture value
    max_aperture_pattern = re.compile(r'[fF]/?(\d+\.\d+)(\w?)', re.IGNORECASE)
    version_pattern = re.compile(r'\b(II|III|IV|V|VI|VII|VIII|IX|X)\b', re.IGNORECASE)
    autofocus_pattern = re.compile(r'(USM|STM|Nano USM)', re.IGNORECASE)
    
    lens_type_match = lens_type_pattern.search(lens)
    focal_length_match = focal_length_pattern.search(lens)
    max_aperture_match = max_aperture_pattern.search(lens)
    version_match = version_pattern.search(lens)
    autofocus_match = autofocus_pattern.search(lens)
    
    features['LensType'] = lens_type_match.group(0) if lens_type_match else None
    features['FocalLength'] = int(focal_length_match.group(1)) if focal_length_match else None
    features['MaxAperture'] = float(max_aperture_match.group(1)) if max_aperture_match else None
    # Use the character immediately after the aperture value for 'Professional'
    features['Professional'] = max_aperture_match.group(2) if max_aperture_match and max_aperture_match.group(2) else 'No'
    features['Version'] = roman_to_arabic(version_match.group(0)) if version_match else 0
    features['AutofocusType'] = autofocus_match.group(0) if autofocus_match else None
    return pd.Series(features)

def load_metadata(metadata_directory):
    metadata_list = []
    for metadata_file in os.listdir(metadata_directory):
        if metadata_file.endswith('.json'):
            with open(os.path.join(metadata_directory, metadata_file), 'r') as f:
                metadata = json.load(f)
                metadata_list.append(metadata)
    return metadata_list

def convert_shutter_speed_to_numeric(value):
    try:
        # Handle the case where the value is already in numeric form
        if '/' not in value:
            return float(value)
        # Convert fraction to decimal
        numerator, denominator = value.split('/')
        return float(numerator) / float(denominator)
    except Exception as e:
        print(f"Error converting {value}: {e}")
        return None