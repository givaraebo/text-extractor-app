from urllib.parse import urlparse, parse_qs
import json

# URL, aus der die Parameter extrahiert werden sollen
url = "https://www.amazon.de/LOr%C3%A9al-Paris-Rizinus-%C3%96l-pflanzlichen-Haarshampoo/dp/B0BWFMZ7LQ?psc=1&pd_rd_w=yLOkG&content-id=amzn1.sym.e5dbb0fd-6936-4959-a333-4001219ba88e&pf_rd_p=e5dbb0fd-6936-4959-a333-4001219ba88e&pf_rd_r=TDWSHQT27K6WQD01SP2N&pd_rd_wg=VqUEs&pd_rd_r=e4484c3a-e548-440c-9a24-4fca99c057f4&ref_=sspa_dk_detail_1&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM="

# Parsen der URL
parsed_url = urlparse(url)

# Extrahieren der Path-Parameter (alles nach dem Domain-Namen)
path_params = parsed_url.path.strip('/').split('/')

# Extrahieren der Query-Parameter
query_params = parse_qs(parsed_url.query)

# Kombinieren der Path- und Query-Parameter
params = {
    "path_params": path_params,
    "query_params": query_params
}

# Umwandeln der kombinierten Parameter in JSON
params_json = json.dumps(params, indent=4)

# Ausgabe der JSON-Daten
print(params_json)
