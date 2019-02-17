import requests
import json
import operator
from contextlib import redirect_stdout

tickerURL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&limit=500'
#https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=0&limit=10&cryptocurrency_type=tokens&convert=USD,BTC


headers = {
 'Accept': 'application/json',
 'Accept-Encoding': 'deflate, gzip',
 'X-CMC_PRO_API_KEY': '898fa24e-dc29-4595-ba19-2616393e20a4',
}

# making a call to all (creating a dictionary of ticker symbol / name pairs)
pairs = {}
r = requests.get(tickerURL, headers=headers)

if r.status_code == 200:
   response = json.loads(r.text)

for x in range(0,500): #hardcoded limit in http link
    ticker = response['data'][x]['name']
    market_cap = response['data'][x]['quote']['USD']['market_cap']
    volume_24h = response['data'][x]['quote']['USD']['volume_24h']
    mcap_div_by_vol = round(float(market_cap) / float(volume_24h),2)
    if ticker is not None and mcap_div_by_vol is not None:
        pairs[ticker] = mcap_div_by_vol

sorted_pairs = sorted(pairs.items(), key=operator.itemgetter(1))

with open('ratio_list.txt', 'w') as f:
    with redirect_stdout(f):
        for ticker,ratio in sorted_pairs:
            print (ticker, "->", ratio)
input("Any key to close")
