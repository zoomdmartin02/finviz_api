# **Finviz API**

## **Description**
A modular python API to collect stock data from Finviz.com, by a sets of performance metrics, in order to create ranked lists of stocks that match the investment styles:  Value, Growth, Dividend and Momentum and write respective output files as Excel files.

## **Overview of API**
Finviz.com is a popular research site for active investors and traders.  The site provides the ability to drill-in to individual stocks to evaluate them and their performance.  The site allows its users to specify different characteristics they are looking for to find a list of stocks that might be of interest to the user. 

A user can go to the screener menu and choose from approximately 150 different performance metrics and a list of stocks that match the criteria are presented.  The user can then export the list to a .csv file for further personal review of the resultant list.

Why this API, you might ask?  Finviz has a limitation in that the more attributes you select to build your list from, the fewer stocks that might be presented to you in the resultant list.  It is possible to want to see a list of stocks that meet thresholds in 10, 15, 20, or even all the way up to 150 of the possible metrics.  Depending on how conservative or liberal of thresholds one sets for each metric, will determine how many stocks are returned in the list.  If conservative thresholds are set, for example a P/E ratio under a conservative number, along with conversative thresholds for other metrics, a likely outcome is a listing of zero stocks that match.

This api solves for this situation allowing the user to set as many metrics with conservative thresholds as desired and it iterates through every stock ticker and counts how many metrics and thresholds the stock is a match for.  Stocks that match the highest number of metric thresholds would be valued more so than stocks that match fewere number of metric thresholds.  The user then gets to see a full list of all stock tickers, ranked by the matched count of specified metrics and thresholds.

But what if one metric and it's threshold is of greater importance than other metrics and their thresholds?  This api allows the user to put a weight on the thresholds and it generates a score for each stock ticker based on this weightings for the matched metrics.

Lastly, this API then sorts the output first by Score and Count and then by the highest weighted metrics so the stocks that match in the most desired manner, rise to the top of the list.

## **Modules**


## **Output File**

