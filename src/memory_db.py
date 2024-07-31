from dataclasses import dataclass
import pandas as pd
from typing import Any, Protocol


class InMemoryDb(Protocol):

    def add_element(self, element: Any)->None: # this really has two jobs, convert the element then add it, should those be split? 
        ...

    def name_present(self, name: str)->bool:
        ...

    def mean(self, measure: str)->float:
        ...

    def export_data(self)->pd.DataFrame:
        ...

    def import_data(self, data: pd.DataFrame)->None:
        ...

class DataFrameDb:

    @staticmethod
    def create_element(element: dict)->pd.Series:
        return pd.Series(element)

    def add_element(self, element: dict)->None:
        row = self.create_element(element)
        n = len(self.data)
        self.data.loc[n, : ] = row

    def name_present(self, name: str)->bool:
        return any(self.data["Name"].str.lower().isin([name.lower()]))

    def mean(self, measure: str)->float:
        try:
            return self.data[measure].mean()
        except KeyError as e: 
            raise KeyError(f"No column {measure} in data. Measure must be in {self.data.columns}") from e
    
    def export_data(self)->pd.DataFrame:
        return self.data

    def import_data(self, data: pd.DataFrame)->None:
        self.data = data

@dataclass
class Element:
    name: str

class ElementDb:

    def __init__(self, element: Element) -> None:
        self.data = []
        self.element = element
    
    def create_element(self, datum: dict)->pd.Series:
        return self.element(**datum)

    def add_element(self, element: dict)->None:
        elem = self.create_element(element)
        self.data.append(elem)

    def name_present(self, name: str)->bool:
        return any(elem.name == name for elem in self.data)

    def mean(self, measure: str)->float:
        try:
            return sum(getattr(elem, measure) for elem in self.data)/len(self.data)
        except KeyError as e: 
            raise KeyError(f"No attribute {measure} in data. Measure must be in {self.data.attrs}") from e
    
    def export_data(self)->pd.DataFrame:
        df = pd.DataFrame()
        for row, elem in enumerate(self.data):
            for col, val in elem.__dict__.items():
                df.loc[row, col] = val
        return self.data

    def import_data(self, data: pd.DataFrame)->None:
        cols = data.columns
        for idx in data.index:
            holder = {col:data.loc[idx, col] for col in cols}
            elem = self.element(**holder)
            self.data.append(elem)

if __name__ == "__main__":
    df = pd.read_csv(r"C:\Users\jonat\Downloads\Root Beer Ratings - Sheet1.csv")

    in_mem = DataFrameDb()
    in_mem.import_data(df)
    in_mem.mean("Rating")


