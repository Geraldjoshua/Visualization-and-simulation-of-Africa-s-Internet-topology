from selenium import webdriver
from ipaddress import IPv4Network
from bs4 import BeautifulSoup
from chromedriver_py import binary_path  # this will get you the path variable
import os
from selenium.webdriver.chrome.options import Options
import random
import subprocess

# set the path to configure webdriver to use chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=binary_path, chrome_options=chrome_options)

file = open("files/countries.txt", "r")
country = file.readlines()

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

if os.path.exists("files/AsnAfrica.txt"):
    os.remove("files/AsnAfrica.txt")
file = open("files/AsnAfrica.txt", "a")

for a in asn:
    file.write(a.strip())
    file.write('\n')
file.close()

# running bash script
print("start")
subprocess.call("bash ip.sh", shell=True)
print("end")

netarr = []
f = open("ipnetwork.txt", "r")
for p in f:
    p = p.split(" ")
    netarr.append(p[1].strip())
count = 0
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

if os.path.exists("files/ip_Africa_address.txt"):
    os.remove("files/ip_Africa_address.txt")
file = open("files/ip_Africa_address.txt", 'a')
for ip in ipaddress:
    file.write(str(ip))
    file.write('\n')
file.close()
driver.quit()
