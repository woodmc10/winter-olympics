import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import medals_plots
from hdi import CleanDataFrame
import noc_codes 

plt.style.use('tableau-colorblind10')

class GenderDataFrames(object):
    
    def __init__(self, file, season):
        self.file = file
        self.season = season
        self.original_df = self.create_df()
        self.athlete_df = None
        self.annual_medals_df = self.create_year_df(ignore_mixed=True)
        self.annual_medals_mixed_df = self.create_year_df(ignore_mixed=False) 
        self.country_medals_df = self.create_country_df(min_year=1994, 
                                                        min_medals=50, 
                                                        ignore_mixed=True)
        self.country_medals_mixed_df = self.create_country_df(min_year=1994, 
                                                            min_medals=50, 
                                                            ignore_mixed=False)
    
    def create_df(self):
        if self.season == 'winter':
            df = pd.read_excel(self.file)
            df.drop(['Medal Rank', 'Age of Athlete'], axis=1, inplace=True)
            df = pd.get_dummies(df, columns=['Gender'])
            return df
        else:
            df = pd.read_csv(self.file)
            df = self.country_codes(df)
            df.drop(['Name', 'Age', 'Height', 'Weight', 'Team', 'Games', 'Season', 'City', 'NOC'], 
                    axis=1, inplace=True)
            df.rename(columns={'Sex': 'Gender'}, inplace=True)
            self.athlete_df = df.copy()
            df.drop(['ID'], axis=1, inplace=True)
            df.dropna(subset=['Medal'], inplace=True)
            df = pd.get_dummies(df, columns=['Gender'])
            df.rename(columns={'Gender_M': 'Gender_Men', 'Gender_F': 'Gender_Women'}, inplace=True)
            return df

    def create_year_df(self, ignore_mixed=True):
        cols_list = ['mens_events', 'womens_events', 'mixed_events']
        if ignore_mixed:
            cols_list.pop() 
        year_df = self.original_df.groupby(['Year', 'Sport', 'Event']).sum().copy()
            # sum is automatically dropping object columns
        if self.season == 'winter':
            year_df['mixed_events'] = np.where(year_df['Gender_Mixed'] > 0, 1, 0)
        else:
            year_df['mixed_events'] = np.where(year_df['Gender_Women'] > 0, 
                                        np.where(year_df['Gender_Men'] > 0, 1, 0), 0)
        year_df['mens_events'] = np.where(year_df['Gender_Men'] > 0, 1, 0)
        year_df['womens_events'] = np.where(year_df['Gender_Women'] > 0, 1, 0)
        year_df = year_df[cols_list]
        year_df.reset_index(inplace=True)
        year_events_df = year_df.groupby('Year').sum()
        year_events_df['total_events'] = year_events_df[cols_list].sum(axis=1)
        cols_list.remove('mens_events')
        year_events_df['%_womens_events'] = (year_events_df[cols_list].sum(axis=1) / 
                                        year_events_df['total_events']) * 100
        return year_events_df

    def create_country_df(self, min_year, min_medals, ignore_mixed=True):
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
        country_df['total_medals'] =country_df[cols_list].sum(axis=1)
        cols_list.remove('mens_medals')
        country_df['%_womens_medals'] = (country_df[cols_list].sum(axis=1)/
                                        country_df['total_medals']) * 100
        over_df = country_df[country_df['total_medals'] >= min_medals]
        sorted_df = over_df.sort_values(by='womens_medals', ascending=False).copy()
        return sorted_df

    def reduce_medal_count(self, df):
        medals_total_df = df.groupby(['Country', 'Year', 'Sport', 'Event']).sum()
        medals_total_df['Gender_Mixed'] = np.where(medals_total_df['Gender_Men'] > 0, np.where(medals_total_df['Gender_Women'] >0, 1, 0), 0)
        medals_total_df['Gender_Men'] = np.where(medals_total_df['Gender_Men'] > 0, 1, 0)
        medals_total_df['Gender_Women'] = np.where(medals_total_df['Gender_Women'] > 0, 1, 0)
        medals_total_df.reset_index(inplace=True)
        return medals_total_df

    def country_codes(self, df):
        df['Country'] = df['NOC'].map(noc_codes.code_dict)
        return df

def do_all_plots(df_obj, save_on=False):
    medals_plots.plot_percent_year(df_obj, save_on)
    medals_plots.plot_bar_year(df_obj, save_on)
    medals_plots.plot_bar_country(df_obj, save_on)
    if not save_on:
        plt.show()

if __name__ == '__main__':
    winter_dataframes = GenderDataFrames('../data/winter-olympic-medals.xlsx', 'winter')
    all_olympics_dataframes = GenderDataFrames('../data/summer_olympics/athlete_events.csv', 'all')
    
    # do_all_plots(winter_dataframes, False)
    do_all_plots(all_olympics_dataframes, False)


    '''
    #Combine data frames from hdi with winter olympic medals (1994 on)
    female_indicator_codes = [23906, 24106, 48706, 49006, 120606, 
                                123306, 123506, 136906, 169706, 169806, 
                                175106, 31706, 36806]
    files = ['usa', 'germany', 'canada', 'austria', 'norway', 'russia',
            'netherlands', 'switzerland', 'italy', 'france', 'sweden']
    years = [2014, 2016]
    multi_country_hdi = CleanDataFrame(files, female_indicator_codes, years)
    multi_2014_hdi_df = multi_country_hdi.df[multi_country_hdi.df['#date+year'] == 2014]
    merge_df = pd.merge(multi_2014_hdi_df, 
                        winter_dataframes.country_medals_df['%_womens_medals'], 
                                                            left_on='#country+name', 
                                                            right_index=True)
    merge_df.drop(49006, inplace=True, axis=1)
    # merge_df['rand'] = np.random.rand(len(merge_df.index))
    corr_df = merge_df.corr()['%_womens_medals']
    abrev_corr_df = corr_df.iloc[[1,2,6,7,11]]
    sorted_df = abrev_corr_df.abs().sort_values(ascending = False)
    y = abrev_corr_df[sorted_df.index]
    x = np.arange(len(y))
    labels_num = sorted_df.index
    labels_txt = ['Female Gross\nNational Income', 'Mean Female\nSchooling', 'Women in\nParlament',
                 'Female HDI', ' % Females with\nSecondary Ed']
    
    fig, ax = plt.subplots(1, figsize=(12,6))
    ax.bar(x,y, color='tab:red')
    ax.set_xticklabels(labels_txt, fontsize=16)
    ax.set_xticks(x)
    ax.axhline(y=0)
    ax.set_xlabel('Human Development Indices', fontsize=18)
    ax.set_ylabel('Correlation with Womens Medals', fontsize=18)
    ax.set_title('Correlation between Womens Winter Olympic Medals\nand\
 Human Development Index', fontsize=20)
    plt.tight_layout()
    plt.savefig('../images/HDI_correlations.png')
    

    fig, ax = plt.subplots(1)
    x = merge_df['%_womens_medals']
    y = merge_df[labels_num[0]]
    ax.scatter(x,y, color='tab:red')
    trendline = np.polyfit(x, y, 1)
    trendline_formula = np.poly1d(trendline)
    ax.set_ylabel('GNI (Female)', fontsize=18)
    ax.set_xlabel('% Winter Olympic Medals', fontsize=18)
    ax.set_title('Correlation Between Female Medals and \n Estimated Gross National Income', fontsize=20)
    ax.plot(x, trendline_formula(x), 'r-')
    plt.tight_layout()
    # plt.savefig('../images/GNI_scatter.png')
    '''