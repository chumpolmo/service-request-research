import sys
from pythainlp.tokenize import word_tokenize, Tokenizer
from pythainlp.corpus.common import thai_words
from pythainlp.util import dict_trie

import spacy
import spacy_pythainlp.core

custom_words = set(thai_words())
custom_words.update(["ไวไฟ", "มีปัญหา", "มีน้ำหยด", "ไม่เย็น"])  # เพิ่มคำใหม่เข้าไป

text = "เครื่องโปรเจคเตอร์แสดงไม่เสถียรในห้อง 973"
tokenizer = Tokenizer(dict_trie(custom_words), engine="newmm")
tokens = tokenizer.word_tokenize(text)
# tokens = word_tokenize(text, engine="newmm")
print(tokens)
# ผลลัพธ์: ['ห้อง', '942', 'กระดานไวท์บอร์ด', 'ไม่ค่อยชัด', 'จาก', 'หลัง', 'ห้องเรียน']
# sys.exit(0)

txt_arr = [
    "ห้อง 953 เครื่องโปรเจคเตอร์ทำงานไม่ได้",
    "ห้อง 961 เครื่องพิมพ์เอกสารหมึกหมด",
    "เครื่องสำรองไฟเสียงดังเป็นระยะในห้อง 983",
]

for tmp in txt_arr:
    i = 0
    print("text:", tmp)
    for txt in tmp:
        print(i, txt, end="|")
        i += 1
    print("")

# nlp = spacy.blank('th')
# nlp.add_pipe('pythainlp')
# doc = nlp('ผมเป็นคนไทย แต่มะลิอยากไปโรงเรียนส่วนผมจะไปไหน ผมอยากไปเที่ยว')

# print(list(doc.sents))