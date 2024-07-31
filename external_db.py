
import pandas as pd
from typing import Protocol

class ExternalDb(Protocol):

    def read(self, connection: str)->pd.DataFrame:
        ...
    
    def write(self, connection: str, data: pd.DataFrame)->None:
        ...

