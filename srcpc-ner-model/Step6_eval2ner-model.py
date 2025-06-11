import spacy
from spacy.tokens import DocBin
from spacy.training import Example
from spacy.scorer import Scorer

# === Step 1: Load trained model ===
model_path = "../../srcpc-ner-model/output_ner-b-set-4/model-best"  # <<< แก้ path หากแตกต่าง
nlp = spacy.load(model_path)

# === Step 2: Load test dataset in .spacy format ===
test_data_path = "../../srcpc-ner-model/dev_ner-b.spacy"  # <<< เปลี่ยนเป็น path ชุดทดสอบที่คุณบันทึกไว้

doc_bin = DocBin().from_disk(test_data_path)
docs = list(doc_bin.get_docs(nlp.vocab))

# === Step 3: Create examples and evaluate ===
examples = [Example(predicted=nlp(doc.text), reference=doc) for doc in docs]

scorer = Scorer()
scores = scorer.score(examples)

# === Step 4: Print evaluation metrics ===
print("\n📊 Model Evaluation Metrics")
print("--------------------------")
print(f"Precision: {scores['ents_p']:.2f}%")
print(f"Recall:    {scores['ents_r']:.2f}%")
print(f"F1-score:  {scores['ents_f']:.2f}%")

# === Optional: Show entity-wise scores ===
print("\n🔍 Entity Type Breakdown")
for ent_type, result in scores['ents_per_type'].items():
    print(f"{ent_type:10}  P: {result['p']:.2f}%  R: {result['r']:.2f}%  F1: {result['f']:.2f}%")
