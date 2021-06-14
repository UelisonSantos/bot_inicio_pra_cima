#import yfinance as yf
import json
import time
import requests
#import mysql.connector
#try:
#  mydb = mysql.connector.connect(
#    host="localhost",
#    user="yourusername",
 #   password="yourpassword"
#  )
#  print(mydb)
#except:
#  print("Error connecting DB.")

'''
stock = yf.Ticker("BTOW3.SA")
#print(stocks.tickers)
stockinfo = stock.info
print(str(stockinfo['symbol']) + " : " + str(stockinfo['regularMarketPrice']))

stock = yf.Ticker("LAME4.SA")
stockinfo = stock.info
print(str(stockinfo['symbol']) + " : " + str(stockinfo['regularMarketPrice']))

stock = yf.Ticker("OIBR3.SA")
stockinfo = stock.info
print(str(stockinfo['symbol']) + " : " + str(stockinfo['regularMarketPrice']))

stock = yf.Ticker("^BVSP")
stockinfo = stock.info
print(str(stockinfo['symbol']) + " : " + str(stockinfo['regularMarketPrice']))
'''

    
response = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/PETR4.SA?modules=price")
#print(response)
result_json = response.json()
price = result_json['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw']
#timestamp = result_json['quoteSummary']['result'][0]['price']['regularMarketTime']
#timehuman = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(timestamp))
#print(result_json)
print(price)

#https://query1.finance.yahoo.com/v8/finance/chart/BTOW3.SA
#https://query1.finance.yahoo.com/v10/finance/quoteSummary/BTOW3.SA?modules=price
'''
inputs for the ?modules= query:

    [
       'assetProfile',
       'summaryProfile',
       'summaryDetail',
       'esgScores',
       'price',
       'incomeStatementHistory',
       'incomeStatementHistoryQuarterly',
       'balanceSheetHistory',
       'balanceSheetHistoryQuarterly',
       'cashflowStatementHistory',
       'cashflowStatementHistoryQuarterly',
       'defaultKeyStatistics',
       'financialData',
       'calendarEvents',
       'secFilings',
       'recommendationTrend',
       'upgradeDowngradeHistory',
       'institutionOwnership',
       'fundOwnership',
       'majorDirectHolders',
       'majorHoldersBreakdown',
       'insiderTransactions',
       'insiderHolders',
       'netSharePurchaseActivity',
       'earnings',
       'earningsHistory',
       'earningsTrend',
       'industryTrend',
       'indexTrend',
       'sectorTrend']
'''   