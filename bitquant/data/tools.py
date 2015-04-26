from pandas.tseries.tools import to_datetime
from time import mktime
from datetime import datetime

#|Create datetime index for DataFrame using "timestamp" column
def date_index(df):
    date = df['timestamp']
    date = to_datetime(date, unit='s')
    df['date'] = date
    df = df.set_index('date')
    return df

#|Convert datetime sting (format: mm/dd/yy) to timestamp
def dateconv(date):
    try:
        date = datetime.strptime(date, "%m/%d/%y")
    except:
        date = datetime.strptime(date, "%Y-%m-%d")
    timestamp = int(mktime(date.timetuple()))	
    return timestamp