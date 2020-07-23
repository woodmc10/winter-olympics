from winter_medals import *

print('All Olympics Unemployment')
print(stats.pearsonr(all_olympics_hdi['all_medals_%_women'], all_olympics_hdi[169706]))
print('Winter Olympics Unemployment')
print(stats.pearsonr(winter_olympics_hdi[winter_olympics_hdi['winter_medals_%_women'].isna()==False], winter_olympics_hdi[winter_olympics_hdi[169706].isna()==False]))
print('Winter Olympics GNI')
print(stats.pearsonr(winter_olympics_hdi[winter_olympics_hdi['winter_medals_%_women'].isna()==False], winter_olympics_hdi[winter_olympics_hdi[123506].isna()==False]))
