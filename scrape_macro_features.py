import requests
from bs4 import BeautifulSoup

def get_observation_ur(industry, year):
  key = "89c89a90854ea7514f605a1af848a7f6"
  series = ur_industries[industry]
  url = "https://api.stlouisfed.org/fred/series/observations?series_id=" \
      + series + "&api_key=" + key + "&file_type=json"

def ur_industries():
  return {"manufacturing": "LNU04032232",
          "constructing": "LNU04032231",
          "finance": "LNU04032238",
          "business": "LNU04032239",
          "agriculture": "LNU04035109",
          "mining": "LNU04032230",
          "trade": "LNU04032235",
          "information": "LNU04032237",
          "education": "LNU04032240",
          "government": "LNU04028615",
          "other": "LNU04032242",
          "transportation": "LNU04032236"
          }
