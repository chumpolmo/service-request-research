from transformers import AutoTokenizer, AutoModelForTokenClassification

model_name = "./output-mbert/checkpoint-265"
AutoTokenizer.from_pretrained(model_name).save_pretrained("mbert-ner-spacy-model")
AutoModelForTokenClassification.from_pretrained(model_name).save_pretrained("mbert-ner-spacy-model")
