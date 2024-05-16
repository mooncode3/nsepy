import requests
import pandas as pd


class OptionChain():
    def __init__(self, fromDate, toDate, symbol='ABB', timeout=5) -> None:
        self.__url = (
            "https://www.nseindia.com/api/historical/securityArchives?from={}&to={}&symbol={}&dataType=priceVolumeDeliverable&series=EQ").format(
            fromDate, toDate, symbol)
        self.__session = requests.sessions.Session()
        self.__session.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5"}
        self.__timeout = timeout
        self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)

    def fetch_data(self):
        try:
            data = self.__session.get(url=self.__url, timeout=self.__timeout)
            data = data.json()
            df = pd.json_normalize(data['data'])
            return df
        except Exception as ex:
            print('Error: {}'.format(ex))
            self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout,
                               cookies=self.__session.cookies)


def get_sum(df):
    try:
        return df['CH_TOT_TRADED_QTY'].sum()
    except Exception as ex:
        print('Error in Sum {}'.format(ex))


if __name__ == '__main__':
    nifty_100_stocks = ['ABB', 'ADANIENSOL', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ADANIPOWER', 'ATGL', 'AMBUJACEM',
                        'APOLLOHOSP', 'ASIANPAINT', 'DMART', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV',
                        'BAJAJHLDNG', 'BANKBARODA', 'BERGEPAINT', 'BEL', 'BPCL', 'BHARTIARTL', 'BOSCHLTD', 'BRITANNIA',
                        'CANBK', 'CHOLAFIN', 'CIPLA', 'COALINDIA', 'COLPAL', 'DLF', 'DABUR', 'DIVISLAB', 'DRREDDY',
                        'EICHERMOT', 'GAIL', 'GODREJCP', 'GRASIM', 'HCLTECH', 'HDFCBANK', 'HDFCLIFE', 'HAVELLS',
                        'HEROMOTOCO', 'HINDALCO', 'HAL', 'HINDUNILVR', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'ITC',
                        'IOC', 'IRCTC', 'IRFC', 'INDUSINDBK', 'NAUKRI', 'INFY', 'INDIGO', 'JSWSTEEL', 'JINDALSTEL',
                        'JIOFIN', 'KOTAKBANK', 'LTIM', 'LT', 'LICI', 'M%26M', 'MARICO', 'MARUTI', 'NTPC', 'NESTLEIND',
                        'ONGC', 'PIDILITIND', 'PFC', 'POWERGRID', 'PNB', 'RECLTD', 'RELIANCE', 'SBICARD', 'SBILIFE',
                        'SRF', 'MOTHERSON', 'SHREECEM', 'SHRIRAMFIN', 'SIEMENS', 'SBIN', 'SUNPHARMA', 'TVSMOTOR', 'TCS',
                        'TATACONSUM', 'TATAMTRDVR', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TECHM', 'TITAN',
                        'TORNTPHARM', 'TRENT', 'ULTRACEMCO', 'MCDOWELL-N', 'VBL', 'VEDL', 'WIPRO', 'ZOMATO',
                        'ZYDUSLIFE']
    nifty_50_stocks = ['COALINDIA', 'CIPLA', 'BPCL', 'BHARTIARTL', 'POWERGRID', 'NTPC', 'M%26M', 'HCLTECH', 'LT',
                       'HINDALCO', 'TATASTEEL', 'ADANIPORTS', 'WIPRO', 'AXISBANK', 'ICICIBANK', 'ADANIENT', 'SBIN',
                       'LTIM', 'DRREDDY', 'KOTAKBANK', 'TECHM', 'BAJFINANCE', 'ONGC', 'GRASIM', 'HEROMOTOCO',
                       'APOLLOHOSP', 'DIVISLAB', 'INDUSINDBK', 'SBILIFE', 'RELIANCE', 'INFY', 'ITC', 'BAJAJFINSV',
                       'MARUTI', 'TCS', 'ULTRACEMCO', 'TITAN', 'SHRIRAMFIN', 'NESTLEIND', 'HINDUNILVR', 'HDFCLIFE',
                       'SUNPHARMA', 'JSWSTEEL', 'HDFCBANK', 'TATACONSUM', 'BRITANNIA', 'EICHERMOT', 'ASIANPAINT',
                       'BAJAJ-AUTO', 'TATAMOTORS']
    lastweek = []
    recentweek = []
    for symbol in nifty_50_stocks:
        oc = OptionChain("06-05-2024", "10-05-2024", symbol)
        lastweek.append(oc.fetch_data())
    #print(lastweek)
    for symbol in nifty_50_stocks:
        oc = OptionChain("11-05-2024", "15-05-2024", symbol)
        recentweek.append(oc.fetch_data())
    #print(recentweek)

    for pair in zip(recentweek, lastweek):
        print(get_sum(pair[0]) > get_sum(pair[1]))
