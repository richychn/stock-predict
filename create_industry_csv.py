import extract_stock_ratios as esr
import scrape_macro_features as smf
import scrape_stock_growth as ssg
import companies_by_industry_dict as cbi
import math
import csv
from multiprocessing import Process

def test_industry(industry):
  dictionary = cbi.final_industry_dict()
  return dictionary[industry]

def check_na(array):
  count = 0
  for el in array:
    if math.isnan(float(el)):
      count += 1
  return count

def list_of_rows(industry):
  rows = []
  for comp in test_industry(industry):
    print(len(rows))
    try:
      stock_growths = ssg.scrape_stock_growth(comp)
      ratios = esr.extract_features(comp, stock_growths)
    except:
      print("error")
      continue
    for year in ratios:
      year = year + 1
      if year + 1 in ratios:
        ur = smf.use_macro_csv(year)[0]
        gdp = smf.use_macro_csv(year)[1]
        ratio = ratios[year]
        growth = stock_growths[year + 1]
        lag_growth = stock_growths[year]
        row = [comp, year, ur, gdp]
        row.extend(ratio)
        row.append(lag_growth)
        row.append(growth)
        if check_na(ratio) < 15: # change NA limit here
          rows.append(row)
  return rows

def csv_name(name):
  ret_string = ""
  for let in name:
    if let.isalpha() or let == "-":
      ret_string = ret_string + let
    elif let.isspace():
      ret_string = ret_string + "-"
  return ret_string

def create_industry_csv(industry):
  csvfile = open("IndustryResults/" + csv_name(industry), "w", newline='' )
  filewriter = csv.writer(csvfile, delimiter=",")
  for row in list_of_rows(industry):
      filewriter.writerow( row )
  csvfile.close()

create_industry_csv("Consumer Durables")
# test_industry("Finance")

# for ind in cbi.final_industry_dict().keys():
#   create_industry_csv(ind)
  # print(ind)

#create_industry_csv("Consumer Non-Durables")

