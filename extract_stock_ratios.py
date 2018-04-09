import numpy as np
import pandas as pd
import good_morning as gm
import math



def get_years(yrs_dict):
    """
    """
    arr_years = []
    for key in yrs_dict:
        k = key - 1
        arr_years.append(k)  
    return arr_years

def get_yr_pos(year,kr_all):
    """
    """
    #year_str = str(year)
    page = kr_all[1]
    years = page.columns
    year_pos = 0
    for period in years:
        yr = period.year
        if (yr == year):
            return year_pos
        year_pos += 1
    return "error"

def extract_features(symbol, yrs_dict):
    """
    """
    if (symbol.isupper()):
        kr = gm.KeyRatiosDownloader()
        kr_all = kr.download(symbol)
        return_dict = {}

        arr_years = get_years(yrs_dict)
        for y in arr_years:
            yp = get_yr_pos(y,kr_all)
            feature_list = []
            for page in kr_all[1:]:
                f_add = page.as_matrix()[:,yp].tolist()
                feature_list.extend(f_add)
            return_dict[y] = feature_list
        clean_dict(return_dict)
        return return_dict

def clean(f_list):
    arr = np.asarray(f_list)
    delete_index = [0,1,3,4,5,7,9,10,12,16,18,19,20,22,23,24,26,27,28,30,31,32,33,36,37,38,39,40,41,43,44,45,46,47,48,49,50,51,53,54,56,57,60,63,65,67]
    clean_arr = np.delete(arr, delete_index)
    clean_list = clean_arr.tolist()

    return clean_list


def clean_dict(pre_dict):
    """
    """
    #final_dict = {}
    for key in pre_dict:
        #final_dict[key] = clean(pre_dict[key])
        pre_dict[key] = clean(pre_dict[key])
    return pre_dict


def main():

    kr = gm.KeyRatiosDownloader()
    yrs_dict = {2014:1,2015:2,2016:3,2017:4}
    Apple_features = extract_features('AAPL', yrs_dict)
    print(Apple_features)

if __name__ == "__main__":
    main()  # hike!
