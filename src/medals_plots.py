import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

plt.style.use('tableau-colorblind10')


def percent_plot(x, y, season, ax=None, **plt_kwargs):
    '''Create a plot of the percent womens events in the season

    Parameters
    ----------
    x: list (or list-like)
        values for x axis
    y: list (or list-like)
        values for y-axis
    season: str
        season of Olympics for title
    ax: plt.ax, optional
        axis to add plot to, if None then a new plot is created
    **plt_kwargs: optional
        other keyword arguments for plotting

    Return
    ------
    None
    '''
    if ax is None:
        fig, ax = plt.subplots(1)
        ax.set_title(f'Women in the {season.capitalize()} Olympics',
                     fontsize=20)
        ax.set_xlabel('Year', fontsize=18)
    ax.plot(x, y, **plt_kwargs)
    ax.set_ylabel('% of Events', fontsize=18)
    ax.legend(loc=9)
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position('right')
    plt.tight_layout()
    return ax


def gender_counts_plot(x, y, labels, ax=None, **plt_kwargs):
    '''Create bar plot of men and women events or medals

    Parameters
    ----------
    x: list (or list-like)
        values for x axis
    y: list (or list-like)
        values for y-axis
    labels: list
        list of values to include in labels
        [season, Events or Medals, xlabel(Year or Country)]
    ax: plt.ax, optional
        axis to add plot to, if None then a new plot is created
    **plt_kwargs: optional
        other keyword arguments for plotting

    Return
    ------
    None
    '''
    if ax is None:
        fig, ax = plt.subplots(1, figsize=(12, 7))
    ax.bar(x, y, **plt_kwargs)
    ax.set_title(f'Mens and Womens {labels[1]}\n in' +
                 f' the {labels[0].capitalize()} Olympics', fontsize=20)
    ax.set_xlabel(labels[2], fontsize=18)
    ax.set_ylabel(f'Number of {labels[1]}', fontsize=18)
    ax.legend()
    plt.tight_layout()
    return ax


def plot_percent_year(df_obj, save_on=True):
    '''Create womens event percent plots for both mixed and non-mixed
    categories of the dataframe object

    Parameters
    ----------
    df_obj: GenderDataFrames object
        contains DataFrames to plot
    save_on: bool, optional
        if true the plots will be saved, if false the plots will show
        on the screen (default is True)

    Returns
    -------
    None
    '''
    year = df_obj.annual_medals_df.index
    y = df_obj.annual_medals_df['%_womens_events']
    ax = percent_plot(year, y, df_obj.season, color='tab:pink',
                      label='Excluding Mixed Events')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/no-mix-year-plot.png')
    y2 = df_obj.annual_medals_mixed_df['%_womens_events']
    ax2 = percent_plot(year, y2, df_obj.season, color='tab:purple',
                       label='Including Mixed Events')
    ax2 = percent_plot(year, y, df_obj.season, ax2, color='tab:pink',
                       label='Excluding Mixed Events')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/mix-year-plot.png')


def plot_bar_year(df_obj, save_on=True):
    '''Create bar plots of mens/womens and mens/womens/mixed events by
    year for the dataframe object

    Parameters
    ----------
    df_obj: GenderDataFrames object
        contains DataFrames to plot
    save_on: bool, optional
        if true the plots will be saved, if false the plots will show
        on the screen (default is True)

    Returns
    -------
    None
    '''
    labels = [df_obj.season, 'Events', 'Year']
    year = df_obj.annual_medals_df.index
    y3_a = df_obj.annual_medals_df['mens_events']
    y3_b = df_obj.annual_medals_df['womens_events']
    ax3 = gender_counts_plot(year, y3_a, labels, color='tab:cyan',
                             label='Mens Events')
    ax3 = gender_counts_plot(year+1, y3_b, labels, ax3, color='tab:pink',
                             label='Womens Events')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/no-mix-count-year-plot.png')
    y4_a = df_obj.annual_medals_mixed_df['mens_events']
    y4_b = df_obj.annual_medals_mixed_df['womens_events']
    y4_c = df_obj.annual_medals_mixed_df['mixed_events']
    ax4 = gender_counts_plot(year-0.7, y4_a, labels, color='tab:cyan',
                             label='Mens Events', width=0.7)
    ax4 = gender_counts_plot(year, y4_b, labels, ax4, color='tab:pink',
                             label='Womens Events', width=0.7)
    ax4 = gender_counts_plot(year+0.7, y4_c, labels, ax4, color='tab:purple',
                             label='Mixed Events', width=0.7)
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/mix-count-year-plot.png')


