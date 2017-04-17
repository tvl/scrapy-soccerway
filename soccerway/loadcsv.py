# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime

matches = pd.read_csv('data/schedule.csv')
matches.dropna(subset = ['venue'], inplace=True)
matches.sort_values(by='datetime', inplace=True)
venues = pd.read_csv('data/venues.csv')
venues.dropna(subset = ['name', 'lat', 'lon'], how='any', inplace=True)

def venue_geo(name):
    name = name.split('(')[0].strip()
    v = venues.loc[venues['name'] == name]
    if v.shape[0] == 1:
        return v.lat.values[0], v.lon.values[0]
    else:
        return 0, 0

for i, m in matches.iterrows():
    print('[{}] {} {} ({}) {}'.format(m.id, m.datetime, m.home_team, m.kick_off, m.away_team))
    print('{} {}'.format(m.venue, venue_geo(m.venue)))

