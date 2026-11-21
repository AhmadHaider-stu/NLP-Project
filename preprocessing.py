import re
import string

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("wordnet", quiet=True)

# Which file each GUI option opens
DATASETS = {
    "IMDB_reviews": "data/IMDB_reviews_cleaned.csv",
    "hotel_reviews": "data/hotel_reviews_cleaned.csv",
    "food_reviews": "data/food_reviews_cleaned.csv",
}

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Keeps the TF-IDF of each dataset so it is built only once
cache = {}


# 1) Data loading
def load_data(dataset):
    path = DATASETS.get(dataset)
    df = pd.read_csv(path)
    text_column = df.columns[0]  # the text is the first column in all three files
    df = df.dropna(subset=[text_column]).reset_index(drop=True)
    return df, text_column


# 2) Preprocessing
def preprocess_text(text):
    text = text.lower().strip()
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    words = [word for word in text.split() if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in word_tokenize(" ".join(words))]
    return " ".join(words)


def preprocess_data(df, text_column):
    df["cleaned_review"] = df[text_column].apply(preprocess_text)
    return df


# 3) TF-IDF matrix
def build_tfidf(df):
    vectorizer = TfidfVectorizer(min_df=2)
    tfidf_matrix = vectorizer.fit_transform(df["cleaned_review"])
    return vectorizer, tfidf_matrix


def load_preprocessed(dataset):
    path = DATASETS.get(dataset)
    df = pd.read_csv(path)
    df = df.drop_duplicates()
    text_column = df.columns[0]
    df["cleaned_review"] = df["cleaned_review"].fillna("")
    return df, text_column


def get_dataset(dataset):
    if dataset not in cache:
        df, text_column = load_preprocessed(dataset)
        vectorizer, tfidf_matrix = build_tfidf(df)
        cache[dataset] = (df, text_column, vectorizer, tfidf_matrix)
    return cache[dataset]


# 4) Search
def search(query, k=5, dataset="IMDB_reviews"):
    df, text_column, vectorizer, tfidf_matrix = get_dataset(dataset)
    query_vector = vectorizer.transform([preprocess_text(query)])
    similarities = cosine_similarity(tfidf_matrix, query_vector).flatten()
    top_indices = similarities.argsort()[::-1][:k]
    return [(df.loc[idx, text_column], similarities[idx]) for idx in top_indices]


# Called by the GUI
def func(K, dataset, query):
    results = search(query, K, dataset)
    output = ""
    for rank, (review, score) in enumerate(results, start=1):
        output += f"Rank {rank} | Similarity Score: {score:.4f}\n"
        output += f"Review: {review}\n"
        output += "-" * 80 + "\n"
    return output