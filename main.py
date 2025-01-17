from PyPDF2 import PdfReader

# PDF-Datei laden
file_path = "files/test.pdf"
reader = PdfReader(file_path)


layout = reader.page_layout
page_mode = reader.page_mode


# Seiten durchgehen und Text extrahieren
for page in reader.pages:
    print(page.extract_text())
print()