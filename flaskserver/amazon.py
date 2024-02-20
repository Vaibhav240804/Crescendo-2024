import numpy as np
import pandas as pd
import requests 
import time
import datetime
from bs4 import BeautifulSoup

reviewList = []
revString = ""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def extractReviews(rurl):
#   print("pg no - ", pg)
  print(rurl)
  page = requests.get(rurl, headers=headers)
  print(page)
  time.sleep(2)
  soup = BeautifulSoup(page.content, "html.parser")
#   print(soup.title.string)
  reviews = soup.findAll('div', {'data-hook': 'review' })
  for item in reviews:
    ratingText = item.find('i', {'data-hook': 'review-star-rating' }).text.strip()
    fullDate = item.find('span', {'data-hook': 'review-date' }).text.strip()
    date_obj = fullDate.split('on')[1].strip()
    review = {
        # 'name': title.strip(),
        'rating': ratingText,
        'star': float(ratingText.split()[0]),
        'body': item.find('span', {'data-hook': 'review-body' }).text.strip(),
        'fullDate': fullDate,
        'date': date_obj,
    }
    print(review)
    reviewList.append(review)
    # revString += review['body']

if __name__ == "__main__":
    # for i in range(1, 11):
    try:
        url = 'https://www.amazon.in/DABUR-Toothpaste-800G-Ayurvedic-Treatment-Protection/dp/B07HKXSC6K?ref_=Oct_d_otopr_d_1374620031_1&pd_rd_w=kY9CL&content-id=amzn1.sym.c4fc67ca-892d-48d9-b9ed-9d9fdea9998e&pf_rd_p=c4fc67ca-892d-48d9-b9ed-9d9fdea9998e&pf_rd_r=MHNFPBXAZ4VTV28WDF48&pd_rd_wg=kpToS&pd_rd_r=e5fbdca6-653c-4ace-80d9-a84f619d8dad&pd_rd_i=B07HKXSC6K'
        # print(headers)
        page = requests.get(url, headers=headers)
        print(page)
        time.sleep(2)
        soup = BeautifulSoup(page.content, "html.parser")
        print(soup.title.string)
        title = soup.find(id="productTitle").get_text
        # title = soup.find('span', {'id': 'productTitle'}).text.strip()
        print(title)
        nurl = url.split('?')
        url = nurl[0]
        reviewUrl = url.replace("dp", "product-reviews") + "?pageNumber=" + str(1)
        # print(reviewUrl)
        extractReviews(reviewUrl)
    except Exception as e:
        print(e)