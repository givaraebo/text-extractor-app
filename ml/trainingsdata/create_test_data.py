import spacy

# Lade das vortrainierte Modell
nlp = spacy.load('de_core_news_sm')

# Beispieltext
text = "Ich hätte alle Möglichkeiten 1 bis 4 nebeneinander liegenden Token."

# Verarbeite den Text mit spaCy
doc = nlp(text)


# Funktion zum Extrahieren der Kombinationen von Tokens mit Start- und End-Indizes
def get_token_combinations_with_indexes(doc, min_len=1, max_len=4):
    combinations = []

    # Schleife, um alle Kombinationen von Token-Längen (1 bis 4) zu extrahieren
    for length in range(min_len, max_len + 1):
        for i in range(len(doc) - length + 1):
            combination = doc[i:i + length]
            start_index = combination[0].idx  # Start-Index des ersten Tokens
            end_index = combination[-1].idx + len(combination[-1].text)  # End-Index des letzten Tokens
            combinations.append({
                "combination": " ".join([token.text for token in combination]),
                "start_index": start_index,
                "end_index": end_index
            })
    return combinations

# Extrahiere die Kombinationen von Token mit Start- und End-Indizes
combinations = get_token_combinations_with_indexes(doc, 1, 4)

# Zeige die gefundenen Kombinationen
for combo in combinations:
    print(f"Combination: {combo['combination']}, Start index: {combo['start_index']}, End index: {combo['end_index']}")
