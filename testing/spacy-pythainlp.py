import spacy
import spacy_pythainlp.core

# Use a pipeline as a high-level helper
from transformers import (
    AutoTokenizer, AutoModelForTokenClassification,
    DataCollatorForTokenClassification,
    TrainingArguments, Trainer, pipeline
)


# Model
model_name = "airesearch/wangchanberta-base-att-spm-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

text = "ห้อง953เครื่องปรับอากาศในห้องบางเครื่องเปิดใช้งานสักพักมีน้ำหยดบนพื้นห้อง"
tokens = tokenizer.tokenize(text)
print(tokens)

# nlp = spacy.blank('th')
# # nlp.add_pipe('pythainlp')
# pipe = pipeline("fill-mask", model="airesearch/wangchanberta-base-att-spm-uncased")
# nlp.add_pipe(pipe, last=True)

# doc = nlp('ผมเป็นคนไทยแต่มะลิอยากไปโรงเรียนส่วนผมจะไปไหนผมอยากไปเที่ยว')
# print(list(doc.sents))
