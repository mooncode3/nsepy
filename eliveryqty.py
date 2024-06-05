import requests
import pandas as pd
import openpyxl


class OptionChain():
    def __init__(self, url_, timeout=5) -> None:
        self.__url = url_
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

    def fetch_sec_data(self):
        try:
            data = self.__session.get(url=self.__url, timeout=self.__timeout)
            data = data.json()
            data = data['data']['indexTurnoverRecords']
            df = pd.json_normalize(data)
            return df
        except Exception as ex:
            print('Error: {}'.format(ex))
            self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout,
                               cookies=self.__session.cookies)


def get_sum(df, key):
    try:
        return df[key].sum()
    except Exception as ex:
        print('Error in Sum {}'.format(ex))


def get_indices(stock):
    nifty_auto = ['M&M', 'TVSMOTOR', 'BALKRISIND', 'MOTHERSON', 'TATAMTRDVR', 'EXIDEIND', 'MARUTI', 'TATAMOTORS',
                  'ASHOKLEY', 'APOLLOTYRE', 'EICHERMOT', 'BOSCHLTD', 'MRF', 'BHARATFORG', 'HEROMOTOCO', 'BAJAJ-AUTO']
    nifty_fin = ['PFC', 'CHOLAFIN', 'SHRIRAMFIN', 'KOTAKBANK', 'SBIN', 'IDFC', 'HDFCLIFE', 'AXISBANK', 'RECLTD',
                 'HDFCBANK', 'SBICARD', 'ICICIBANK', 'LICHSGFIN', 'BAJFINANCE', 'ICICIPRULI', 'BAJAJFINSV', 'ICICIGI',
                 'MUTHOOTFIN', 'SBILIFE', 'HDFCAMC']
    nifty_oil = ['GAIL', 'CASTROLIND', 'BPCL', 'GSPL', 'HINDPETRO', 'GUJGASLTD', 'MGL', 'IOC', 'RELIANCE', 'IGL',
                 'AEGISCHEM', 'ATGL', 'OIL', 'ONGC', 'PETRONET']
    nifty_fmcg = ['VBL', 'MARICO', 'BALRAMCHIN', 'UBL', 'ITC', 'MCDOWELL-N', 'PGHH', 'RADICO', 'COLPAL', 'TATACONSUM',
                  'GODREJCP', 'NESTLEIND', 'HINDUNILVR', 'BRITANNIA', 'DABUR']
    nifty_it = ['COFORGE', 'PERSISTENT', 'LTIM', 'TECHM', 'INFY', 'WIPRO', 'HCLTECH', 'LTTS', 'TCS', 'MPHASIS']
    nifty_pvt_bank = ['KOTAKBANK', 'BANDHANBNK', 'INDUSINDBK', 'AXISBANK', 'IDFCFIRSTB', 'HDFCBANK', 'ICICIBANK',
                      'RBLBANK', 'FEDERALBNK', 'CUB']
    nifty_bank = ['KOTAKBANK', 'BANDHANBNK', 'SBIN', 'AUBANK', 'INDUSINDBK', 'AXISBANK', 'IDFCFIRSTB', 'HDFCBANK',
                  'PNB', 'ICICIBANK', 'FEDERALBNK', 'BANKBARODA']
    nifty_pharma = ['ZYDUSLIFE', 'SANOFI', 'ALKEM', 'GLENMARK', 'IPCALAB', 'GRANULES', 'AUROPHARMA', 'GLAND', 'MANKIND',
                    'TORNTPHARM', 'BIOCON', 'ABBOTINDIA', 'SUNPHARMA', 'NATCOPHARM', 'DIVISLAB', 'LUPIN', 'JBCHEPHARM',
                    'LAURUSLABS', 'DRREDDY', 'CIPLA']
    nifty_metal = ['NMDC', 'APLAPOLLO', 'RATNAMANI', 'NATIONALUM', 'JSL', 'VEDL', 'HINDCOPPER', 'SAIL', 'JSWSTEEL',
                   'JINDALSTEL', 'WELCORP', 'HINDZINC', 'TATASTEEL', 'ADANIENT', 'HINDALCO']
    nifty_consumer_durable = ['CROMPTON', 'DIXON', 'AMBER', 'KAJARIACER', 'WHIRLPOOL', 'HAVELLS', 'CENTURYPLY', 'CERA',
                              'BATAINDIA', 'RAJESHEXPO', 'TITAN', 'KALYANKJIL', 'BLUESTARCO', 'VGUARD', 'VOLTAS']

    if stock in nifty_pharma:
        return "NIFTY_PHARMA"
    if stock in nifty_auto:
        return "NIFTY_AUTO"
    if stock in nifty_fin:
        return "NIFTY_FIN"
    if stock in nifty_pvt_bank:
        return "NIFTY_BANK"
    if stock in nifty_oil:
        return "NIFTY_OIL"
    if stock in nifty_fmcg:
        return "NIFTY_FMCG"
    if stock in nifty_it:
        return "NIFTY_IT"
    if stock in nifty_bank:
        return "BANK_NIFTY"
    if stock in nifty_metal:
        return "NIFTY_METAL"
    if stock in nifty_consumer_durable:
        return "NIFTY_CONSUMER_DUR"
    return "NO INDICES"


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
    sectors = []
    lastweek = []
    recentweek = []
    for symbol in nifty_50_stocks:
        fromDate = "06-05-2024"
        toDate = "10-05-2024"
        url = "https://www.nseindia.com/api/historical/securityArchives?from={}&to={}&symbol={}&dataType=priceVolumeDeliverable&series=EQ".format(
            fromDate, toDate, symbol)
        oc = OptionChain(url)
        lastweek.append(oc.fetch_data())
    #print(lastweek)
    for symbol in nifty_50_stocks:
        fromDate = "13-05-2024"
        toDate = "17-05-2024"
        url = "https://www.nseindia.com/api/historical/securityArchives?from={}&to={}&symbol={}&dataType=priceVolumeDeliverable&series=EQ".format(
            fromDate, toDate, symbol)
        oc = OptionChain(url)
        recentweek.append(oc.fetch_data())
    #print(recentweek)

    stocks_vol_bo = []
    for pair in zip(recentweek, lastweek):
        if get_sum(pair[0], 'CH_TOT_TRADED_QTY') > get_sum(pair[1], 'CH_TOT_TRADED_QTY'):
            #print(pair[0]['CH_SYMBOL'][0] + ' ====== ' + pair[1]['CH_SYMBOL'][0])
            #print(get_sum(pair[0],'CH_TOT_TRADED_QTY') - get_sum(pair[1],'CH_TOT_TRADED_QTY'))
            data = {'symbol': pair[0]['CH_SYMBOL'][0], 'indices': get_indices(pair[0]['CH_SYMBOL'][0])}
            stocks_vol_bo.append(data)
    #print(stocks_vol_bo)

    # sector bo
    sectors = ['NIFTY%2050', 'NIFTY%20BANK', 'NIFTY%20AUTO', 'NIFTY%20FINANCIAL%20SERVICES', 'NIFTY%20FMCG',
               'NIFTY%20IT', 'NIFTY%20MEDIA', 'NIFTY%20METAL', 'NIFTY%20PHARMA', 'NIFTY%20PSU%20BANK',
               'NIFTY%20PRIVATE%20BANK', 'NIFTY%20REALTY', 'NIFTY%20HEALTHCARE%20INDEX', 'NIFTY%20CONSUMER%20DURABLES',
               'NIFTY%20OIL%20%26%20GAS', 'NIFTY%20ENERGY', ]
    sec_recent_week = []
    sec_last_week = []
    for sector in sectors:
        fromDate = "06-05-2024"
        toDate = "10-05-2024"
        url = "https://www.nseindia.com/api/historical/indicesHistory?indexType={}&from={}&to={}".format(sector,
                                                                                                         fromDate,
                                                                                                         toDate)
        oc = OptionChain(url)
        sec_last_week.append(oc.fetch_sec_data())
    #print(sec_recent_week)

    #sectors = ['NIFTY%2050','NIFTY%20BANK','NIFTY%20AUTO','NIFTY%20FIN%20SERVICE','NIFTY%20FMCG','NIFTY%20IT','NIFTY%20MEDIA','NIFTY%20METAL','NIFTY%20PHARMA','NIFTY%20PSU%20BANK','NIFTY%20PVT%20BANK','NIFTY%20REALTY','NIFTY%20HEALTHCARE','NIFTY%20CONSR%20DURBL','NIFTY%20OIL%20AND%20GAS','NIFTY%20CONSUMPTION','NIFTY%20CPSE','NIFTY%20ENERGY','NIFTY%20INFRA','NIFTY%20PSE','NIFTY%20SERV%20SECTOR','NIFTY%20IND%20DIGITAL']
    sec_recent_week = []
    for sector in sectors:
        fromDate = "13-05-2024"
        toDate = "17-05-2024"
        url = "https://www.nseindia.com/api/historical/indicesHistory?indexType={}&from={}&to={}".format(sector,
                                                                                                         fromDate,
                                                                                                         toDate)
        oc = OptionChain(url)
        sec_recent_week.append(oc.fetch_sec_data())
    #print(sec_recent_week)

    indices_vol_bo = []
    for pair in zip(sec_recent_week, sec_last_week):
        if get_sum(pair[0], 'HIT_TRADED_QTY') > get_sum(pair[1], 'HIT_TRADED_QTY'):
            #print(pair[0]['HIT_INDEX_NAME_UPPER'][0] + ' ====== ' + pair[1]['HIT_INDEX_NAME_UPPER'][0])
            #print(get_sum(pair[0]) - get_sum(pair[1]))
            #data = {'symbol': pair[0]['HIT_INDEX_NAME_UPPER'][0], 'vol': get_sum(pair[0], 'HIT_TRADED_QTY') - get_sum(pair[1], 'HIT_TRADED_QTY')}
            data = {'symbol': pair[0]['HIT_INDEX_NAME_UPPER'][0]}
            indices_vol_bo.append(data.values())
    #print(indices_vol_bo)
    res_data = [stocks_vol_bo, indices_vol_bo]

    print(res_data)

#EOD_INDEX_NAME,
#https://www.nseindia.com/api/historical/indicesHistory?indexType=NIFTY%2050&from=10-05-2024&to=17-05-2024
