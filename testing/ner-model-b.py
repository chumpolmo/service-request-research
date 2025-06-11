import spacy

# Load English NER model
nlp = spacy.load("en_core_web_sm")

text = "AC unit in Room 203 is not working."

# Run NER
doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.label_)

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.pipeline import Pipeline

# pipeline = Pipeline([
#     ("tfidf", TfidfVectorizer()),
#     ("clf", RandomForestClassifier())
# ])

# # Fit model
# pipeline.fit(X_train_texts, y_train_labels)

# # Predict
# y_pred = pipeline.predict(X_test_texts)