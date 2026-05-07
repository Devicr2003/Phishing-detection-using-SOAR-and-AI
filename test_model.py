import pickle

model = pickle.load(open("phishing_model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

email = ["Verify your bank account immediately"]

email_vector = vectorizer.transform(email)

prediction = model.predict(email_vector)

print(prediction)