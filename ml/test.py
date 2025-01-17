import random
import spacy
from spacy.training import Example

# Lade das leere Modell für das Training (hier verwenden wir das vortrainierte Modell de_core_news_sm)
nlp = spacy.load('de_core_news_sm')

# Erstelle den Text und die Annotationsdaten
train_data = [
    ("Brückenstraße 39, 12345 Frankfurt", {"entities": [(0, 14, "STRAßE"), (15, 17, "HAUSNUMMER"), (18, 23, "PLZ"), (24, 33, "STADT")]}),
    ("Musterstraße 25, 98765 Musterstadt", {"entities": [(0, 12, "STRAßE"), (13, 15, "HAUSNUMMER"), (16, 21, "PLZ"), (22, 34, "STADT")]}),
]

# Aktivieren der Entitätserkennungspipeline
if "ner" not in nlp.pipe_names:
    ner = nlp.create_pipe("ner")
    nlp.add_pipe(ner, last=True)
else:
    ner = nlp.get_pipe("ner")

# Entitäten zum NER hinzufügen
for _, annotations in train_data:
    for ent in annotations["entities"]:
        ner.add_label(ent[2])

# Start des Trainings
optimizer = nlp.begin_training()

# Iteriere über die Trainingsdaten und trainiere das Modell
for i in range(20):
    random.shuffle(train_data)
    losses = {}
    for text, annotations in train_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], losses=losses)
    print(losses)
# Speichere das trainierte Modell
nlp.to_disk("adresse_model")
