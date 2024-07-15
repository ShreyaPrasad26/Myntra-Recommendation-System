import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
import base64
from io import BytesIO
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv('Updated_Insta_Urls.csv')

df = load_data()

# Load the model
@st.cache_resource
def load_model():
    base_model = EfficientNetB0(weights='imagenet', include_top=False)
    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(256, activation='relu')(x)
    return Model(inputs=base_model.input, outputs=x)

model = load_model()

# Feature extraction function
def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = model.predict(img_data)
    return features.flatten()

# Load or compute features
@st.cache_data
def get_features():
    if 'features' not in df.columns:
        df['features'] = df['product_id'].apply(lambda x: extract_features(f"images/{x}.jpg", model))
    return np.stack(df['features'].values)

features = get_features()

# Compute cosine similarities
@st.cache_data
def compute_similarities():
    return cosine_similarity(features)

cosine_similarities = compute_similarities()

# Get recommendations function
def get_recommendations(product_id, num_recommendations=5):
    product_id = int(product_id)  # Convert product_id to integer
    product_rows = df[df['product_id'] == product_id]
    if product_rows.empty:
        st.error(f"Product ID {product_id} not found in the DataFrame.")
        return pd.DataFrame()
    
    idx = product_rows.index[0]
    similarity_scores = list(enumerate(cosine_similarities[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:num_recommendations+1]
    recommended_indices = [i[0] for i in similarity_scores]
    
    recommendations = df.iloc[recommended_indices].copy()
    recommendations['price_diff'] = abs(df.loc[idx, 'price'] - recommendations['price'])
    recommendations['similarity'] = [score for _, score in similarity_scores]
    
    recommendations = recommendations.sort_values(['price_diff', 'similarity'], ascending=[True, False])
    
    return recommendations.head(num_recommendations)

# Streamlit app
st.title("Myntra Product Recommender")

# Display all images in a scrollable boundary
st.header("All Products")
image_files = os.listdir("images/")

# Function to convert image to base64
def img_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Create HTML for scrollable image grid
image_html = "<div style='display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;'>"
for image_file in image_files:
    product_id = os.path.splitext(image_file)[0]
    img = Image.open(f"images/{image_file}")
    img.thumbnail((200, 200))  # Resize image for performance
    b64_img = img_to_base64(img)
    image_html += f"<div><img src='data:image/png;base64,{b64_img}' style='width:100%;'><p>{product_id}</p></div>"
image_html += "</div>"

# Create scrollable container
st.markdown(
    f"""
    <style>
        .scrollable-container {{
            height: 400px;
            overflow-y: scroll;
            padding: 10px;
        }}
    </style>
    <div class="scrollable-container">
        {image_html}
    </div>
    """,
    unsafe_allow_html=True
)

# Add a selectbox to choose a product ID
product_ids = [os.path.splitext(file)[0] for file in image_files]
selected_product = st.selectbox("Select a Product ID", product_ids)

# Get recommendations when a product is selected
if st.button("Get Recommendations"):
    st.header(f"Recommendations for Product {selected_product}")
    recommendations = get_recommendations(selected_product)
    
    if not recommendations.empty:
        # Display recommendation details
        st.subheader("Recommendation Details:")
        
        # Function to make links clickable
        def make_clickable(link):
            return f'<a href="{link}" target="_blank">{link}</a>'
        
        # Apply the function to the 'link' column
        recommendations['link'] = recommendations['link'].apply(make_clickable)
        
        # Display the dataframe with clickable links
        st.write(recommendations[['product_id', 'name', 'price', 'brand', 'link', 'price_diff']].to_html(escape=False, index=False), unsafe_allow_html=True)
        
        # Display recommended images
        st.subheader("Recommended Products:")
        rec_cols = st.columns(5)
        for i, (_, row) in enumerate(recommendations.iterrows()):
            with rec_cols[i]:
                rec_img = Image.open(f"images/{row['product_id']}.jpg")
                st.image(rec_img, caption=f"Product ID: {row['product_id']}", use_column_width=True)
    else:
        st.warning("No recommendations available.")