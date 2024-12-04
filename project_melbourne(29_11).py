# -*- coding: utf-8 -*-
"""project_Melbourne(29/11).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-lLGxucTGosjAzXgmEUvC4iLh7XDLKTv
"""

!pip install feedparser pandas

!pip install transformers

import feedparser
import pandas as pd
from datetime import datetime

rss_feeds = [
    'https://www.theage.com.au/rss/national/victoria.xml',
    'https://www.9news.com.au/rss',
    'https://www.theguardian.com/rss',
    'https://7news.com.au/feed'
]

"""Parse the RSS Fees"""

#Define a function to parse each feed and extract relevant information
def parse_rss(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        article = {
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'published': entry.get('published', ''),
            'description': entry.get('description', entry.get('summary', '')),  # Extract description if available, otherwise use summary
            'source': feed.feed.get('title', 'Unknown Source')
        }
        articles.append(article)

    return articles

#Loop through each RSS feed, parse it, and collect all articles
all_articles = []

for feed_url in rss_feeds:
    print(f"Parsing feed: {feed_url}")
    articles = parse_rss(feed_url)
    all_articles.extend(articles)

print(f"Total articles fetched: {len(all_articles)}")

#Organize the collected data into a structured format using pandas.

df = pd.DataFrame(all_articles)

# Optional: Convert published date to datetime object
df['published'] = pd.to_datetime(df['published'], errors='coerce')

# Display the first few rows
print(df.head())

# Save to CSV
df.to_csv('melbourne_news.csv', index=False)
print("Data saved to melbourne_news.csv")

"""2. Text Preprocessing"""

#Loading and Inspecting the Data

import pandas as pd

# Load the saved CSV file
df = pd.read_csv('melbourne_news.csv')

# Inspect the first few rows
print(df.head())

# Check for missing values
print(df.isnull().sum())

#fill missing values
df = df.fillna('Unknown')

# Remove duplicate rows based on the 'title' or 'link'
df = df.drop_duplicates(subset='title', keep='first')

# Selecting only relevant columns
df = df[['title', 'description', 'link']]

import re

# Function to clean the text
def clean_text(text):
    # Remove HTML tags and URLs
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove non-alphanumeric characters and lower-case the text
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower()

# Apply the cleaning function to the description
df['cleaned_description'] = df['description'].apply(clean_text)

df.to_csv('cleaned_news_data.csv', index=False)

"""Categorizing Data with LLM"""

from transformers import pipeline

# Load the zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define candidate labels for your task
candidate_labels = ['violent crime', 'accident', 'other']

# Classify an example text
example_text = "A robbery occurred in Melbourne last night involving multiple suspects."
result = classifier(example_text, candidate_labels)

# Print the results
print(result)

df = pd.read_csv('cleaned_news_data.csv')
df['category'] = df['cleaned_description'].apply(lambda x: classifier(x, candidate_labels)['labels'][0])

df.to_csv('categorized_news_data.csv', index=False)

"""Zero shot Classification using DeBERTa"""

from transformers import pipeline

# Load the DeBERTa-based classification model
classifier = pipeline("zero-shot-classification", model="microsoft/deberta-v3-large")

# Define candidate labels for your task
candidate_labels = ['violent crime', 'accident', 'other']

# Classify an example text
example_text = "A robbery occurred in Melbourne last night involving multiple suspects."
result = classifier(example_text, candidate_labels)

# Print the results
print(result)

# Apply the classifier to your DataFrame
df = pd.read_csv('cleaned_news_data.csv')
df['category'] = df['cleaned_description'].apply(lambda x: classifier(x, candidate_labels)['labels'][0])

df.to_csv('categorized_news_data_deberta.csv', index=False)

"""Zero Shot classification using T5 model

"""

from transformers import pipeline

# Load the T5-based classification model (ensure you use a fine-tuned version for classification tasks)
classifier = pipeline("zero-shot-classification", model="valhalla/t5-base-qa-qg-hl")

# Define candidate labels for your task
candidate_labels = ['violent crime', 'accident', 'other']

# Classify an example text
example_text = "A robbery occurred in Melbourne last night involving multiple suspects."
result = classifier(example_text, candidate_labels)

# Print the results
print(result)

# Apply the classifier to your DataFrame
df = pd.read_csv('cleaned_news_data.csv')
df['category'] = df['cleaned_description'].apply(lambda x: classifier(x, candidate_labels)['labels'][0])

df.to_csv('categorized_news_data_t5.csv', index=False)

"""Extractiing Crime and Accident Location"""

!pip install beautifulsoup4 requests

#Scraping news articles from URL with crime or accident news

import requests
from bs4 import BeautifulSoup

# Load the CSV file with the categorized news data
df = pd.read_csv('categorized_news_data.csv')

# Filter rows where category is 'violent crime' or 'accident'
df = df[df['category'].isin(['violent crime', 'accident'])]

# Function to scrape full article from URL
def scrape_full_article(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the main article content (depends on the website structure)
        article_text = " ".join([p.get_text() for p in soup.find_all('p')])
        return article_text
    except Exception as e:
        return None

# Scrape only articles labeled 'crime' or 'accident'
for index, row in df.iterrows():
    if row['category'] in ['violent crime', 'accident']:
        full_article_text = scrape_full_article(row['link'])
        df.at[index, 'full_text'] = full_article_text

#Using NER to extract location of crime and accidents

from transformers import pipeline

# Load pre-trained NER model from Hugging Face
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

# Function to extract locations using Hugging Face NER
def extract_location_with_bert(text):
    entities = ner_pipeline(text)
    locations = [entity['word'] for entity in entities if entity['entity_group'] == "LOC"]  # LOC represents locations
    return locations

# Create 'locations' column if it doesn't exist
if 'locations' not in df.columns:
    df['locations'] = None

# Apply the NER model to the full text (remove if condition, this condition has already been preapplied)
for index, row in df.iterrows():
    if row['category'] in ['crime', 'accident'] and pd.notna(row['full_text']):
        locations = extract_location_with_bert(row['full_text'])
        df.at[index, 'locations'] = locations

df.to_csv('location_news_data.csv', index=False)

#RUNNING NER AGAIN USING SPACY THIS TIME
import pandas as pd

# Load the CSV file with the loacions news data
df = pd.read_csv('location_news_data.csv')

# Filter rows where category is 'violent crime' or 'accident'
filtered_df = df[df['category'].isin(['violent crime', 'accident'])]

# Save the result to a new CSV file (optional)
filtered_df.to_csv("filtered_data.csv", index=False)

filtered_df.head()

import spacy
import pandas as pd

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load the CSV file with the loacions news data
df = pd.read_csv('location_news_data.csv')

# Function to extract locations
def extract_locations(text):
    if pd.isna(text):  # Handle missing values
        return ""
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]
    return ", ".join(locations)

# Apply the function to the "full_text" column
df["locations"] = df["full_text"].apply(extract_locations)

# Save the updated DataFrame
df.to_csv("updated_dataset.csv", index=False)

"""Open assistant continuously crashing"""

#define locations using OpenAssistant/oasst-sft-1-pythia-12b

from transformers import pipeline

# Load OpenAssistant model for text generation (dialogue/refinement)
oasst_model = pipeline("text-generation", model="OpenAssistant/oasst-sft-1-pythia-12b")

# Define a function to refine extracted locations
def refine_locations(ner_locations, full_text):
    if not ner_locations:
        return None

    # Prepare the input prompt for OpenAssistant
    prompt = f"In the following article, the locations {ner_locations} were mentioned. Which location is most likely the site of the crime or accident? Here is the article text:\n\n{full_text}"

    # Get refined location from the OpenAssistant model
    response = oasst_model(prompt, max_length=200, do_sample=False)[0]['generated_text']

    # Extract the location mentioned in the response (we assume it returns one or two relevant locations)
    refined_location = response.strip()
    return refined_location

# Apply the refinement to the DataFrame
df['refined_location'] = df.apply(lambda row: refine_locations(row['locations'], row['full_text']), axis=1)

"""Locating on Map"""

!pip install geopandas folium geopy

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium

# Load the dataset
df = pd.read_csv("updated_dataset.csv")

# Initialize geolocator
geolocator = Nominatim(user_agent="location_mapper")

# Define the bounding box for Melbourne and outer suburbs (lat_min, lat_max, lon_min, lon_max)
melbourne_bounds = {
    "lat_min": -38.4339,  # Southernmost point (e.g., Mornington Peninsula)
    "lat_max": -37.4000,  # Northernmost point (e.g., Craigieburn)
    "lon_min": 144.3331,  # Westernmost point (e.g., Werribee)
    "lon_max": 145.8788   # Easternmost point (e.g., Lilydale)
}

# Define a function to check if a point lies within the bounding box
def is_within_bounds(lat, lon, bounds):
    return (bounds["lat_min"] <= lat <= bounds["lat_max"]) and (bounds["lon_min"] <= lon <= bounds["lon_max"])

# Extend the get_coordinates function
def get_coordinates(location):
    try:
        if pd.isna(location):  # Handle missing values
            return None, None
        # Geocode the location, appending "Victoria, Australia" for broader search
        location = geolocator.geocode(location + ", Victoria, Australia")
        if location:
            lat, lon = location.latitude, location.longitude
            # Check if the coordinates are within Melbourne bounds
            if is_within_bounds(lat, lon, melbourne_bounds):
                return lat, lon
        return None, None
    except GeocoderTimedOut:
        return None, None

# Apply the function to the 'locations' column
df[['latitude', 'longitude']] = df['locations'].apply(lambda loc: pd.Series(get_coordinates(loc)))

# Filter rows with valid coordinates
df = df.dropna(subset=['latitude', 'longitude'])

# Create a map centered on Melbourne
melbourne_map = folium.Map(location=[-37.8136, 144.9631], zoom_start=10)

# Add points to the map
for _, row in df.iterrows():
    folium.Marker(location=[row['latitude'], row['longitude']],
                  popup=row['locations']).add_to(melbourne_map)

# Save the map as an HTML file
melbourne_map.save("melbourne_outer_suburbs_map.html")

# Display the map (optional, requires a Jupyter environment)
melbourne_map

df.head()

"""Trying classification with clustering techniques"""

!pip install sentence_transformers

import pandas as pd
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Load the CSV file with the cleaned and normalized text
df = pd.read_csv('cleaned_news_data.csv')

# Initialize sentence-transformer for embedding text data
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Convert news descriptions into embeddings
embeddings = model.encode(df['normalized_description'].tolist())

# Perform K-Means clustering
num_clusters = 5  # You can change the number of clusters based on your preference
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
df['cluster'] = kmeans.fit_predict(embeddings)

# Save the results to a new CSV file
df.to_csv('clustered_news.csv', index=False)
print("News articles clustered and saved to 'clustered_news.csv'")

# Optional: Visualize the clusters using PCA (for dimensionality reduction)
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embeddings)

