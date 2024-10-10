# News-Classification-using-Zero-Shot-Models
This project demonstrates the use of zero-shot classification models to categorize news articles into predefined categories.
News Classification using Zero-Shot Models
This project demonstrates the use of zero-shot classification models to categorize news articles into predefined categories. The models used in this project are:

BART (facebook/bart-large-mnli)
T5 (valhalla/t5-base-qa-qg-hl)
DeBERTa (microsoft/deberta-v3-large)
The project classifies news articles into three main categories:

violent crime
accident
other
Dataset
The dataset consists of news articles with columns such as:

title: Title of the news article
description: Short description of the news article
full_text: Full article text (if available)
category: Predefined category labels applied by the models
The cleaned descriptions are stored in a CSV file named cleaned_news_data.csv.

Requirements
To run this project, you need the following libraries:

bash
Copy code
pip install pandas transformers
How to Use
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/news-classification.git
cd news-classification
Ensure that your cleaned_news_data.csv is in the same directory.

Choose a classification model: You can select between BART, T5, or DeBERTa models.

Using BART for Classification
python
Copy code
from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
candidate_labels = ['violent crime', 'accident', 'other']
df['category'] = df['cleaned_description'].apply(lambda x: classifier(x, candidate_labels)['labels'][0])
Using T5 for Classification
python
Copy code
from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="valhalla/t5-base-qa-qg-hl")
candidate_labels = ['violent crime', 'accident', 'other']
df['category'] = df['cleaned_description'].apply(lambda x: classifier(x, candidate_labels)['labels'][0])
Using DeBERTa for Classification
python
Copy code
from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="microsoft/deberta-v3-large")
candidate_labels = ['violent crime', 'accident', 'other']
df['category'] = df['cleaned_description'].apply(lambda x: classifier(x, candidate_labels)['labels'][0])
Save the results: After running the classification, the categorized data will be saved into a CSV file.

python
Copy code
df.to_csv('categorized_news_data.csv', index=False)
Model Comparison
In this project, you can compare the performance of BART, T5, and DeBERTa in classifying news articles. This can help determine the most suitable model for your specific task.

Contributing
Feel free to submit pull requests to improve the classification accuracy, add more models, or refine the dataset.
