# From taking input to get in proper format

import sys
from src.data_ingestion import DataReader
from src.data_crawler import data_crawling_fn
from src.data_formatting import data_formatting_fn

import pandas as pd

import time

pd.set_option("display.max_columns", None)


# steps
if __name__ == "__main__":
    args = sys.argv

    if len(args) < 2:
        raise ValueError("input file path is not given")

    file_path = args[-1]

    print("=======" * 12)
    print(f"File path : {file_path}")

    start = time.time()
    df = (
        DataReader().get_data(file_path)
        .assign(
            crawled_data=lambda df_: df_.URL.apply(data_crawling_fn)
        )
        .pipe(data_formatting_fn)
    )


    # not reccomanded
    # df = pd.read_csv("./notebooks/extracted_data.csv")
    # df = (
    #     df.pipe(data_formatting_fn)
    # )

    end = time.time() - start
    print("time taken", end)
    print("=======" * 12)
    print(df)

    
    print("=======" * 12)
    print("Saving file...")
    print("=======" * 12)

    df.to_csv(f"./outputs/output_{file_path.split("/")[-1].replace(".","_")}.csv", index=False)

    print("=======" * 12)
    print("File saved at ./outputs")
    print("=======" * 12)

