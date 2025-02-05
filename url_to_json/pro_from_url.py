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

            # Find all elements that may contain JSON-like data
            for element in soup.find_all(True):  # True matches all tags
                # Get the innerText or innerHTML of the element
                inner_content = element.get_text(strip=True) or element.decode_contents()

                try:
                    # Try to parse inner content as JSON
                    parsed_data = json.loads(inner_content)

                    # Check if parsed data has the 'type' key and if it's 'int' or 'number'
                    if 'type' in parsed_data and parsed_data['type'] in ['int', 'number']:
                        continue  # Skip this element if 'type' is 'int' or 'number'

                    # Check if the 'value' key exists and is not empty
                    if 'value' in parsed_data and not parsed_data['value']:
                        continue  # Skip if 'value' is empty

                    # Add valid JSON data to dictionary using the tag name as key
                    if element.name not in data_elements:
                        data_elements[element.name] = []
                    data_elements[element.name].append({
                        'inner_json_data': parsed_data
                    })
                except (json.JSONDecodeError, TypeError):
                    # Ignore non-JSON data
                    continue

            # Close browser
            await browser.close()

            # Return the extracted data in JSON format
            return json.dumps(data_elements, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)



def clean_json(jsons):
    new_json = []

    # Iterating through the JSON data to dynamically create product cards
    for json_data in jsons:
        data = json.loads(json_data['data'])
        url = json_data['url']
        new_data = {}
        new_data['url'] = url

        for div in data['div']:
            buybox_list = []

            # Handling `desktop_buybox_group_1`
            for buybox in div['inner_json_data'].get('desktop_buybox_group_1', []):
                display_price = buybox.get('displayPrice')
                price_amount = buybox.get('priceAmount')
                currency_symbol = buybox.get('currencySymbol')
                integer_value = buybox.get('integerValue')
                decimal_separator = buybox.get('decimalSeparator')
                fractional_value = buybox.get('fractionalValue')
                locale = buybox.get('locale')
                buying_option_type = buybox.get('buyingOptionType')

                buybox_list.append({
                    "displayPrice": display_price,
                    "priceAmount": price_amount,
                    "currencySymbol": currency_symbol,
                    "integerValue": integer_value,
                    "decimalSeparator": decimal_separator,
                    "fractionalValue": fractional_value,
                    "locale": locale,
                    "buyingOptionType": buying_option_type
                })

            # Handling `desktop_buybox_group_2`
            for buybox in div['inner_json_data'].get('desktop_buybox_group_2', []):
                display_price = buybox.get('displayPrice')
                price_amount = buybox.get('priceAmount')
                currency_symbol = buybox.get('currencySymbol')
                integer_value = buybox.get('integerValue')
                decimal_separator = buybox.get('decimalSeparator')
                fractional_value = buybox.get('fractionalValue')
                locale = buybox.get('locale')
                buying_option_type = buybox.get('buyingOptionType')

                buybox_list.append({
                    "displayPrice": display_price,
                    "priceAmount": price_amount,
                    "currencySymbol": currency_symbol,
                    "integerValue": integer_value,
                    "decimalSeparator": decimal_separator,
                    "fractionalValue": fractional_value,
                    "locale": locale,
                    "buyingOptionType": buying_option_type
                })

            new_data['buybox'] = buybox_list

        for script in data['script']:
            if 'landingImageUrl' in script['inner_json_data']:
                new_data['landingImageUrl'] = script['inner_json_data']['landingImageUrl']

            if 'strings' in script['inner_json_data']:
                new_data['title'] = script['inner_json_data']['strings'].get('TURBO_CHECKOUT_HEADER')

            if 'buyingOptionTypes' in script['inner_json_data']:
                new_data['buyingOptionTypes'] = script['inner_json_data']['buyingOptionTypes']

        new_json.append(new_data)
    return new_json

# Beispielaufruf
async def main():
    urls = [
        "https://amzn.to/4jat5Wm",
        "https://amzn.to/429ETSI",
        "https://amzn.to/40shRoQ",
        "https://www.amazon.de/-/en/Heldengr%C3%BCn%C2%AE-Organic-Rosemary-Natural-Booster/dp/B0CNTJ92F4/ref=sr_1_5?crid=TVEEZG6K6OT8&dib=eyJ2IjoiMSJ9.thMtlOl1kb3EHmnFDaMHd44mglo0ldihywH6sw9E492iCW1mbU32gLaUM8Jqooojf97J-Khj3Zw8248CmIxGfqwE_pxNVMnW307xwfu4c_uuTEUgWMTNtadmG7aFBo-Hq8bNTf4pqgjA-kAVqKCtYxEUD-WLSOuD-2RRBsZiLK0sdDDm3McYICqH9pQr8WsI2Nc1SKPusTilTKGMiahDZ_8cdhas0pEHESwR50PvxZM1JTpCB2WicH2w2iluPlgqDNZQz7u0jms7gB2ZbrW3uqZdqKii5u8wMGpZ-uZWI8IZYOC9sZHAn_7XUGgx_eAVzlda0dzWWSpJAfugthFL_qg42ZudwxYqhUpx1JOkAQyiy6A8w0O8G5s2VbK0kL4uFu2Lr2bI9wBAekHRZEda3HpH5I9Rd9g4zJmg8zW2kme_httj2n6j6LL2enoZn8fS.YMzGgQ83hfD9OCfLJp9weB30K9U4cHeQbVqr2Pdnqbg&dib_tag=se&keywords=rosmarin%C3%B6l%2Bhaare&nsdOptOutParam=true&qid=1737148501&sprefix=ros%2Caps%2C126&sr=8-5&th=1"
    ]
    jsons = []
    for url in urls:
        try:
            result_json = await extract_json_from_inner_content(url)
            jsons.append({'url': url, 'data': result_json})
        except Exception as e:
            print(f"Error extracting JSON from {url}: {e}")

    with open("index.html", "r") as html_file:
        html = html_file.read()
        html = html.replace("{{PRODUCT_CARDS}}", json.dumps(clean_json(jsons), indent=4))
        with open("indexOut.html", "w") as output_file:
            output_file.write(html)



# Run asynchronous code
asyncio.run(main())
