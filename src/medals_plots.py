import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('tableau-colorblind10')

def percent_plot(x, y, ax=None, **plt_kwargs):
    if ax is None:
        fig, ax = plt.subplots(1)
    ax.plot(x,y, **plt_kwargs)
    ax.set_title('Womens in the Winter Olympics', fontsize=20)
    ax.set_xlabel('Year', fontsize=18)
    ax.set_ylabel('% of Events', fontsize=18)
    ax.legend()
    plt.tight_layout()
    return ax

def gender_counts_plot(x, y, ax=None, **plt_kwargs):
    if ax is None:
        fig, ax = plt.subplots(1)
    ax.bar(x, y, **plt_kwargs)
    ax.set_title('Mens and Womens Events \n in the Winter Olympics',
                    fontsize=20)
    ax.set_xlabel('Year', fontsize=18)
    ax.set_ylabel('Number of Events', fontsize=18)
    ax.legend()
    return ax

if __name__ == '__main__':
    pass
