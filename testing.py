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
    df = pd.DataFrame.from_dict(data, orient="columns")

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
    new_df = pd.DataFrame(df['co2'].values.tolist())

    print(new_df)

# python specific, allows explicit call
if __name__ == "__main__":
    main()
