import os
import requests
import pandas as pd

# Function to download an image from a URL and save it to a path
def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Load your DataFrame
df = pd.read_csv('updated_insta_urls_with_images.csv')  # Example to load DataFrame from a CSV file

# Create a folder to store the images
save_folder = 'images'
os.makedirs(save_folder, exist_ok=True)

# Iterate over DataFrame rows
for index, row in df.iterrows():
    image_url = row['image_url']
    product_id = row['product_id']  # Assuming 'product_id' is used for filenames
    image_path = os.path.join(save_folder, f"{product_id}.jpg")  # Change extension if needed
    download_image(image_url, image_path)
