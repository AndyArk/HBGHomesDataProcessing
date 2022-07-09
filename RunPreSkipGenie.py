# Andrew Ark
# HBGHomes
# 7/9/2022

# Takes a file exported from REISift and formats it for SkipGenie

import pandas as pd
from datetime import date

today = date.today()
file = input('What is the path\\file you want to prepare to send to SkipGenie? ')
campaign = input('What campaign is this data for? ')
df = pd.read_csv(file)

df_ready = pd.DataFrame(columns=['LastName','FirstName','MiddleName','Address','City','State','ZipCode','Campaign'])

df_ready['LastName'] = df['Last Name']
df_ready['FirstName'] = df['First Name']
df_ready['Address'] = df['Mailing address']
df_ready['City'] = df['Mailing city']
df_ready['State'] = df['Mailing state']
df_ready['ZipCode'] = df['Mailing zip']
df_ready['Campaign'] = campaign

df_ready.to_csv('C:\\Users\\gark\\Documents\\HBGHomes\\ReadyforSkip\\' + campaign + '-' + str(today) + 'ReadyForSkipGenie'+'.csv', index=False)

