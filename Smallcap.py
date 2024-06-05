import datetime
import json

import requests
import pandas as pd


class OptionChain():
    def __init__(self, fund_name='INF179KA1RW5', timeout=5) -> None:
        self.__url = "https://staticassets.zerodha.com/coin/scheme-portfolio/{}.json".format(fund_name)
        self.__session = requests.sessions.Session()
        self.__session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "application/json", "Accept-Language": "en-US,en;q=0.5",
            "App - Id": "growwWeb",
            "Device - Id": "a2574403 - 339a - 5cb3 - a79b - 31ad494f85df",
            "Device - Type": "desktop",
            "Platform": "web"

        }

        self.__timeout = timeout
        self.__session.get("https://staticassets.zerodha.com", timeout=self.__timeout)

    def fetch_data(self, expiry_date=None, starting_strike_price=None, number_of_rows=2):
        try:
            data = self.__session.get(url=self.__url, timeout=self.__timeout)
            data = data.json()
            df = pd.json_normalize(data)

            if not df.empty:
                return data['data']
        except Exception as ex:
            print('Error: {}'.format(ex))
            self.__session.get("https://groww.in", timeout=self.__timeout)


previous_week = [];

if __name__ == '__main__':
    small_cap = ['INF179KA1RW5', 'INF204K01K15', 'INF200K01T51', 'INF966L01663', 'INF846K01K35', 'INF174K01KT2',
                 'INF917K01QA1', 'INF740K01QD1', 'INF090I01IQ4', 'INF109K015M0', 'INF277K011O1',
                 'INF194KB1AL4', 'INF209K01WN4', 'INF174V01BK7', 'INF205K013T3', 'INF205K012T5', 'INF789F1AUQ1',
                 'INF754K01JN6', 'INF903J01NK9', 'INF00XX01747', 'INF247L01BY3', 'INF663L01W06', 'INF582M01BU9',
                 'INF251K01SR5', 'INF761K01EP7', 'INF397L01JS1', 'INF082J01432']
    #ex - 'INF760K01JC'
    symbol_report_today = {}
    for fund in small_cap:
        oc = OptionChain(fund)
        data = oc.fetch_data()

        #print(fund)
        for d in data:
            if d[1] in symbol_report_today:
                if symbol_report_today[d[1]]:
                    symbol_report_today[d[1]].append(d)
            else:
                symbol_report_today[d[1]] = [d]

    f = open('lasts.json')
    last = json.load(f)
    #print(last.keys())
    for k in symbol_report_today:
        if len(symbol_report_today[k]) >= 5:
            total = 0
            for item in symbol_report_today[k]:
                total += item[5]
            if total > 10:
                pass
                #print(k)

    addedSybol = [item for item in symbol_report_today.keys() if item not in last.keys()]
    print("addedd {}".format(addedSybol))
    increaseQuantity = []
    for k in last:
        if last[k] and symbol_report_today[k]:
            preQty = 0
            currQty = 0
            for item in symbol_report_today[k]:
                currQty += item[5]
            for item in last[k]:
                preQty += item[5]
            if currQty > preQty:
                increaseQuantity.append({k: symbol_report_today[k]})

    print("increased {}".format(increaseQuantity))

    lastfile = "lasts.json"
    with open(lastfile, "w") as outfile:
        json.dump(symbol_report_today, outfile)
