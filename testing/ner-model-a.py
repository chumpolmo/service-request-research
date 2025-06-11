import spacy
from spacy.symbols import ORTH, LEMMA
from spacy.tokens import Token
from spacy.language import Language

nlp = spacy.load('en_core_web_sm')
doc = nlp(u'I am flying to Frisco.')
print([w.text for w in doc])

# Add custom tokenizer exception for 'Frisco'
#special_case = [{ORTH: "Frisco", LEMMA: "San Francisco"}]
special_case = [{ORTH: "Frisco"}]

# Add it to tokenizer exceptions
nlp.tokenizer.add_special_case("Frisco", special_case)

# Test
doc = nlp(u'I am flying to Frisco.')
for token in doc:
	#print(f"{token.text} -> {token.lemma_}")
	#print(token.text, token.pos_, token.dep_)
	#print(token.head.text, token.dep_, token.text)
	if token.ent_type != 0:
		print(token.text, token.ent_type_)

print([w.text for w in doc if w.tag_== 'VBG' or w.tag_== 'VB' or w.pos_ == 'PROPN'])

for sent in doc.sents:
	print([w.text for w in sent if w.dep_ == 'ROOT' or w.dep_ == 'pobj'])

"""
doc = nlp(u'this product integrates both libraries for downloading and applying patches')
for token in doc:
	print(token.text, token.lemma_)
"""
