#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GPIO-In-Out.py
    allgemeines Beispiel zur Ansteuerung der GPIO-Pins

    Erzeugung einer Rechteckspannung am Ausgabe-Pin durch
    Verändern der Spannung am Eingabe-Pin

    z.B. Steuerung einer Leuchtdiode über einen
    lichtempfindlichen Widerstand (Hell-Dunkel-Schaltung)
"""

# Importieren der GPIO-Bibliothek
import RPi.GPIO as GPIO
# ... und weiterer nützlicher Module
import time
import sys

# -- Setzen der Parameter für das Script
pSens = 20  # Sensor-Pin (Stecker 38)
pOut = 21  # Ausgabe-Pin (Stecker 40)
dt = 0.03  # Wartezeit zwischen Abfragen in Sekunden

# -- Initialisieren der GPIO-Pins
GPIO.setmode(GPIO.BCM)  # Nummerierungsschema der GPIO-Pins festlegen
GPIO.setup(pSens, GPIO.IN)  # als Eingang festgelegen
GPIO.setup(pOut, GPIO.OUT)  # als Ausgang festgelegen

print('*==* ', sys.argv[0], ' Lesen von Pin ', pSens, '    Ausgabe an Pin ', pOut)

print('        <STRG>c zum Beenden ... ', end="-> ", flush=True)
# -- Endlosschleife
try:  # Ausführen des Programmcodes, solange es keine Unterbrechung gibt.

    while True:  # Dauerschleife (alles eingerückte danach wird wiederholt).

        if GPIO.input(pSens):  # Abfrage des Zustands am Eingangspin
            GPIO.output(pOut, 1)  # Ausgabe auf Eins, wenn Eins
        else:  # sonst ...
            GPIO.output(pOut, 0)  # .... Ausgabe auf Null
        time.sleep(dt)  # warten (Raspberry Pi "schläft").

except KeyboardInterrupt:  # Wenn das Programm mit Strg + C unterbrochen wird,
    GPIO.cleanup()  # ... wird noch aufgeräumt#
    print(' *==* ', sys.argv[0], ' Ende')
