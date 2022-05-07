from abc import ABC, abstractmethod


class Predictor(ABC):
    @abstractmethod
    def create_model(self, x, y):
        pass

    @abstractmethod
    def predict(self, x):
        pass
