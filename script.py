import pandas as pd
import matplotlib.pyplot as plt
from utilities import *


def main():

    """
    ==================================================================================================================
    Importing CO2 data from the https://global-warming.org/ API
    Url is: https://global-warming.org/api/co2-api
    ==================================================================================================================
    """

    util = Utility()
    data = util.fetch_data_from_api("https://global-warming.org/api/co2-api")
    unformatted_co2_df = pd.DataFrame.from_dict(data, orient="columns")

    """
    Currently the imported data exists in the dataframe in the following format:

                                                        co2
    0     {'year': '2011', 'month': '1', 'day': '1', 'cy...
    1     {'year': '2011', 'month': '1', 'day': '2', 'cy...
    2     {'year': '2011', 'month': '1', 'day': '3', 'cy...
    3     {'year': '2011', 'month': '1', 'day': '4', 'cy...
    4     {'year': '2011', 'month': '1', 'day': '5', 'cy...

    This is not optimal, I want to reshape the data so that the keys of each dictionary/json
    object are dataframe columns corresponding to their associated values. 
    ==================================================================================================================
    """

    # reshape the data
    co2_df = pd.DataFrame(unformatted_co2_df["co2"].values.tolist())

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

    # get the shape of the dataframe:
    # print(df.shape)
    """
    Output: 
    (3752, 5)
    3752 rows and 5 columns
    """

    # Check the dataframe for any null or duplicate values:

    # rows with missing data
    rows_null_data = co2_df[co2_df.isnull()]

    """
    Get the sum of all null values in a specific row (replace with any column from dataframe).
    Instead of manually assigning each column name and checking individually, I used a utility function 'check_rows_null_values()'.
    The function will use a for loop to iterate over a list of column names contained in the dataframe, 
    and return a count for the number of null values in each columns corresponding rows. 
    """

    util = Utility(co2_df)  # init utility class with dataframe
    columns_list = util.check_rows_null_values(
        co2_df.columns
    )  # call check_rows_null_values()

    # (optional) for ease of use, convert the list of dict again to a dataframe to get a report of the findings:
    null_row_value_report = pd.DataFrame(columns_list)
    # print(null_row_value_report.to_string(index=False))

    """
    CO2 dataframe ready for use:
    """
    co2_dataframe = co2_df

    """
    ==================================================================================================================
    Importing Temperature data from the https://global-warming.org/ API
    Url is: https://global-warming.org/api/temperature-api
    ==================================================================================================================
    """

    util = Utility()
    data = util.fetch_data_from_api("https://global-warming.org/api/temperature-api")
    unformatted_temp_df = pd.DataFrame.from_dict(data, orient="columns")

    # reshape the data
    temp_df = pd.DataFrame(unformatted_temp_df["result"].values.tolist())
    print("temp_df")
    print(temp_df)

    """
    ==================================================================================================================
    Dataset cleaning:
    ==================================================================================================================
    The global warming dataset I have chosen has already been cleaned, and appears to be in good condition. 
    For the sake of fulfilling the milestone requirements of the project, I will demonstrate some data cleansing
    best practices with a datasets that is better suited for the same:

    Dataset: Iris Species

    Classify iris plants into three species in this classic dataset
    
    https://www.kaggle.com/uciml/iris
    ==================================================================================================================
    """

    # This data is from a CSV import, the file can be found in the data folder of the project repo.
    # import the csv file:
    iris_species = pd.read_csv("data/iris.csv")
    iris_species_dataframe = pd.DataFrame(iris_species)

    # get the number of distinct values in a column, in this case the number of different species in the species column
    distinct_species = iris_species_dataframe["Species"].value_counts()

    """
    Output: 

    Iris-setosa        50
    Iris-versicolor    50
    Iris-virginica     50
    """

    # visually represent this breakdown on a bar-chart:

    # create the x-labels for the graph
    distinct_species_x_labels_unformatted = list(distinct_species.index)
    distinct_species_y_labels_unformatted = list(distinct_species.values)

    # iterate over the list and remove the 'Iris-' part of the string, it is not needed
    # store the new formatted values in a new list called 'distinct_species_x_labels_formatted.

    distinct_species_x_labels_formatted = []

    for item in distinct_species_x_labels_unformatted:
        distinct_species_x_labels_formatted.append(item.split("-")[-1])

    bar_chart = plt.bar(
        distinct_species_x_labels_formatted,
        distinct_species_y_labels_unformatted,
        color=["cyan", "magenta", "royalblue"],
    )
    # plt.show()

    # observe the different variable types in the dataframe
    """
    print(iris_species_dataframe.dtypes)

    output:

    Id                 int64
    SepalLengthCm    float64
    SepalWidthCm     float64
    PetalLengthCm    float64
    PetalWidthCm     float64
    Species           object
    dtype: object

    """

    # get the number of na values per column:
    nan_values_per_column = iris_species_dataframe.isna().sum()
    """
    Output:
    
    Id               0
    SepalLengthCm    0
    SepalWidthCm     0
    PetalLengthCm    0
    PetalWidthCm     0
    Species          0
    dtype: int64
    """


# python specific, allows explicit call
if __name__ == "__main__":
    main()
