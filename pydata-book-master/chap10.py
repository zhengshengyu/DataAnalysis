#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np
pd.options.display.max_rows = 12
np.set_printoptions(precision=4, suppress=True)
import matplotlib.pyplot as plt
plt.rc('figure', figsize=(12, 4))

# Time series
## Date and Time Data Types and Tools
from datetime import datetime
now = datetime.now()
delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)

from datetime import timedelta
start = datetime(2011, 1, 7)
end = start + timedelta(12)

### Converting between string and datetime
stamp = datetime(2011, 1, 3)
#### str strftime
print str(stamp)
print stamp.strftime('%Y-%m-%d')
#### strptipme
value = '2011-4-28'
print datetime.strptime(value, '%Y-%m-%d')
datestrs = ['7/6/2011', '8/6/2011']
print [datetime.strptime(x, '%m/%d/%Y') for x in datestrs]
#### 第三方包的parse
from dateutil.parser import parse
parse('2011-01-03')
parse('Jan 31, 1997 10:45 PM')
parse('6/12/2011', dayfirst=True)
#### to_datetime
print pd.to_datetime(datestrs)
idx = pd.to_datetime(datestrs + [None])
print idx

## Time Series Basics
dates = [datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7),
         datetime(2011, 1, 8), datetime(2011, 1, 10), datetime(2011, 1, 12)]
ts = Series(np.random.randn(6), index=dates)
print ts
print ts + ts[::2]
print ts.index.dtype
### Indexing, selection, subsetting
print ts[ts.index[2]]
print ts['1/10/2011']
print ts['2011']
print ts[datetime(2011, 1, 7):]
print ts['1/5/2011':'1/10/2011']
print ts.truncate(after='1/9/2011')
print ts.truncate(before='1/9/2011')

longer_ts = Series(np.random.randn(1000),
                   index=pd.date_range('1/1/2000', periods=1000))
# print longer_ts
# print longer_ts['2001']
# print longer_ts['2001-01']
# print longer_ts[datetime(2011, 1, 7):] # No
print longer_ts.truncate(after='1/10/2000') # Yes

dates = pd.date_range('1/1/2000', periods=100, freq='W-WED')
long_df = DataFrame(np.random.randn(100, 4),
                    index=dates,
                    columns=['Colorado', 'Texas', 'New York', 'Ohio'])
print long_df.ix['5-2001']
### Time series with duplicate indices
dates = pd.DatetimeIndex(['1/1/2000', '1/2/2000', '1/2/2000', '1/2/2000',
                          '1/3/2000'])
dup_ts = Series(np.arange(5), index=dates)
print dup_ts.index.is_unique
print dup_ts
print dup_ts['1/2/2000']  # duplicated
print dup_ts['1/3/2000']  # not duplicated
grouped = dup_ts.groupby(level=0)
print grouped.count()

## Date ranges, Frequencies, and Shifting
print ts
print ts.resample('D')
### Generating date ranges
print pd.date_range(start='4/1/2012', periods=10)
print pd.date_range(end='4/1/2012', periods=10)
print pd.date_range('1/1/2000', '12/1/2000', freq='BM') #business end of month
print pd.date_range('5/2/2012 12:56:31', periods=5, freq='3D', normalize=True)
### Frequencies and Date Offsets
from pandas.tseries.offsets import Hour, Minute
hour = Hour()
print hour
four_hours = Hour(4)
print four_hours
print Hour(2) + Minute(30)
print pd.date_range('1/1/2000', '1/2/2000 23:59', freq='3H30MIN')
rng = pd.date_range('1/1/2012', '9/1/2012', freq='WOM-3FRI')
### Shifting (leading and lagging) data
ts = Series(np.random.randn(6),
            index=pd.date_range('1/1/2000', periods=6, freq='B'))
print ts
print ts.shift(2, freq='D')
#### Shifting dates with offsets
from pandas.tseries.offsets import Day, MonthEnd
now = datetime(2011, 11, 17)
print now + 3 * Day()
print now + MonthEnd()
offset = MonthEnd()
print offset.rollforward(now), offset.rollback(now)
ts = Series(np.random.randn(20),
            index=pd.date_range('1/15/2000', periods=20, freq='4d'))
print ts.groupby(offset.rollforward).mean()
print ts.resample('M', how='mean')

## Time Zone Handling
import pytz
print pytz.common_timezones[-12:]
print pytz.timezone('US/Eastern')
### Localization and Conversion
rng = pd.date_range('3/9/2012 9:30', periods=6, freq='D')
ts = Series(np.random.randn(len(rng)), index=rng)
print(ts.index.tz)
ts_utc = ts.tz_localize('UTC')
print ts_utc
ts_eastern = ts.tz_localize('US/Eastern')
print ts_eastern.tz_convert('UTC')
print ts_eastern.tz_convert('Europe/Berlin')
print ts.index.tz_localize('Asia/Shanghai')
### Operations with time zone-aware Timestamp objects
stamp = pd.Timestamp('2011-03-12 04:00')
stamp_utc = stamp.tz_localize('utc')
print stamp_utc, stamp_utc.value
print stamp_utc.tz_convert('US/Eastern'), stamp_utc.tz_convert('US/Eastern').value
stamp_moscow = pd.Timestamp('2011-03-12 04:00', tz='Europe/Moscow')
print stamp_moscow, stamp_moscow.value

# 30 minutes before DST transition
from pandas.tseries.offsets import Hour
stamp = pd.Timestamp('2012-03-12 01:30', tz='US/Eastern')
print stamp, stamp + 2*Hour()

### Operations between different time zones
rng = pd.date_range('3/7/2012 9:30', periods=10, freq='B')
ts = Series(np.random.randn(len(rng)), index=rng)
print ts
ts1 = ts[:7].tz_localize('Europe/London')
ts2 = ts1[2:].tz_convert('Europe/Moscow')
print ts1
print ts2
result = ts1 + ts2
print result
print result.index

## Periods and Period Arithmetic
p = pd.Period(2007, freq='A-DEC')
print p
print pd.Period('2017', freq='A-DEC') - p
rng = pd.period_range('1/1/2000', '6/30/2000', freq='M')
print Series(np.random.randn(6), index=rng), type(rng)

values = ['2001Q3', '2002Q2', '2003Q1']
index = pd.PeriodIndex(values, freq='Q-DEC')
print index

### Period Frequency Conversion
p = pd.Period('2007', freq='A-DEC')
print p
print p.asfreq('M', how='start')
print p.asfreq('M', how='end')
p = pd.Period('2007', freq='A-JUN')
print p.asfreq('M', 'start')
print p.asfreq('M', 'end')