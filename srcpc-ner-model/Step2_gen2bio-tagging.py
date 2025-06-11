import spacy, json
from spacy.tokens import DocBin
from pythainlp.tokenize import word_tokenize

def create_bio_tags(text, entities):
    tokens = word_tokenize(text, engine="newmm")
    bio_tags = ["O"] * len(tokens)

    char_to_token = {}
    start = 0
    for i, token in enumerate(tokens):
        for j in range(len(token)):
            char_to_token[start + j] = i
        start += len(token)

    for start_char, end_char, label in entities:
        token_start = char_to_token.get(start_char, None)
        token_end = char_to_token.get(end_char - 1, None)

        if token_start is None or token_end is None:
            continue

        bio_tags[token_start] = f"B-{label}"
        for i in range(token_start + 1, token_end + 1):
            bio_tags[i] = f"I-{label}"

    return tokens, bio_tags

# ตัวอย่างใช้งาน
# data = {
#     "text": "ไวไฟ ห้อง 963 มีปัญหาอีกแล้ว",
#     "entities": [
#         [0, 3, "PRODUCT"],
#         [5, 12, "ROOM"],
#         [14, 20, "ISSUE"]
#     ]
# }

# Load file
with open('../../Dataset/train_dataset_3-c.json', encoding='utf-8') as f:
    data = json.load(f)

# # Save in a format compatible with Huggingface or SpaCy
with open('./train_bio_ner_dataset_3-c.txt', 'w', encoding='utf-8') as f:
    # f.write("[\n")
    for obj in data:
        tokens, bio_tags = create_bio_tags(obj["text"], obj["entities"])
        # f.write("\t[")
        for t, tag in zip(tokens, bio_tags):
            f.write(f"{t} {tag}\n")
            # f.write(f"(\"{t}\" \"{tag}\"), ")
        f.write("\n")  # Sentence boundary
        # f.write("],\n")
    # f.write("]")
