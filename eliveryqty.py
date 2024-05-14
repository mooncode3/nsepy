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

            return data
        except Exception as ex:
            print('Error: {}'.format(ex))
            self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)


if __name__ == '__main__':
    oc = OptionChain("15-04-2024", "15-05-2024")
    print(oc.fetch_data())
