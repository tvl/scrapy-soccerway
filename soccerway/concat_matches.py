# -*- coding: utf-8 -*-

import glob, os, sys
import pandas as pd
d = '/home/tvl/dev/scrapy-soccerway/soccerway/data/h/'
frames = []
os.chdir(d)
print('Read csv files:')
for f in glob.glob("matches*.csv"):
        print(f)
        frames.append(pd.read_csv(d+f))
df = pd.concat(frames)
df.set_index('id', inplace=True)
df.sort_values(by='datetime', inplace=True)
print('Totals:')
print(df.count())
df.to_csv(d+'historical2010-2120.csv', sep=',', encoding='utf-8')
print('Dataframe size (bytes): {}'.format(sys.getsizeof(df)))
