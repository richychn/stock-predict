#objective: stringing the entire program together 
import extract_stock_ratios as esr
import scrape_macro_features as smf
import scrape_stock_growth as ssg
import companies_by_industry_dict as cbi
import create_industry_csv as cic
import randomforest2 as rf
import neuralnets as nn
import adaboost as ad

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

# def intro(comp):
#     is_here, industry = checkComp(comp)
#     if (is_here):
#         return industry
#     else:
#         return "Job Terminated: Company not found in dataset"

def gather_predict_data(comp):
    """
    This functions also takes in a company ticker as input. Scrapes using 
    functions we wrote in extract_stockratios and scrape_macro_features needed 
    for predicting the input company's annual growth rate  
    """
    now = datetime.datetime.now()
    output = []
    year = now.year 
    predict = {year:0}
    try:
      #stock_growths = ssg.scrape_stock_growth(comp)
      ratios = esr.extract_features(comp, predict)
    except:
      print("error")
      pass
    ur = float(smf.get_ur(2017))#use_macro_csv(year)[0]
    gdp = float(smf.get_gdp(2017))#use_macro_csv(year)[1]
    ratio = ratios[year-1]#[year]
    row = [comp, year-1, ur, gdp]
    #row = [comp, year-1]
    row.extend(ratio)
    if cic.check_na(ratio) < 15: # change NA limit here
        output.append(row)
    return output
    

def alltogether():
    """
    """
    comp = input("What is the company symbol of the company you want to predict?")
    if (checkComp(comp)):
        is_here, industry = checkComp(comp)
        print(industry)
        predict_arr = gather_predict_data(comp)
        predict_arr[0] = predict_arr[0][2:]
        predict_arr = np.asarray(predict_arr)
        tree_score, tprediction = rf.randomforest(industry, predict_arr)
        nn_score, nprediction= nn.neural_network(industry, predict_arr)
        ad_score, adprediction = ad.adaboost(industry, predict_arr)
        # print(nn.neural_network(industry, predict_arr))
        if (tree_score >= nn_score and tree_score >= ad_score):
            print("tree model")
            return tprediction
        elif (nn_score >= tree_score and nn_score >= ad_score):
            print("neural_network model")
            return nprediction
        else:
            print("adaboost model")
            return adprediction
    else:
        print("Job Terminated: Company not found in dataset")
    
    



    

