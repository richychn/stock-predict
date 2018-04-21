import requests
from bs4 import BeautifulSoup
import datetime
from decimal import *

def get_stock_price_page(symbol):
  url = "https://finance.yahoo.com/quote/" + symbol \
      + "/history?period1=1262332800&period2=1514793600&" \
      + "interval=1mo&filter=history&frequency=1mo"
  response = requests.get(url)
  if response.status_code != 404:
    soup = BeautifulSoup(response.text, "lxml")

  return soup

def find_stock_prices(soup):
  stock_prices = {}
  this_year = datetime.datetime.now().year
  table = soup.find('tbody')
  for row in table.find_all('tr'):
    spans = row.find_all('span')
    if len(spans) == 7:
      year = int(row.find_all('span')[0].text[-4:])
      price = Decimal(row.find_all('span')[4].text)
      if year not in stock_prices and year != this_year:
        stock_prices[year] = price
  return stock_prices

def calculate_price_growth(stock_prices):
  stock_growth = {}
  for key in stock_prices:
    if key - 1 in stock_prices:
      stock_growth[key] = growth_calculate(
        stock_prices[key], stock_prices[key-1])
  return stock_growth

def categorize_price_growth(stock_growth):
  categories = {}
  for year in stock_growth:
    categories[year] = define_category(stock_growth[year])
  return categories

def scrape_stock_growth(symbol):
  soup = get_stock_price_page(symbol)
  stock_prices = find_stock_prices(soup)
  stock_growth = calculate_price_growth(stock_prices)
  # growth_categories = categorize_price_growth(stock_growth)
  return stock_growth

def growth_calculate(second, first):
  return (second - first)/first

def define_category(growth):
  if growth < -1:
    return 0
  elif growth < -0.2:
    return 1
  elif growth < 0:
    return 2
  elif growth < 0.2:
    return 3
  elif growth < 1:
    return 4
  else:
    return 5

def main():
  print (scrape_stock_growth("BUFF"))

if __name__ == "__main__":
    main()  # hike!
