from PyPDF2 import PdfReader

reader = PdfReader("../../files/test.pdf")
page = reader.pages[0]

parts = []


def visitor_body(
        text,
        cm, # Current Transformation Matrix
        tm, # Text Transformation Matrix tm[4] (X-Koordinate) und tm[5] (Y-Koordinate)
        fontDict,
        fontSize
):
    y = tm[5]
    x = tm[4]
    if y > 50 and y < 720:
        pass
    parts.append(text)


page.extract_text(visitor_text=visitor_body)
text_body = "".join(parts)

print(text_body)

import spacy
import re

# Lade das deutsche Sprachmodell
#nlp = spacy.load("de_core_news_sm")


# Lade das gespeicherte Modell
nlp = spacy.load("../../ml/adresse_model")




# Beispieltext mit Adressen
text = text_body

# Verarbeite den Text mit spaCy
doc = nlp(text)

# Zeige die erkannten Entitäten
for ent in doc.ents:
    print(ent.text, ent.label_)