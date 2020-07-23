import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class PipelineHDI(object):
    '''Takes file_list of file names from the data/ folder and cleans them
    to compile a single, multicountry dataframe containing the human
    development indicators from the codes_list limited to the years in
    the years_list

    Parameters
    ----------
    file_list: list
        list of all files to add to multi-country DataFrame
    codes_list: list
        list of HDI codes to include in multi-country DataFrame
    years_list: list
        list of years to include in multi-country DataFrame

    Returns
    -------
    files: list
        list of all files used to create multi-country DataFrame
    codes: list
        list of all codes included in multi-country DataFrame
    year: list
        list of all years included in multi-country DataFrame
    indicator_dict: dict
        dictionary with all HDI codes as keys and the names associated
        with those codes as values
    df: pandas DataFrame
        DataFrame including the provided countries and HDI codes for
        the provided years
    '''

    def __init__(self, file_list, codes_list, years_list):
        self.files = file_list
        self.codes = codes_list
        self.years = years_list
        self.indicator_dict = None
        self.df = self.create_multi_country()

    def create_country_df(self, file):
        '''Creates the country DataFrame from a single file by creating
        a pandas PivotTable with the indicator values, codes, and names
        and the year and country. Then reduces the DataFrame to only
        include HDI codes in self.cdes
        '''
        df = pd.read_csv('../data/' + file)
        country = df.loc[0, '#country+name']
        table = pd.pivot_table(df, values='#indicator+value+num',
                               index=['#country+name', '#date+year'],
                               columns='#indicator+code',
                               aggfunc=np.sum)
        if self.indicator_dict is None:
            self.create_dict(df)
        women_df = table[self.codes]
        women_years_df = women_df.loc[(country, self.years), ]
        women_years_df.reset_index(inplace=True)
        return women_years_df

    def create_multi_country(self):
        '''Create the multi-country HDI DataFrame by looping through
        all files in self.files and appending each to the end of the
        DataFrame
        '''
        for i, elem in enumerate(self.files):
            if i == 0:
                self.df = self.create_country_df(elem).copy()
            else:
                multi_df = self.df
                new_df = self.create_country_df(elem)
                self.df = multi_df.append(new_df, ignore_index=True)
        return self.df

    def create_dict(self, df):
        '''Create a dictionary with #indicator+code as keys and
        #indicator+name as values
        '''
        self.indicator_dict = df.set_index('#indicator+code').to_dict()[
            '#indicator+name']


if __name__ == '__main__':
    female_indicator_codes = [23906, 24106, 48706, 49006, 120606,
                              123306, 123506, 136906, 169706, 169806,
                              175106, 31706, 36806]
    files = ['usa', 'germany', 'canada', 'austria', 'norway', 'russia',
             'netherlands', 'switzerland', 'italy', 'france', 'sweden']
    years = [2014, 2016]
    multi_country_hdi_df = PipelineHDI(files,
                                       female_indicator_codes, years).df
    print(multi_country_hdi_df.info())
