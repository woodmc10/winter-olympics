import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from medals_plots import percent_plot, gender_counts_plot

plt.style.use('tableau-colorblind10')


def create_df(file):
    return pd.read_excel(file)

def clean_df(df, col):
    df.drop(['Medal Rank', 'Age of Athlete'], axis=1, inplace=True)
    return pd.get_dummies(df, columns=[col])

def create_year_df(df, ignore_mixed=True):
    if ignore_mixed:
        cols_list = ['mens_events', 'womens_events']
    else:
        cols_list = ['mens_events', 'womens_events', 'mixed_events']
    
    year_df = df.groupby(['Year', 'Sport', 'Event']).sum().copy()
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

def create_country_df(df, ignore_mixed=True):
    if ignore_mixed:
        cols_list = ['mens_medals', 'womens_medals']
    else:
        cols_list = ['mens_medals', 'womens_medals', 'mixed_medals']
    country_df = df.groupby('Country').sum()
    country_df.rename(columns={'Gender_Men': 'mens_medals', 
                                'Gender_Women': 'womens_medals', 
                                'Gender_Mixed': 'mixed_medals'}, 
                                inplace=True)
    country_df = country_df[cols_list]
    country_df['total_medals'] =country_df[cols_list].sum(axis=1)
    cols_list.remove('mens_medals')
    country_df['%_womens_medals'] = (country_df[cols_list].sum(axis=1)/
                                    country_df['total_medals']) * 100
    over_50_df = country_df[country_df['total_medals'] > 50]
    sorted_df = over_50_df.sort_values(by='womens_medals', ascending=False).copy()
    return sorted_df


if __name__ == '__main__':
    df_medals = create_df('../data/winter-olympic-medals.xlsx')
    df_medals = clean_df(df_medals, 'Gender')
    df_gender_by_year_no_mixed = create_year_df(df_medals)
    df_gender_by_year_with_mixed = create_year_df(df_medals, False)
    # print(df_gender_by_year_no_mixed.head())
    # print(df_gender_by_year_with_mixed.head())

    df_medals_50_no_mixed = create_country_df(df_medals)
    df_medals_50_with_mixed = create_country_df(df_medals, False)
    # print(df_medals_50_no_mixed.head())
    # print(df_medals_50_with_mixed.head())

    # df_gender_by_year_no_mixed.plot(y='%_womens_events')
    # Plot with function
    
    year = df_gender_by_year_no_mixed.index
    

    fig, ax = plt.subplots(1)
    year = df_gender_by_year_no_mixed.index
    y = df_gender_by_year_no_mixed['%_womens_events']
    ax = percent_plot(year, y, color='tab:red', label='Excluding Mixed Events')
    plt.tight_layout()
    plt.savefig('../images/no-mix-year-plot.png')

    fig2, ax2 = plt.subplots(1)
    y2 = df_gender_by_year_with_mixed['%_womens_events']
    ax2 = percent_plot(year, y2, color='tab:red', label='Including Mixed Events')
    plt.tight_layout()
    plt.savefig('../images/mix-year-plot.png')

    fig3, ax3 = plt.subplots(1)
    y3_a = df_gender_by_year_no_mixed['mens_events'] 
    y3_b = df_gender_by_year_no_mixed['womens_events']
    ax3 = gender_counts_plot(year, y=y3_a, color='tab:blue', label='Mens Events')
    ax3 = gender_counts_plot(year+1, y3_b, color='tab:red', label='Womens Events')
    plt.tight_layout()
    plt.savefig('../images/no-mix-count-year-plot.png')

    fig4, ax4 = plt.subplots(1, figsize=(12,6))
    y4_a = df_gender_by_year_with_mixed['mens_events'] 
    y4_b = df_gender_by_year_with_mixed['womens_events']
    y4_c = df_gender_by_year_with_mixed['mixed_events']
    ax3 = gender_counts_plot(year-0.7, y=y4_a, color='tab:blue', label='Mens Events', width=0.7)
    ax3 = gender_counts_plot(year, y4_b, color='tab:red', label='Womens Events', width=0.7)
    ax3 = gender_counts_plot(year+0.7, y4_c, color='tab:purple', label='Mixed Events', width=0.7)
    plt.tight_layout()
    plt.savefig('../images/mix-count-year-plot.png')

    fig5, ax5 = plt.subplots(1)
    country = df_medals_50_no_mixed.index
    x = np.arange(len(country))
    y5_a = df_medals_50_no_mixed['mens_medals']
    y5_b = df_medals_50_no_mixed['womens_medals']
    ax5 = gender_counts_plot(x-0.15, y5_a, color='tab:blue', label='Mens Medals', width=0.25)
    ax5 = gender_counts_plot(x+0.15, y5_b, color='tab:red', label='Womens Medals', width=0.25)
    ax5.set_xticks(x)
    ax5.set_xticklabels(country)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('../images/no-mix-country-plot.png')

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
    plt.tight_layout()
    plt.savefig('../images/mix-country-plot.png')
  
