import pandas as pd
import requests
import os

# Read Excel file
df = pd.read_excel('databank.xlsx')

# Create a directory to save images
os.makedirs('images', exist_ok=True)

# Counter for limiting downloaded images
downloaded_images = 0

# Loop through image links
for index, row in df.iterrows():
    # Limit the number of downloaded images to 2000
    if downloaded_images >= 2000:
        break

    image_url = row['image link']
    gender = row['Gender']
    age = row['Age']

    # Map gender to integer
    gender_map = {'female': 0, 'male': 1}
    gender_int = gender_map.get(gender.lower(), -1)

    # Skip if gender is not specified or age is missing
    if gender_int == -1 or pd.isnull(age):
        continue

    # Limit age to 99
    age = min(int(age), 99)

    # Rename image with age, gender, and index
    filename = f"{age}_{gender_int}_{index}.jpg"
    filepath = os.path.join('images', filename)

    # Download image
    response = requests.get(image_url)
    with open(filepath, 'wb') as f:
        f.write(response.content)

    # Increment downloaded images counter
    downloaded_images += 1
