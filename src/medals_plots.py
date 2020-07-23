import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('tableau-colorblind10')

def percent_plot(x, y, season, ax=None, **plt_kwargs):
    if ax is None:
        fig, ax = plt.subplots(1)
    ax.plot(x,y, **plt_kwargs)
    ax.set_title(f'Women in the {season.capitalize()} Olympics', fontsize=20)
    ax.set_xlabel('Year', fontsize=18)
    ax.set_ylabel('% of Events', fontsize=18)
    # ax.legend()
    plt.tight_layout()
    return ax

def gender_counts_plot(x, y, labels, ax=None, **plt_kwargs):
    if ax is None:
        fig, ax = plt.subplots(1, figsize=(12,7))
    ax.bar(x, y, **plt_kwargs)
    ax.set_title(f'Mens and Womens {labels[1]} \n in the {labels[0].capitalize()} Olympics',
                    fontsize=20)
    ax.set_xlabel(labels[2], fontsize=18)
    ax.set_ylabel(f'Number of {labels[1]}', fontsize=18)
    ax.legend()
    plt.tight_layout()
    return ax
def plot_percent_year(df_obj, save_on=True):
    year = df_obj.annual_medals_df.index
    y = df_obj.annual_medals_df['%_womens_events']
    ax = percent_plot(year, y, df_obj.season, color='tab:red', label='Excluding Mixed Events')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/no-mix-year-plot.png')
    y2 = df_obj.annual_medals_mixed_df['%_womens_events']
    ax2 = percent_plot(year, y2, df_obj.season, color='tab:purple', label='Including Mixed Events')
    ax2 = percent_plot(year, y, df_obj.season, ax2, color='tab:red', label='Excluding Mixed Events')
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

if __name__ == '__main__':
    pass
