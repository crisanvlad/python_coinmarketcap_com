import requests
import json
import operator
from contextlib import redirect_stdout
from pandas import DataFrame

tickerURL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&limit=500'
#https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=0&limit=10&cryptocurrency_type=tokens&convert=USD,BTC


headers = {
 'Accept': 'application/json',
 'Accept-Encoding': 'deflate, gzip',
 'X-CMC_PRO_API_KEY': 'COPY PASTE HERE YOUR COINMARKETCAP API KEY',
}

# making a call to all (creating a dictionary of ticker symbol / name dict_ticker_ratio)
dict_ticker_ratio = {}
dict_ticker_cap = {}
dict_ticker_volume = {}
l_ticker = []
l_ratio = []
l_cap = []
l_vol = []

r = requests.get(tickerURL, headers=headers)

if r.status_code == 200:
   response = json.loads(r.text)
#--------------------------------------Code for Excel files----------------------------------------------------
for x in range(0,500): #hardcoded limit in http link
    ticker = response['data'][x]['name']
    market_cap = response['data'][x]['quote']['USD']['market_cap']
    volume_24h = response['data'][x]['quote']['USD']['volume_24h']
    mcap_div_by_vol = round(float(market_cap) / float(volume_24h),2)
    if ticker is not None and mcap_div_by_vol is not None:
        l_ticker.append(ticker)
        l_ratio.append(mcap_div_by_vol)
        l_cap.append(market_cap/1000000)
        l_vol.append(volume_24h/1000000)

df = DataFrame({'Ticker': l_ticker, 'Ratio': l_ratio,'Market Cap[MM]': l_cap,'Volume24h[MM]': l_vol })
df.to_excel('ratio_list_all.xlsx', sheet_name='All', index=False)
input("Any key to close")
#--------------------------------------END Code for Excel files-------------------------------------------------

#--------------------------------------Code for TXT files-------------------------------------------------------
#for x in range(0,500): #hardcoded limit in http link
#    ticker = response['data'][x]['name']
#    market_cap = response['data'][x]['quote']['USD']['market_cap']
#    volume_24h = response['data'][x]['quote']['USD']['volume_24h']
#    mcap_div_by_vol = round(float(market_cap) / float(volume_24h),2)
#    if ticker is not None and mcap_div_by_vol is not None:
#        string = str(ticker)+"Ratio: "+str(mcap_div_by_vol)+"->Mcap[MM]: "+str(market_cap/1000000)+"->Vol24[MM]: "+str(volume_24h/1000000)
#        dict_ticker_ratio[ticker] = mcap_div_by_vol
#        dict_ticker_cap[ticker] = round(float(market_cap),2)/1000000
#        dict_ticker_volume[ticker] = round(float(volume_24h),2)/1000000


#sorted_dict_ticker_ratio = sorted(dict_ticker_ratio.items(), key=operator.itemgetter(1))
#sorted_dict_ticker_cap = sorted(dict_ticker_cap.items(), key=operator.itemgetter(1))
#sorted_dict_ticker_vol = sorted(dict_ticker_volume.items(), key=operator.itemgetter(1))


#Print all sorted ratios to a file
#with open('ratio_list_all.txt', 'w') as f:
#    with redirect_stdout(f):
#        for ticker,ratio in sorted_dict_ticker_ratio:
#            print (ticker, "->", ratio)

#Print top 100 sorted ratios to a file
#counter = 0
#with open('top_100_ratios.txt', 'w') as f:
#    with redirect_stdout(f):
#        for ticker,ratio in sorted_dict_ticker_ratio:
#            for ticker2,cap in sorted_dict_ticker_cap:
#                if ticker == ticker2:
#                    for ticker3, vol in sorted_dict_ticker_vol:
#                        if ticker == ticker3:
#                            if counter <= 100:
#                                print (ticker, "Ratio: ", ratio,"->Mcap[MM]: ", cap, "->Vol24[MM]: ", vol)
#                                counter = counter + 1
#--------------------------------------END Code for TXT files-------------------------------------------------------
