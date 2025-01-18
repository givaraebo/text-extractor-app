import asyncio
import json
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def extract_json_from_inner_content(url):
    try:
        # Start Playwright
        async with async_playwright() as p:
            # Start browser
            browser = await p.chromium.launch(headless=True)  # headless=False for visible browser
            page = await browser.new_page()

            # Go to the given URL
            await page.goto(url)

            # Wait for the page to load completely
            await page.wait_for_load_state("domcontentloaded")

            # Extract the HTML content of the entire page
            content = await page.content()

            # Load the HTML content into BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            # Dictionary to hold valid JSON content
            data_elements = {}
            # give price and quantity in list
            price_quantity_two_ = [{"price": price.find_all(class_='price')[i].find('span').get_text(strip=True),
              "quantity": price.find_all(class_='quality')[i].get_text(strip=True)} for price in
             soup.find_all(class_='product-price') for i in range(len(price))]
            print(price_quantity)


            # Close browser
            await browser.close()

            # Return the extracted data in JSON format
            return json.dumps(data_elements, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)


# Beispielaufruf
async def main():
    urls = ["https://www.alibaba.com/product-detail/2-4G-Wireless-Gaming-Keyboard-and_1600554967892.html?spm=a2700.galleryofferlist.normal_offer.d_image.752913a0wxhkzq",
            "https://www.alibaba.com/product-detail/LT500-Wireless-Gaming-Keyboard-Mouse-Set_1600554190076.html?spm=a2700.details.you_may_like.2.105e9d9erfZa1p",
            "https://www.alibaba.com/product-detail/Ultra-Thin-Protective-Clear-Hard-Anti_60799571520.html?spm=a2700.details.you_may_like.4.32c811735hUrON "
         ]
    jsons = []
    for url in urls:
        try:
            result_json = await extract_json_from_inner_content(url)
            jsons.append({'url': url, 'data': result_json})
        except Exception as e:
            print(f"Error extracting JSON from {url}: {e}")

    print(jsons)



# Run asynchronous code
asyncio.run(main())
