import spacy
from spacy import displacy

# Load pre-trained model
nlp = spacy.load("en_core_web_sm")

# Sample text
text = "Elon Musk founded SpaceX and now lives in Texas."

# Process the text
doc = nlp(text)

# Print the sample sentence’s tokens
print([w.text for w in doc])

# Print a simple example of how to do lemmatization
for token in doc:
    # print(token.tag_, token.text, token.lemma_)
    if token.tag_ == 'VBG' or token.tag_ == 'VB' or token.tag_ == 'VBZ' or token.tag_ == 'RB':
        print(token.tag_, token.text, token.lemma_)
    print(token.pos_, token.dep_, token.head.text, token.ent_type)
    if token.ent_type != 0:
        print("NER: ", token.text, token.ent_type_)

# Print syntactic relations
for sent in doc.sents:
    print("Syntactic Relations: ", [w.text for w in sent if w.dep_ == 'ROOT' or w.dep_ == 'pobj'])

# Print named entities
for ent in doc.ents:
    print(ent.text, ent.label_)

# displacy.render(doc, style="ent", jupyter=True)  # If using Jupyter Notebook

from spacy.tokens import Span
# Create a new span
span = Span(doc, 5, 6, label=nlp.vocab.strings["ORG"])
doc.ents = list(doc.ents) + [span]

# Now print again
for ent in doc.ents:
    print(ent.text, ent.label_)
