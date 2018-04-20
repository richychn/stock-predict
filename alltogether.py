#objective: stringing the entire program together 
import extract_stock_ratios as esr
import scrape_macro_features as smf
import scrape_stock_growth as ssg
import companies_by_industry_dict as cbi
import create_industry_csv as cic
import csv
import numpy as np
import datetime

def checkComp(comp):
    """
    This function takes in a company ticker as an input. It first checks 
    whether the company ticker exists in any of our datasets. If so, returns
    the industry name the company belongs to. Else, return by saying "company"
    is not found
    """

    industry_dict = cbi.final_industry_dict()
    for ind in industry_dict:
        if (comp in industry_dict[ind]):
            return True, ind
    return False

def intro(comp):
    is_here, industry = checkComp(comp)
    if (is_here):
        return industry
    else:
        return "Job Terminated: Company not found in dataset"

def gather_predict_data(comp):
    """
    This functions also takes in a company ticker as input. Scrapes using 
    functions we wrote in extract_stockratios and scrape_macro_features needed 
    for predicting the input company's annual growth rate  
    """
    now = datetime.datetime.now()
    output = []
    year = now.year - 1 
    predict = {year:0}
    try:
      #stock_growths = ssg.scrape_stock_growth(comp)
      ratios = esr.extract_features(comp, predict)
    except:
      print("error")
      pass
    ur = smf.use_macro_csv(year)[0]
    gdp = smf.use_macro_csv(year)[1]
    ratio = ratios[year]
    row = [comp, year, ur, gdp]
    row.extend(ratio)
    if cic.check_na(ratio) < 15: # change NA limit here
        output.append(row)

    return output

    

