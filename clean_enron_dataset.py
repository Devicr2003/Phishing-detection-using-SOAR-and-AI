import pandas as pd

# load dataset
data = pd.read_csv("emails.csv")

# keep only message column
data = data[["message"]]

# rename column
data = data.rename(columns={"message": "text"})

# add label for legitimate email
data["label"] = 0

# save cleaned dataset
data.to_csv("enron_legitimate.csv", index=False)

print("Enron dataset cleaned successfully")