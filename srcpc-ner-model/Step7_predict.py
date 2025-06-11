import spacy
import spacy_thai
from pythainlp.tokenize import word_tokenize

ner_model = "./output_ner-b/model-best"
text = "แอร์มีน้ำหยดเมื่อเปิดใช้งานไปสักพักในห้อง 953 "

nlp = spacy.load(ner_model)
doc = nlp(text)
print([(ent.text, ent.label_) for ent in doc.ents])