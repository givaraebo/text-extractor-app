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


def json_to_html(json_data):
    # JSON-Daten in Python-Datenstrukturen umwandeln
    url = json_data['url']
    data = json.loads(json_data['data'])

    # HTML-Template als Ausgangspunkt
    html = f"""
    <a href="{url}" target="_blank" style="text-decoration: none;">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-around; gap: 20px; padding: 20px;">
    """

    # Landing Image, Titel und Preis
    for item in data['script']:
        if 'inner_json_data' in item and 'landingImageUrl' in item['inner_json_data']:
            image_url = item['inner_json_data']['landingImageUrl']
            # Produktkarte
            html += f"""
            <div style="border: 1px solid #ddd; border-radius: 15px; width: 280px; margin: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); background-color: #fff; transition: transform 0.3s ease;">
                <img src="{image_url}" alt="Produktbild" style="width: 100%; border-radius: 10px; object-fit: cover; height: 200px;">
            """

    # Produktbezeichnung und Beschreibung
    for item in data['script']:
        if 'inner_json_data' in item and 'strings' in item['inner_json_data']:
            product_header = item['inner_json_data']['strings'].get('TURBO_CHECKOUT_HEADER',
                                                                    'Produktname nicht verfügbar')
            html += f'<h3 style="font-size: 1.2em; font-weight: bold; color: #333;">{product_header}</h3>'

    # Preis
    for item in data['div']:
        if 'inner_json_data' in item and 'desktop_buybox_group_1' in item['inner_json_data']:
            price = item['inner_json_data']['desktop_buybox_group_1'][0].get('displayPrice', 'Preis nicht verfügbar')
            html += f'<p style="font-size: 1.1em; color: #007bff; font-weight: bold;">Preis: {price}</p>'

    # Abschluss für jedes Produkt
    html += """
        </div>
    """
    html += """
    </div>
    </a>
    """
    return html


# Beispielaufruf
async def main():
    urls = [
        "https://amzn.to/4fTa5ca",
        "https://amzn.to/429ETSI",
        "https://amzn.to/4acOo5q"
    ]
    jsons = []
    for url in urls:
        result_json = await extract_json_from_inner_content(url)
        jsons.append({'url': url, 'data': result_json})

    # Start HTML Dokument
    html = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Produktseite</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
            }
            h1 {
                text-align: center;
                color: #333;
                margin-top: 20px;
            }
            p {
                font-size: 1em;
                color: #555;
            }
            /* Flexbox Styling für die Produktkarten */
            .product-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
                gap: 20px;
                padding: 20px;
            }
            .product-card {
                border: 1px solid #ddd;
                border-radius: 15px;
                width: 280px;
                margin: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                background-color: #fff;
                transition: transform 0.3s ease;
            }
            .product-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            }
            img {
                width: 100%;
                border-radius: 10px;
                object-fit: cover;
                height: 200px;
            }
            h3 {
                font-size: 1.2em;
                font-weight: bold;
                color: #333;
            }
            p {
                font-size: 1.1em;
                color: #007bff;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
    <h1>Unsere Produkte</h1>
    <div class="product-container">
    """

    # Gehe durch alle JSON-Daten und erstelle die HTML-Seite
    for json_data in jsons:
        html += json_to_html(json_data)

    # Schließe HTML
    html += """
    </div>
    </body>
    </html>
    """

    # Speichere die HTML-Datei
    with open("product_page.html", "w") as f:
        f.write(html)


# Run asynchronous code
asyncio.run(main())
