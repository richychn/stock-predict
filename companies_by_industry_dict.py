import csv

def readcsv( csv_file_name ):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open( csv_file_name, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object

        all_rows = []                               # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append( row )                  # adds only the word to our list

        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        return all_rows                              # return the list of lists

    except FileNotFoundError as e:
        print("File not found: ", e)
        return []

#
# write_to_csv shows how to write that format from a list of rows...
#  + try   write_to_csv( [['a', 1 ], ['b', 2]], "smallfile.csv" )
#
def write_to_csv( list_of_rows, filename ):
    """ write_to_csv shows how to write that format from a list of rows...
#  + try   write_to_csv( [['a', 1 ], ['b', 2]], "smallfile.csv" )
    """
    try:
        csvfile = open( filename, "w", newline='' )
        filewriter = csv.writer( csvfile, delimiter=",")
        for row in list_of_rows:
            filewriter.writerow( row )
        csvfile.close()

    except:
        print("File", filename, "could not be opened for writing...")

# ### New Methods 
# def get_subsector_names(filename, subsector_list):
#     """
#     """
#     #subsector_list = []
#     allRows = readcsv(filename)
#     allComps = allRows[1:]
#     for comp in allComps:
#         subsector = comp[6] #7 for industry csv
#         if subsector not in subsector_list:
#             subsector_list.append(subsector)

# def generate_subsectorList_csv():
#     """
#     """
#     subsector_list = []
#     get_subsector_names("NASDAQALL.csv", subsector_list)
#     get_subsector_names("NYSEALL.csv", subsector_list)
#     get_subsector_names("AMEXALL.csv", subsector_list)
#     final_subsector_list = []
#     for sub in subsector_list:
#         final_subsector_list.append([sub])
#     write_to_csv(final_subsector_list, "subsectorList.csv")

# def generate_subsector_dict(filename):
#     """
#     """
#     subsector_dict = {}
#     sub_and_ind = readcsv(filename)
#     for line in sub_and_ind:
#         sub_name = line[0]
#         ind_name = line[1]
#         if (ind_name not in subsector_dict.keys()):
#             subsector_dict[ind_name] = []
#         subsector_dict[ind_name].append(sub_name)
#     return subsector_dict


# #manual step: categorize what subsectors fall under what FRED Industires 
# #return a dictionary of Fred industries as keys, and corresponding subsectors as key values 
# def locate_industry(subsector_dict, comp_sub):
#     """
#     """
#     for industry_name in subsector_dict:
#         if (comp_sub in subsector_dict[industry_name]):
#             return industry_name
#     return False

# def generate_final_dict(subsector_dict):
#     """
#     """
#     final_dict = {}
#     for key in subsector_dict:
#         final_dict[key] = []
#     return final_dict

# example_sd = {"manufacturing": ["Industrial Machinery/Components", "Major Pharmaceuticals"],
#     "finance": ["Oil Refining/Marketing"],
#     "agriculture":["Diversified Commercial Services"],
#     "n/a":["n/a"]}

# def final_dict_helper(subsector_dict, industry_csv, final_dict):
#     """
#     """
#     allRows = readcsv(industry_csv)
#     allComps = allRows[1:]
#     for comp in allComps:
#         comp_sub = comp[6] # for industry csv
#         industry_belong = locate_industry(subsector_dict, comp_sub)
#         if (industry_belong != False):
#             comp_symbol = comp[0]
#             final_dict[industry_belong].append(comp_symbol)
#     #return final_dict
# #use final_dict_helper(example_sd, "example_industry.csv", finalD) and uncomment final_dict to test final_dict_helper
# def final_industry_dict(subsector_dict):
#     """
#     """
#     final_dict = generate_final_dict(subsector_dict)
#     # final_dict_helper(subsector_dict, "Finance.csv", final_dict)
#     # final_dict_helper(subsector_dict, "BasicIndustry.csv", final_dict)
#     # final_dict_helper(subsector_dict, "HealthCare.csv", final_dict)
#     # final_dict_helper(subsector_dict, "Miscellaneous.csv", final_dict)
#     # final_dict_helper(subsector_dict, "PublicUtilities.csv", final_dict)
#     # final_dict_helper(subsector_dict, "Technology.csv", final_dict)
#     # final_dict_helper(subsector_dict, "Transporation.csv", final_dict)
#     # final_dict_helper(subsector_dict, "Capital_Goods.csv", final_dict)
#     # final_dict_helper(subsector_dict, "Consumer_nondurables.csv", final_dict)
#     # final_dict_helper(subsector_dict, "Consumer_Services.csv", final_dict)
#     # final_dict_helper(subsector_dict, "Energy.csv", final_dict)
#     final_dict_helper(subsector_dict, "NASDAQALL.csv", final_dict)
#     final_dict_helper(subsector_dict, "NYSEALL.csv", final_dict)
#     final_dict_helper(subsector_dict, "AMEXALL.csv", final_dict)

#     return final_dict

def final_dict_helper(csv, final_dict):
    """
    """
    allRows = readcsv(csv)
    allComps = allRows[1:] #all observations 
    for comp in allComps:
        comp_symbol = comp[0]
        comp_ind = comp[5] # for industry csv
        if (comp_ind not in final_dict.keys()):
            final_dict[comp_ind] = []
            final_dict[comp_ind].append(comp_symbol)
        else:
            final_dict[comp_ind].append(comp_symbol)
    
def final_industry_dict():
    """
    """
    final_industry_dict = {}
    final_dict_helper("Exchanges/NASDAQALL.csv", final_industry_dict)
    final_dict_helper("Exchanges/NYSEALL.csv", final_industry_dict)
    final_dict_helper("Exchanges/AMEXALL.csv", final_industry_dict)

    return final_industry_dict

def dic_to_2darrays(dic):
    """return a 2d array converted from a dictionary 
    """
    list_of_rows = []
    for key in dic:
        list_of_rows += [[key,dic.get(key)]]
    return list_of_rows

def main():
    """ run this file as a script """
    final_dict = final_industry_dict()
    file_array = dic_to_2darrays(final_dict)
    write_to_csv( file_array, "industry_company.csv")

    



# if __name__ == "__main__":
   # main()