# **Finviz API**

## **Description**
A modular python API to collect stock data from Finviz.com, by a sets of performance metrics, in order to create ranked lists of stocks that match the investment styles:  Value, Growth, Dividend and Momentum and write respective output files as Excel files.

## **Overview of API**
Finviz.com is a popular research site for active investors and traders.  The site provides the ability to drill-in to individual stocks to evaluate them and their performance.  It allows its users to specify different characteristics they are looking for to find a list of stocks that might be of specific interest to the user. 

A user can go to the screener menu and choose from approximately 150 different performance metrics and a list of stocks that match the criteria are presented.  The user can then export the list to a .csv file for further personal review of the resultant list.

==Why this API, you might ask?==  Finviz has a limitation in that the more attributes you select to build your list from, the fewer stocks that might be presented to you in the resultant list.  It is possible to want to see a list of stocks that meet thresholds in 10, 15, 20, or even all the way up to 150 of the possible metrics.  Depending on how conservative or liberal of thresholds one sets for each metric, will determine how many stocks are returned in the list.  If conservative thresholds are set, for example a P/E ratio under a conservative number, along with conversative thresholds for other metrics, a likely outcome is a listing of zero stocks that match.

This api solves for this situation allowing the user to set as many metrics with conservative thresholds as desired and it iterates through every stock ticker and counts how many metrics and thresholds the stock is a match for.  Stocks that match the highest number of metric thresholds would be valued more so than stocks that match fewere number of metric thresholds.  The user then gets to see a full list of all stock tickers, ranked by the matched count of specified metrics and thresholds.

But what if one metric and it's threshold is of greater importance than other metrics and their thresholds?  This api allows the user to put a weight on the thresholds and it generates a score for each stock ticker based on this weightings for the matched metrics.

Lastly, this API then sorts the output first by Score and Count and then by the highest weighted metrics so the stocks that match in the most desired manner, rise to the top of the list.

## **Modules**
This API is constructed in a modular fashion involving 3 separate python files:
1. models.py
2. file_downloader.py
3. processing_models.py

### models.py
This file is where the model (i.e. they types of stocks to pick such as Growth stocks, Value stocks, Dividend stocks or Momentum stocks), the metrics and thresholds and their respective weights, and some information about metric groupings are all specified.

This file leverages python classes for object generation.  models, metric groups and metrics are each class objects established by this file.  This allows any number of models to be specified.  It currently establishes 4 models:  Value, Growth, Dividend and Momentum.

### file_downloader.py
The primary purpose of this file is to download all of the necessary files to generate the final output file.  It imports from models.py a list of models, a variable set in the models.py file.  This list can be modified to increase or decrease the number of models processed.  It also imports from models.py all of the objects, methods of the 3 classes.  Last it imports the finviz generated token and different variables necessary to generate a URL.

This file builds an API link for each metric and threshold specified in the models.py file.  It then downloads from finviz.com a .csv file specific to each metric in the model.  For every metric and threshold specified in the model, it will create a url and download a file consisting of every stock that matches that specific metric and threshold.

### processing_models.py
This module also imports model objects from models.py file, but it's purpose is to concatenate all of the individual metric files into a single output file that counts how many matching metrics each stock is a member of, scores them and ranks them in descending order by score and count.  It additionaly sorts by key weighted metric items.

To produce this output file, it leverages python libraries to read files in a file path specified in the model object, creates an empty dataframe with Pandas libraries and concatenates them all into a single combined dataframe.  Once combined, a python loop will iterate over each stocker in an all_stocks dataframe and create a results dataframe where new columns are created for the count of matching metrics, the stocks score, date of the file run and even a clickable hyperlink for each ticker back to the finviz web site.  Custom data points from finviz are also included in the output file based on those custom columns specified in the manufactured finviz url, taken from the models.py file.

After processing, an excel .xlsx file is generated in the appropriate file path derived from the model class objects.  The user is given the option to delete or retain any of the metric files.  This is so that the user can process the files again if he wanted to change column ordering or sorting priorities and reprocess the files without having to download them again.  Finviz rate limits the API to no more than 1 download per 60 seconds, so not having to download every time you want to reprocess the files is beneficial.

## **Output File(s)**
As mentioned above, the output files are in xlsx format and include all of the ranked and sorted data with one file created for each model in the models.py file.  With this file, the user can then click on the Ticker in the file and pull up the specific ticker charts on Finviz and decide what to do about the stock in question.  With stocks ranked in association with the metrics and thresholds that are important to the user, it becomes a time-saver to go down the list from most interesting stocks to least interesting.
