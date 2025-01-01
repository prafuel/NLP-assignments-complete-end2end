
import pandas as pd

from src.sentiment_analysis import (
    removing_stopwords_fn,
    get_score_fn,
    polarity_score_fn,
    subjectivity_score_fn,
    get_num_of_sentences_fn,
    get_num_of_complex_words_fn,
    count_syllables_per_word_fn,
    count_personal_pronouns_fn
)

def data_formatting_fn(df: pd.DataFrame):

    print("=======" * 12)
    print("Generating Results from given data...")
    print("=======" * 12)


    if "crawled_data" not in df.columns:
        raise ValueError("Column name 'crawled_data' is not available, you need to crawl data using src/data_crawler")
    
    return (
        df
        .assign(
            ARTICLE_DATA_CASE=lambda df_: df_.crawled_data.replace("$", " ").apply(removing_stopwords_fn),
            ARTICLE_DATA=lambda df_: df_.ARTICLE_DATA_CASE.str.lower(),

            # Creating a dictionary of Positive and Negative words
            SCORES=lambda df_: df_.ARTICLE_DATA.apply(get_score_fn),

            # Extracting Derived variables
            POSITIVE_SCORE=lambda df_: df_.SCORES.str.split("|").str[0].astype("int"),
            NEGATIVE_SCORE=lambda df_: df_.SCORES.str.split("|").str[1].astype("int"),
            NEUTRAL_SCORE = lambda df_: df_.SCORES.str.split("|").str[2].astype("int"),
            POLARITY_SCORE=lambda df_: (
                # formula : (pos_score - neg_score) / ((pos_score + neg_score) + 0.000001)
                (df_.POSITIVE_SCORE - df_.NEGATIVE_SCORE) / ((df_.POSITIVE_SCORE + df_.NEGATIVE_SCORE) + 0.000001)
            ),
            SUBJECTIVITY_SCORE=lambda df_: (
                # formula : (pos_score + neg_score) / (total_words + 0.000001)
                (df_.POSITIVE_SCORE + df_.NEGATIVE_SCORE) / ((df_.POSITIVE_SCORE + df_.NEGATIVE_SCORE + df_.NEUTRAL_SCORE) + 0.000001)
            ),

            # Analysis of Readability
            # Word Count
            WORD_COUNT=lambda df_: df_.ARTICLE_DATA.str.split(" ").str.len(),
            SENTENCE_COUNT=lambda df_: df_.ARTICLE_DATA.apply(get_num_of_sentences_fn),

            # Syllable Count Per Word
            SYLLABLE_PER_WORD=lambda df_: df_.ARTICLE_DATA.apply(count_syllables_per_word_fn),
            AVG_SENTENCE_LENGTH=lambda df_: df_.WORD_COUNT / df_.SENTENCE_COUNT,

            # Complex Word Count
            COMPLEX_WORD_COUNT=lambda df_: df_.ARTICLE_DATA.apply(get_num_of_complex_words_fn),
            PERCENTAGE_OF_COMPLEX_WORDS=lambda df_: df_.COMPLEX_WORD_COUNT / df_.WORD_COUNT,
            FOG_INDEX=lambda df_: 0.4 * (df_.AVG_SENTENCE_LENGTH + df_.PERCENTAGE_OF_COMPLEX_WORDS),

            # Average Number of Words Per Sentence
            AVG_NUMBER_OF_WORDS_PER_SENTENCE=lambda df_: df_.SYLLABLE_PER_WORD.apply(sum) / df_.WORD_COUNT,

            # Personal Pronouns
            PERSONAL_PRONOUNS=lambda df_: df_.ARTICLE_DATA_CASE.apply(count_personal_pronouns_fn),

            # Average Word Length
            AVG_WORD_LENGTH=lambda df_: df_.ARTICLE_DATA.str.replace(" ", "").str.split("").apply(len) / df_.WORD_COUNT
        )
        .drop(columns=['crawled_data'])

        [['URL_ID', 'URL', 'POSITIVE_SCORE',
        'NEGATIVE_SCORE', 'POLARITY_SCORE',
        'SUBJECTIVITY_SCORE',
        'AVG_SENTENCE_LENGTH', 'PERCENTAGE_OF_COMPLEX_WORDS',
        'FOG_INDEX', 'AVG_NUMBER_OF_WORDS_PER_SENTENCE',
        'COMPLEX_WORD_COUNT', 'WORD_COUNT', 'SYLLABLE_PER_WORD',
        'PERSONAL_PRONOUNS', 'AVG_WORD_LENGTH']]

        .rename(columns=lambda df_: df_.replace("_", " "))
        .rename(columns={"URL ID" : "URL_ID"})
    )

if __name__ == "__main__":
    # df = pd.read_csv("./notebooks/extracted_data.csv")
    # print(data_formatting_fn(df).POLARITY_SCORE[144])
    pass