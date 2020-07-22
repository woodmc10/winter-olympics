import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CleanDataFrame(object):
    '''Takes a list of file names from the data/ folder and cleans them
    to compile a single, multicountry dataframe containing the given
    human development indicators for the given years. '''

    def __init__ (self, file_list, codes_list, years_list):
        self.files = file_list
        self.codes = codes_list
        self.years = years_list
        self.indicator_dict = None
        self.df = self.compile()

    def create_country_df(self, file):
        df = pd.read_csv('../data/' + file + '.csv')
        country = df.loc[0, '#country+name']
        table = pd.pivot_table(df, values='#indicator+value+num', 
                                index=['#country+name', '#date+year'], 
                                columns='#indicator+code', 
                                aggfunc=np.sum)
        if self.indicator_dict == None:
            self.create_dict(df)
        women_df = table[self.codes]
        women_years_df = women_df.loc[(country, self.years),]
        women_years_df.reset_index(inplace=True)
        return women_years_df

    def compile(self):
        for i, elem in enumerate(self.files):
            if i == 0: 
                self.df = self.create_country_df(elem).copy()
            else:
                multi_df = self.df
                new_df = self.create_country_df(elem)
                self.df = multi_df.append(new_df, ignore_index=True)
        return self.df

    def create_dict(self, df):
        self.indicator_dict = df.set_index('#indicator+code').to_dict()['#indicator+name']

if __name__ == '__main__':
    female_indicator_codes = [23906, 24106, 48706, 49006, 120606, 
                                123306, 123506, 136906, 169706, 169806, 
                                175106, 31706, 36806]
    files = ['usa', 'germany', 'canada', 'austria', 'norway', 'russia',
            'netherlands', 'switzerland', 'italy', 'france', 'sweden']
    years = [2014, 2016]
    multi_country_hdi_df = CleanDataFrame(files, female_indicator_codes, years).df
    print(multi_country_hdi_df.info())
    