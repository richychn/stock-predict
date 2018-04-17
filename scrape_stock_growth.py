import requests
from bs4 import BeautifulSoup
import datetime
from decimal import *

def get_stock_price_page(symbol):
  url = "https://finance.yahoo.com/quote/" + symbol \
      + "/history?period1=1325404800&period2=1514793600&" \
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

def scrape_stock_growth(symbol):
  soup = get_stock_price_page(symbol)
  stock_prices = find_stock_prices(soup)
  stock_growth = calculate_price_growth(stock_prices)
  return stock_growth

def growth_calculate(second, first):
  return (second - first)/first

def main():
  print (scrape_stock_growth("DYTL"))

if __name__ == "__main__":
    main()  # hike!
#aefaefefaefaef