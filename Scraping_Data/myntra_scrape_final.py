import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time

def search_url(search_term, page_number):
    template = 'https://www.myntra.com/{}?rawQuery={}&p={}'
    return template.format(search_term, search_term, page_number)


driver = webdriver.Chrome()

org_url = input('Enter your search term: ')

# Initialize lists
brands = []
price = []
original_price = []
description = []
ratings = []
product_url = []
product_code = []
category = []
subcategory = []

def extract_product_details(soup):
    global brands, price, original_price, description, ratings, product_url, product_code, category, subcategory
    
    # Extract JSON-LD data
    try:
        json_ld_script = soup.find('script', type='application/ld+json')
        if json_ld_script:
            json_ld_data = json.loads(json_ld_script.string)
            if isinstance(json_ld_data, dict) and json_ld_data.get('@type') == 'Product':
                brand_name = json_ld_data.get('brand', {}).get('name', 'N/A')
                sku = json_ld_data.get('sku', 'N/A')
                price_value = json_ld_data.get('offers', {}).get('price', 'N/A')
                description_value = json_ld_data.get('description', 'N/A')
                product_url_value = json_ld_data.get('offers', {}).get('url', 'N/A')

                brands.append(brand_name)
                product_code.append(sku)
                price.append(int(price_value) if price_value.isdigit() else None)
                original_price.append(None)  # JSON-LD does not include original price
                description.append(description_value)
                product_url.append(product_url_value)
                
            else:
                brands.append('N/A')
                product_code.append('N/A')
                price.append(None)
                original_price.append(None)
                description.append('N/A')
                product_url.append('N/A')
    except Exception as e:
        print(f"Error extracting JSON-LD data: {e}")
        brands.append('N/A')
        product_code.append('N/A')
        price.append(None)
        original_price.append(None)
        description.append('N/A')
        product_url.append('N/A')
    
    try:
        brand = soup.find_all('h3', class_="product-brand")
        for a in brand:
            brands.append(a.text)
    except AttributeError:
        pass
    
    # Fallback methods
    try:
        price_elements = soup.find_all('span', class_="product-discountedPrice")
        for element in price_elements:
            price.append(int(element.text.strip('Rs. ').replace(',', '')))
    except Exception as e:
        price.append(None)
        print(f"Error extracting price: {e}")

    try:
        original_price_elements = soup.find_all('span', class_='product-strike')
        for element in original_price_elements:
            original_price.append(int(element.text.strip('Rs. ').replace(',', '')))
    except Exception as e:
        original_price.append(None)
        print(f"Error extracting original price: {e}")

    try:
        description_elements = soup.find_all('h4', class_='product-product')
        description.extend([element.text.strip() for element in description_elements])
    except Exception as e:
        description.append('N/A')
        print(f"Error extracting description: {e}")

    try:
        rating_elements = soup.find_all('div', class_='product-ratingsContainer')
        for element in rating_elements:
            ratings.append(element.text.strip())
    except Exception as e:
        ratings.append('N/A')
        print(f"Error extracting ratings: {e}")

    try:
        product_elements = soup.find_all('li', class_="product-base")
        for element in product_elements:
            link = element.find('a', {'data-refreshpage': 'true', 'target': '_blank'})
            if link:
                href = 'https://www.myntra.com/' + link['href']
                product_url.append(href)

                # Extract product code from the URL
                product_code_value = href.split('/')[-2]
                product_code.append(product_code_value)

                # Extract subcategory from the URL
                url_parts = href.split('/')
                subcategory_value = url_parts[3] if len(url_parts) > 3 else 'N/A'
                subcategory.append(subcategory_value)
    except Exception as e:
        product_url.append('N/A')
        product_code.append('N/A')
        subcategory.append('N/A')
        print(f"Error extracting product URL or subcategory: {e}")

    try:
        # Try to extract brands from the product details if not found in JSON-LD
        brand_elements = soup.find_all('a', class_='brand-name')  # Update this selector if needed
        for element in brand_elements:
            brands.append(element.text.strip())
    except Exception as e:
        print(f"Error extracting brands: {e}")
        brands.append('N/A')

    try:
        category_elements = soup.find_all('a', class_='horizontal-filters-sub')
        for element in category_elements:
            category.append(element.text.strip())
        subcategory_elements = soup.find_all('a', class_='horizontal-filters-crumb')
        for element in subcategory_elements:
            subcategory.append(element.text.strip())
    except Exception as e:
        category.append('N/A')
        subcategory.append('N/A')
        print(f"Error extracting category and subcategory: {e}")

# Scrape data from the first 10 pages
for i in range(1, 11):
    driver.get(search_url(org_url, i))
    time.sleep(3)  # Giving some time for the page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    extract_product_details(soup)

# Ensure all lists have the same length
max_length = max(len(brands), len(price), len(original_price), len(description), len(ratings), len(product_url), len(product_code), len(category), len(subcategory))

# Extend lists with appropriate default values if they are shorter
brands.extend(['N/A'] * (max_length - len(brands)))
price.extend([None] * (max_length - len(price)))
original_price.extend([None] * (max_length - len(original_price)))
description.extend(['N/A'] * (max_length - len(description)))
ratings.extend(['N/A'] * (max_length - len(ratings)))
product_url.extend(['N/A'] * (max_length - len(product_url)))
product_code.extend(['N/A'] * (max_length - len(product_code)))
category.extend(['N/A'] * (max_length - len(category)))
subcategory.extend(['N/A'] * (max_length - len(subcategory)))

driver.quit()

# Save the scraped data to a DataFrame
data = {
    'Brand': brands,
    'Price': price,
    'Original Price': original_price,
    'Description': description,
    'Ratings': ratings,
    'Product URL': product_url,
    'Product Code': product_code,
    'Category': category,
    'Subcategory': subcategory
}

df = pd.DataFrame(data)
df.to_csv('myntra_topwear.csv', index=False)

print("Data scraping complete. Saved to 'myntra_topwear.csv'.")
