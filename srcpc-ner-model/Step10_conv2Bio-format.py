def convert_to_spacy_format(input_file):
    """
    แปลงไฟล์ข้อมูลดิบเป็นรูปแบบที่เหมาะสำหรับการฝึกโมเดล NER
    
    :param input_file: เส้นทางไปยังไฟล์ข้อมูลต้นฉบับ
    :return: train_texts, train_labels ในรูปแบบที่พร้อมใช้งาน
    """
    train_texts = []
    train_labels = []
    current_text = []
    current_labels = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:  # บรรทัดว่างหมายถึงจบประโยค
                if current_text:
                    train_texts.append(current_text)
                    train_labels.append(current_labels)
                    current_text = []
                    current_labels = []
                continue
            
            parts = line.split()
            if len(parts) < 2:  # ตรวจสอบรูปแบบข้อมูล
                continue
                
            word = parts[0]
            label = parts[1]
            
            current_text.append(word)
            current_labels.append(label)
    
    # เพิ่มประโยคสุดท้ายหากไฟล์ไม่จบด้วยบรรทัดว่าง
    if current_text:
        train_texts.append(current_text)
        train_labels.append(current_labels)
    
    return train_texts, train_labels

# ตัวอย่างการใช้งาน
input_file = "train_bio_ner_dataset_42x.txt"  # เปลี่ยนเป็นเส้นทางไฟล์ของคุณ
train_texts, train_labels = convert_to_spacy_format(input_file)

# แสดงผลลัพธ์ตัวอย่าง
print("train_texts =", train_texts[:])  # แสดงตัวอย่างแรก
print("train_labels =", train_labels[:])  # แสดงตัวอย่างแรก

# บันทึกผลลัพธ์เป็นไฟล์ JSON หรือ CSV หากต้องการ
import json
with open("train_texts_bio_format.json", "w", encoding="utf-8") as f:
    json.dump(train_texts, f, ensure_ascii=False, indent=4)
with open("train_labels_bio_format.json", "w", encoding="utf-8") as f:
    json.dump(train_labels, f, ensure_ascii=False, indent=4)