import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# Example dataset
data = {
    'Age': [22, 25, 47, 52, 46, 56, 30, 23, 1],
    'Income': [15000, 25000, 50000, 60000, 45000, 70000, 35000, 18000,10],
    'BuyProduct': [0, 1, 1, 1, 0, 1, 0, 0,0]  # 1 = Buy, 0 = Don't Buy
}

df = pd.DataFrame(data)

# Features (X) and Target (y)
X = df[['Age', 'Income']]
y = df['BuyProduct']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25, # Dieser Parameter gibt an, wie viel Prozent der gesamten Daten für den Testdatensatz verwendet werden.
    random_state=42 # Dieser Parameter stellt sicher, dass die Aufteilung der Daten reproduzierbar ist.
)

# Erstellen des Modells (Entscheidungsbaum-Klassifikator)
model = DecisionTreeClassifier()


# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)


# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')
