import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
import medals_plots
from hdi import PipelineHDI

plt.style.use('tableau-colorblind10')


class GenderDataFrames(object):
    '''A data cleaning pipeline to take Olympic data including country,
    medal, gender, sport, event and year information and create
    DataFrames grouped by year or country for comparing men vs women in
    event numbers and medals by country

    Parameters
    ----------
    file: str
        file containing olympic medal information
    season: str
        season of the olympic data
    noc_code_dict: dict
        dictionary with NOC codes as the keys and country names as the
        values

    Returns
    -------
    file: str
        file containing olympic medal information
    noc_code_dict: dict
        dictionary with NOC codes as the keys and country names as the
        values
    season: str
        season of the olympic data
    original_df: pandas DataFrame
        DataFrame after removing uncessary columns and one hot incoding
        the Gender column
    athlete_df: pandas DataFrame
        DataFrame containing the athlete information before removing
        athletes that did not win medals
    annual_medals_df: pandas DataFrame
        DataFrame grouped by year, ignoring mixed gender events, with
        the percent womens events calculated
    annual_medals_mixed df: pandas DataFrame
        DataFrame grouped by year, including mixed gender events, with
        the percent womens events calculated
    country_medals_df: pandas DataFrame
        DataFrame grouped by country, ignoring mixed gender events,
        with the percent womens medals calculated for years 1994 and
        after and excluding countries with less than 50 medals
    country_medals_mixed_df: pandas DataFrame
        DataFrame grouped by country, including mixed gender events,
        with the percent womens medals calculated for years 1994 and
        after and excluding countries with less than 50 medals
    '''

    def __init__(self, file, season, noc_code_dict):
        self.file = file
        self.noc_code_dict = code_dict
        self.season = season
        self.original_df = self.create_df()
        self.athlete_df = None
        self.annual_medals_df = self.create_year_df(ignore_mixed=True)
        self.annual_medals_mixed_df = self.create_year_df(ignore_mixed=False)
        self.country_medals_df = self.create_country_df(min_year=1994,
                                                        min_medals=50,
                                                        ignore_mixed=True)
        self.country_medals_mixed_df =\
            self.create_country_df(min_year=1994, min_medals=50,
                                   ignore_mixed=False)

    def create_df(self):
        '''Import the file into a pandas DataFrame, remove uncessary
        columns, and one hot encode the Genders
        '''
        if self.season == 'winter':
            df = pd.read_excel(self.file)
            df.drop(['Medal Rank', 'Age of Athlete'], axis=1, inplace=True)
            df = pd.get_dummies(df, columns=['Gender'])
            return df
        else:
            df = pd.read_csv(self.file)
            df = self.country_codes(df)
            df.drop(['Name', 'Age', 'Height', 'Weight', 'Team', 'Games',
                     'Season', 'City', 'NOC'], axis=1, inplace=True)
            df.rename(columns={'Sex': 'Gender'}, inplace=True)
            self.athlete_df = df.copy()
            df.drop(['ID'], axis=1, inplace=True)
            df.dropna(subset=['Medal'], inplace=True)
            df = pd.get_dummies(df, columns=['Gender'])
            df.rename(columns={'Gender_M': 'Gender_Men',
                               'Gender_F': 'Gender_Women'}, inplace=True)
            return df

    def create_year_df(self, ignore_mixed=True):
        '''Create a DataFrame grouped by Year'''
        cols_list = ['mens_events', 'womens_events', 'mixed_events']
        if ignore_mixed:
            cols_list.pop()
        year_df = self.original_df.groupby(['Year',
                                            'Sport', 'Event']).sum().copy()
        if self.season == 'winter':
            year_df['mixed_events'] = np.where(year_df['Gender_Mixed'] > 0,
                                               1, 0)
        else:
            year_df['mixed_events'] = np.where(year_df['Gender_Women'] > 0,
                                               np.where(year_df['Gender_Men']
                                                        > 0, 1, 0), 0)
        year_df['mens_events'] = np.where(year_df['Gender_Men'] > 0, 1, 0)
        year_df['womens_events'] = np.where(year_df['Gender_Women'] > 0, 1, 0)
        year_df = year_df[cols_list]
        year_df.reset_index(inplace=True)
        year_events_df = year_df.groupby('Year').sum()
        year_events_df['total_events'] = year_events_df[cols_list]\
            .sum(axis=1)
        cols_list.remove('mens_events')
        year_events_df['%_womens_events'] =\
            (year_events_df[cols_list].sum(axis=1) /
             year_events_df['total_events']) * 100
        return year_events_df

    def create_country_df(self, min_year, min_medals, ignore_mixed=True):
        '''Create a DataFrame grouped by Country'''
        cols_list = ['mens_medals', 'womens_medals', 'mixed_medals']
        if ignore_mixed:
            cols_list.pop()
        filter_df = self.original_df[self.original_df['Year'] >= min_year]
        if self.season != 'winter':
            filter_df = self.reduce_medal_count(filter_df)
        country_df = filter_df.groupby('Country').sum()
        country_df.rename(columns={'Gender_Men': 'mens_medals',
                                   'Gender_Women': 'womens_medals',
                                   'Gender_Mixed': 'mixed_medals'},
                          inplace=True)
        country_df = country_df[cols_list]
        country_df['total_medals'] = country_df[cols_list].sum(axis=1)
        cols_list.remove('mens_medals')
        country_df['%_womens_medals'] = (country_df[cols_list].sum(axis=1) /
                                         country_df['total_medals']) * 100
        over_df = country_df[country_df['total_medals'] >= min_medals]
        sorted_df = over_df.sort_values(by='womens_medals', ascending=False)\
            .copy()
        return sorted_df

    def reduce_medal_count(self, df):
        '''Normalize the medal count in data other that contains a list
        of medals by athlete instead of event. Reduce the medal count
        to one medal per country per event to avoid biasing results to
        team events
        '''
        medals_total_df = df.groupby(['Country', 'Year',
                                      'Sport', 'Event']).sum()
        medals_total_df['Gender_Mixed']\
            = np.where(medals_total_df['Gender_Men'] > 0,
                       np.where(medals_total_df['Gender_Women'] > 0, 1, 0), 0)
        medals_total_df['Gender_Men']\
            = np.where(medals_total_df['Gender_Men'] > 0, 1, 0)
        medals_total_df['Gender_Women']\
            = np.where(medals_total_df['Gender_Women'] > 0, 1, 0)
        medals_total_df.reset_index(inplace=True)
        return medals_total_df

    def country_codes(self, df):
        '''Create a 'Country' column by comparing 'NOC' column with
        noc_code_dict
        '''
        df['Country'] = df['NOC'].map(self.noc_code_dict)
        return df


