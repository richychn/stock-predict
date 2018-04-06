import requests
from bs4 import BeautifulSoup
import datetime
from decimal import *

def get_finance_features_page(symbol):
    url = "http://financials.morningstar.com/ratios/r.html?t=BABA"
    response = requests.get(url)

    if response.status_code == 404:
        print("There was a problem with getting the page")
        #print(color_popularity_url)

    
    url = response.text 
    soup = BeautifulSoup(url,"lxml") 
    return soup

def convert_years(price_dict):
    yearList = []
    for key in price_dict:
        year = key 
        year = year - 1
        yearList.insert(0,year)
    
    return yearList

def year_col_pos(soup, input_yr):
    #table = soup.find_all('div', {'class': "r_header"})
    #table = soup.find_all('div', {'id': "tab_content tab_override"})
    table = soup.find(id = 'financeWrap')
    print(table)
    # t = table.find_all('tr')[1:][1]
    # t_next = t.find_all('td')
    # print(t_next[len(t_next)-1].text)
    # for row in table.find_all('tr'):
    #     print(row.find_all('td'))

    #print(table.find_all('tr'))
    #print(len(table.find_all('tr')))
    #[1].find_all('td'))#.find_all('td')[1].text)
   # print(len(table))
    #years = table.find_all('tr', limit =1)
    # yrs = years.find_all('th')
    # for year_pos in range(len(yrs)):
    #     year = yrs[year_pos][0].text[:4]
    #     if (year.isdigit()):
    #         year = int(year)
    #         if (year == input_yr):
    #             return year_pos

# def find_stock_prices(soup, yrList):
#   stock_prices = {}
#   table = soup.find('tbody')
#   for row in table.find_all('tr'):
#     year = int(row.find_all('span')[0].text[-4:])
#     price = Decimal(row.find_all('span')[4].text)
#     if year not in stock_prices and year != this_year:
#       stock_prices[year] = price
#   return stock_prices

# def calculate_growth(stock_prices):
#   stock_growth = {}
#   for key in stock_prices:
#     if key - 1 in stock_prices:
#       stock_growth[key] = growth_calculate(
#         stock_prices[key], stock_prices[key-1])
#   # early = min(stock_growth.keys())
#   # del stock_growth[early]
#   return stock_growth

# def scrape_stock_growth(symbol):
#   soup = get_stock_page(symbol)
#   stock_prices = find_stock_prices(soup)
#   stock_growth = calculate_growth(stock_prices)
#   return stock_growth

# def growth_calculate(second, first):
#   return (second - first)/first

def main():
    s = get_finance_features_page("BABA")
    #print(s)
   
    year_col_pos(s, 2014)
  #print (scrape_stock_growth("BABA"))

if __name__ == "__main__":
    main()  # hike!