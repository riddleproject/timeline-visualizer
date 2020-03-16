import pandas as pd
from datetime import datetime
import numpy as np

riddles = pd.read_csv('Complete_Menus.csv', index_col=0)

riddles.dropna(subset=["Newspaper Issue Date"], inplace=True)

riddles["Newspaper Issue Date"] = riddles.apply(
    lambda row: datetime.strptime(str(row["Newspaper Issue Date"]), "%Y-%m-%d"),
    axis=1,
)

riddles['Year'] = [date.year for date in riddles['Newspaper Issue Date']]
# riddles['Day of the Year (Publication)'] = [date.strftime('%j') for date in riddles['Newspaper Issue Date']]
# riddles['Weekday (Publication)'] = [date.strftime('%a') for date in riddles['Newspaper Issue Date']]



def guess_date(string):
    string = string.strip()
    if string == 'nan' or string is None:
    	return np.nan
    if '~' in string:
    	string = string[1:]
    for fmt in ["%B %d, %Y", "%B %Y", "%Y-%m-%d", "%d-%b-%y", "%m/%d/%y", '%d-%b-%Y', '%B, %Y', '%Y', '%Y-%m-%d', '%d %B, %Y', '%B, %d %Y', "%Y-%m-%d %X"]:
        try:
            date = datetime.strptime(string, fmt)
            if date.year >= 2000:
                date -= pd.DateOffset(years=100)
            if date.year < 1600:
            	return None
            return date.strftime("%Y-%m-%d")
        except ValueError:
        	continue
    print(string)
    return np.nan


riddles['Event_Date'] = riddles.apply(
    lambda row: guess_date(str(row["Event_Date"])),
    axis=1,
)


riddles = riddles.drop('Year', axis=1).reset_index(drop=True)
riddles.to_csv('/Users/ndrezn/OneDrive - McGill University/Plotly/Intro/Complete_Menus.csv')

exit()


british_late = riddles.loc[('England' in riddles['Location']) & (riddles['Year'] <= 1890) & (riddles['Year'] >= 1895)]

print(british_late)
 