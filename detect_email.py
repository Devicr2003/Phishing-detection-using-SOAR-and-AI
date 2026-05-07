import pickle
#from soar_simulation import soar_response

# Load model
model = pickle.load(open("phishing_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Input email
email = input("Enter email content: ")

# Convert to vector
email_vector = vectorizer.transform([email])

# Prediction
prediction = model.predict(email_vector)

if prediction[0] == 1:

    print("Phishing Email Detected")

    soar_response(email)

else:

    print("Safe Email")