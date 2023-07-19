import os
import sys
from typing import List, Tuple

import pandas as pd

from network.exception import NetworkException


class NetworkData:
    def __init__(self):
        pass

    def read_csv_from_folder(
        self, folder_name: str
    ) -> List[Tuple[pd.DataFrame, str, str]]:
        """
        It takes a folder name as a string, and returns a list of tuples, each tuple containing a pandas
        dataframe, the full path of the file, and the file name

        Args:
          folder_name (str): str - The name of the folder to read the csv files from

        Returns:
          A list of tuples.
        """
        try:
            lst: List[Tuple(pd.DataFrame, str, str)] = [
                (
                    pd.read_csv(folder_name + "/" + f),
                    folder_name + "/" + f,
                    f.split("/")[-1],
                )
                for f in os.listdir(folder_name)
            ]

            return lst

        except Exception as e:
            raise NetworkException(e, sys)
