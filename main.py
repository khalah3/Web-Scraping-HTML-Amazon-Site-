import smtplib
import requests
from bs4 import BeautifulSoup
from smtplib import SMTP
import os
from dotenv import load_dotenv

url="https://appbrewery.github.io/instant_pot/"
load_dotenv()

email=os.environ.get("Email_address")
password=os.environ.get("Email_password")
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
         "Accept-Language":"en-US,en;q=0.9"}


instant_pot_content=requests.get(url=url,headers=headers)
instant_pot_response=BeautifulSoup(instant_pot_content.text, 'html.parser')

#Find price integer(99) and decimal(99) for total price of 99.99
soup_integer=instant_pot_response.find(name='span',class_='a-price-whole')
soup_decimal=instant_pot_response.find(name='span',class_='a-price-fraction')
#Find title in html soup
title=instant_pot_response.select("div h1 span")
title_text=title[0].get_text()
print(title_text)
#Combine 99 and 99 to get 99.99
price=soup_integer.text+soup_decimal.text
#Change string to float
price=float(price)
print(price)
message=f"Subject:Amazon Sale \n\n The price of : ({title_text}) has dropped \n url={url}"
if price < 100:
    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
        connection.starttls()
        result=connection.login(email,password)
        connection.sendmail(from_addr=email,to_addrs=email,msg=message.encode("utf-8"))
