import extract_stock_ratios as esr
import scrape_macro_features as smf
import scrape_stock_growth as ssg
import csv

def test_industry(industry):
  dictionary = {'finance': ['PIH', 'PIHPP', 'TURN', 'FCCY', 'SRCE', 'ABM'],
                'transportation': ['AIRT', 'ATSG', 'ALK', 'AAL', 'ARCB']}
  return dictionary[industry]

def list_of_rows(industry):
  rows = []
  for comp in test_industry(industry):
    stock_growths = ssg.scrape_stock_growth(comp)
    ratios = esr.extract_features(comp, stock_growths)
    for year in ratios:
      if industry == 'wholesale' || industry == 'retail':
        ur = smf.get_ur('trade', year)
      else:
        ur = smf.get_ur(industry, year)
      gdp = smf.get_gdp(industry, year)
      ratio = ratios[year]
      growth = stock_growths[year + 1]
      row = [comp, year, ur, gdp]
      row.extend(ratio)
      row.append(growth)
      rows.append(row)
  return rows

def create_industry_csv(industry, filename):
  csvfile = open(filename, "w", newline='' )
  filewriter = csv.writer( csvfile, delimiter=",")
  for row in list_of_rows(industry):
      filewriter.writerow( row )
  csvfile.close()
