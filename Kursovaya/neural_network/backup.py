import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

from data_handling import DataLoader

data = DataLoader.load_data_pd('../data/marks.tsv')
test_data = DataLoader.load_data_pd('../data/test.tsv')
#names = test_data['ФИО']

train_all_subj_scores, train_targ_subj_scores = DataLoader.prepare_to_predict_subject(data, 'МоиАПР')
test_all_subj_scores, test_targ_subj_scores = DataLoader.prepare_to_predict_subject(test_data, 'МоиАПР')

train_all_subj_scores = train_all_subj_scores / 10.0
test_all_subj_scores = test_all_subj_scores / 10.0


model = keras.Sequential([
    keras.layers.Flatten(input_shape=(len(train_all_subj_scores[0]), )),
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(11, activation="softmax")
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(train_all_subj_scores, train_targ_subj_scores, batch_size=20, epochs=200, verbose=1)

test_loss, test_acc = model.evaluate(test_all_subj_scores, test_targ_subj_scores)

print('\nTest accuracy:', test_acc)

predictions = model.predict(test_all_subj_scores)

for i in range(5):
    #print(f'{names[i]}:\t{np.argmax(predictions[i])}')
    print(f'{np.argmax(predictions[i])}')
