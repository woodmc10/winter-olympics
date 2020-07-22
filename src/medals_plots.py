import pandas as pd
import matplotlib.pyplot as plt

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

if __name__ == '__main__':
    pass
