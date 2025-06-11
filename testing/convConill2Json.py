from datasets import Dataset

train_data = {
    "tokens": [], 
    "ner_tags": []
}

label_set = set()

with open('../srcpc-ner-model/train_bio_ner_dataset_42x.txt', 'r', encoding='utf-8') as f:
    tokens = []
    tags = []
    for line in f:
        line = line.strip()
        if not line:
            if tokens:
                train_data["tokens"].append(tokens)
                train_data["ner_tags"].append(tags)
                tokens = []
                tags = []
        else:
            splits = line.split()
            if len(splits) >= 2:
                token, tag = splits[0], splits[-1]
                tokens.append(token)
                tags.append(tag)
                label_set.add(tag)
    # Append the last sentence if the file doesn't end with a newline
    if tokens:
        train_data["tokens"].append(tokens)
        train_data["ner_tags"].append(tags)

label_list = sorted(label_set)

print("label_list:", label_list)

# Create mapping dictionaries
label2id = {label: idx for idx, label in enumerate(label_list)}
id2label = {idx: label for label, idx in label2id.items()}

# Convert ner_tags from string labels to integer IDs
train_data_indexed = {
    "tokens": train_data["tokens"],
    "ner_tags": [
        [label2id[tag] for tag in tag_seq]
        for tag_seq in train_data["ner_tags"]
    ]
}

# Save the processed data to a new file
# print("train_data:", train_data_indexed)
# with open('../srcpc-ner-model/train_bio_ner_dataset_42x_indexed.txt', 'w', encoding='utf-8') as f:
    # for tokens, tags in zip(train_data_indexed["tokens"], train_data_indexed["ner_tags"]):
    #     for token, tag in zip(tokens, tags):
    #         f.write(f"{token} {tag}\n")
    #     f.write("\n")  # Separate sentences with a newline

# Assuming you already have `train_data_indexed`
hf_dataset = Dataset.from_dict(train_data_indexed)

# To preview
print(hf_dataset[0])