import spacy

nlp = spacy.load("./application/server/ner_model_spacy/model-last")

def get_priority(entities):
    product_keywords_high = ["wi-fi", "อินเทอร์เน็ต", "ups", "เบรกเกอร์", "คอมพิวเตอร์", "หน้าจอ", "โปรเจคเตอร์"]
    issue_high = ["เปิดไม่ติด", "ใช้งานไม่ได้", "ไม่ทำงาน", "เชื่อมต่อไม่ได้"]
    issue_medium = ["ชำรุด", "เสีย", "หมึกหมด", "ไม่พิมพ์", "ไม่แสดงผล", "ติด ๆ ดับ ๆ"]
    issue_low = ["เสียงดัง", "สีเพี้ยน", "ลบไม่สะอาด", "สัญญาณอ่อน", "ไม่ชัด", "ภาพเบลอ", "สัญญาณค่อนข้างอ่อน"]

    product_texts = [e[0].lower() for e in entities if e[2] == "PRODUCT"]
    issue_texts = [e[0].lower() for e in entities if e[2] == "ISSUE"]

    print("Product texts:", product_texts)
    print("Issue texts:", issue_texts)

    # Rule: High
    if any(p for p in product_texts if any(pk in p for pk in product_keywords_high)) \
       and any(i for i in issue_texts if any(ih in i for ih in issue_high)):
        return "High"
    
    # Rule: Medium
    if any(i for i in issue_texts if any(im in i for im in issue_medium)):
        return "Medium"
    
    # Rule: Low
    if any(i for i in issue_texts if any(il in i for il in issue_low)):
        return "Low"
    
    return "Unknown"

doc = nlp("สัญญาณ Wi-Fi ในห้อง 953 ใช้งานไม่ได้")
print("Text:", doc.text)
print("Entities found:")

for ent in doc.ents:
    print(ent.text, ent.label_)

entities = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
priority = get_priority([(e[0], e[1], e[3]) for e in entities])
print("Priority:", priority)
