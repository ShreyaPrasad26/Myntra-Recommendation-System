# Myntra Recommendation System

Trend generation and product recommendation system in python

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
   python myntra_scrape_final.py
   ```
### Myntra Product URL Scraper

This python script scrapes product details from Myntra product pages using URLs obtained from an Instagram dataset.
It scrapes the following details: Product ID, Name, Price, Brand, Rating Count, Average Rating

To run the script:
```
python scraping_urls.py
```

## Data Preprocessing

## Trend Generation

This streamlit application provides interactive visualizations of product trends from Myntra

### Features
- Brand Popularity: Visulaizes the top 10 most poppular brands based on rating count
- Top Brands by Rating Count: Displays a bar chart of the top 10 brands by total rating count
- Price vs Average Rating: Scatter plot showing the relationship between product price and average rating
- Brand vs Average Rating: Scatter plot comparing average ratings across top brands

### Installations
```
pip install streamlit pandas matplotlib seaborn
```
To run the streamlit app:
```
streamlit run trends-myntra.py
```
## Content Based Recommendations

This streamlit application provides product recommendations based on user interactions and cosine similarity between product features

### Features
- Tracks visited products within a user section
- Provides recommendation based on selected product ID
- Aggregates recommendations from multiple visited products
- Displays recommended products as clickable links
- Search functionality to filter products
- Custom CSS within the Streamlit app

### 1. Session State:
   - Manages user interactions and tracks visited products
     
### 2. Data Preprocessing:
   - Combines one-hot encoded categorical features with numeric features
   - Creates cosine similarity matrix
     
### 3. Recommendation Functions:
   - recommend_cosine: Recommends similar products based on a product ID
   - get_aggregated_recommendations: Aggregates recommendations from all visited products
   - display_recommentions: Shows recommended products as clickable links
     
### 4. Streamlit App:
   - User Interface for searching products, selecting a product ID, and getting recommendations
   - Displays inventory and recommendations in a scrollable table
   - To run the streamlit app:
     ```
     streamlit run content_based_recommendation.py
     ```

## Image Based Recommendations

This streamlit application provides product recommendations for Myntra items based on image similarity using a deep learning model (EfficientNetB0)

### Requirements

- Python 3.x
- Streamlit
- Pandas
- Numpy
- PIL (Python Imaging Library)
- Tensorflow/Keras
- scikit-learn

### Usage

1. Clone this repository
2. Install the required packages
3. Ensure you have the necessary data files:
   - `Updated_Insta_Urls.csv`: Contains product inforamation
   - `images/`: Directory containing product images
4. Run the streamlit app:
   ```
   streamlit run image_recommendation.py
   ```
   
### How It Works

1. The app uses an EfficientNetB0 model pre-trained on ImageNet to extract features from product images
2. Cosine similarity is computed between the feature vectors of all products
3. When a product is selected, the app finds the most similar products based on these similarity scores
4. Recommendations are sorted by price difference and similarity to provide relevant suggestions

