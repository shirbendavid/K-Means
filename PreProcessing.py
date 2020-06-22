import pandas as pd
import numpy as np


class PreProcessing:
    df_header = []
    df = pd.DataFrame({})

    def __init__(self, data):
        self.df = data
        self.df_header = list(data)

    # clean the df
    def clean(self):
        self.fill_and_standardization()
        self.group_by_country()
        return self.df

    # fill missing values and normalize the data
    def fill_and_standardization(self):
        for col in self.df_header[2:]:
            self.df[col].fillna(self.df[col].mean(), inplace=True)
            mean = np.mean(self.df[col])
            std = np.std(self.df[col])
            self.df[col] = (self.df[col] - mean) / std

    # group by country
    def group_by_country(self):
        self.df = self.df.groupby('country').mean()
        del self.df['year']
