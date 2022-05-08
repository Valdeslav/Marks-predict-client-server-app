import matplotlib.pyplot as plt

import data_handling

from app import console_interface
from neural_network import neural_network
from regr import regression

if __name__ == '__main__':
    console_interface()
    predictor = regression.RegressionPrediction()
    data_loader = data_handling.RegrDataLoader()
    #app(predictor, data_loader)


