from tensorflow import keras
import numpy as np

from prediction import Predictor


class NeuralNetworkPredictor(Predictor):
    def __init__(self):
        self.model = None

    def create_model(self, train_all_subj_scores, train_targ_subj_scores):
        train_all_subj_scores = train_all_subj_scores / 10.0

        self.model = keras.Sequential([
            keras.layers.Flatten(input_shape=(len(train_all_subj_scores[0]),)),
            keras.layers.Dense(100, activation="relu"),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(100, activation="relu"),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(11, activation="softmax")
        ])
        self.model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                      metrics=["accuracy"])

        self.model.fit(train_all_subj_scores, train_targ_subj_scores, batch_size=20,
                  epochs=200, verbose=1)

    def predict(self, test_all_subj_scores):
        test_all_subj_scores / 10.0
        predictions = self.model.predict(test_all_subj_scores)
        predictions = [np.argmax(predictions[i]) for i in range(len(predictions))]
        return predictions
