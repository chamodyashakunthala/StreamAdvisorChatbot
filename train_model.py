import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pickle


data = pd.read_csv("dataset.csv")


data = pd.get_dummies(data, columns=["Interest"])


X = data.drop("Stream", axis=1)
y = data["Stream"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


model = DecisionTreeClassifier()
model.fit(X_train, y_train)


accuracy = model.score(X_test, y_test)
print(f" Model trained successfully! Accuracy: {accuracy*100:.2f}%")


with open("stream_selection_model.pkl", "wb") as f:
    pickle.dump((model, X.columns.tolist()), f)

print(" Model saved as stream_selection_model.pkl")
