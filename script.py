import requests, json
import pandas as pd
import matplotlib.pyplot as plt


def main():

    # specify the required format of the data requested from the api
    headers = {
        "Content-type": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
    }

    # make the request
    request = requests.get("https://global-warming.org/api/co2-api", headers=headers)

    # assign the json result to a variable called 'data'
    data = request.json()

    # confirm the data has the expected type
    # print(type(data))

    # coerce the data into a dataframe
    unformatted_df = pd.DataFrame.from_dict(data, orient="columns")

    # verify the output
    # print(df)

    # Beging data cleaning
    """
    Currently the dataframe exists in the following format:

                                                        co2
    0     {'year': '2011', 'month': '1', 'day': '1', 'cy...
    1     {'year': '2011', 'month': '1', 'day': '2', 'cy...
    2     {'year': '2011', 'month': '1', 'day': '3', 'cy...
    3     {'year': '2011', 'month': '1', 'day': '4', 'cy...
    4     {'year': '2011', 'month': '1', 'day': '5', 'cy...

    This is not optimal, I want to rearrange the data so that the keys of each dictionary/json
    object are dataframe columns corresponding to their associated values. 
    """

    # rearrange the data
    df = pd.DataFrame(unformatted_df["co2"].values.tolist())

    # Now you can see the dataframe is more suited for manipulation
    """
          year month day   cycle   trend
    0     2011     1   1  391.25  389.75
    1     2011     1   2  391.29  389.76
    2     2011     1   3  391.32  389.77
    3     2011     1   4  391.36  389.77
    4     2011     1   5  391.39  389.78
    ...    ...   ...  ..     ...     ...
    3743  2021     4   1  416.28  414.44
    3744  2021     4   2  416.29  414.45
    3745  2021     4   3  416.30  414.46
    3746  2021     4   4  416.32  414.46
    3747  2021     4   5  416.33  414.47
    """

    # Check the dataframe for any null or duplicate values

    # rows with missing data
    rows_null_data = df[df.isnull()]

    # the sum null values in a specific row (replace with any column from dataframe)
    sum_rows_null_data = df["trend"].isnull().sum()

    # check for NaN under single column (replace with any column from dataframe)
    nan_column = df["trend"].isnull().values.any()
    # print(nan_column)

    """
    The global warming dataset I have chosen has already been cleaned, and appears to be in good condition. 
    For the sake of fulfilling the milestone requirements of the project, I will demonstrate some data cleansing
    best practices with a datasets that is better suited for the same:

    Dataset: Iris Species

    Classify iris plants into three species in this classic dataset
    
    https://www.kaggle.com/uciml/iris
    """

    # This data is from a CSV import, the file can be found in the data folder of the project repo.
    # import the csv file:
    iris_species = pd.read_csv("data/iris.csv")
    iris_species_dataframe = pd.DataFrame(iris_species)

    # get the number of distinct values in a column, in this case the number of different species in the species column
    distinct_species = iris_species_dataframe["Species"].value_counts()
    print(distinct_species)


# python specific, allows explicit call
if __name__ == "__main__":
    main()
