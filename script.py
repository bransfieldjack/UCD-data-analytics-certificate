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

    # perform the same task for the temperature increase
    mean_station_averages = []
    for year in unique_years:
        station_averages = reindexed_final_df.loc[
            reindexed_final_df["year"] == year, "station"
        ]
        float_list = [float(i) for i in station_averages.to_list()]
        unique_values = list(set(float_list))

        mean = Utility.Average(unique_values)
        mean_temperateure_rounded = round(mean, 2)
        mean_station_averages.append(mean_temperateure_rounded)

    """
    ==================================================================================================================
    Begin correlation between temperature C02 rise and growth in global energy demand
    CSV obtained from data.worldbank.org
    https://data.worldbank.org/indicator/EG.USE.PCAP.KG.OE?end=2015&start=2015&view=bar
    ==================================================================================================================
    """

    energy_data = pd.read_csv("data/energy.csv")
    energy_dataframe = pd.DataFrame(energy_data)

    # rename 'entity' column to country
    energy_dataframe.rename(columns={"Entity": "Country"}, inplace=True)

    # distinct country names:
    world_dataframe = energy_dataframe[energy_dataframe["Country"] == "World"]

    # filter to only return rows beginning from 2011
    energy_filtered_for_time = world_dataframe[world_dataframe["Year"] >= 2011]

    # utility checks:
    util = Utility(energy_filtered_for_time)  # init utility class with dataframe
    columns_list = util.check_rows_null_values(
        energy_filtered_for_time.columns
    )  # call check_rows_null_values()

    # output:
    """
    [{'Name': 'Country', 'Null counts': 0}, 
    {'Name': 'Code', 'Null counts': 201}, 
    {'Name': 'Year', 'Null counts': 0}, 
    {'Name': 'Primary energy consumption (TWh)', 'Null counts': 0}]
    """

    # dropping 'Code' & 'Country' - column, not required
    del energy_filtered_for_time["Code"]
    del energy_filtered_for_time["Country"]

    year = energy_filtered_for_time["Year"]
    energy = energy_filtered_for_time["Primary energy consumption (TWh)"]

    """
    Plot all data here:
    """
    fig, axs = plt.subplots(3)

    # Co2 plot
    axs[0].scatter(unique_years, mean_per_year, color="red")
    m, b = np.polyfit(unique_years, mean_per_year, 1)  # linear regression line
    axs[0].plot(unique_years, m * unique_years + b)
    axs[0].set_title("C02 ppm (parts per million) 2011 - 2020")
    axs[0].set_ylabel("PPM")
    axs[0].set_xlabel("Years")

    # Temperature plot
    axs[1].scatter(unique_years, mean_station_averages, color="orange")
    m, b = np.polyfit(unique_years, mean_station_averages, 1)  # linear regression line
    axs[1].plot(unique_years, m * unique_years + b)
    axs[1].set_title("Temperature increase (Celcius) 2011 - 2020")
    axs[1].set_ylabel("Degrees Celsius")
    axs[1].set_xlabel("Years")

    # Energy plot
    axs[2].scatter(year, energy, color="purple")
    m, b = np.polyfit(year, energy, 1)  # linear regression line
    axs[2].plot(year, m * year + b)
    axs[2].set_title("Global Energy demand 2011 - 2019")
    axs[2].set_ylabel("Primary energy consumption (TWh)")
    axs[2].set_xlabel("Years")
    plt.show()

    # linear regression plot:


# python specific, allows explicit call
if __name__ == "__main__":
    main()
