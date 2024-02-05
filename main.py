import joblib

# Loading the model
print("Loading model ..")
loaded_model = joblib.load("./data/model.pk1")
print("Model loaded!")
print()

# Predicting
print("Input a word to correct into a silly name for a cat")
input_word = input("Word: ").lower().strip().split(' ')

print("Here are some variations:")
names: [str] = []
for i in range(0, 20):
    prediction: str = loaded_model.predict(input_word)
    if prediction not in names:
        names.append(prediction)

# Output
for name in names:
    print(f"- {name}")
