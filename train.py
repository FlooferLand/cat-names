import tokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
import joblib

# Loading the data sets
(train, test) = tokenizer.get_datasets()

# Create a pipeline with a bag-of-words model and a Naive Bayes classifier
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(train.data, train.labels)

# Make predictions on the test data
predictions = model.predict(test.data)

# Evaluate the accuracy
accuracy = accuracy_score(test.labels, predictions)
print(f"Model accuracy: {accuracy}")
if accuracy < 0.6:
    print("WARNING: LOW MODEL ACCURACY")

# Saving the model
joblib.dump(model, "./data/model.pk1")
