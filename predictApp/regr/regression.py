import numpy as np
from sklearn.linear_model import LinearRegression

from predictApp.prediction import Predictor


class RegressionPrediction(Predictor):
    def __init__(self):
        self.model = None
        self.max_cor_index = None

    def __find_max_corelation(self, train_all_subj_scores, train_targ_subj_scores):
        cors = np.corrcoef(train_all_subj_scores, train_targ_subj_scores)[-1][:-1]
        self.max_cor_index = np.argmax(cors)
        return self.max_cor_index

    def create_model(self, train_all_subj_scores, train_targ_subj_scores):
        x = train_all_subj_scores[RegressionPrediction.__find_max_corelation(self, train_all_subj_scores, train_targ_subj_scores)]
        x = x.reshape((-1, 1))
        self.model = LinearRegression().fit(x, train_targ_subj_scores)  # Модель регрессии

    def score(self, x, y):
        return self.model.score(x, y)

    def predict(self, x):
        x = x[self.max_cor_index]
        x = x.reshape((-1, 1))
        return self.model.predict(x)

