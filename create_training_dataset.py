import pandas as pd

# legitimate emails
legit = pd.read_csv("emails.csv")
legit["label"] = 0

# phishing dataset
phishing = pd.read_csv("phishing_dataset.csv")

# spear phishing dataset
spear = pd.read_csv("spear_phishing_dataset.csv")

# combine all datasets
dataset = pd.concat([legit, phishing, spear])

# shuffle data
dataset = dataset.sample(frac=1)

# save final dataset
dataset.to_csv("final_dataset.csv", index=False)

print("Dataset created successfully")