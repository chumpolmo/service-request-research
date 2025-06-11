from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import torch.nn.functional as F
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # หรือ ["*"] สำหรับทุก origin (ระวังความปลอดภัย)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# โหลด Model และ Tokenizer ที่ fine-tune แล้ว
model_path = "../testing/output-mbert/checkpoint-265"  # เปลี่ยน path ให้ตรงกับโมเดลที่คุณฝึกเอง
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

class InputText(BaseModel):
    text: str

@app.post("/ner")
async def ner(input_text: InputText):
    text = input_text.text
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)

    logits = outputs.logits  # [batch_size, seq_len, num_labels]
    probs = F.softmax(logits, dim=-1)  # Convert logits to probabilities
    predictions = torch.argmax(logits, dim=-1)  # [batch_size, seq_len]

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    labels = [model.config.id2label[label_id] for label_id in predictions[0].tolist()]
    probs_list = probs[0].tolist()  # [seq_len, num_labels]

    # สร้างผลลัพธ์สำหรับแต่ละ token
    token_results = []
    for token, label, prob_vec in zip(tokens, labels, probs_list):
        if label != "O":  # 🔥 เพิ่ม filter เฉพาะ entity
            confidence = max(prob_vec)
            token_result = {
                "token": token,
                "label": label,
                "confidence": max(prob_vec),
                "all_probs": {model.config.id2label[i]: float(prob) for i, prob in enumerate(prob_vec)}
            }
            token_results.append(token_result)

    return {
        "text": text,
        "entities": token_results,
        "labels": model.config.id2label  # แถม mapping id2label ทั้งหมด
    }