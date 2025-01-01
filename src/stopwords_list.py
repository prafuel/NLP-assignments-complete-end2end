
parent_dir = "../StopWords" if __name__ == "__main__" else "./StopWords"

def get_stop_words_fn() -> list:

    # Stopwords_auditor
    with open(f"{parent_dir}/StopWords_Auditor.txt", "r") as sa:
        auditor_sw = [item.strip() for item in sa.readlines()]
        # print(auditor_sw)

    # StopWords_currencies
    with open(f"{parent_dir}/StopWords_Currencies.txt", "r", encoding='latin-1' ) as sc:
        currencies_sw = [i.strip() for item in sc.readlines() for i in item.split("|")]
        # print(currencies_sw)

    # StopWords_DatesandNumbers
    with open(f"{parent_dir}/StopWords_DatesandNumbers.txt", "r") as sdn:
        date_and_num_sw = [i.strip() for item in sdn.readlines() for i in item.split("|")]
        # print(date_and_num_sw)

    # StopWords_Generic.txt
    with open(f"{parent_dir}/StopWords_Generic.txt", "r") as sg:
        generic_sw = [item.strip() for item in sg.readlines()]
        # print(generic_sw)

    # StopWords_GenericLong
    with open(f"{parent_dir}/StopWords_GenericLong.txt", "r") as sgl:
        generic_long_sw = [item.strip() for item in sgl.readlines()]
        # print(generic_long_sw)

    # StopWords_Geographic
    with open(f"{parent_dir}/StopWords_Geographic.txt", "r") as sge:
        geographic_sw = [i.strip() for item in sge.readlines() for i in item.split("|")]
        # print(geographic_sw)

    # # StopWords_Names
    with open(f"{parent_dir}/StopWords_Names.txt", "r") as sn:
        names_sw = [item.split('|')[0].strip()
            for item in sn.readlines()
            if not any(keyword in item for keyword in ['http', 'www', '>']) ]
        # print(names_sw)

    return auditor_sw + currencies_sw + date_and_num_sw + generic_sw + generic_long_sw + geographic_sw + names_sw

if __name__ == "__main__":
    print(get_stop_words_fn())