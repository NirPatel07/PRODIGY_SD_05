
import requests
from bs4 import BeautifulSoup
import csv

def get_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    products = []
    
    for item in soup.find_all('div', class_='s-result-item'):
        try:
            name = item.find('span', class_='a-text-normal').text.strip()
            price = item.find('span', class_='a-price').find('span', class_='a-offscreen').text.strip()
            rating = item.find('span', class_='a-icon-alt').text.strip().split()[0] # Extracting the numerical part of the rating
            products.append({'Name': name, 'Price': price, 'Rating': rating})
        except AttributeError:
            pass
    
    return products

def save_to_csv(products, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Price', 'Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

if __name__ == "__main__":
    url = input("Enter the URL of the Amazon search results page: ")
    products = get_product_info(url)
    if products:
        filename = input("Enter the name of the CSV file to save the product information (e.g., products.csv): ")
        save_to_csv(products, filename)
        print(f"Product information has been saved to {filename}")
    else:
        print("No products found on the provided URL.")

