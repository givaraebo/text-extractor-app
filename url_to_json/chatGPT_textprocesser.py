import requests
from bs4 import BeautifulSoup

def scrape_product_data(url):
    # Send a request to the website
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find product names and prices (replace the class names with actual ones from the website)
    product_prices = soup.find_all('div', class_='price')
    # Collect data in a list
    products = []
    for price in product_prices:
        product = {
            'price': price.get_text(strip=True)
        }
        products.append(product)

    return products

url = 'https://www.alibaba.com/product-detail/Customizable-Rainbow-Backlit-Wired-Gaming-Keyboard_1601159729050.html?spm=a2700.galleryofferlist.normal_offer.d_image.752913a0SYq0N6'  # Replace with the actual URL
product_data = scrape_product_data(url)

for product in product_data:
    print(f"Product Name: , Price: {product['price']}")
