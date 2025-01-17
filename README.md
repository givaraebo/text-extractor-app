# text-extractor-app
Text extraction application

## PyPDF2
- https://pypdf2.readthedocs.io/en/3.x/user/migration-1-to-2.html#imports-and-modules

- cm (Current Transformation Matrix)
Bedeutung: Dies ist die aktuelle Transformationsmatrix, die beschreibt, wie der Text auf der Seite platziert ist. Sie enthält Informationen über Skalierung, Drehung, Verschiebung und andere Transformationen.
Struktur: cm ist eine Liste oder ein Array mit sechs Werten: [a, b, c, d, e, f].

  - a, b, c, d: Beschreiben Skalierung und Rotation.
  
  - e, f: Beschreiben die Verschiebung (Position) auf der Seite.
  
- Verwendung: Selten direkt verwendet, außer wenn präzise Layout-Analysen notwendig sind.

- tm (Text Transformation Matrix)
Bedeutung: Dies ist die Text-Transformationsmatrix, die ähnlich wie cm funktioniert, aber spezifisch für den Text ist. Sie enthält die Position und Orientierung des Texts auf der Seite.
Struktur: tm ist ebenfalls eine Liste oder ein Array mit sechs Werten: [a, b, c, d, e, f].

  - tm[4] (X-Koordinate): Gibt die horizontale Position des Texts auf der Seite an.
  
  - tm[5] (Y-Koordinate): Gibt die vertikale Position des Texts auf der Seite an.
  
- Verwendung: Im gezeigten Code wird tm[5] genutzt, um den Text anhand seiner Y-Koordinate zu filtern (z. B. if y > 50 and y < 720).