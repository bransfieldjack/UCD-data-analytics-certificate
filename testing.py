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
    print(type(data))

    # coerce the data into a dataframe
    df = pd.DataFrame.from_dict(data, orient="columns")

    print(df)


# python specific, allows explicit call
if __name__ == "__main__":
    main()