def plot_bar_year_overlay(df_obj, save_on=True):
    '''Create bar plots of mens/womens and mens/womens/mixed events by
    year for the dataframe object with an overlay of the percent womens
    events

    Parameters
    ----------
    df_obj: GenderDataFrames object
        contains DataFrames to plot
    save_on: bool, optional
        if true the plots will be saved, if false the plots will show
        on the screen (default is True)

    Returns
    -------
    None
    '''
    year = df_obj.annual_medals_df.index
    y = df_obj.annual_medals_df['%_womens_events']
    labels = [df_obj.season, 'Events', 'Year']
    y3_a = df_obj.annual_medals_df['mens_events']
    y3_b = df_obj.annual_medals_df['womens_events']
    ax3 = gender_counts_plot(year, y3_a, labels, color='tab:cyan',
                             label='Mens Events')
    ax3_a = gender_counts_plot(year+1, y3_b, labels, ax3, color='tab:pink',
                               label='Womens Events')
    ax3_b = ax3_a.twinx()
    ax3_b = percent_plot(year, y, df_obj.season, ax3_b, color='tab:pink',
                         label='Percent Womens Events')
    ax3_b.annotate('Olympics\ncanceled\ndurring\nWWII', (1938, 6),
                   multialignment='center', fontsize=14)
    # ax3_b.annotate('Olympic\nGames on\ndifferent\n4-year\ncylces', (1986.5, 6),
    #                multialignment='center', fontsize=14, 
    #                bbox=dict(facecolor='white', edgecolor='black'))
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/no-mix-count-year-plot.png')
    y = df_obj.annual_medals_mixed_df['%_womens_events']
    y4_a = df_obj.annual_medals_mixed_df['mens_events']
    y4_b = df_obj.annual_medals_mixed_df['womens_events']
    y4_c = df_obj.annual_medals_mixed_df['mixed_events']
    ax4 = gender_counts_plot(year-0.7, y4_a, labels, color='tab:cyan',
                             label='Mens Events', width=0.7)
    ax4 = gender_counts_plot(year, y4_b, labels, ax4, color='tab:pink',
                             label='Womens Events', width=0.7)
    ax4 = gender_counts_plot(year+0.7, y4_c, labels, ax4, color='tab:purple',
                             label='Mixed Events', width=0.7)
    ax4 = percent_plot(year, y, df_obj.season, ax4, color='tab:purple',
                       label='Percent Womens Events')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/mix-count-year-plot.png')


def plot_bar_country(df_obj, save_on=True):
    '''Create bar plots of mens/womens and mens/womens/mixed medals by
    country for the dataframe object

    Parameters
    ----------
    df_obj: GenderDataFrames object
        contains DataFrames to plot
    save_on: bool, optional
        if true the plots will be saved, if false the plots will show
        on the screen (default is True)

    Returns
    -------
    None
    '''
    country = df_obj.country_medals_df.index
    labels = [df_obj.season, 'Medals', 'Country']
    x = np.arange(len(country))
    y5_a = df_obj.country_medals_df['mens_medals']
    y5_b = df_obj.country_medals_df['womens_medals']
    ax5 = gender_counts_plot(x-0.15, y5_a, labels, color='tab:cyan',
                             label='Mens Medals', width=0.25)
    ax5 = gender_counts_plot(x+0.15, y5_b, labels, ax5, color='tab:pink',
                             label='Womens Medals', width=0.25)
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
    ax6 = gender_counts_plot(x-0.25, y6_a, labels,   color='tab:cyan',
                             label='Mens Medals', width=0.25)
    ax6 = gender_counts_plot(x, y6_b, labels, ax6, color='tab:pink',
                             label='Womens Medals', width=0.25)
    ax6 = gender_counts_plot(x+0.25, y6_c, labels, ax6, color='tab:purple',
                             label='Mixed Medals', width=0.25)
    ax6.set_xticks(x)
    ax6.set_xticklabels(country)
    plt.xticks(rotation=25, ha='right')
    if save_on:
        plt.savefig(f'../images/{df_obj.season}/mix-country-plot.png')


