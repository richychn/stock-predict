import requests
import string
import json
import numpy
import decimal
from bs4 import BeautifulSoup

def get_observation_ur(industry, year):
  key = "89c89a90854ea7514f605a1af848a7f6"
  series = ur_industries(industry)
  url = "https://api.stlouisfed.org/fred/series/observations?series_id=" \
      + series + "&api_key=" + key + "&file_type=json"
  result = requests.get(url)
  data = result.json()
  ret = 0
  count = 0
  for ob in data['observations']:
    if str(ob['date'][0:4]) == str(year):
      ret += decimal.Decimal(ob['value'])
      count += 1
  return ret / count

def get_observation_gdp(industry, year):
  key = "89c89a90854ea7514f605a1af848a7f6"
  series = ur_industries(industry)
  url = "https://api.stlouisfed.org/fred/series/observations?series_id=" \
      + series + "&api_key=" + key + "&file_type=json"
  result = requests.get(url)
  data = result.json()
  ret = 0
  for ob in data['observations']:
    if str(ob['date'][0:4]) == str(year):
      ret += decimal.Decimal(ob['value'])
  return ret

def ur_industries(industry):
  industries = {"manufacturing": "LNU04032232",
          "constructing": "LNU04032231",
          "finance": "LNU04032238",
          "business": "LNU04032239",
          "agriculture": "LNU04035109",
          "mining": "LNU04032230",
          "trade": "LNU04032235",
          "information": "LNU04032237",
          "education": "LNU04032240",
          "transportation": "LNU04032236"
          }
  return industries[industry]

def gdp_industries(industry):
  industries = {"manufacturing": "USMANRQGSP",
          "constructing": "USCONSTRQGSP",
          "finance": "USFININSRQGSP",
          "business": "USPROSCITCHRQGSP",
          "agriculture": "USAGRRQGSP",
          "mining": "USMINRQGSP",
          "retail": "USRETAILRQGSP",
          "wholesale": "USWHOLERQGSP",
          "information": "USINFORQGSP",
          "education": "USHLTHSOCASSRQGSP",
          "transportation": "USTRANSWARERQGSP"
          }
  return industries[industry]

def main():
  print(get_observation_gdp("mining", 2009))

if __name__ == "__main__":
    main()  # hike!
