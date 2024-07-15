import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset (replace with your actual dataset path)
data = pd.read_csv('/Users/shreyaprasad/Downloads/Updated_Insta_Urls.csv')

# Title of the Streamlit app
st.title('Myntra Product Trends')

# Plotting Brand Popularity
st.subheader('Brand Popularity (Top 10 Brands)')
top_brands = data.groupby('brand')['ratingCount'].sum().nlargest(10).index
top_brands_data = data[data['brand'].isin(top_brands)]

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x='brand', y='ratingCount', data=top_brands_data, palette='viridis', ax=ax1)
ax1.set_xlabel('Brand')
ax1.set_ylabel('Number of Products')
ax1.set_title('Brand Popularity')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
st.pyplot(fig1)  # Display the plot using st.pyplot()

# Plotting Top 10 Brands by Rating Count
st.subheader('Top 10 Brands by Rating Count')
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='brand', y='ratingCount', data=top_brands_data, palette='plasma', ax=ax2)
ax2.set_xlabel('Brand')
ax2.set_ylabel('Rating Count')
ax2.set_title('Top 10 Brands by Rating Count')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)  # Display the plot using st.pyplot()

# Scatter plot of Price vs Average Rating
st.subheader('Price vs Average Rating Scatter Plot')
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.scatter(data['price'], data['avg_rating'], color='orange', alpha=0.5)
ax3.set_xlabel('Price')
ax3.set_ylabel('Average Rating')
ax3.set_title('Price vs. Average Rating')
ax3.grid(True)
st.pyplot(fig3)  # Display the plot using st.pyplot()

# Plotting Brand vs Average Rating
st.subheader('Brand vs Average Rating')
avg_ratings_by_brand = top_brands_data.groupby('brand')['avg_rating'].mean()

fig4, ax4 = plt.subplots(figsize=(10, 6))
ax4.scatter(avg_ratings_by_brand.index, avg_ratings_by_brand.values, color='orange', alpha=0.5)
ax4.set_xlabel('Brand')
ax4.set_ylabel('Average Rating')
ax4.set_title('Brand vs. Average Rating')
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45)
ax4.grid(True)
st.pyplot(fig4)  # Display the plot using st.pyplot()

