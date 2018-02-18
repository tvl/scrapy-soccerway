# -*- coding: utf-8 -*-

import glob, os, sys
import pandas as pd
#d = '/home/tvl/dev/scrapy-soccerway/soccerway/data/h/'
d = '/home/tvl/dev/swe/out/calc/2018.02/'

frames = []
os.chdir(d)
print('Read csv files:')
#for f in glob.glob("matches*.csv"):
for f in glob.glob("201*.csv"):

        print(f)
        frames.append(pd.read_csv(d+f))
df = pd.concat(frames)
df.set_index('id', inplace=True)
#df.sort_values(by='datetime', inplace=True)
df.sort_values(by=['date', 'time'], inplace=True)

print('Totals:')
print(df.count())
df.to_csv(d+'out.csv', sep=',', encoding='utf-8')
print('Dataframe size (bytes): {}'.format(sys.getsizeof(df)))
