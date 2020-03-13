from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import plot_model

import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling


# Parse data in Pandas dataframes
column_names = ["feature_no","date","site_name","daily_mean_pm_2_5_concentration","state",
                "station_name","elevation","latitude","longitude","mtd_prcp_normal","mtd_snow_normal",
                "ytd_prcp_normal","ytd_snow_normal","dly_tavg_normal","dly_dutr_normal","dly_tmax_normal",
                "dly_tmin_normal","aod_value47","aod_value55","mtd_prcp_normal_lag","mtd_snow_normal_lag",
                "day_of_week","weekday","season"

]
raw_dataset = pd.read_csv("../../data/merged/all_w_aod.csv", header=0)

dataset = raw_dataset.copy()
print(dataset.tail())
refinedData = pd.DataFrame([dataset.pop(x) for x in ["daily_mean_pm_2_5_concentration",
                "elevation","latitude","longitude","mtd_prcp_normal","mtd_snow_normal",
                "dly_tavg_normal","dly_dutr_normal"
                ,"aod_value47","aod_value55","mtd_prcp_normal_lag","mtd_snow_normal_lag",
                "day_of_week","weekday","season"
]]).T

# Split dataframes into training set and testing set
# Index range specifies the state that we're selecting
testing_indices = [i for i in range(13615,16830)]
train_dataset = refinedData.drop(testing_indices)
test_dataset = refinedData.drop(train_dataset.index)

# Remove all NAs
train_dataset = train_dataset.dropna()
test_dataset = test_dataset.dropna()

# Plot pm 2.5 vs. average daily temp for funsies
plt.scatter(test_dataset[["dly_tavg_normal"]],test_dataset[["daily_mean_pm_2_5_concentration"]])
plt.xlabel("Average Daily Temp")
plt.ylabel("Mean PM 2.5 ($\mu$g/$m^3$)")
plt.show()

# Split off the dependent variable (pm 2.5 concentration) column
train_stats = refinedData.describe()
train_stats.pop("daily_mean_pm_2_5_concentration")
train_stats = train_stats.transpose()
train_labels = train_dataset.pop('daily_mean_pm_2_5_concentration')
test_labels = test_dataset.pop('daily_mean_pm_2_5_concentration')


# Normalize our data to make convergence faster and possible
def norm(x):
  return (x - train_stats['mean']) / train_stats['std']
normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)
print(normed_test_data.tail())

# Build the neural network itself
def build_model():
  model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model

model = build_model()

model.summary()

# specify how many epochs to train for
EPOCHS = 4123
#early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

# start the training
history = model.fit(
  normed_train_data, train_labels,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
  callbacks=[tfdocs.modeling.EpochDots()])

# Looking at the training history as a function of epochs
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()

plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)

plotter.plot({'Basic': history}, metric = "mae")
plt.ylim([0, 7])
plt.ylabel('MAE')
plt.show()

plotter.plot({'Basic': history}, metric = "mse")
plt.ylim([0, 25])
plt.ylabel('MSE')
plt.title('Tampa Bay')
plt.show()
test_predictions = model.predict(normed_test_data).flatten()

# Look at how well our model predicts
a = plt.axes(aspect='equal')
plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values of PM 2.5')
plt.ylabel('Predicted Values of PM 2.5')
plt.title('Tampa Bay')
lims = [0, 50]
plt.xlim(lims)
plt.ylim(lims)
_ = plt.plot(lims, lims)
plt.show()