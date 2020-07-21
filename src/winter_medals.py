import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from medals_plots import percent_plot, gender_counts_plot
from hdi import CleanDataFrame

plt.style.use('tableau-colorblind10')

class GenderDataFrames(object):
    
    def __init__(self, file):
        self.file = file
        self.original_df = self.create_df()
        self.annual_medals_df = self.create_year_df(ignore_mixed=True)
        self.annual_medals_mixed_df = self.create_year_df(ignore_mixed=False) 
        self.country_medals_df = self.create_country_df(min_year=1994, 
                                                        min_medals=50, 
                                                        ignore_mixed=True)
        self.country_medals_mixed_df = self.create_country_df(min_year=1994, 
                                                            min_medals=50, 
                                                            ignore_mixed=False)
    
    def create_df(self):
        df = pd.read_excel(self.file)
        df.drop(['Medal Rank', 'Age of Athlete'], axis=1, inplace=True)
        return pd.get_dummies(df, columns=['Gender'])

    def create_year_df(self, ignore_mixed=True):
        cols_list = ['mens_events', 'womens_events', 'mixed_events']
        if ignore_mixed:
            cols_list.pop() 
        year_df = self.original_df.groupby(['Year', 'Sport', 'Event']).sum().copy()
            # sum is automatically dropping object columns
        year_df['mens_events'] = np.where(year_df['Gender_Men'] > 0, 1, 0)
        year_df['womens_events'] = np.where(year_df['Gender_Women'] > 0, 1, 0)
        year_df['mixed_events'] = np.where(year_df['Gender_Mixed'] > 0, 1, 0)
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


if __name__ == '__main__':
    winter_dataframes = GenderDataFrames('../data/winter-olympic-medals.xlsx')
    
    '''
    Plots - add more to functions, less repetative here
    ---------------------------------------------------

    year = df_gender_by_year_no_mixed.index
    y = df_gender_by_year_no_mixed['%_womens_events']
    ax = percent_plot(year, y, color='tab:red', label='Excluding Mixed Events')
    plt.savefig('../images/no-mix-year-plot.png')

    y2 = df_gender_by_year_with_mixed['%_womens_events']
    ax2 = percent_plot(year, y2, color='tab:red', label='Including Mixed Events')
    plt.savefig('../images/mix-year-plot.png')

    y3_a = df_gender_by_year_no_mixed['mens_events'] 
    y3_b = df_gender_by_year_no_mixed['womens_events']
    ax3 = gender_counts_plot(year, y3_a, color='tab:blue', label='Mens Events')
    ax3 = gender_counts_plot(year+1, y3_b, ax3, color='tab:red', label='Womens Events')
    plt.savefig('../images/no-mix-count-year-plot.png')

    fig4, ax4 = plt.subplots(1, figsize=(12,6))
    y4_a = df_gender_by_year_with_mixed['mens_events'] 
    y4_b = df_gender_by_year_with_mixed['womens_events']
    y4_c = df_gender_by_year_with_mixed['mixed_events']
    ax3 = gender_counts_plot(year-0.7, y4_a, ax4, color='tab:blue', label='Mens Events', width=0.7)
    ax3 = gender_counts_plot(year, y4_b, ax4, color='tab:red', label='Womens Events', width=0.7)
    ax3 = gender_counts_plot(year+0.7, y4_c, ax4 color='tab:purple', label='Mixed Events', width=0.7)
    plt.savefig('../images/mix-count-year-plot.png')
    
    fig5, ax5 = plt.subplots(1, figsize=(12,6))
    country = df_medals_50_no_mixed.index
    x = np.arange(len(country))
    y5_a = df_medals_50_no_mixed['mens_medals']
    y5_b = df_medals_50_no_mixed['womens_medals']
    ax5 = gender_counts_plot(x-0.15, y5_a, ax5, color='tab:blue', label='Mens Medals', width=0.25)
    ax5 = gender_counts_plot(x+0.15, y5_b, ax5, color='tab:red', label='Womens Medals', width=0.25)
    ax5.set_xticks(x)
    ax5.set_xticklabels(country)
    plt.xticks(rotation=45, ha='right')
    plt.savefig('../images/no-mix-country-plot-1993.png')
    
    fig6, ax6 = plt.subplots(1)
    country = df_medals_50_with_mixed.index
    x = np.arange(len(country))
    y6_a = df_medals_50_with_mixed['mens_medals']
    y6_b = df_medals_50_with_mixed['womens_medals']
    y6_c = df_medals_50_with_mixed['mixed_medals']
    ax6 = gender_counts_plot(x-0.25, y6_a, color='tab:blue', label='Mens Medals', width=0.25)
    ax6 = gender_counts_plot(x, y6_b, color='tab:red', label='Womens Medals', width=0.25)
    ax6 = gender_counts_plot(x+0.25, y6_c, color='tab:purple', label='Mixed Medals', width=0.25)
    ax6.set_xticks(x)
    ax6.set_xticklabels(country)
    plt.xticks(rotation=45, ha='right')
    plt.savefig('../images/mix-country-plot.png')

    '''

    #Combine data frames from hdi with winter olympic medals (1994 on)
    female_indicator_codes = [23906, 24106, 48706, 49006, 120606, 
                                123306, 123506, 136906, 169706, 169806, 
                                175106, 31706, 36806]
    files = ['usa', 'germany', 'canada', 'austria', 'norway', 'russia',
            'netherlands', 'switzerland', 'italy', 'france', 'sweden']
    years = [2014, 2016]
    multi_country_hdi_df = CleanDataFrame(files, female_indicator_codes, years).df
    multi_2014_hdi_df = multi_country_hdi_df[multi_country_hdi_df['#date+year'] == 2014]
    corr_df = pd.merge(multi_2014_hdi_df, 
                        winter_dataframes.country_medals_df['%_womens_medals'], 
                                                            left_on='#country+name', 
                                                            right_index=True)
    corr_df.drop(49006, inplace=True, axis=1)
    corr_df['rand'] = np.random.rand(len(corr_df.index))
    
    print(corr_df.corr()['%_womens_medals'].to_markdown())
    
