from sec_edgar_downloader import Downloader

import os

def getFilings(ticker):
    dl = Downloader("MyCompanyName", "my.email@domain.com", "./")
    dl.get("10-K", ticker, after="1995-01-01", before="2023-12-31")
#getFilings("AAPL")
ticker = "AAPL"
directory = './sec-edgar-filings/AAPL/10-K'
for root, dirs, files in os.walk(directory):
    for filename in files:
        print(os.path.join(root, filename))