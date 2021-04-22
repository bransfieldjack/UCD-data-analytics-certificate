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


class ClimateModelData:
    def __init__(self, dataset) -> None:
        self._dataset = dataset
        self._clean_data()

    def _clean_data(self):
        self._dataset.isna().sum()
        self._dataset = self._dataset.dropna()
        return self._dataset

    @property
    def get_dataset(self) -> None:
        return self._dataset


class TensorFlowProcessing:
    def __init__(self, dataset) -> None:
        self._dataset = dataset
        self._process()

    def _process(self) -> None:

        # Tensorflow version
        print(tf.__version__)

        # import processed dataset:
        data = ClimateModelData(self._dataset)
        dataset = data.get_dataset

        print(dataset)

        """
        Split the dataset into a training and test.
        Use the test set in the final evaluation.
        """

        train_dataset = dataset.astype(float).sample(frac=0.8, random_state=0)
        test_dataset = dataset.astype(float).drop(train_dataset.index)

        # print(" test_dataset ")
        # print(test_dataset)

        # print(" train dataset ")
        # print(train_dataset)

        # print(train_dataset.describe().transpose())

        train_features = train_dataset.copy()
        test_features = test_dataset.copy()

        train_labels = train_features.pop("trend")
        test_labels = test_features.pop("trend")

        # print(train_dataset.describe().transpose()[["mean", "std"]])

        normalizer = preprocessing.Normalization()

        normalizer.adapt(np.array(train_features))

        mean_and_variance = normalizer.mean.numpy()

        first = np.array(train_features[:1])

        # with np.printoptions(precision=2, suppress=True):
        #     print("First example:", first)
        #     print()
        #     print("Normalized:", normalizer(first).numpy())

        energy_consumption = np.array(
            train_features["Primary energy consumption (TWh)"]
        )

        energy_consumption_normalizer = preprocessing.Normalization(
            input_shape=[
                1,
            ]
        )
        energy_consumption_normalizer.adapt(energy_consumption)

        energy_consumption_model = tf.keras.Sequential(
            [energy_consumption_normalizer, layers.Dense(units=1)]
        )

        energy_consumption_model.summary()

        """
        This model should predict C02 from energy consumption.
        """

        # Run the untrained model on the first 10 energy values
        energy_consumption_model.predict(energy_consumption[:10])

        # configure the training procedure
        energy_consumption_model.compile(
            optimizer=tf.optimizers.Adam(learning_rate=0.1), loss="mean_absolute_error"
        )

        # execute the training
        history = energy_consumption_model.fit(
            train_features["Primary energy consumption (TWh)"],
            train_labels,
            epochs=100,
            # suppress logging
            verbose=0,
            # Calculate validation results on 20% of the training data
            validation_split=0.2,
        )

        # hist = pd.DataFrame(history.history)
        # hist["epoch"] = history.epoch
        # hist.tail()

        # def plot_loss(history):
        #     plt.plot(history.history["loss"], label="loss")
        #     plt.plot(history.history["val_loss"], label="val_loss")
        #     plt.ylim([0, 10])
        #     plt.xlabel("Epoch")
        #     plt.ylabel("Error [MPG]")
        #     plt.legend()
        #     plt.grid(True)

        # plot_loss(history)

        # Collect the results on the test set, for later:

        test_results = {}

        test_results["energy_consumption_model"] = energy_consumption_model.evaluate(
            test_features["Primary energy consumption (TWh)"], test_labels, verbose=0
        )

        x = tf.linspace(0.0, 250, 251)
        y = energy_consumption_model.predict(x)

        def energy_consumption(x, y):
            plt.scatter(
                train_features["Primary energy consumption (TWh)"],
                train_labels,
                label="Data",
            )
            plt.plot(x, y, color="k", label="Predictions")
            plt.xlabel("Primary energy consumption (TWh)")
            plt.ylabel("C02")
            plt.legend()
            plt.show()

        # plot consumption vs c02 levels
        energy_consumption(x, y)
