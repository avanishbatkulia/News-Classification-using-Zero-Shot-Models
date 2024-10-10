# News Classification using Zero-Shot Models

This project demonstrates the use of zero-shot classification models to categorize news articles into predefined categories. The models used in this project are:
- **BART** (`facebook/bart-large-mnli`)
- **T5** (`valhalla/t5-base-qa-qg-hl`)
- **DeBERTa** (`microsoft/deberta-v3-large`)

The project classifies news articles into three main categories:
- `violent crime`
- `accident`
- `other`

## Dataset

The dataset consists of news articles with columns such as:
- `title`: Title of the news article
- `description`: Short description of the news article
- `full_text`: Full article text (if available)
- `category`: Predefined category labels applied by the models

The cleaned descriptions are stored in a CSV file named `cleaned_news_data.csv`.

## Requirements

To run this project, you need the following libraries:

```bash
pip install pandas transformers
