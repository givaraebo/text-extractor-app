import json

# JSON-Daten aus der Datei laden
with open('extracted_inner_json.json') as f:
    json_data = f.read()

# JSON-Daten in Python-Datenstrukturen umwandeln
data = json.loads(json_data)

# HTML-Template als Ausgangspunkt
html = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Produktseite</title>
</head>
<body>
"""

# Landing Image
for item in data['script']:
    if 'inner_json_data' in item and 'landingImageUrl' in item['inner_json_data']:
        image_url = item['inner_json_data']['landingImageUrl']
        html += f'<img src="{image_url}" alt="Produktbild"><br>'

# Produktbezeichnung und Beschreibung
for item in data['script']:
    if 'inner_json_data' in item and 'strings' in item['inner_json_data']:
        product_header = item['inner_json_data']['strings'].get('TURBO_CHECKOUT_HEADER', 'Produktname nicht verfügbar')
        html += f'<h2>{product_header}</h2>'

# Preis
for item in data['div']:
    if 'inner_json_data' in item and 'desktop_buybox_group_1' in item['inner_json_data']:
        price = item['inner_json_data']['desktop_buybox_group_1'][0].get('displayPrice', 'Preis nicht verfügbar')
        html += f'<p>Preis: {price}</p>'

# Lieferung und Einsparungen
for item in data['script']:
    if 'inner_json_data' in item and 'snsFrequencyParamsMap' in item['inner_json_data']:
        delivery_info = item['inner_json_data']['snsFrequencyParamsMap']
        html += f'<p>Lieferinformationen: {delivery_info}</p>'

# Rabattoptionen
for item in data['script']:
    if 'inner_json_data' in item and 'discountOptionsParamsMap' in item['inner_json_data']:
        discount_options = item['inner_json_data']['discountOptionsParamsMap']
        html += f'<p>Rabattoptionen: {discount_options}</p>'

# Abschließen des HTML
html += """
</body>
</html>
"""

# HTML-Ausgabe
print(html)

# HTML in eine Datei speichern
with open('product_page.html', 'w') as f:
    f.write(html)