def plot_hdi_corrs(hdi_list, corr_df, labels_dict, season, ax=None,
                   save_on=False):
    '''Create a bar chart showing the correlation between the listed
    hdi codes and the percent women medals for the countries in the
    corr_df

    Parameters
    ----------
    hdi_list: list
        list of HDI codes to include in abbreviated correlation
        DataFrame
    corr_df: pandas DataFrame
        DataFrame containing the correlation between all HDI and
        percent womens medals
    labels_dict: dict
        dictionary with HDI codes as keys and abbreviated descriptions
        of the HDI as values
    season: str
        'all' or 'winter' used to set color and labels for plots
    ax: plt.ax, optional
        axis to add plot to, if None then a new plot is created
    save_on: bool, optional
        if true the plots will be saved (default is False)

    Returns
    -------
    ax: plt.ax
        the axis on which the plot was created
    '''
    abrev_corr_df = corr_df.loc[hdi_list]
    sorted_df = abrev_corr_df.abs().sort_values(ascending=False)
    y = abrev_corr_df[hdi_list]
    x = np.arange(len(y), dtype=float)
    labels_num = hdi_list
    labels_txt = [labels_dict[elem] for elem in labels_num]
    if ax is None:
        fig, ax = plt.subplots(1, figsize=(12, 6))
        width = -0.4
    else:
        width = 0.4
    if season == 'winter':
        c = 'tab:pink'
        label = 'Winter Olympics'
    else:
        c = 'tab:red'
        label = 'All Olympics'
    ax.bar(x, y, width=width, align='edge', color=c, label=label)
    ax.set_xticklabels(labels_txt, fontsize=14)
    ax.set_xticks(x)
    ax.axhline(y=0)
    ax.set_xlabel('Human Development Indices', fontsize=18)
    ax.set_ylabel('Correlation', fontsize=18)
    ax.set_title('Correlation between Womens Olympic Medals\nand' +
                 ' Human Development Index', fontsize=20)
    ax.legend()
    ax.annotate('p-value\n0.20', (-0.38, -0.42),
                multialignment='center', fontsize=14)
    ax.annotate('p-value\n0.49', (0.62, -0.23),
                multialignment='center', fontsize=14)
    ax.annotate('p-value\n0.02', (1.02, -0.4),
                multialignment='center', fontsize=14)
    plt.tight_layout()
    if save_on:
        plt.savefig(f'../images/{season}/HDI_correlations.png')
    return ax


def scatter_corr(x, y, labels_list, save_as=None, save_on=False):
    '''Create a scatter plot of the HDI values (y) and the percent
    women medals (x)

    Parameters
    ----------
    x: list (or list-like)
        values for x axis
    y: list (or list-like)
        values for y-axis
    labels: list
        list of values to include in labels
        [ylabel(HDI), xlabel(Womens Medals/Athletes)]
    save_as: str, optional
        file name for saving plot
    save_on: bool, optional
        if true the plots will be saved, if false the plots will show
        on the screen (default is False)

    Returns
    -------
    None
    '''
    fig, ax = plt.subplots(1)
    ax.scatter(x, y, color='tab:pink')
    trendline = np.polyfit(x, y, 1)
    trendline_formula = np.poly1d(trendline)
    ax.set_ylabel(labels_list[0], fontsize=18)
    ax.set_xlabel(labels_list[1], fontsize=18)
    ax.set_title('Correlation to HDI', fontsize=20)
    ax.plot(x, trendline_formula(x), 'r-')
    plt.tight_layout()
    if save_on:
        plt.savefig(save_as)


if __name__ == '__main__':
    pass
