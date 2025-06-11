import spacy
import spacy_thai
from pythainlp.tokenize import word_tokenize
from spacy.language import Language
from spacy.tokens import Doc
from spacy.tokens import DocBin
import json
from tqdm import tqdm

# Variables
ds_path = "../../../Dataset/dev_ner_data_4xx.json"  # <<< แก้ path หากแตกต่าง
op_path = "./test-4xx.spacy"

# Custom tokenizer function
@Language.factory("pythainlp_tokenizer")
def create_tokenizer(nlp, name):
    def custom_tokenizer(text):
        words = word_tokenize(text)
        return Doc(nlp.vocab, words=words)
    return custom_tokenizer

# โหลดโมเดลพื้นฐานภาษาไทย (หรือใช้ en_core_web_sm ถ้าข้อมูลเป็นภาษาอังกฤษ)
nlp = spacy.blank("th")  # ใช้โมเดลเปล่าสำหรับฝึกใหม่
# nlp = spacy_thai.load()
nlp.tokenizer = create_tokenizer(nlp, "pythainlp_tokenizer")

# เพิ่ม pipeline สำหรับ NER
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")

# โหลดชุดข้อมูลที่เตรียมไว้
with open(ds_path, "r", encoding="utf-8") as f:
    training_data = json.load(f)

# เพิ่ม label ที่พบใน dataset เข้าไปใน pipeline
for entry in training_data:
    for start, end, label in entry["entities"]:
        ner.add_label(label)

# เตรียมข้อมูลเป็น spaCy format
db = DocBin()
for entry in tqdm(training_data):
    text = entry["text"]
    doc = nlp.make_doc(text)
    ents = []
    for start, end, label in entry["entities"]:
        span = doc.char_span(start, end, label=label)
        if span:
            ents.append(span)
    doc.ents = ents
    db.add(doc)

# บันทึกข้อมูลฝึกฝน
db.to_disk(op_path)
