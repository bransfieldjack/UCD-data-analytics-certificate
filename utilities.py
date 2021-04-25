import requests, json
import pandas as pd
from typing import Dict, Union


class Utility:

    """
    A utility class to encapsulate reusable functionality for my script (DRY).
    The class constructor expects an optional 'df' parameter of dataframe, defaulting to None.
    """

    def __init__(self, df=None) -> None:
        self._df = df
        self._row_null_values = None

    def fetch_data_from_api(self, url) -> Union[Dict[str, str], str]:
        """
        fetch data from an API and return JSON
        """
        # specify the required format of the data requested from the api
        headers = {
            "Content-type": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
        }
        try:
            # make the request
            request = requests.get(url, headers=headers)
            # assign the json result to a variable called 'data'
            data = request.json()
            return data
        except ValueError as exception:
            print("An exception occurred in 'fetch_data_from_api()': " + exception)
            return "An exception occurred in 'fetch_data_from_api()': " + exception

    def check_rows_null_values(self, columns) -> list:
        """
        Expects a parameter called 'columns' of type list.
        The function will iterate over the columns list and return a new list containing a value dictionary
        with each column name as the key and the count of nulls as the corresponding value.
        This method can be reused elsewhere in the program, hence avoiding the DRY principal of pythonic programming.
        """
        value_dict_list = (
            []
        )  # list to store the results of the for loop operation, which will be a sequence of dicts for each column with corresponding values.
        for column in columns:
            value_dict = {
                "Name": column,
                "Null counts": self._df[column].isnull().sum(),
            }
            value_dict_list.append(value_dict)
        self._row_null_values = value_dict_list
        return self._row_null_values

    def get_row_value_counts(self, column) -> int:
        res = self._df.groupby([column]).count()
        return res

    def Average(lst) -> int:
        """
        Get the mean of a list of numbers
        """
        return sum(lst) / len(lst)