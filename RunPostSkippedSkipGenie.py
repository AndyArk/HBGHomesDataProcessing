# Andrew Ark
# HBG Homes
# 7/9/2022

# Takes 3 inputs:
# A file exported from REISift containing data not yet skiptraces
# The file returned by SkipGenie containing skiptraced data in the Horizontal Format
# The file returned by SkipGenie containing data that SkipGenie failed to find information for

# Returns:
# One file containing the failed skiptrace data with property addresses added
# One file containing the succesful skiptrace with property addresses added,
# columns for mobile phone types added, Lists column added, and deceased
# altered to allow proper reupload into REISift

# If using outside of HBGHomes, make sure to change name of lists to whatever Lists you use in Sift
# Also change default file paths, or delete entirely if files are in same folder as script

import pandas as pd

# Import Files
skipped_path = r'C:\Users\gark\Documents\HBGHomes_files\Skipped\SkipGenie\\'
unskipped_path = r'C:\Users\gark\Documents\HBGHomes_files\UnSkipped Data\\'
failed_path = r'C:\Users\gark\Documents\HBGHomes_files\Skipped\SkipGenie\Failed\\'

skipped_file = input('Skipped File name: ')
unskipped_file = input('UN-Skipped File name: ')
failed_file = input('FAILED Skip File name: ')

skipped_df = pd.read_csv(skipped_path + skipped_file).set_index("INPUT_ADDRESS")
unskipped_df = pd.read_csv(unskipped_path + unskipped_file).set_index("Mailing address")
failed_df = pd.read_csv(failed_path + failed_file).set_index("Address")

# Removes duplicate mailing addresses that prevent indexing
unskipped_df = unskipped_df[~unskipped_df.index.duplicated(keep='first')]

# Change DECEASED to Y
skipped_df.loc[skipped_df['DECEASED']=='DECEASED', 'DECEASED'] = 'y'

# Add Lists
skipped_df.loc[(skipped_df['JUDGMENTS'] > 0) & (skipped_df['BANKRUPTCIES'] == 0) & (skipped_df['LIENS'] == 0), 'Lists'] = 'Judgements'
skipped_df.loc[(skipped_df['JUDGMENTS'] == 0) & (skipped_df['BANKRUPTCIES'] == 0) & (skipped_df['LIENS'] > 0), 'Lists'] = 'Tax Lien (not del)'
skipped_df.loc[(skipped_df['JUDGMENTS'] == 0) & (skipped_df['BANKRUPTCIES'] > 0) & (skipped_df['LIENS'] == 0), 'Lists'] = 'Bankruptcy'
skipped_df.loc[(skipped_df['JUDGMENTS'] > 0) & (skipped_df['BANKRUPTCIES'] > 0) & (skipped_df['LIENS'] > 0), 'Lists'] = 'Judgements, Tax Lien (not del), Bankruptcy'
skipped_df.loc[(skipped_df['JUDGMENTS'] == 0) & (skipped_df['BANKRUPTCIES'] > 0) & (skipped_df['LIENS'] > 0), 'Lists'] = 'Tax Lien (not del), Bankruptcy'
skipped_df.loc[(skipped_df['JUDGMENTS'] > 0) & (skipped_df['BANKRUPTCIES'] > 0) & (skipped_df['LIENS'] == 0), 'Lists'] = 'Judgements, Bankruptcy'
skipped_df.loc[(skipped_df['JUDGMENTS'] > 0) & (skipped_df['BANKRUPTCIES'] == 0) & (skipped_df['LIENS'] > 0), 'Lists'] = 'Judgements, Tax Lien (not del)'

# Add Phone Types
skipped_df['MobileType1'] = 'MOBILE'
skipped_df['MobileType2'] = 'MOBILE'
skipped_df['MobileType3'] = 'MOBILE'
skipped_df['MobileType4'] = 'MOBILE'

# Add property
skipped_df["Property address"] = unskipped_df["Property address"]
skipped_df["Property state"] = unskipped_df["Property state"]
skipped_df["Property zip"] = unskipped_df["Property zip"]
skipped_df["Property city"] = unskipped_df["Property city"]
skipped_df["Property county"] = unskipped_df["Property county"]

failed_df["Property address"] = unskipped_df["Property address"]
failed_df["Property state"] = unskipped_df["Property state"]
failed_df["Property zip"] = unskipped_df["Property zip"]
failed_df["Property city"] = unskipped_df["Property city"]
failed_df["Property county"] = unskipped_df["Property county"]

# Export Files
skipped_df.to_csv(skipped_file + 'CLEAN' + '.csv')
failed_df.to_csv(failed_filed + 'CLEAN' + '.csv')