plt.figure(figsize=(10, 7))
plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=df['cluster'], cmap='viridis')
plt.title('Clusters of News Articles')
plt.show()

"""Elbow Method for Finding Optimal Clusters:"""

from sklearn.metrics import silhouette_score

def find_optimal_clusters(embeddings, max_k):
    iters = range(2, max_k+1)
    sse = []
    silhouette_scores = []

    for k in iters:
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(embeddings)
        sse.append(kmeans.inertia_)  # Sum of squared distances
        silhouette_scores.append(silhouette_score(embeddings, kmeans.labels_))

    plt.figure(figsize=(10, 7))
    plt.plot(iters, sse, marker='o')
    plt.title('Elbow Method for Optimal Clusters')
    plt.xlabel('Number of clusters')
    plt.ylabel('SSE')
    plt.show()

    plt.figure(figsize=(10, 7))
    plt.plot(iters, silhouette_scores, marker='o')
    plt.title('Silhouette Score for Optimal Clusters')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette Score')
    plt.show()

# Run the Elbow Method to find the optimal number of clusters
find_optimal_clusters(embeddings, 10)

"""One Shot Classification Using BERT"""

!pip install openai

import openai
import pandas as pd

# Load your CSV file with news descriptions
df = pd.read_csv('cleaned_news_data.csv')

# Define your categories for classification
categories = ['Crime', 'Government', 'Business', 'violence', 'Science', 'Culture']

# Initialize OpenAI API
openai.api_key = ""

# Function to generate GPT-3 prompt for zero-shot classification
def classify_article_with_gpt3(article, categories):
    prompt = f"Classify the following news article into one of these categories: {', '.join(categories)}.\n\nArticle: {article}\n\nCategory:"

    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        prompt=prompt,
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0  # Lower temperature for deterministic output
    )

    category = response.choices[0].text.strip()
    return category

# Apply classification on each article
df['gpt3_category'] = df['normalized_description'].apply(lambda x: classify_article_with_gpt3(x, categories))

# Save the results to CSV
df.to_csv('gpt3_classified_news.csv', index=False)
print("GPT-3 classification complete. Results saved to 'gpt3_classified_news.csv'")