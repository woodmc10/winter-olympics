import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from medals_plots import percent_plot, gender_counts_plot
from hdi import CleanDataFrame

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
            df.drop(['Name', 'Age', 'Height', 'Weight', 'Team', 'Games', 'Season', 'City'], 
                    axis=1, inplace=True)
            df.rename(columns={'Sex': 'Gender', 'NOC': 'Country'}, inplace=True)
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

def plot_percent_year(df_obj, save_on=True):
    year = df_obj.annual_medals_df.index
    y = df_obj.annual_medals_df['%_womens_events']
    ax = percent_plot(year, y, df_obj.season, color='tab:red', label='Excluding Mixed Events')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/no-mix-year-plot.png')
    y2 = df_obj.annual_medals_mixed_df['%_womens_events']
    ax2 = percent_plot(year, y2, df_obj.season, color='tab:purple', label='Including Mixed Events')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/mix-year-plot.png')

def plot_bar_year(df_obj, save_on=True):
    labels = [df_obj.season, 'Events', 'Year']
    year = df_obj.annual_medals_df.index
    y3_a = df_obj.annual_medals_df['mens_events'] 
    y3_b = df_obj.annual_medals_df['womens_events']
    ax3 = gender_counts_plot(year, y3_a, labels, color='tab:blue', label='Mens Events')
    ax3 = gender_counts_plot(year+1, y3_b, labels, ax3, color='tab:red', label='Womens Events')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/no-mix-count-year-plot.png')
    y4_a = df_obj.annual_medals_mixed_df['mens_events'] 
    y4_b = df_obj.annual_medals_mixed_df['womens_events']
    y4_c = df_obj.annual_medals_mixed_df['mixed_events']
    ax4 = gender_counts_plot(year-0.7, y4_a, labels, color='tab:blue', label='Mens Events', width=0.7)
    ax4 = gender_counts_plot(year, y4_b, labels, ax4, color='tab:red', label='Womens Events', width=0.7)
    ax4 = gender_counts_plot(year+0.7, y4_c, labels, ax4, color='tab:purple', label='Mixed Events', width=0.7)
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/mix-count-year-plot.png')

def plot_bar_country(df_obj, save_on=True):
    country = df_obj.country_medals_df.index
    labels = [df_obj.season, 'Medals', 'Country']
    x = np.arange(len(country))
    y5_a = df_obj.country_medals_df['mens_medals']
    y5_b = df_obj.country_medals_df['womens_medals']
    ax5 = gender_counts_plot(x-0.15, y5_a, labels, color='tab:blue', label='Mens Medals', width=0.25)
    ax5 = gender_counts_plot(x+0.15, y5_b, labels, ax5, color='tab:red', label='Womens Medals', width=0.25)
    ax5.set_xticks(x)
    ax5.set_xticklabels(country)
    plt.xticks(rotation=25, ha='right')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/no-mix-country-plot-1993.png')
    country = df_obj.country_medals_mixed_df.index
    x = np.arange(len(country))
    y6_a = df_obj.country_medals_mixed_df['mens_medals']
    y6_b = df_obj.country_medals_mixed_df['womens_medals']
    y6_c = df_obj.country_medals_mixed_df['mixed_medals']
    ax6 = gender_counts_plot(x-0.25, y6_a, labels,   color='tab:blue', label='Mens Medals', width=0.25)
    ax6 = gender_counts_plot(x, y6_b, labels, ax6, color='tab:red', label='Womens Medals', width=0.25)
    ax6 = gender_counts_plot(x+0.25, y6_c, labels, ax6, color='tab:purple', label='Mixed Medals', width=0.25)
    ax6.set_xticks(x)
    ax6.set_xticklabels(country)
    plt.xticks(rotation=25, ha='right')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/mix-country-plot.png')

def do_all_plots(df_obj, save_on=False):
    plot_percent_year(df_obj, save_on)
    plot_bar_year(df_obj, save_on)
    plot_bar_country(df_obj, save_on)
    if not save_on:
        plt.show()

if __name__ == '__main__':
    winter_dataframes = GenderDataFrames('../data/winter-olympic-medals.xlsx', 'winter')
    all_olympics_dataframes = GenderDataFrames('../data/summer_olympics/athlete_events.csv', 'all')
    
    do_all_plots(winter_dataframes, True)
    do_all_plots(all_olympics_dataframes, True)

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