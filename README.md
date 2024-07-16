# Myntra Recommendation System

## Data Scraping

### Myntra Web Scraper

This python script scrapes product data from the Myntra website. It extracts various details about product based on a user-provided search term.
The product details extracted are: Brand, Price, Original Price, Description, Ratings, Product URL, Product Code, Category and Subcategory

#### Requirements 

- Python 3.x
- pandas
- Selenium
- BeautifulSoup4
- ChromeDriver

#### Usage

1. Clone this repository
2. Install the required packages:
   ```
   pip install pandas beautifulsoup4 selenium
   ```
4. Download and install ChromeDriver
5. Run the script
   ```
   python myntra_scraper.py
   ```

## Data Preprocessing

## Trend Generation

## Content Based Recommendations

## Image Based Recommendations

This streamlit application provides product recommendations for Myntra items based on image similarity using a deep learning model (EfficientNetB0)

## Requirements

- Python 3.x
- Streamlit
- Pandas
- Numpy
- PIL (Python Imaging Library)
- Tensorflow/Keras
- scikit-learn

## Usage

1. Clone this repository
2. Install the required packages
3. Ensure you have the necessary data files:
   - `Updated_Insta_Urls.csv`: Contains product inforamation
   - `images/`: Directory containing product images
4. Run the streamlit app:
   ```
   streamlit run image_recommendation.py

## How It Works

1. The app uses an EfficientNetB0 model pre-trained on ImageNet to extract features from product images
2. Cosine similarity is computed between the feature vectors of all products
3. When a product is selected, the app finds the most similar products based on these similarity scores
4. Recommendations are sorted by price difference and similarity to provide relevant suggestions

