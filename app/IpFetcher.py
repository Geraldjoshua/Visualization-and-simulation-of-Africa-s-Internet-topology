import os

from selenium import webdriver
from ipaddress import IPv4Network
from bs4 import BeautifulSoup
from chromedriver_py import binary_path  # this will get you the path variable
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import random
import pyasn

Africa_asn = []

"""
Scrapes African asns from ipinfo.io
"""


def scrape_africa_asn():
    global Africa_asn
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    country = ["DZ", "AO", "BJ", "BW", "BF", "BI", "CM", "CV", "CF", "TD", "KM", "CG", "CD", "CI", "DJ",
               "EG", "GQ", "ER", "ET", "GA", "GM", "GH", "GN", "GW", "KE", "LS", "LR", "LY", "MG", "MW",
               "ML", "MR", "MU", "YT", "MA", "MZ", "NA", "NE", "NG", "RE", "RW", "SH", "ST", "SN", "SC",
               "SL", "SO", "ZA", "SS", "SD", "SZ", "TZ", "TG", "TN", "UG", "EH", "ZM", "ZW"]
    asn = []
    for code in country:
        cod = code.lower().strip()
        driver.get("https://ipinfo.io/countries/" + cod)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        driver.implicitly_wait(25)
        for body in soup.findAll('tr'):
            temp = []
            for a in body.findAll('td', attrs={'class': 'p-3'}):
                temp.append(a.text.strip())
            driver.implicitly_wait(10)
            if len(temp) != 0 and temp[2] != 0:
                asn.append(temp[0])
    Africa_asn = asn
    driver.quit()

"""
from the asns, gets ip address to be used for doing traceroute and ping measurements
"""


def get_random_africa_ip():
    # Initialize module and load IP to ASN database
    projectroot = os.path.realpath((os.path.dirname(__file__)))
    path = os.path.join(projectroot, 'files/ipasn.dat')
    asndb = pyasn.pyasn(path)
    netarr = []

    for asn1 in Africa_asn:
        iprange = asndb.get_as_prefixes(int(asn1[2:]))
        if iprange is not None:
            for i in iprange:
                netarr.append(str(i).strip())
                break

    randomip = []
    ipaddress = []
    for net in netarr:
        net = IPv4Network(net)
        for addr in net:
            randomip.append(addr)
        # randomize the array
        randomip = random.sample(randomip, len(randomip))
        ipaddress.append(randomip[0])
        ipaddress.append(randomip[1])
        randomip.clear()

    return ipaddress
