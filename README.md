# News Classification using Zero-Shot Models

## Overview

This project demonstrates the use of zero-shot classification models to categorize news articles into predefined categories. 

### Supported Models
- **BART** (`facebook/bart-large-mnli`)
- **T5** (`valhalla/t5-base-qa-qg-hl`)
- **DeBERTa** (`microsoft/deberta-v3-large`)

### Classification Categories
- `violent crime`
- `accident`
- `other`

## Dataset

The dataset consists of news articles with the following columns:
- `title`: Title of the news article
- `description`: Short description of the news article
- `full_text`: Full article text (if available)
- `category`: Predefined category labels applied by the models

The cleaned descriptions are stored in `cleaned_news_data.csv`.

## Prerequisites

### System Requirements
- Python 3.7+
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/news-classification.git
cd news-classification

# Install required libraries
pip install pandas transformers torch
```

## Usage

### 1. Prepare Your Data
Ensure `cleaned_news_data.csv` is in the project directory.

### 2. Classification Models

#### Using BART
```python
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
candidate_labels = ['violent crime', 'accident', 'other']
df['category'] = df['cleaned_description'].apply(
    lambda x: classifier(x, candidate_labels)['labels'][0]
)
```

#### Using T5
```python
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="valhalla/t5-base-qa-qg-hl")
candidate_labels = ['violent crime', 'accident', 'other']
df['category'] = df['cleaned_description'].apply(
    lambda x: classifier(x, candidate_labels)['labels'][0]
)
```

#### Using DeBERTa
```python
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="microsoft/deberta-v3-large")
candidate_labels = ['violent crime', 'accident', 'other']
df['category'] = df['cleaned_description'].apply(
    lambda x: classifier(x, candidate_labels)['labels'][0]
)
```

### 3. Save Results
```python
df.to_csv('categorized_news_data.csv', index=False)
```

## Model Comparison

The project allows comparison of **BART**, **T5**, and **DeBERTa** performance in news article classification. This helps determine the most suitable model for specific tasks.

### Performance Metrics
| Model | Pros | Cons |
|-------|------|------|
| BART | High contextual understanding | Computationally expensive |
| T5 | Versatile, good for QA | Slightly lower accuracy |
| DeBERTa | State-of-the-art performance | Large model size |

## Advanced Usage

### Custom Categories
Modify the `candidate_labels` list to include your own categories.

### Performance Optimization
- Adjust batch size
- Use GPU acceleration
- Implement caching mechanisms

## Limitations
- Zero-shot models may have lower accuracy compared to fine-tuned models
- Performance varies with input complexity
- Computational resources required

## Future Improvements
- Add more classification categories
- Implement model ensemble techniques
- Create visualization of classification results

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


Project Link: [https://github.com/yourusername/news-classification](https://github.com/yourusername/news-classification)
