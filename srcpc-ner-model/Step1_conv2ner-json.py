import pandas as pd
import json
import re
from pythainlp.tokenize import word_tokenize
from sklearn.model_selection import train_test_split

# โหลดไฟล์ CSV
df = pd.read_csv('../../Dataset/service_request_dataset_4xx.txt')

# กำหนดรายการ entities
room_numbers = [str(r) for r in range(941, 984)]
room_numbers.append('อาคาร9ชั้น4')
room_numbers.append('อาคาร9')
room_numbers.append('อาคาร6')
equipments = [
        'อินเทอร์เน็ต', 'internet', 'wi-fi', 'wifi', 'ไวไฟ', 'เครื่องสำรองไฟ', 'เครื่อง ups',
        'เครื่องคอมพิวเตอร์ตั้งโต๊ะ', 'คอมพิวเตอร์notebook', 'เครื่องปรับอากาศ', 'air', 'แอร์', 'notebook','คอมพิวเตอร์โน้ตบุ๊ค',
        'wi fi', 'air containing', 'aircontaining', 'เครื่องโปรเจคเตอร์', 'projector', 'สายhdmi', 'สายvga',
        'เก้าอี้', 'ช่องเสียบสายสัญญาณอินเทอร์เน็ต', 'ช่องเสียบสายแลน', 'เมาส์', 'mouse', 'ไวท์บอร์ด',
        'เครื่องพิมพ์เอกสาร', 'เครื่องprint', 'printer', 'เครื่องพิมพ์','เครื่องprinter','เมาส์','mouse','คีย์บอร์ด','keyboard',
        'กระดานหน้าห้อง', 'โปรเจคเตอร์', 'จอคอมพิวเตอร์', 'monitor','สายแลน', 'คอม', 
        'เบรกเกอร์', 'breaker', 'ups', 'สายชาร์จ', 'powerbank', 'power bank', 'คอมพิวเตอร์',
        'คอมพิวเตอร์โน้ตบุ๊ก', 'โน้ตบุ๊ก', 'laptop', 'หน้าจอคอมพิวเตอร์', 'เครื่องคอมพิวเตอร์', 'ชักโครก',
        'vpn', 'ไมค์โครโฟน', 'ไมโครโฟน', 'ลำโพง', 'speaker','แป้นพิมพ์', 'keyboard', 'เมาส์',
        'หลอดไฟ', 'หลอดไฟฟ้า','ลิฟต์','ปุ่มกดลิฟต์','อุปกรณ์','device','ห้องน้ำ','โต๊ะเรียน','ซอฟต์แวร์'
    ] # รายการ equipments
issues = [ 
        'ใช้งานไม่ได้','พัง','ชำรุด','เสีย','เปิดไม่ติด','เปิดไม่ได้','เชื่อมต่อไม่ได้','ไม่เสถียร','สัญญาณอ่อน','เก่า','ทำงานไม่ได้','ไม่ทำงาน',
        'ไม่พิมพ์','ไม่แสดงผล','ขาดๆหายๆ','ติดๆดับๆ','มาๆหายๆ','ไม่ชัด','ภาพเบลอ','สีเพี้ยน','สีไม่ปกติ','เสียงดัง','ไม่สะอาด','ไม่สามารถเชื่อมต่อได้',
        'ไม่สามารถใช้งานได้','ไม่สามารถเปิดได้','ไม่สามารถใช้งานได้','ไม่สามารถเชื่อมต่อได้','ไม่สามารถเปิดได้','ไม่สามารถใช้งานได้','เชื่อมต่อไม่ได้',
        'ไม่สามารถเปิดได้','ไม่สามารถใช้งานได้','ไม่สามารถเชื่อมต่อได้','ไม่สามารถเปิดได้','มีเสียงดัง','เสียงดัง','เสียงดังเป็นระยะๆ','มีเสียงเป็นพักๆ','เสียงไม่ค่อยดัง',
        'เสียงไม่ชัด','เสียงไม่ดัง','เสียงไม่ค่อยดัง','หมึกหมด','เป็นพักๆ','มีเสียงเป็นพักๆ', 'off','trip','กระพริบ','ติดตั้งไม่สำเร็จ',
        'ไม่เย็น','ไม่ทำงาน','ใช้งานไม่ดี','ไม่ค่อยชัด','ใช้ได้บางครั้ง','ทริป','ติดตั้งซอฟต์แวร์ไม่ได้','แบตเตอร์รี่เสื่อม','แบตเตอรี่หมด','แบตเตอรี่เสื่อม',
        'แบตเตอรี่ไม่ชาร์จ','แบตเตอรี่ไม่ทำงาน','ติดตั้งโปรแกรมไม่ได้','ติดตั้งโปรแกรมไม่สำเร็จ','ติดตั้งโปรแกรมไม่เสร็จ','ติดตั้งโปรแกรมไม่สำเร็จ','ติดตั้งโปรแกรมไม่เสร็จ',
        'ติดตั้งโปรแกรมไม่สำเร็จ','แสดงผลได้ไม่ดี','แสดงผลไม่ดี','แสดงผลไม่ชัดเจน','แสดงผลไม่ชัด','แสดงผลไม่ค่อยชัด','แสดงผลไม่ค่อยชัดเจน','ไฟดูด','ใช้อินเทอร์เน็ตไม่ได้',
        'หมึกจาง','เกิดปัญหา','หน่วยความจำเต็ม','ไม่พร้อมใช้งาน','มีน้ำหยด','น้ำหยด','ไม่ติด','ไม่ได้','ใช้งานได้ไม่ดี','พื้นที่จำกัด','ไม่สะดวกในการใช้งาน',
        'สัญญาณไม่เสถียร','สัญญาณอ่อน','สัญญาณไม่ดี','สัญญาณไม่ค่อยดี','สัญญาณไม่ค่อยเสถียร','สัญญาณไม่ค่อยแรง','สัญญาณไม่แรง','โหลดซอฟต์แวร์ช้า',
        'ทำงานช้า','ความเร็วลดลง','ใช้งานไม่ดี','ใช้งานสะดุด',

    ] # รายการ issues

def find_entities(text, keywords, label):
    for kw in sorted(keywords, key=lambda x: -len(x)):
        match = re.search(re.escape(kw), text)
        if match:
            return [(match.start(), match.end(), label)]
    return []

# แปลงข้อมูลเป็น SpaCy format
ner_data = []
for _, row in df.iterrows():
    text = row['Issue Description']
    text = text.replace(" ", "")
    text = text.lower()
    # tokens = word_tokenize(text, engine="newmm")
    # for token in tokens:
    entities = []
    entities += find_entities(text, room_numbers, 'ROOM')
    entities += find_entities(text, equipments, 'EQUIPMENT')
    entities += find_entities(text, issues, 'ISSUE')
    ner_data.append({
        'text': text,
        'entities': entities
    })

# แยก train/dev
train_data, dev_data = train_test_split(ner_data, test_size=0.2, random_state=42)

# บันทึกไฟล์ JSON
with open('../../Dataset/train_dataset_4xx-80-b.json', 'w', encoding='utf-8') as f:
    json.dump(train_data, f, ensure_ascii=False, indent=2)
with open('../../Dataset/dev_dataset_4xx-20-b.json', 'w', encoding='utf-8') as f:
    json.dump(dev_data, f, ensure_ascii=False, indent=2)
