import numpy as np
import pandas as pd
import requests 
import time
import datetime
from bs4 import BeautifulSoup
import pymongo

reviewList = []
revString = [""]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def createProduct(url):
  page = requests.get(url, headers=headers)
  time.sleep(2)
  soup = BeautifulSoup(page.content, "html.parser")
  title = soup.find(id="productTitle").get_text()
  desc = soup.find(id="productDescription").get_text()
  img = soup.find('img', {'id': 'landingImage'})['src']
  price = soup.find('span', class_='a-offscreen').text.strip()
  date = datetime.datetime.now()
  strDate = date.strftime("%Y-%m-%d %H:%M:%S")
  print(price)
  print(desc)
  print(img)
  print(date)
  product_details = {
      'name': title.strip(),
      'url': url,
      'description': desc.strip(),
      'image': img,
      'price': price,
      'date': strDate,
      }
  client = pymongo.MongoClient("mongodb+srv://sonarsiddhesh105:K5NuO27RwuV2R986@cluster0.0aedb3y.mongodb.net/?retryWrites=true&w=majority")
  db = client['test']
  collect = db['cres_users']
  filter_query = { "email": "sonarsiddhesh105@gmail.com" }
  # print(db)
  update_result = collect.update_one(filter_query, { "$push": { "products": product_details } })
  print("Documents matched:", update_result.matched_count)
  print("Documents modified:", update_result.modified_count)
  return url

def extractReviews(rurl, uurl):
  # print(rurl)
  # print("pg no - ", pg)
  page = requests.get(rurl, headers=headers)
  # print(page)
  soup = BeautifulSoup(page.content, "html.parser")
  reviews = soup.findAll('div', {'data-hook': 'review' })
  print(len(reviews))
  # print(reviews[0])
  for item in reviews:
    # print(item)
    ratingText = item.find('i', {'data-hook': 'review-star-rating' }).text.strip()
    fullDate = item.find('span', {'data-hook': 'review-date' }).text.strip()
    date_obj = fullDate.split('on')[1].strip()
    review = {
        # 'title': title.strip(),
        'rating': ratingText,
        'star': float(ratingText.split()[0]),
        'body': item.find('span', {'data-hook': 'review-body' }).text.strip(),
        'fullDate': fullDate,
        'date': date_obj,
    }
    # print(review)
    reviewList.append(review)
    revString[0] = revString[0] + " " + review['body']
  client = pymongo.MongoClient("mongodb+srv://sonarsiddhesh105:K5NuO27RwuV2R986@cluster0.0aedb3y.mongodb.net/?retryWrites=true&w=majority")
  db = client['test']
  collect = db['cres_users']
  filter_query = { "email": "sonarsiddhesh105@gmail.com" }  # Filter to find the user with the specified email
  update_query = { "$set": { "products.$[product].reviews": reviewList } }  # Update the reviews field of the matched product

  # Use arrayFilters to match the specific product within the products array
  array_filters = [{ "product.url": uurl }]

  update_result = collect.update_one(filter_query, update_query, array_filters=array_filters)


  print("Documents matched:", update_result.matched_count)
  print("Documents modified:", update_result.modified_count)
  return reviewList

if __name__ == "__main__":
    # for i in range(1, 11):
    try:
        url = 'https://www.amazon.in/DABUR-Toothpaste-800G-Ayurvedic-Treatment-Protection/dp/B07HKXSC6K?ref_=Oct_d_otopr_d_1374620031_1&pd_rd_w=kY9CL&content-id=amzn1.sym.c4fc67ca-892d-48d9-b9ed-9d9fdea9998e&pf_rd_p=c4fc67ca-892d-48d9-b9ed-9d9fdea9998e&pf_rd_r=MHNFPBXAZ4VTV28WDF48&pd_rd_wg=kpToS&pd_rd_r=e5fbdca6-653c-4ace-80d9-a84f619d8dad&pd_rd_i=B07HKXSC6K'
        uniqueUrl = createProduct(url)
        nurl = url.split('?')
        url = nurl[0]
        reviewUrl = url.replace("dp", "product-reviews") + "?pageNumber=" + str(1)
        # print(reviewUrl)
        x = extractReviews(reviewUrl, uniqueUrl)
        # print(x)
        print(revString)
    except Exception as e:
        print(e)