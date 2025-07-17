# @title Standardtext für Titel
# Installation

import streamlit as st
!pip install pytrends --quiet

# Importe
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math # Import the math module
import time # Import the time module

# Suppress FutureWarning
pd.set_option('future.no_silent_downcasting', True)

# Verbindung zur Google Trends API
pytrends = TrendReq(hl='de-DE', tz=360)


# Kategorien bilden
search_categories = {
    "interesse_mentale_gesundheit": [
        "Psychologie", "psychische Gesundheit", "mentale Gesundheit", "Achtsamkeit",
        "Meditation", "Selbstfürsorge", "Selbstmitgefühl", "Resilienz", "Stressbewältigung",
        "emotionale Intelligenz", "innere Ruhe", "Gefühlsregulation", "positive Psychologie",
        "mentale Stärke", "psychisches Wohlbefinden", "Lebenszufriedenheit",
        "Gefühle verstehen", "mentale Gesundheit stärken"
    ],
    "Therapie": [
            "Psychotherapie", "Therapeut finden", "psychologische Hilfe", "Therapie Depression",
            "Psychologe in der Nähe", "Psychiater Hilfe", "Psychotherapeuten finden", "Termin Psychotherapeut", "Psychotherapeut", "Therapieplatz", "Therapie Depression",
            "Therapie beginnen", "Therapie finden", "Wartezeit Therapieplatz", "Psychotherapeut in der Nähe", "Psychiater in der Nähe", "Psychologe finden",
            "psychologische Beratung", "ambulante Psychotherapie", "stationäre Psychotherapie", "Verhaltenstherapie", "Tiefenpsychologie", "analytische Psychotherapie",
            "systemische Therapie", "EMDR Therapie", "psychotherapeutische Hilfe", "kostenlose Psychotherapie", "Online Therapie", "Krankenkasse Psychotherapie"
        ],

    "Stoerungsbilder": {
        "Depression": [
            "depressiv", "Anzeichen Depression", "Depression", "depressive Symptome",
            "nicht mehr leben wollen", "Leere fühlen", "keine Freude mehr"
        ],
        "Angststörung": [
            "Angststörung", "soziale Angst", "generalisierte Angst", "Panikattacke",
            "plötzliche Angst", "Herzrasen Angst", "Angst", "Panik"
        ],
        "Burnout": [
            "Burnout", "ausgebrannt", "Stress am Arbeitsplatz", "Burnout Symptome",
            "Dauerstress", "ausgebrannt fühlen", "keine Energie mehr", "emotionale Erschöpfung"
        ],
        "Suizid": [
            "Suizidgedanken", "Hilfe bei Suizid", "Selbstmordgedanken", "Suizid Gedanken", "Suizid",
            "ich will nicht mehr leben", "Leben beenden", "Suizid Hilfe", "was tun bei Suizidgedanken"
        ],
        "Schlaf": [
            "Schlafprobleme", "Schlaflosigkeit", "nicht einschlafen können", "Schlafstörung",
            "nachts wach werden", "Durchschlafstörung"
        ],
        "Essstörungen": [
            "Essstörung", "Bulimie", "Magersucht", "Essanfälle", "Überessen",
            "Anorexia Nervosa", "Bulimia Nervosa", "pro Ana"
        ],
    "ADHS": [
           "Was ist ADHS", "ADHS erklärt", "ADHS Symptome", "Aufmerksamkeitsdefizit", "Aufmerksamkeitsdefizit Hyperaktivitätssyndrom",
           "Anzeichen ADHS", "ADHS bei Erwachsenen", "ADHS bei Kindern", "Verhalten bei ADHS", "ADHS in der Schule",
           "Schwierigkeiten bei ADHS", "ADHS"
    ]
    }
}


# Zeitrahmen und Land
timeframe = 'all'
geo = 'DE'

# Ergebnisse initialisieren
all_data = pd.DataFrame()

# Daten abrufen und zusammenführen
for category, terms in search_categories.items():
    print(f"Abrufen: {category}")
    # Remove duplicates from terms
    unique_terms = list(dict.fromkeys(terms))
    # Split terms into chunks of max 5 keywords
    n = 5 # Max keywords per request
    chunks = [unique_terms[i:i + n] for i in range(0, len(unique_terms), n)]
    category_data = pd.DataFrame()
    for chunk in chunks:
        pytrends.build_payload(chunk, timeframe=timeframe, geo=geo)
        df = pytrends.interest_over_time().drop(columns='isPartial')
        category_data = pd.concat([category_data, df], axis=1)
        time.sleep(10) # Increase delay to 10 seconds


    # Calculate the mean for the category from all chunks
    all_data[category] = category_data.mean(axis=1)


# Kombinierte Linie für alle Kategorien
all_data['Gesamt'] = all_data.mean(axis=1)

# Visualisierung
plt.figure(figsize=(18, 10))
sns.set(style="whitegrid")

for col in all_data.columns:
    plt.plot(all_data.index, all_data[col], label=col)

plt.title('Google-Suchinteresse zu psychischer Gesundheit', fontsize=20)
plt.xlabel('Datum')
plt.ylabel('Suchinteresse (0–100)')
plt.legend()
plt.tight_layout()
plt.show()

import matplotlib.dates as mdates

# 📌 Liste der wichtigen Ereignisse (Datum, Beschreibung)
events = [
    ("2008-09-15", "Finanzkrise Lehman"),
    ("2011-03-11", "Fukushima & Atomausstieg"),
    ("2015-09-04", "Flüchtlingskrise DE"),
    ("2020-03-15", "Beginn Corona-Lockdown"),
    ("2021-01-01", "Corona-Impfstart DE"),
    ("2021-07-15", "Flutkatastrophe Ahrtal"),
    ("2022-02-24", "Krieg Ukraine beginnt"),
    ("2022-12-01", "Energiepreise Höchststand"),
    ("2023-12-24", "Weihnachten 2023"),
    ("2024-06-09", "EU-Wahl & Rechtsruck")
]

# 🖼️ Visualisierung
plt.figure(figsize=(18, 10))
sns.set(style="whitegrid")

# 📈 Alle Linien aus Trenddaten zeichnen
for column in all_data.columns:
    plt.plot(all_data.index, all_data[column], label=column)

# 📍 Ereignislinien mit Beschriftung
for date_str, label in events:
    plt.axvline(pd.to_datetime(date_str), color='gray', linestyle='--', alpha=0.6)
    plt.text(pd.to_datetime(date_str), plt.ylim()[1]*0.95, label, rotation=90, verticalalignment='top', fontsize=9)

# 🔠 Achsen & Legende
plt.title("Suchtrends psychische Gesundheit mit gesellschaftlichen Ereignissen", fontsize=20)
plt.xlabel("Datum")
plt.ylabel("Suchinteresse (0–100)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()