import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Make numpy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing


def main():

    # print(tf.__version__)

    # import dataset
    url = "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
    column_names = [
        "MPG",
        "Cylinders",
        "Displacement",
        "Horsepower",
        "Weight",
        "Acceleration",
        "Model Year",
        "Origin",
    ]

    raw_dataset = pd.read_csv(
        url,
        names=column_names,
        na_values="?",
        comment="\t",
        sep=" ",
        skipinitialspace=True,
    )

    # clean the dataset
    dataset = raw_dataset.copy()
    dataset.isna().sum()
    dataset = dataset.dropna()

    """
    Since the origin column is categorical, its values need to be mapped, ex:
    1: 'USA', 2: 'Europe', 3: 'Japan'
    """
    dataset["Origin"] = dataset["Origin"].map({1: "USA", 2: "Europe", 3: "Japan"})

    dataset = pd.get_dummies(dataset, columns=["Origin"], prefix="", prefix_sep="")
    print(dataset.tail())

    """
    Now split the dataset into a training set and a test set.
    Use the test set in the final evaluation of our models.
    """

    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    sns.pairplot(
        train_dataset[["MPG", "Cylinders", "Displacement", "Weight"]], diag_kind="kde"
    )


if __name__ == "__main__":
    main()
