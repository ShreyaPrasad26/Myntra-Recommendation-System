
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Define a custom SessionState class
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if 'visited_products' not in self.__dict__:
            self.visited_products = []

    def add_visited_product(self, product_id):
        if product_id not in self.visited_products:
            self.visited_products.append(product_id)

    def get_visited_products(self):
        return self.visited_products

# Initialize SessionState (do this at the beginning of your script)
if 'session_state' not in st.session_state:
    st.session_state.session_state = SessionState()

# Add CSS for scrollable table
st.markdown("""
<style>
    .scrollable-table {
        height: 300px;
        overflow-y: auto;
    }
    .scrollable-table table {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Load data
data = pd.read_csv('Updated_Insta_Urls.csv')

# One-hot encoding for categorical features
encoder = OneHotEncoder(sparse_output=False)
encoder_value = encoder.fit_transform(data[['brand', 'color', 'name']])

# Numeric features
encoder_numeric = data[['price', 'avg_rating', 'ratingCount']].values

# Combined feature set
features_net = np.hstack((encoder_numeric, encoder_value))

# Cosine similarity matrix
similarity_matrix = cosine_similarity(features_net)

# Recommendation function
def recommend_cosine(data, item_ids, visited_products):
    if 'product_id' not in data.columns:
        raise KeyError("The DataFrame does not contain a 'product_id' column.")
    
    similar_indices = []
    for item_id in item_ids:
        if item_id in data['product_id'].values:
            item_index = data[data['product_id'] == item_id].index[0]
            similarity_scores = similarity_matrix[item_index]
            similar_indices.extend(similarity_scores.argsort()[::-1][1:6])  # Top 5 similar items
    
    # Filter out visited products and keep top recommendations
    similar_items = data.iloc[list(set(similar_indices))]
    similar_items = similar_items[~similar_items['product_id'].isin(visited_products)]
    
    return similar_items.head(3)  # Return top 3 non-visited items

# Function to get aggregated recommendations based on multiple visited items
def get_aggregated_recommendations(data, visited_products):
    if not visited_products:
        return None
    
    similar_indices = []
    for product_id in visited_products:
        if product_id in data['product_id'].values:
            item_index = data[data['product_id'] == product_id].index[0]
            similarity_scores = similarity_matrix[item_index]
            similar_indices.extend(similarity_scores.argsort()[::-1][1:6])  # Top 5 similar items
    
    # Filter out visited products and calculate aggregated similarity scores
    aggregated_scores = {}
    for idx in list(set(similar_indices)):
        product_id = data.loc[idx, 'product_id']
        if product_id not in visited_products:
            if product_id in aggregated_scores:
                aggregated_scores[product_id] += similarity_matrix[item_index, idx]
            else:
                aggregated_scores[product_id] = similarity_matrix[item_index, idx]
    
    # Sort by aggregated scores and get top 5 recommendations
    if aggregated_scores:
        sorted_scores = sorted(aggregated_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        recommended_items = data[data['product_id'].isin([item[0] for item in sorted_scores])]
        return recommended_items
    else:
        return None

# Function to display recommendations as clickable links
def display_recommendations(recommendations):
    clickable_links = []
    for _, row in recommendations.iterrows():
        clickable_links.append({
            'brand': row['brand'],
            'name': row['name'],
            'price': row['price'],
            'link': f'<a href="{row["link"]}" target="_blank">View Product</a>'
        })
    
    clickable_df = pd.DataFrame(clickable_links)
    
    html_table = clickable_df.to_html(escape=False, index=False)
    scrollable_table = f'<div class="scrollable-table">{html_table}</div>'
    
    st.markdown(scrollable_table, unsafe_allow_html=True)

# Streamlit app
st.title('Myntra Recommendation System')

# Format the 'link' column to make it clickable
data['link'] = data['link'].apply(lambda x: f'<a href="{x}" target="_blank">View Product</a>')

# Select columns for display
sample_data = data[['product_id', 'name', 'brand', 'price', 'link']]

# Search functionality
search_term = st.text_input("Search products:")
if search_term:
    sample_data = sample_data[sample_data.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

# Display the data
st.write('Inventory:')

# Convert DataFrame to HTML and wrap it in a scrollable div
html_table = sample_data.to_html(escape=False, index=False)
scrollable_table = f'<div class="scrollable-table">{html_table}</div>'
st.markdown(scrollable_table, unsafe_allow_html=True)

# Get user input for product_id
st.write('')
st.write('Click on a row to get recommendations')
selected_product_id = st.selectbox('Select product_id:', data['product_id'])

# Recommend products based on selected item and visited products
if st.button('Recommend Products'):
    # Get recommendations based on the selected item
    single_recommendations = recommend_cosine(data, [selected_product_id], st.session_state.session_state.get_visited_products())
    
    # Get aggregated recommendations based on visited products
    aggregated_recommendations = get_aggregated_recommendations(data, st.session_state.session_state.get_visited_products())
    
    # Merge and display recommendations
    all_recommendations = pd.concat([single_recommendations, aggregated_recommendations]).drop_duplicates(subset=['product_id'], keep='first').head(5)

    if all_recommendations is not None and not all_recommendations.empty:
        st.write('Top Recommendations based on Selected Item and Aggregated Recommendations:')
        display_recommendations(all_recommendations)

    # Update visited products in session state
    st.session_state.session_state.add_visited_product(selected_product_id)
    
    # Print visited products to the terminal
    print("Visited Products:", st.session_state.session_state.visited_products)

    # Display visited products in the Streamlit app
    st.write("Visited Products:")
    st.write(st.session_state.session_state.visited_products)
