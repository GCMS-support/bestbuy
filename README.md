# Best Buy 2.0

Python-Shop mit lagerhaltigen, unbegrenzten und pro Bestellung limitierten
Produkten sowie prozentualen Rabatten, zweitem Artikel zum halben Preis und
jedem dritten Artikel gratis.

## Starten

```sh
python3 main.py
```

## Tests

```sh
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
python3 -m pycodestyle *.py
```

Bestellungen fassen wiederholte Positionen desselben Produkts zusammen.
Mengen, Bestelllimits, Aktivstatus und Rabattberechnung werden fuer die
gesamte Bestellung geprueft, bevor der Lagerbestand geaendert wird.

Die Regressionstests pruefen unter anderem:

- Zwei einzeln hinzugefuegte MacBooks kosten zusammen 2175.00 Dollar.
- Zweimal einzeln hinzugefuegter Versand wird abgelehnt.
- Eine ungueltige Bestellung veraendert weder Bestand noch Aktivstatus.
- Nicht lagerhaltige Produkte bleiben bei Menge 0 kaufbar.
- Die Fehlerfaelle funktionieren auch ueber das interaktive Menue.

## In Codio klonen

```sh
cd ~/workspace
git clone https://github.com/GCMS-support/bestbuy.git
cd bestbuy
git log --oneline
python3 -m pytest -q
python3 main.py
```

Nach spaeteren Aenderungen auf GitHub im geklonten Ordner `git pull` ausfuehren.
