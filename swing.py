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


def getGainPercentage(df):
    return (df['CH_CLOSING_PRICE'][len(df['CH_CLOSING_PRICE']) - 1] - df['CH_OPENING_PRICE'][len(df['CH_OPENING_PRICE'])-1]) * 100 / df['CH_OPENING_PRICE'][len(df['CH_OPENING_PRICE']) - 1]


def getLossPercentage(df):
    return (df['CH_OPENING_PRICE'][len(df['CH_OPENING_PRICE'])-1] - df['CH_CLOSING_PRICE'][len(df['CH_CLOSING_PRICE']) - 1]) * 100 / df['CH_CLOSING_PRICE'][len(df['CH_CLOSING_PRICE']) - 1]


def getFactorGain(df):
    if df['CH_CLOSING_PRICE'][len(df['CH_CLOSING_PRICE'])-1] > df['CH_OPENING_PRICE'][len(df['CH_OPENING_PRICE'])-1]:
        if getGainPercentage(df) > 4:
            return getGainPercentage(df)
        return 0
    else:
        if getLossPercentage(df) > 4:
            return getLossPercentage(df)
        return 0



def get_sum(df, key):
    try:
        if df[key][len(df[key])-1] > df[key].mean():
            if getFactorGain(df) > 4:

            #return df[key][len(df[key])-1] - df[key].mean()
                return (100 * df[key][len(df[key]) - 1] - df[key].mean()) / df[key][len(df[key]) - 1]
            return 0
        #groupby('weight').mean()
        return 0
    except Exception as ex:
        print('Error in Sum {}'.format(ex))


