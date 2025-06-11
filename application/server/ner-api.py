# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spacy

# Load trained NER model
model_path = "./nms-hw64-dr0.1-ms2k-lr0.0005-vth-a/model-last"  # Update with your model path
nlp = spacy.load(model_path)

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # หรือ ["*"] ถ้าอยากให้ทุกที่เรียกได้ (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request body
class TextRequest(BaseModel):
    text: str

def get_priority(entities):
    equipment_keywords_high = [
        'อินเทอร์เน็ต', 'internet', 'wi-fi', 'wifi', 'ไวไฟ', 'เครื่องสำรองไฟ', 'เครื่อง ups', 'ups',
        'เครื่องคอมพิวเตอร์ตั้งโต๊ะ', 'คอมพิวเตอร์notebook', 'เครื่องปรับอากาศ', 'air', 'แอร์', 'notebook','คอมพิวเตอร์โน้ตบุ๊ค',
        'wi fi', 'air containing', 'aircontaining', 'เครื่องโปรเจคเตอร์', 'projector', 'สายhdmi', 'สายvga',
        'เก้าอี้', 'ช่องเสียบสายสัญญาณอินเทอร์เน็ต', 'ช่องเสียบสายแลน', 'เมาส์', 'mouse', 'ไวท์บอร์ด',
        'เครื่องพิมพ์เอกสาร', 'เครื่องprint', 'printer', 'เครื่องพิมพ์','เครื่องprinter','เมาส์','mouse','คีย์บอร์ด','keyboard',
        'กระดาน', 'whiteboard', 'กระดานไวท์บอร์ด', 'โปรเจคเตอร์', 'จอคอมพิวเตอร์', 'monitor','สายแลน', 'คอม', 
        'เบรกเกอร์', 'breaker', 'ups', 'สายชาร์จ', 'powerbank', 'power bank', 'คอมพิวเตอร์', 'หน้าจอ', 
        'คอมพิวเตอร์โน้ตบุ๊ก', 'โน้ตบุ๊ก', 'laptop', 'หน้าจอคอมพิวเตอร์', 'เครื่องคอมพิวเตอร์', 'ชักโครก',
        'vpn', 'ไมค์โครโฟน', 'ไมโครโฟน', 'ลำโพง', 'speaker','แป้นพิมพ์', 'keyboard', 'เมาส์',
        'หลอดไฟ', 'หลอดไฟฟ้า','ลิฟต์','ปุ่มกดลิฟต์','อุปกรณ์','device','ห้องน้ำ','โต๊ะเรียน','ซอฟต์แวร์'
    ]
    issue_high = [
        'เปิดไม่ติด', 'เปิดไม่ได้', 'ใช้งานไม่ได้', 'ทำงานไม่ได้', 'ไม่ทำงาน', 'เชื่อมต่อไม่ได้', 'ไม่สามารถเชื่อมต่อได้', 'ไม่สามารถใช้งานได้',
        'ไม่สามารถเปิดได้', 'พัง', 'ชำรุด', 'เสีย', 'ไม่พิมพ์', 'ไม่แสดงผล', 'หมึกหมด', 'off', 'trip', 'ทริป', 'แบตเตอรี่หมด', 'แบตเตอรี่ไม่ชาร์จ', 
	    'แบตเตอรี่ไม่ทำงาน', 'ไฟดูด', 'ใช้อินเทอร์เน็ตไม่ได้', 'หน่วยความจำเต็ม', 'ไม่ติด', 'ไม่ได้', 'พิมพ์ไม่ได้',
    ] 
    issue_medium = [
        'ขาดๆหายๆ', 'ติดๆดับๆ', 'มาๆหายๆ', 'ทำงานช้า', 'สีเพี้ยน', 'สีไม่ปกติ', 'ไม่ชัด', 'ภาพเบลอ',
	    'เสียงดัง', 'มีเสียงดัง', 'มีเสียง', 'กระพริบ', 'ติดตั้งไม่สำเร็จ', 'ติดตั้งซอฟต์แวร์ไม่ได้', 'แบตเตอร์รี่เสื่อม', 'แบตเตอรี่เสื่อม',
	    'ติดตั้งโปรแกรมไม่ได้','ติดตั้งโปรแกรมไม่สำเร็จ','ติดตั้งโปรแกรมไม่เสร็จ', 'ไม่พร้อมใช้งาน', 'สัญญาณไม่ดี', 'สัญญาณไม่ค่อยดี', 
    ]
    issue_low = [
        'ลบไม่สะอาด', 'สัญญาณอ่อน', 'ไม่ชัด', 'ภาพเบลอ', 'สัญญาณค่อนข้างอ่อน', 'ไม่เสถียร', 'พื้นที่จำกัด','ไม่สะดวกในการใช้งาน', 'ไม่เย็น', 
        'สัญญาณอ่อน', 'เก่า', 'ไม่สะอาด', 'เสียงไม่ดัง', 'เสียงไม่ชัด', 'ใช้งานไม่ดี', 'ไม่ค่อยชัด', 'ใช้ได้บางครั้ง', 'แสดงผลได้ไม่ดี', 'แสดงผลไม่ดี',
	    'แสดงผลไม่ชัดเจน', 'แสดงผลไม่ชัด', 'แสดงผลไม่ค่อยชัด', 'แสดงผลไม่ค่อยชัดเจน', 'หมึกจาง', 'เกิดปัญหา', 'มีน้ำหยด', 'น้ำหยด', 'ใช้งานได้ไม่ดี',
        'สัญญาณไม่เสถียร', 'สัญญาณไม่ค่อยเสถียร','สัญญาณไม่ค่อยแรง', 'สัญญาณไม่แรง', 'โหลดซอฟต์แวร์ช้า', 'ความเร็วลดลง', 'ใช้งานสะดุด',
    ]

    equipment_texts = [e[0].lower() for e in entities if e[2] == "EQUIPMENT"]
    issue_texts = [e[0].lower() for e in entities if e[2] == "ISSUE"]

    # Rule: High
    if any(p for p in equipment_texts if any(pk in p for pk in equipment_keywords_high)) \
       and any(i for i in issue_texts if any(ih in i for ih in issue_high)):
        return "High"
    
    # Rule: Medium
    if any(i for i in issue_texts if any(im in i for im in issue_medium)):
        return "Medium"
    
    # Rule: Low
    if any(i for i in issue_texts if any(il in i for il in issue_low)):
        return "Low"
    
    return "Unknown"

# Define endpoint
@app.post("/predict/")
def predict(request: TextRequest):
    doc = nlp(request.text)
    entities = [{"text": ent.text, "start_char": ent.start_char, "end_char": ent.end_char, "label": ent.label_} for ent in doc.ents]
    simplified_entities = [(ent.text, ent.start_char, ent.label_) for ent in doc.ents]
    # Get priority based on entities
    priority = get_priority(simplified_entities)
    return {"entities": entities, "priority": priority}

# Root endpoint
@app.get("/", summary="Root", tags=["Basic"])
def read_root():
    return {"message": "Welcome to the Service Request NER API!"}