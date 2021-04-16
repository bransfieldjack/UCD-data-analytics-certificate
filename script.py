import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utilities import *


def main():

    """
    ==================================================================================================================
    Importing CO2 data from the https://global-warming.org/ API
    Url is: https://global-warming.org/api/co2-api
    ==================================================================================================================
    """

    data = Utility().fetch_data_from_api("https://global-warming.org/api/co2-api")
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
    co2_df["year"] = co2_df["year"].astype(float).astype(int)

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
    ==================================================================================================================
    Importing Temperature data from the https://global-warming.org/ API
    Url is: https://global-warming.org/api/temperature-api
    ==================================================================================================================
    """

    data = Utility().fetch_data_from_api(
        "https://global-warming.org/api/temperature-api"
    )
    unformatted_temp_df = pd.DataFrame.from_dict(data, orient="columns")

    # reshape the data
    temp_df = pd.DataFrame(unformatted_temp_df["result"].values.tolist())

    # the temperature data has a data range from years 1880 - 2021, but I am only interested in from 2011 onwards, similar to the co2 data.
    # convert all values in the time column to type int.
    temp_df["time"] = temp_df["time"].astype(float).astype(int)

    # to see how many values exist for each year in the dataframe:
    months_per_year = Utility(temp_df).get_row_value_counts("time")

    # greater than the start date and smaller than the end date
    time_filter = (temp_df["time"] >= 2011) & (temp_df["time"] <= 2021)

    # the final (usable) temperature dataframe after formatting:
    temp_df = temp_df.loc[time_filter]
    temp_df.rename(columns={"time": "year"}, inplace=True)

    """
    Merge both the co2 dataframe and the temperature dataframes:
    """

    dataframes_merged = pd.merge(co2_df, temp_df)

    # remove unsued columns (month & day)
    del dataframes_merged["month"]
    del dataframes_merged["day"]

    # reset the dataframe index
    reindexed_final_df = dataframes_merged

    # reuse of utility function to see how many unique values exist for each year in the dataframe:
    uniq_values_per_year = Utility(reindexed_final_df).get_row_value_counts("year")
    """
    Output: 

          cycle  trend  station  land
    year                             
    2011   4380   4380     4380  4380
    2012   4392   4392     4392  4392
    2013   4380   4380     4380  4380
    2014   4380   4380     4380  4380
    2015   4380   4380     4380  4380
    2016   4392   4392     4392  4392
    2017   4380   4380     4380  4308
    2018   4380   4380     4380  4380
    2019   4380   4380     4380  4380
    2020   4392   4392     4392  4392
    2021    200    200      200   200
    """

    print(reindexed_final_df)
    # get the average C02 trend level for each year.
    unique_years = reindexed_final_df["year"].unique()
    years_averages_co2 = []

    # for every year, get the average occuring values
    for year in unique_years:
        averages = reindexed_final_df.loc[reindexed_final_df["year"] == year, "trend"]
        float_list = [float(i) for i in averages.to_list()]
        int_list = [int(i) for i in float_list]
        years_averages_co2.append(list(set(int_list)))

    # get the mean c02 values per year
    mean_per_year = []
    for i in years_averages_co2:
        mean = Utility.Average(i)
        mean_per_year.append(mean)

    # plot C02 levels with line
    # plt.plot(mean_per_year, unique_years, color="red")
    # plt.xlabel("C02 ppm (parts per million)")
    # plt.show()

    # perform the same task for the temperature increase
    station_averages = []
    for year in unique_years:
        station_averages = reindexed_final_df.loc[
            reindexed_final_df["year"] == year, "station"
        ]

        # get the mean station values per year
        mean_station_per_year = []
        for i in station_averages.to_list():
            print(i)

        # plot station temperature increase levels with line
        # plt.plot(mean_station_per_year, unique_years, color="orange")
        # plt.xlabel("Temperature increase")
        # plt.show()

    # """
    # ==================================================================================================================
    # Dataset cleaning:
    # ==================================================================================================================
    # The global warming dataset I have chosen has already been cleaned, and appears to be in good condition.
    # For the sake of fulfilling the milestone requirements of the project, I will demonstrate some data cleansing
    # best practices with a datasets that is better suited for the same:

    # Dataset: Iris Species

    # Classify iris plants into three species in this classic dataset

    # https://www.kaggle.com/uciml/iris
    # ==================================================================================================================
    # """

    # # This data is from a CSV import, the file can be found in the data folder of the project repo.
    # # import the csv file:
    # iris_species = pd.read_csv("data/iris.csv")
    # iris_species_dataframe = pd.DataFrame(iris_species)

    # # get the number of distinct values in a column, in this case the number of different species in the species column
    # distinct_species = iris_species_dataframe["Species"].value_counts()

    # """
    # Output:

    # Iris-setosa        50
    # Iris-versicolor    50
    # Iris-virginica     50
    # """

    # # visually represent this breakdown on a bar-chart:

    # # create the x-labels for the graph
    # distinct_species_x_labels_unformatted = list(distinct_species.index)
    # distinct_species_y_labels_unformatted = list(distinct_species.values)

    # # iterate over the list and remove the 'Iris-' part of the string, it is not needed
    # # store the new formatted values in a new list called 'distinct_species_x_labels_formatted.

    # distinct_species_x_labels_formatted = []

    # for item in distinct_species_x_labels_unformatted:
    #     distinct_species_x_labels_formatted.append(item.split("-")[-1])

    # bar_chart = plt.bar(
    #     distinct_species_x_labels_formatted,
    #     distinct_species_y_labels_unformatted,
    #     color=["cyan", "magenta", "royalblue"],
    # )
    # # plt.show()

    # # observe the different variable types in the dataframe
    # """
    # print(iris_species_dataframe.dtypes)

    # output:

    # Id                 int64
    # SepalLengthCm    float64
    # SepalWidthCm     float64
    # PetalLengthCm    float64
    # PetalWidthCm     float64
    # Species           object
    # dtype: object

    # """

    # # get the number of na values per column:
    # nan_values_per_column = iris_species_dataframe.isna().sum()
    # """
    # Output:

    # Id               0
    # SepalLengthCm    0
    # SepalWidthCm     0
    # PetalLengthCm    0
    # PetalWidthCm     0
    # Species          0
    # dtype: int64
    # """


# python specific, allows explicit call
if __name__ == "__main__":
    main()
