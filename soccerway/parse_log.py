# -*- coding: utf-8 -*-

import pandas as pd

def venues():
    l = []
    df = pd.read_csv('404.log', delimiter=' ', header=None)

    for row in df[7]:
        l.append(int((row.split('/')[6][1:])))
    print('Nonexitent ({}) venues:'.format(len(l)))
    print(str(l))

if __name__ == "__main__":
    # execute only if run as a script
    venues()
