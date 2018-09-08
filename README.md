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
<img width="546" alt="screen shot 2018-09-07 at 5 12 53 pm" src="https://user-images.githubusercontent.com/36837456/45248545-fd6f5200-b2c6-11e8-8b3e-91dc8d2e78f9.png">
2. Run alltogether.py and the alltogether(), then the terminal will promote you to type in the symbol of the company you like to predict. For example I chose Delta Airline above
<img width="522" alt="screen shot 2018-09-07 at 5 14 58 pm" src="https://user-images.githubusercontent.com/36837456/45248625-512e6b00-b2c8-11e8-8b14-af1276a87213.png">
3. The program will start to print out a lot of things, indicating that the program is running correctly. Note the first line says “Transportation.” This means that we have found Delta to be apart of Transportation Industry and thus will use all transportation companies’s data for prediction. The list here following it are just features 
<img width="490" alt="screen shot 2018-09-07 at 5 13 19 pm" src="https://user-images.githubusercontent.com/36837456/45248598-c3eb1680-b2c7-11e8-88b2-418849d96ef0.png">
4. Then the program would run several ML algorithms (Random forest, decision, addabost..) and use the algorithm with the highest prediction score to predict next year’s annual growth rate. The above is printout that the Random Forest has started running.
<img width="549" alt="screen shot 2018-09-07 at 5 14 31 pm" src="https://user-images.githubusercontent.com/36837456/45248603-dfeeb800-b2c7-11e8-87f5-86d14fbcbe99.png">
5. After running all the ML algorithms, it will print out the highest confidence score produced from all the algorithm. So in the above case, the highest confidence score for Delta is ~0.72 and the result is 1 (1 means stock annual growth rate will increase by 10% or more, -1 means stock annual growth rate will decrease by 10% or more, 0 is everything in between) 
<img width="559" alt="screen shot 2018-09-07 at 5 15 47 pm" src="https://user-images.githubusercontent.com/36837456/45248636-80dd7300-b2c8-11e8-96a8-b0166f6a7efc.png">

## Webapp *everything else work the same, but on a webapp with better UX
Index page

<img width="696" alt="screen shot 2018-09-07 at 5 33 20 pm" src="https://user-images.githubusercontent.com/36837456/45248642-99e62400-b2c8-11e8-9b7b-b0a788309a5a.png">
Create page

<img width="829" alt="screen shot 2018-09-07 at 5 33 51 pm" src="https://user-images.githubusercontent.com/36837456/45248646-b1bda800-b2c8-11e8-9cdb-d2eb9455916c.png">
Show page

<img width="643" alt="screen shot 2018-09-07 at 5 34 07 pm" src="https://user-images.githubusercontent.com/36837456/45248654-bc783d00-b2c8-11e8-8480-f985ec8ba19a.png"> 
 


