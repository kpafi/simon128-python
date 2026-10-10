Implementierung der Blockchiffre Simon128/128 in Python. Das Projekt ist aus einer Kryptographie-Praktikumsaufgabe entstanden.

- Rundenfunktion: f(x) = (x <<< 1 & x <<< 8) ^ (x <<< 2)
- Verschlüsselung einzelner 128-Bit-Blöcke
- Messung des Lawineneffekts: Wie viele Ausgabebits ändern sich nach 2 bis 39
  Runden, wenn sich ein Eingabebit ändert?

Rotationen und Bitoperationen sind selbst geschrieben, es wurde keine library verwendet


