'''module for reading and handling training and test data'''
from abc import ABC, abstractmethod

import pandas as pd
import numpy as np


class DataLoader(ABC):
    '''reading and handling data'''
    @staticmethod
    def series_to_ndarray(ser):
        '''converting Series to NdArray'''
        return np.array(ser.array)

    @staticmethod
    def load_data_pd(filename):
        '''loading data in pandas DataFrame format'''
        return pd.read_csv(filename, '\t')

    @staticmethod
    def df_to_ndarray(df: pd.DataFrame):
        return df.values

    @staticmethod
    @abstractmethod
    def prepare_to_predict_subject(df: pd.DataFrame, subj_name):
        pass


class NeuralDataLoader(DataLoader):
    @staticmethod
    def prepare_to_predict_subject(df: pd.DataFrame, subj_name):
        df.drop("ФИО", axis=1, inplace=True)
        subj = df[subj_name]
        df.drop(subj_name, axis=1, inplace=True)
        return df.values, DataLoader.series_to_ndarray(subj)


class RegrDataLoader(DataLoader):
    @staticmethod
    def df_to_ndarray(df: pd.DataFrame):
        columns_names = df.columns.values
        return np.array([DataLoader.series_to_ndarray(df[i]) for i in columns_names])

    @staticmethod
    def prepare_to_predict_subject(df: pd.DataFrame, subj_name):
        df.drop("ФИО", axis=1, inplace=True)
        subj = df[subj_name]
        df.drop(subj_name, axis=1, inplace=True)
        return RegrDataLoader.df_to_ndarray(df), RegrDataLoader.series_to_ndarray(subj)


