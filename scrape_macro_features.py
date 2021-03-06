import requests
import string
import json
import numpy
import decimal
import csv
from bs4 import BeautifulSoup

def get_ur(year):
  key = "89c89a90854ea7514f605a1af848a7f6"
  url = "https://api.stlouisfed.org/fred/series/observations?series_id=" \
      + "UNRATE" + "&api_key=" + key + "&file_type=json"
  result = requests.get(url)
  data = result.json()
  ret = 0
  count = 0
  for ob in data['observations']:
    if str(ob['date'][0:4]) == str(year):
      ret += decimal.Decimal(ob['value'])
      count += 1
  return ret / count

def get_gdp(year):
  key = "89c89a90854ea7514f605a1af848a7f6"
  url = "https://api.stlouisfed.org/fred/series/observations?series_id=" \
      + "gdp" + "&api_key=" + key + "&file_type=json"
  result = requests.get(url)
  data = result.json()
  ret = 0
  for ob in data['observations']:
    if str(ob['date'][0:4]) == str(year):
      ret += decimal.Decimal(ob['value'])
  return ret

def use_macro_csv(year):
  year = str(year)
  csvfile = open("MacroFeatures.csv", newline='' )
  csvrows = csv.reader( csvfile )
  all_rows = {}
  for row in csvrows:
      all_rows[row[0]] = row[1:]
  if year in all_rows.keys():
    return all_rows[year]
  else:
    csvfile = open("MacroFeatures.csv", "w", newline='' )
    filewriter = csv.writer(csvfile, delimiter=",")
    all_rows[year] = [get_ur(year), get_gdp(year)]
    for year in all_rows:
      filewriter.writerow( [year, all_rows[year][0], all_rows[year][1]] )
  csvfile.close()
  return use_macro_csv(year)

# def main():
#  print(use_macro_csv(2017))

# if __name__ == "__main__":
#     main()  # hike!
