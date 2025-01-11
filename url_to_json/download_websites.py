import requests


def download_html(url, output_file):
    try:
        # Sende eine GET-Anfrage an die URL
        response = requests.get(url)
        response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war

        # Speichere die HTML-Inhalte in der Datei
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(response.text)

        print(f"HTML-Seite erfolgreich heruntergeladen und gespeichert in: {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Herunterladen der Seite: {e}")


# Beispielaufruf
url = "https://www.amazon.de/LOr%C3%A9al-Paris-Rizinus-%C3%96l-pflanzlichen-Haarshampoo/dp/B0BWFMZ7LQ?psc=1&pd_rd_w=yLOkG&content-id=amzn1.sym.e5dbb0fd-6936-4959-a333-4001219ba88e&pf_rd_p=e5dbb0fd-6936-4959-a333-4001219ba88e&pf_rd_r=TDWSHQT27K6WQD01SP2N&pd_rd_wg=VqUEs&pd_rd_r=e4484c3a-e548-440c-9a24-4fca99c057f4&ref_=sspa_dk_detail_1&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM="
output_file = "seite.html"
download_html(url, output_file)
