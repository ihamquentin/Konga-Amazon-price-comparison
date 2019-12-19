import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import time
from urllib.request import Request
import requests
import json
import re
import sys


def compare(mystring):
    def usd_to_ngn():
        print("Getting USD to NGN Rate")
        req = requests.get("http://free.currconv.com/api/v7/convert?q=USD_NGN&apiKey=5029a99b396929294f63")
        req.raise_for_status()

        res = str(req.content)[2:-1]
        res = json.loads(res)

        rate = float(res['results']['USD_NGN']['val'])
        return rate
    
    def amazon(mystring):
        search_term = mystring.replace(" ", "+")
        header = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
        html = Request("https://www.amazon.com/s?k={}&ref=nb_sb_noss_1".format(search_term), headers=header)
        time.sleep(10)
        page_html2 = uReq(html).read()
        page_soup = soup(page_html2, 'html.parser')
        price_tags1 = page_soup.select('span.a-offscreen')
        prices = [el.get_text() for el in price_tags1]  # get text
        # print(f"1 : {prices}")
        prices = ["".join(re.findall("([\S]?)([0-9\.]+)", i)[0]) for i in prices]
        # ^ remove spaces, and get the price range minimum, with the currency
        rate = usd_to_ngn()
        prices = [(float(i[1:]) * rate) for i in prices] 
        return prices

    
    
    def konga(mystring):
         #mystring = (input('enter your search term: '))
        search_term = mystring.replace(" ", "+")
        my_url = 'https://www.konga.com/search?search='
        new = my_url+search_term
        header = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
        #print(new)
        request = Request(new, headers=header)
        time.sleep(10)
        response = uReq(request).read()
        page_soup = soup(response, 'html.parser')
    #price_containers = page_soup.find_all('span', {'class':'d7c0f_sJAqi'})
    #containers = page_soup.find_all('div', {'class':'af885_1iPzH'})
        price_tags = page_soup.select("span.d7c0f_sJAqi")
        prices = [float(str(el.contents[1]).replace(",", "")) for el in price_tags[:30]]
        return prices

        
        
    konga = konga(mystring)
    # print(konga)
    amazon = amazon(mystring)
    # print(alibaba)
    """
    if len(konga) > len(alibaba) > 0:
        konga = konga[:len(alibaba)]
    elif len(konga) > 0:
        alibaba = alibaba[:len(konga)]
    """
    def find_avg(lst):
        if len(lst) < 1:
            return None
        avg = 0
        for i in lst:
            avg += i
        return avg / len(lst)

    obj = {"avg_konga_price": find_avg(konga), "avg_Amazon_price": find_avg(amazon),
            "currency"       : "NGN",
            'konga'          : ("Unable To Fetch Prices" if (len(konga) < 1) else konga),
            'amazon'        : ("Unable To Fetch Prices" if (len(amazon) < 1) else amazon)}
    # print(f"k = {konga} : a = {alibaba}")
    print(obj)


if len(sys.argv) > 1:
    compare(" ".join(sys.argv[1:]))

# Uncomment the code below to run a test with query='diamond jewelry'
term = str(input('enter your search term: '))
compare(term)

