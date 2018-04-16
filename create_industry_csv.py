import extract_stock_ratios as esr
import scrape_macro_features as smf
import scrape_stock_growth as ssg
import companies_by_industry_dict as cbi
import math
import csv

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
    try:
      stock_growths = ssg.scrape_stock_growth(comp)
      ratios = esr.extract_features(comp, stock_growths)
    except:
      continue
    for year in ratios:
      ur = smf.get_ur(year)
      gdp = smf.get_gdp(year)
      ratio = ratios[year]
      growth = stock_growths[year + 1]
      row = [comp, year, ur, gdp]
      row.extend(ratio)
      row.append(growth)
      if check_na(ratio) < 15: # change NA limit here
        rows.append(row)
  return rows

def create_industry_csv(industry):
  csvfile = open(industry + ".csv", "w", newline='' )
  filewriter = csv.writer(csvfile, delimiter=",")
  for row in list_of_rows(industry):
      filewriter.writerow( row )
  csvfile.close()

# create_industry_csv("Finance")
test_industry("Finance")

for ind in cbi.final_industry_dict().keys():
  create_industry_csv(ind)