def make_all_plots(df_obj, save_on=False):
    '''Create all plots of interest for a GenderDataFrames object

    Parameters
    ----------
    df_obj: GenderDataFrames object
        an instance of the GenderDataFrames object that contains the
        seasons of interest
    save_on: bool, optional
        if true the plots will be saved, if false the plots will show
        on the screen (default is False)

    Return
    ------
    None
    '''

    medals_plots.plot_percent_year(df_obj, save_on)
    medals_plots.plot_bar_year_dual(df_obj, save_on)
    medals_plots.plot_bar_country(df_obj, save_on)
    if not save_on:
        plt.show()


def correlation(codes, year, df_obj):
    '''Create a dataframe containing the HDI data from multiple countries.
    Pulls in every .csv file in the ../data folder which is just the HDI
    exports for 30 different countries

    Parameters
    ----------
    codes: list
        list of HDI codes to filter dataframe
    year: int
        (either 2014 or 2016) filter HDI codes for this year
    df_obj: GenderDataFrames
        an instance of the GenderDataFrames object that contains the
        percent of womens medals for the 20 years of interest

    Returns
    -------
    merge_dict_df: pandas DataFrame
        contains the HDI values and the % womens medals
    corr_df: pandas Series
        contains the correlations between each HDI and the % womens
        medals
    '''
    files = []
    for filename in os.listdir('../data'):
        if filename.endswith('csv'):
            files.append(filename)
    years = [2014, 2016]
    multi_country_hdi = PipelineHDI(files, codes, years)
    multi_2014_hdi_df = multi_country_hdi.df[multi_country_hdi.df
                                             ['#date+year'] == year]
    df_temp = df_obj.country_medals_df.copy()
    df_temp.reset_index(inplace=True)
    country_medals_dict = df_temp.set_index('Country')\
        .to_dict()['%_womens_medals']
    merge_dict_df = multi_2014_hdi_df.copy()
    merge_dict_df[f'{df_obj.season}_medals_%_women'] =\
        merge_dict_df['#country+name'].map(country_medals_dict)
    corr_df = merge_dict_df.corr()[f'{df_obj.season}_medals_%_women']
    return merge_dict_df, corr_df


def create_code_dict(file):
    '''Creates a dictionary with NOC codes as keys and country names as
    values

    Parameters
    ----------
    file (str): text file containing codes and country names

    Return
    ------
    code_dict (dict): dictionary of codes and country names
    '''
    f = open(file)
    codes = f.read()
    num = 0
    tab_split = codes.split('\t')
    code_dict = dict()
    for i, elem in enumerate(tab_split):
        if '\n' in elem and str(num) in elem:
            code = elem[-3:]
            country = tab_split[i + 1][1:]
            num += 1
            if code not in code_dict:
                code_dict[code] = country
    return code_dict


if __name__ == '__main__':
    code_dict = create_code_dict('../data/noc_codes.txt')
    winter_dataframes = GenderDataFrames('../data/winter-olympic-medals.xlsx',
                                         'winter', code_dict)
    all_olympics_dataframes = GenderDataFrames(
        '../data/summer_olympics/athlete_events.csv', 'all', code_dict
        )

    # make_all_plots(winter_dataframes, False)
    # make_all_plots(all_olympics_dataframes, False)
    medals_plots.plot_bar_year_overlay(all_olympics_dataframes,
                                       winter_dataframes, True)

    female_indicator_codes = [23906, 24106, 48706, 120606,
                              123306, 123506, 136906, 169706, 169806,
                              175106, 31706, 36806]
    all_olympics_hdi, all_olympics_corr = correlation(female_indicator_codes,
                                                      2016,
                                                      all_olympics_dataframes)
    winter_olympics_hdi, winter_corr = correlation(female_indicator_codes,
                                                   2014, winter_dataframes)

    hdi_list = [123506, 169706, 24106, 31706, 136906]
    labels_dict = {31706: 'Women in\nParlament', 123506:
                   'Female Gross\nNational Income', 136906: 'Female HDI',
                   24106: 'Mean Female\nSchooling', 169706:
                   'Unemployment\nFemale:Male'}
    # corr_ax = medals_plots.plot_hdi_corrs(hdi_list, winter_corr,
    #                                       labels_dict, 'winter',
    #                                       save_on=False)
    # medals_plots.plot_hdi_corrs(hdi_list, all_olympics_corr, labels_dict,
                                # 'all', corr_ax, save_on=True)

    x = all_olympics_hdi['all_medals_%_women']
    y = all_olympics_hdi[169706]
    label_list = ['Female GNI', '% Winter Olympic Medals']
    # medals_plots.scatter_corr(x, y, label_list,
                            #   save_as='../images/winter/GNI-scatter.png',
                            #   save_on=False)

    plt.show()
