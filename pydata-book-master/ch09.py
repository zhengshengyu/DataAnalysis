#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Data Aggregation and Group Operations
from __future__ import division
from numpy.random import randn
import numpy as np
import os
import matplotlib.pyplot as plt
np.random.seed(12345)
plt.rc('figure', figsize=(10, 6))
from pandas import Series, DataFrame
import pandas as pd
np.set_printoptions(precision=4)

## GroupBy mechanics
df = DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'],
	'key2' : ['one', 'two', 'one', 'two', 'one'],
	'data1' : np.random.randn(5),
	'data2' : np.random.randn(5)})
print df

grouped = df['data1'].groupby(df['key1'])
print grouped
# print grouped.mean(), grouped.size()

grouped2 =  df['data1'].groupby([df['key1'], df['key2']])
# print grouped2.mean().unstack()

states = np.array(['Ohio', 'California', 'California', 'Ohio', 'Ohio'])
years = np.array([2005, 2005, 2006, 2005, 2006])
# print df['data1'].groupby([states, years]).mean()
# print df['data1'].groupby(df['key1']).mean()
# print df.groupby('key1').mean()
# print df.groupby(['key1','key2']).mean()

### Iterating over groups
for name, group in df.groupby('key1'):
    print(name)
    # print(group)

for (k1, k2), group in df.groupby(['key1', 'key2']):
    print((k1, k2))
    # print(group)

pieces = dict(list(df.groupby('key1')))
print pieces['b']
grouped = df.groupby(df.dtypes, axis=1)
print dict(list(grouped))

### Selecting a column or subset of columns
print df.groupby('key1')['data1']
print df['data1'].groupby(df['key1'])
print df.groupby('key1')[['data2']]
print df[['data2']].groupby(df['key1'])
s_grouped = df.groupby(['key1', 'key2'])['data2']
d_grouped = df.groupby(['key1', 'key2'])[['data2']]
print s_grouped, d_grouped
print s_grouped.mean(), d_grouped.mean()


### Grouping with dicts and Series
people = DataFrame(np.random.randn(5, 5),
                   columns=['a',  'c', 'd', 'e', 'b'],
                   index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
people.ix[0:3, ['b', 'c']] = np.nan # Add a few NA values
print people

mapping = {'a': 'red', 'c': 'blue',  'b': 'red',
           'd': 'blue', 'e': 'red', 'f' : 'orange'}
by_column = people.groupby(mapping, axis=1)
print by_column.sum()
map_series = Series(mapping)
print map_series
print people.groupby(map_series, axis=1).count()

### Grouping with functions
print people.groupby(len).sum()
key_list = ['one', 'one', 'one', 'two', 'two']
print people.groupby([len, key_list]).min()

### Grouping by index levels
columns = pd.MultiIndex.from_arrays([['US', 'US', 'US', 'JP', 'JP'],
                                    [1, 3, 5, 1, 3]], names=['cty', 'tenor'])
hier_df = DataFrame(np.random.randn(4, 5), columns=columns)
print hier_df
print hier_df.groupby(level='tenor', axis=1).count()


## Data aggregation
grouped = df.groupby('key1')
print grouped['data1'].quantile(0.9)

def peak_to_peak(arr):
    return float(arr.max()) - float(arr.min())
print grouped.agg(peak_to_peak)
print grouped.describe()



tips = pd.read_csv('ch08/tips.csv')
# Add tip percentage of total bill
tips['tip_pct'] = tips['tip'] / tips['total_bill']
print tips[:6]

### Column-wise and multiple function application
grouped = tips.groupby(['sex', 'smoker'])
grouped_pct = grouped['tip_pct']
print grouped, grouped_pct
# print grouped_pct.agg('mean')
# print grouped_pct.agg(['mean', 'std', peak_to_peak])
print grouped_pct.agg([('foo', 'mean'), ('bar', np.std)])
functions = ['count', 'mean', 'max']
result = grouped['tip_pct', 'total_bill'].agg(functions)
print result
# print result['tip_pct']
ftuples = [('Durchschnitt', 'mean'), ('Abweichung', np.var)]
print grouped['tip_pct', 'total_bill'].agg(ftuples)
grouped.agg({'tip' : np.max, 'size' : 'sum'})
grouped.agg({'tip_pct' : ['min', 'max', 'mean', 'std'],
             'size' : 'sum'})

### Returning aggregated data in \unindexed\ form
print tips.groupby(['sex', 'smoker'], as_index=False).mean()


## Group-wise operations and transformations
print df
k1_means = df.groupby('key1').mean().add_prefix('mean_')
print k1_means
pd.merge(df, k1_means, left_on='key1', right_index=True)

key = ['one', 'two', 'one', 'two', 'one']
people.groupby(key).mean()
people.groupby(key).transform(np.mean)
def demean(arr):
    return arr - arr.mean()
demeaned = people.groupby(key).transform(demean)
print demeaned
print demeaned.groupby(key).mean()

### Apply: General split-apply-combine
def top(df, n=5, column='tip_pct'):
    return df.sort_index(by=column)[-n:]
print top(tips, n=6)
tips.groupby('smoker').apply(top)
print tips.groupby(['smoker', 'day']).apply(top, n=3, column='total_bill')
result = tips.groupby('smoker')['tip_pct'].describe()
# print result
# print result.unstack('smoker')
f = lambda x: x.describe()
# print grouped.apply(f)

#### Suppressing the group keys
tips.groupby('smoker', group_keys=False).apply(top)

### Quantile and bucket analysis
frame = DataFrame({'data1': np.random.randn(1000),
                   'data2': np.random.randn(1000)})
factor = pd.cut(frame.data1, 4)
factor[:10]
def get_stats(group):
    return {'min': group.min(), 'max': group.max(),
            'count': group.count(), 'mean': group.mean()}

grouped = frame.data2.groupby(factor)
grouped.apply(get_stats).unstack()

#ADAPT the output is not sorted in the book while this is the case now (swap first two lines)
# Return quantile numbers
grouping = pd.qcut(frame.data1, 10, labels=False)

grouped = frame.data2.groupby(grouping)
grouped.apply(get_stats).unstack()
### Example: Filling missing values with group-specific values
s = Series(np.random.randn(6))
s[::2] = np.nan
s
s.fillna(s.mean())
states = ['Ohio', 'New York', 'Vermont', 'Florida',
          'Oregon', 'Nevada', 'California', 'Idaho']
group_key = ['East'] * 4 + ['West'] * 4
data = Series(np.random.randn(8), index=states)
data[['Vermont', 'Nevada', 'Idaho']] = np.nan
data
data.groupby(group_key).mean()
fill_mean = lambda g: g.fillna(g.mean())
data.groupby(group_key).apply(fill_mean)
fill_values = {'East': 0.5, 'West': -1}
fill_func = lambda g: g.fillna(fill_values[g.name])

data.groupby(group_key).apply(fill_func)

### Example: Random sampling and permutation

