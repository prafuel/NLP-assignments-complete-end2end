
from abc import ABC, abstractmethod
import pandas as pd


class ReadData(ABC):
    @abstractmethod
    def read(self, file_path: str) -> pd.DataFrame:
        pass

class ReadExcel(ReadData):
    def read(self, file_path: str) -> pd.DataFrame:
        extention = file_path.split(".")[-1]
        if extention not in ["xlsx", "xls"]:
            raise ValueError("Following file is not supported please provide excel or csv only")
        
        return pd.read_excel(file_path)

class ReadCsv(ReadData):
    def read(self, file_path: str) -> pd.DataFrame:
        extention = file_path.split(".")[-1]
        if extention not in ["csv", "tsv"]:
            raise ValueError("Following file is not supported please provide excel or csv only")
        
        if extention == "tsv":
            return pd.read_csv(file_path, sep="\t")
        else:
            return pd.read_csv(file_path)

class DataReader():
    def get_data(self, file_path: str) -> pd.DataFrame:
        extenstion = file_path.split(".")[-1]
        
        if extenstion in ["xlsx", "xls"]:
            return ReadExcel().read(file_path)
        if extenstion in ["csv", "tsv"]:
            return ReadCsv().read(file_path)

        raise ValueError("Following file is not supported please provide excel or csv only")