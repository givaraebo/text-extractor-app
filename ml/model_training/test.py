import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Beispiel-Textdaten (Sentiment: Positiv = 1, Negativ = 0)
texts = ["Ich liebe dieses Produkt", "Das ist schrecklich", "Absolut fantastisch", "Ich hasse es", "Sehr gut gemacht", "Ganz schlecht"]
labels = [1, 0, 1, 0, 1, 0]  # 1 = positiv, 0 = negativ

# Tokenisierung der Texte
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
X = tokenizer.texts_to_sequences(texts)
X_pad = pad_sequences(X, padding='post')

# Modell erstellen
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=10, input_length=X_pad.shape[1]))  # Embedding-Schicht
model.add(LSTM(64))  # LSTM-Schicht mit 64 Einheiten
model.add(Dense(1, activation='sigmoid'))  # Ausgabe-Schicht mit einer Sigmoid-Aktivierungsfunktion (für binäre Klassifikation)

# Modell kompilieren
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Modell trainieren
model.fit(X_pad, np.array(labels), epochs=5, batch_size=2)

# Vorhersagen mit dem trainierten Modell
test_texts = ["Ich mag es", "Es ist so schlecht"]
test_sequences = tokenizer.texts_to_sequences(test_texts)
test_padded = pad_sequences(test_sequences, padding='post', maxlen=X_pad.shape[1])

# Vorhersagen
predictions = model.predict(test_padded)
predictions = (predictions > 0.5).astype(int)  # Konvertiere Wahrscheinlichkeiten in 0 oder 1

print(predictions)  # Vorhersagen für die Testtexte
