import json

def bio_to_spacy_jsonl(input_path, output_path):
    data = []
    with open(input_path, encoding='utf-8') as f:
        lines = f.readlines()

    sentence = []
    tags = []

    for line in lines:
        line = line.strip()
        if line == "":
            if sentence:
                data.append((sentence, tags))
                sentence = []
                tags = []
        else:
            try:
                token, tag = line.split()
                sentence.append(token)
                tags.append(tag)
            except ValueError:
                continue  # ข้ามกรณีบรรทัดไม่สมบูรณ์

    if sentence:
        data.append((sentence, tags))

    output_data = []

    for tokens, tags in data:
        text = ''.join(tokens)
        entities = []
        idx = 0
        char_pos = 0

        while idx < len(tokens):
            token = tokens[idx]
            tag = tags[idx]
            token_len = len(token)

            if tag.startswith("B-"):
                label = tag[2:]
                start = char_pos
                end = start + token_len
                idx += 1
                char_pos += token_len

                while idx < len(tokens) and tags[idx].startswith("I-"):
                    end += len(tokens[idx])
                    char_pos += len(tokens[idx])
                    idx += 1

                entities.append([start, end, label])
            else:
                char_pos += token_len
                idx += 1

        output_data.append({
            "text": text,
            #"annotations": {
                "entities": entities
            #}
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        for item in output_data:
            json.dump(item, f, ensure_ascii=False)
            f.write(',\n')

# 🟢 ตัวอย่างการใช้:
bio_to_spacy_jsonl("./train_bio_ner_dataset_4xx.txt", "./train-b.spacy.jsonl")
bio_to_spacy_jsonl("./dev_bio_ner_dataset_4xx.txt", "./dev-b.spacy.jsonl")
