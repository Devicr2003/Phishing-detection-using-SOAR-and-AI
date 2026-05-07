import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# load dataset
data = pd.read_csv("final_dataset.csv")

# remove empty emails
data = data.dropna(subset=["text"])

X = data["text"]
y = data["label"]

# TF-IDF
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# train model
model = LogisticRegression()
model.fit(X_vectorized, y)

# save model
pickle.dump(model, open("phishing_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained successfully")