if __name__ == '__main__':
    fromDate = "15-05-2024"
    toDate = "31-05-2024"
    nifty_500_stocks = ['360ONE', '3MINDIA', 'ABB', 'ACC', 'AIAENG', 'APLAPOLLO', 'AUBANK', 'AARTIIND', 'AAVAS',
                        'ABBOTINDIA', 'ACE', 'ADANIENSOL', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ADANIPOWER', 'ATGL',
                        'AWL', 'ABCAPITAL', 'ABFRL', 'AEGISCHEM', 'AETHER', 'AFFLE', 'AJANTPHARM', 'APLLTD', 'ALKEM',
                        'ALKYLAMINE', 'ALLCARGO', 'ALOKINDS', 'ARE%26M', 'AMBER', 'AMBUJACEM', 'ANANDRATHI', 'ANGELONE',
                        'ANURAS', 'APARINDS', 'APOLLOHOSP', 'APOLLOTYRE', 'APTUS', 'ACI', 'ASAHIINDIA', 'ASHOKLEY',
                        'ASIANPAINT', 'ASTERDM', 'ASTRAZEN', 'ASTRAL', 'ATUL', 'AUROPHARMA', 'AVANTIFEED', 'DMART',
                        'AXISBANK', 'BEML', 'BLS', 'BSE', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BAJAJHLDNG',
                        'BALAMINES', 'BALKRISIND', 'BALRAMCHIN', 'BANDHANBNK', 'BANKBARODA', 'BANKINDIA', 'MAHABANK',
                        'BATAINDIA', 'BAYERCROP', 'BERGEPAINT', 'BDL', 'BEL', 'BHARATFORG', 'BHEL', 'BPCL',
                        'BHARTIARTL', 'BIKAJI', 'BIOCON', 'BIRLACORPN', 'BSOFT', 'BLUEDART', 'BLUESTARCO', 'BBTC',
                        'BORORENEW', 'BOSCHLTD', 'BRIGADE', 'BRITANNIA', 'MAPMYINDIA', 'CCL', 'CESC', 'CGPOWER',
                        'CIEINDIA', 'CRISIL', 'CSBBANK', 'CAMPUS', 'CANFINHOME', 'CANBK', 'CAPLIPOINT', 'CGCL',
                        'CARBORUNIV', 'CASTROLIND', 'CEATLTD', 'CELLO', 'CENTRALBK', 'CDSL', 'CENTURYPLY', 'CENTURYTEX',
                        'CERA', 'CHALET', 'CHAMBLFERT', 'CHEMPLASTS', 'CHENNPETRO', 'CHOLAHLDNG', 'CHOLAFIN', 'CIPLA',
                        'CUB', 'CLEAN', 'COALINDIA', 'COCHINSHIP', 'COFORGE', 'COLPAL', 'CAMS', 'CONCORDBIO', 'CONCOR',
                        'COROMANDEL', 'CRAFTSMAN', 'CREDITACC', 'CROMPTON', 'CUMMINSIND', 'CYIENT', 'DCMSHRIRAM', 'DLF',
                        'DOMS', 'DABUR', 'DALBHARAT', 'DATAPATTNS', 'DEEPAKFERT', 'DEEPAKNTR', 'DELHIVERY', 'DEVYANI']

    # nifty_500_stocks = ['360ONE', '3MINDIA', 'ABB', 'ACC', 'AIAENG']
    lastweek = []
    stocks = []
    for symbol in nifty_500_stocks:
        # print(symbol)

        url = ("https://www.nseindia.com/api/historical/securityArchives?from={}&to={}&symbol={"
               "}&dataType=priceVolumeDeliverable&series=EQ").format(
            fromDate, toDate, symbol)
        oc = OptionChain(url)
        lastweek.append(oc.fetch_data())
    # print(lastweek)
    # print(sec_recent_week)

    for pair in lastweek:
        if pair is not None and not pair.empty:
            stocks.append({'symbol': pair['CH_SYMBOL'][0], 'vol': get_sum(pair, 'COP_DELIV_PERC')})
    # sorted = sorted(stocks,key=lambda x:stocks[1])
    # sorted(stocks.items(), key=lambda x: x[1])
    from operator import itemgetter

    newlist1 = stocks
    #print(newlist1)
    stocks = []
    lastweek = []

    nifty_500_stocks = ['DIVISLAB', 'DIXON', 'LALPATHLAB', 'DRREDDY', 'EIDPARRY', 'EIHOTEL', 'EPL', 'EASEMYTRIP',
                        'EICHERMOT', 'ELECON', 'ELGIEQUIP', 'EMAMILTD', 'ENDURANCE', 'ENGINERSIN', 'EQUITASBNK', 'ERIS',
                        'ESCORTS', 'EXIDEIND', 'FDC', 'NYKAA', 'FEDERALBNK', 'FACT', 'FINEORG', 'FINCABLES', 'FINPIPE',
                        'FSL', 'FIVESTAR', 'FORTIS', 'GAIL', 'GMMPFAUDLR', 'GMRINFRA', 'GRSE', 'GICRE', 'GILLETTE',
                        'GLAND', 'GLAXO', 'GLS', 'GLENMARK', 'MEDANTA', 'GPIL', 'GODFRYPHLP', 'GODREJCP', 'GODREJIND',
                        'GODREJPROP', 'GRANULES', 'GRAPHITE', 'GRASIM', 'GESHIP', 'GRINDWELL', 'GAEL', 'FLUOROCHEM',
                        'GUJGASLTD', 'GMDCLTD', 'GNFC', 'GPPL', 'GSFC', 'GSPL', 'HEG', 'HBLPOWER', 'HCLTECH', 'HDFCAMC',
                        'HDFCBANK', 'HDFCLIFE', 'HFCL', 'HAPPSTMNDS', 'HAPPYFORGE', 'HAVELLS', 'HEROMOTOCO', 'HSCL',
                        'HINDALCO', 'HAL', 'HINDCOPPER', 'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'POWERINDIA',
                        'HOMEFIRST', 'HONASA', 'HONAUT', 'HUDCO', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'ISEC', 'IDBI',
                        'IDFCFIRSTB', 'IDFC', 'IIFL', 'IRB', 'IRCON', 'ITC', 'ITI', 'INDIACEM', 'IBULHSGFIN',
                        'INDIAMART', 'INDIANB', 'IEX', 'INDHOTEL', 'IOC', 'IOB', 'IRCTC', 'IRFC', 'INDIGOPNTS', 'IGL',
                        'INDUSTOWER', 'INDUSINDBK', 'NAUKRI', 'INFY', 'INOXWIND', 'INTELLECT', 'INDIGO', 'IPCALAB',
                        'JBCHEPHARM', 'JKCEMENT', 'JBMA', 'JKLAKSHMI', 'JKPAPER', 'JMFINANCIL', 'JSWENERGY', 'JSWINFRA',
                        'JSWSTEEL', 'JAIBALAJI', 'J%26KBANK', 'JINDALSAW', 'JSL', 'JINDALSTEL', 'JIOFIN', 'JUBLFOOD',
                        'JUBLINGREA', 'JUBLPHARMA', 'JWL', 'JUSTDIAL', 'JYOTHYLAB', 'KPRMILL', 'KEI', 'KNRCON',
                        'KPITTECH', 'KRBL', 'KSB', 'KAJARIACER', 'KPIL', 'KALYANKJIL', 'KANSAINER', 'KARURVYSYA']

    # nifty_500_stocks = ['360ONE', '3MINDIA', 'ABB', 'ACC', 'AIAENG']
    lastweek = []
    stocks = []
    for symbol in nifty_500_stocks:
        # print(symbol)
        url = ("https://www.nseindia.com/api/historical/securityArchives?from={}&to={}&symbol={"
               "}&dataType=priceVolumeDeliverable&series=EQ").format(
            fromDate, toDate, symbol)
        oc = OptionChain(url)
        lastweek.append(oc.fetch_data())
    # print(lastweek)
    # print(sec_recent_week)

    for pair in lastweek:
        #print(pair)
        if pair is not None and not pair.empty:
            if pair is not None:
                stocks.append({'symbol': pair['CH_SYMBOL'][0], 'vol': get_sum(pair, 'COP_DELIV_PERC')})
    from operator import itemgetter

    newlist2 = stocks
    #print(newlist2)
    stocks = []
    lastweek = []

    nifty_500_stocks = ['KAYNES', 'KEC', 'KFINTECH', 'KOTAKBANK', 'KIMS', 'LTF', 'LTTS', 'LICHSGFIN', 'LTIM', 'LT',
                        'LATENTVIEW', 'LAURUSLABS', 'LXCHEM', 'LEMONTREE', 'LICI', 'LINDEINDIA', 'LLOYDSME', 'LUPIN',
                        'MMTC', 'MRF', 'MTARTECH', 'LODHA', 'MGL', 'MAHSEAMLES', 'M%26MFIN', 'M%26M', 'MHRIL',
                        'MAHLIFE', 'MANAPPURAM', 'MRPL', 'MANKIND', 'MARICO', 'MARUTI', 'MASTEK', 'MFSL', 'MAXHEALTH',
                        'MAZDOCK', 'MEDPLUS', 'METROBRAND', 'METROPOLIS', 'MINDACORP', 'MSUMI', 'MOTILALOFS', 'MPHASIS',
                        'MCX', 'MUTHOOTFIN', 'NATCOPHARM', 'NBCC', 'NCC', 'NHPC', 'NLCINDIA', 'NMDC', 'NSLNISP', 'NTPC',
                        'NH', 'NATIONALUM', 'NAVINFLUOR', 'NESTLEIND', 'NETWORK18', 'NAM-INDIA', 'NUVAMA', 'NUVOCO',
                        'OBEROIRLTY', 'ONGC', 'OIL', 'OLECTRA', 'PAYTM', 'OFSS', 'POLICYBZR', 'PCBL', 'PIIND',
                        'PNBHOUSING', 'PNCINFRA', 'PVRINOX', 'PAGEIND', 'PATANJALI', 'PERSISTENT', 'PETRONET',
                        'PHOENIXLTD', 'PIDILITIND', 'PEL', 'PPLPHARMA', 'POLYMED', 'POLYCAB', 'POONAWALLA', 'PFC',
                        'POWERGRID', 'PRAJIND', 'PRESTIGE', 'PRINCEPIPE', 'PRSMJOHNSN', 'PGHH', 'PNB', 'QUESS',
                        'RRKABEL', 'RBLBANK', 'RECLTD', 'RHIM', 'RITES', 'RADICO', 'RVNL', 'RAILTEL', 'RAINBOW',
                        'RAJESHEXPO', 'RKFORGE', 'RCF', 'RATNAMANI', 'RTNINDIA', 'RAYMOND', 'REDINGTON', 'RELIANCE',
                        'RBA', 'ROUTE', 'SBFC', 'SBICARD', 'SBILIFE', 'SJVN', 'SKFINDIA', 'SRF', 'SAFARI', 'MOTHERSON']
    # nifty_500_stocks = ['360ONE', '3MINDIA', 'ABB', 'ACC', 'AIAENG']
    lastweek = []
    stocks = []
    for symbol in nifty_500_stocks:
        # print(symbol)

        url = "https://www.nseindia.com/api/historical/securityArchives?from={}&to={}&symbol={}&dataType=priceVolumeDeliverable&series=EQ".format(
            fromDate, toDate, symbol)
        oc = OptionChain(url)
        lastweek.append(oc.fetch_data())
    # print(lastweek)
    # print(sec_recent_week)

    # indices_vol_bo = []
    for pair in lastweek:
        #print(pair)
        if pair is not None and not pair.empty:
            stocks.append({'symbol': pair['CH_SYMBOL'][0], 'vol': get_sum(pair, 'COP_DELIV_PERC')})
    from operator import itemgetter

    newlist3 = stocks
    #print(newlist3)

    nifty_500_stocks = ['SANOFI', 'SAPPHIRE', 'SAREGAMA', 'SCHAEFFLER', 'SCHNEIDER', 'SHREECEM', 'RENUKA', 'SHRIRAMFIN',
                        'SHYAMMETL', 'SIEMENS', 'SIGNATURE', 'SOBHA', 'SOLARINDS', 'SONACOMS', 'SONATSOFTW',
                        'STARHEALTH', 'SBIN', 'SAIL', 'SWSOLAR', 'STLTECH', 'SUMICHEM', 'SPARC', 'SUNPHARMA', 'SUNTV',
                        'SUNDARMFIN', 'SUNDRMFAST', 'SUNTECK', 'SUPREMEIND', 'SUVENPHAR', 'SUZLON', 'SWANENERGY',
                        'SYNGENE', 'SYRMA', 'TV18BRDCST', 'TVSMOTOR', 'TVSSCS', 'TMB', 'TANLA', 'TATACHEM', 'TATACOMM',
                        'TCS', 'TATACONSUM', 'TATAELXSI', 'TATAINVEST', 'TATAMTRDVR', 'TATAMOTORS', 'TATAPOWER',
                        'TATASTEEL', 'TATATECH', 'TTML', 'TECHM', 'TEJASNET', 'NIACL', 'RAMCOCEM', 'THERMAX', 'TIMKEN',
                        'TITAGARH', 'TITAN', 'TORNTPHARM', 'TORNTPOWER', 'TRENT', 'TRIDENT', 'TRIVENI', 'TRITURBINE',
                        'TIINDIA', 'UCOBANK', 'UNOMINDA', 'UPL', 'UTIAMC', 'UJJIVANSFB', 'ULTRACEMCO', 'UNIONBANK',
                        'UBL', 'MCDOWELL-N', 'USHAMART', 'VGUARD', 'VIPIND', 'VAIBHAVGBL', 'VTL', 'VARROC', 'VBL',
                        'MANYAVAR', 'VEDL', 'VIJAYA', 'IDEA', 'VOLTAS', 'WELCORP', 'WELSPUNLIV', 'WESTLIFE',
                        'WHIRLPOOL', 'WIPRO', 'YESBANK', 'ZFCVINDIA', 'ZEEL', 'ZENSARTECH', 'ZOMATO', 'ZYDUSLIFE',
                        'ECLERX']
    # nifty_500_stocks = ['360ONE', '3MINDIA', 'ABB', 'ACC', 'AIAENG']
    lastweek = []
    stocks = []
    for symbol in nifty_500_stocks:
        # print(symbol)

        url = "https://www.nseindia.com/api/historical/securityArchives?from={}&to={}&symbol={}&dataType=priceVolumeDeliverable&series=EQ".format(
            fromDate, toDate, symbol)
        oc = OptionChain(url)
        lastweek.append(oc.fetch_data())
    # print(lastweek)
    # print(sec_recent_week)

    # indices_vol_bo = []
    for pair in lastweek:
        if pair is not None and not pair.empty:
            stocks.append({'symbol': pair['CH_SYMBOL'][0], 'vol': get_sum(pair, 'COP_DELIV_PERC')})
    from operator import itemgetter

    newlist4 = stocks
    #print(newlist4)

    sortedStocks = newlist1 + newlist2 + newlist3 + newlist4
    sortedStocks = sorted(sortedStocks, key=itemgetter('vol'))

    print(sortedStocks)