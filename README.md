# stock-predict (Money Learn aka ML)
## Overview
The goal of our project is to predict whether a stock price would increase or not in the following year using only financial & accounting metrics. This project has two forms: 1) the master branch of the project include the python backend, which includes web scraping and ML files 2) The webapp branch include everything from the master branch plus the ruby on rails framework and additional codes that link python to ruby.
## Python Backend -- master branch
This branch essentially includes all the operations of the program written in python. Files here each serve functions, like web scrapping, data handling, generating proper datasets, machine learning algorithms, and error analysis.

Files Included:
Some important sub folders includes: goodmorning, Exchanges, IndustryCSV, Industry_Results, and. Goodmorning is a python module we found online that assisted us tremendous in webscrapping. Exchanges and industryCSV are raw data csv’s generated from webscraping. Lastly, Industry_results includes all post-data-handling csv datasets ready to be used for machine learning analysis.

Aside from alltogether.py, every python file of the rest not included in a subfolder each has a narrow yet specific role in achieving a specific functionality. For example, extract_stock_ratios.py is the major function in webscrapping a company’s accounting data as features. Many files build on top of each other to work. 

At the end, alltogether.py serves as the main function that links everything together into a one-method/input user facing method. 

To Run in Ipython interpreter:
-require ipython; libraries: csv, sklearn, numpy, panda, math 
Unzip folder 
cd into root folder 
Ipython 
Run alltogether.py 
alltogether() → then there will be a prompt into the terminal for you to put in company ticker
Then everything will be taken care of in the terminal
Last line printed is the result *in array form, [best ml model, confidence score, result in categories] 
Result categories: 1(10%growth or more) 0(price stay the same) -1(-10%growth or less)

## Webapp
This branch of the the project is a ruby on rails application (without DB) that uses the above python backend. It includes all the fundamental rails files as well as a modified version of the python backend file shown in form one. 

Files Included:
All of the python backend files are included in the root folder of this project as well as essential rails folders like app, config, db, etc. Some major files of functions are: controller folder, view folder within app. 

To Run: 
Require everything stated in requirement above, has to have Ipython working + all ruby on rails programs (ex. Ruby with version2.3 or above, rails gem, and other related files) 
Unzip the file 
rails db:create //this creates a empty table in database
rails db:migrate //this creates a table for the model 
Rails s 
Go to browser and open http://localhost:3000/predictions/ 

# RESULTS
## Python Backend
1. Start Ipython

2. Run alltogether.py and the alltogether(), then the terminal will promote you to type in the symbol of the company you like to predict. For example I chose Delta Airline above

3. The program will start to print out a lot of things, indicating that the program is running correctly. Note the first line says “Transportation.” This means that we have found Delta to be apart of Transportation Industry and thus will use all transportation companies’s data for prediction. The list here following it are just features 

4. Then the program would run several ML algorithms (Random forest, decision, addabost..) and use the algorithm with the highest prediction score to predict next year’s annual growth rate. The above is printout that the Random Forest has started running.

5. After running all the ML algorithms, it will print out the highest confidence score produced from all the algorithm. So in the above case, the highest confidence score for Delta is ~0.72 and the result is 1 (1 means stock annual growth rate will increase by 10% or more, -1 means stock annual growth rate will decrease by 10% or more, 0 is everything in between) 

## WebApp: *everything else work the same, but on a webapp with better UX
