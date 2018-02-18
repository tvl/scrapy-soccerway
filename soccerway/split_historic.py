# -*- coding: utf-8 -*-

import os
import pandas as pd
#d = '/home/tvl/dev/scrapy-soccerway/soccerway/data/h/'
d = '/home/tvl/dev/swe/data/soccerway/historic/'

frames = []
os.chdir(d)
print('Read csv file...')
matches = pd.read_csv('{}h2010-2017.csv'.format(d))
print('Matches : {}'.format(matches.shape[0]))
for y in range(2010, 2018):
    m = matches[matches['year'] == y]
    m.set_index('id', inplace=True)
    m.sort_values(by='datetime', inplace=True)
    m.to_csv('{}{}.csv'.format(d, y), sep=',', encoding='utf-8')
    print('{} : {}'.format(y, m.shape[0]))
