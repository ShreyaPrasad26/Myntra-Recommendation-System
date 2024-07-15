import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Instantiate a webdriver
driver = webdriver.Chrome()

# Sample Instagram DataFrame with product URLs
instagram_data = pd.read_csv('instagram.csv')\

# Function to scrape product details from a Myntra product page
def scrape_product_details(url):
    driver.get(url)
    time.sleep(5)  # Let the page load (adjust as necessary)
    
    try:
        product_id = url.split('/')[-1]
        name = driver.find_element(By.CLASS_NAME, 'pdp-name').text.strip()
        price = driver.find_element(By.CLASS_NAME, 'pdp-price').text.strip()
        brand = driver.find_element(By.CLASS_NAME, 'pdp-title').text.strip()
        rating_count = driver.find_element(By.CLASS_NAME, 'index-ratingsCount').text.strip()
        average_rating = driver.find_element(By.CLASS_NAME, 'index-overallRating').text.strip()
        
        return {
            'product_id': product_id,
            'name': name,
            'price': price,
            'brand': brand,
            'ratingCount': rating_count,
            'avg_rating': average_rating
        }
    except Exception as e:
        print(f"Error parsing URL: {url}, error: {e}")
        return None

# List to store the scraped data
scraped_data = []

# Iterate over the URLs and scrape data
for url in instagram_data['product_url']:
    product_details = scrape_product_details(url)
    if product_details:
        scraped_data.append(product_details)

# Convert the scraped data to a DataFrame
scraped_df = pd.DataFrame(scraped_data)

# Display the scraped DataFrame
print(scraped_df.head())

scraped_df.to_csv('scraped_insta_urls.csv')

# Quit the driver
driver.quit()
