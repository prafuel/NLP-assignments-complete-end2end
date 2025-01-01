

with open("./MasterDictionary/positive-words.txt", "r") as pos:
    pos_words = [item.strip() for item in pos.readlines()]
    # print(pos_words)

with open("./MasterDictionary/negative-words.txt", "r", encoding='latin-1') as pos:
    neg_words = [item.strip() for item in pos.readlines()]
    # print(neg_words)

