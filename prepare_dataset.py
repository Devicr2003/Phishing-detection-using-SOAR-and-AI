import pandas as pd

# legitimate emails
enron = pd.read_csv("enron_legitimate.csv")

# phishing emails
phishing = pd.read_csv("phishing_email.csv")

# spear phishing
spear = pd.read_csv("spear_phishing_dataset.csv")

# combine datasets
dataset = pd.concat([enron, phishing, spear])

# shuffle
dataset = dataset.sample(frac=1)

# save final dataset
dataset.to_csv("final_dataset.csv", index=False)

print("Final dataset created")