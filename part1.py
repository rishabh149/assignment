import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape product listings
def scrape_product_listings(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    data = []
    for product in products:
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
        product_name = product.find('span', {'class': 'a-size-medium'}).text.strip()
        product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
        rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
        num_reviews = product.find('span', {'class': 'a-size-base'}).text.strip()

        data.append({
            'Product URL': product_url,
            'Product Name': product_name,
            'Product Price': product_price,
            'Rating': rating,
            'Number of Reviews': num_reviews
        })

    return data

# Function to scrape individual product pages
def scrape_product_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    description = soup.find('div', {'id': 'feature-bullets'}).text.strip()
    asin = soup.find('th', text='ASIN').find_next('td').text.strip()
    product_description = soup.find('div', {'id': 'productDescription'}).text.strip()
    manufacturer = soup.find('th', text='Manufacturer').find_next('td').text.strip()

    return description, asin, product_description, manufacturer

# Main function
def main():
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
    page_limit = 20
    products_data = []

    for page in range(1, page_limit+1):
        url = base_url + str(page)
        print(f"Scraping page {page}...")
        products_data.extend(scrape_product_listings(url))
        time.sleep(2)  # Delay between requests to avoid overwhelming the server

    print("Scraping individual product pages...")
    for product in products_data:
        url = product['Product URL']
        description, asin, product_description, manufacturer = scrape_product_page(url)
        product['Description'] = description
        product['ASIN'] = asin
        product['Product Description'] = product_description
        product['Manufacturer'] = manufacturer
        time.sleep(2)  #
