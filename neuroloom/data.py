"""Song dataset. Columns: Title, Artist, Energy, Valence, Acousticness (all floats 0-1)."""
import pandas as pd

SONGS = pd.DataFrame([
    # Despair (Valence 0.05-0.18)
    {"Title": "Hurt",                   "Artist": "Johnny Cash",             "Energy": 0.18, "Valence": 0.08, "Acousticness": 0.75},
    {"Title": "Mad World",              "Artist": "Gary Jules",              "Energy": 0.10, "Valence": 0.10, "Acousticness": 0.92},
    {"Title": "Everybody Hurts",        "Artist": "R.E.M.",                  "Energy": 0.22, "Valence": 0.12, "Acousticness": 0.60},
    {"Title": "Black",                  "Artist": "Pearl Jam",               "Energy": 0.35, "Valence": 0.15, "Acousticness": 0.45},

    # Sorrow (0.18-0.32)
    {"Title": "Skinny Love",            "Artist": "Bon Iver",                "Energy": 0.25, "Valence": 0.22, "Acousticness": 0.82},
    {"Title": "Someone Like You",       "Artist": "Adele",                   "Energy": 0.30, "Valence": 0.25, "Acousticness": 0.88},
    {"Title": "Creep",                  "Artist": "Radiohead",               "Energy": 0.40, "Valence": 0.28, "Acousticness": 0.42},
    {"Title": "Fix You",                "Artist": "Coldplay",                "Energy": 0.42, "Valence": 0.30, "Acousticness": 0.35},

    # Melancholy (0.32-0.48)
    {"Title": "Holocene",               "Artist": "Bon Iver",                "Energy": 0.20, "Valence": 0.38, "Acousticness": 0.70},
    {"Title": "Nude",                   "Artist": "Radiohead",               "Energy": 0.30, "Valence": 0.35, "Acousticness": 0.55},
    {"Title": "Teardrop",               "Artist": "Massive Attack",          "Energy": 0.38, "Valence": 0.42, "Acousticness": 0.45},
    {"Title": "Spiegel im Spiegel",     "Artist": "Arvo Part",               "Energy": 0.08, "Valence": 0.40, "Acousticness": 0.98},

    # Contemplative (0.48-0.62)
    {"Title": "Intro",                  "Artist": "The xx",                  "Energy": 0.45, "Valence": 0.52, "Acousticness": 0.40},
    {"Title": "Re: Stacks",             "Artist": "Bon Iver",                "Energy": 0.28, "Valence": 0.55, "Acousticness": 0.80},
    {"Title": "Porcelain",              "Artist": "Moby",                    "Energy": 0.50, "Valence": 0.58, "Acousticness": 0.35},
    {"Title": "Strobe",                 "Artist": "deadmau5",                "Energy": 0.55, "Valence": 0.60, "Acousticness": 0.12},

    # Hopeful (0.62-0.75)
    {"Title": "Night Owl",              "Artist": "Galimatias",              "Energy": 0.55, "Valence": 0.65, "Acousticness": 0.30},
    {"Title": "Midnight City",          "Artist": "M83",                     "Energy": 0.68, "Valence": 0.70, "Acousticness": 0.10},
    {"Title": "Electric Feel",          "Artist": "MGMT",                    "Energy": 0.72, "Valence": 0.74, "Acousticness": 0.12},

    # Upbeat (0.75-0.88)
    {"Title": "Feel Good Inc.",         "Artist": "Gorillaz",                "Energy": 0.75, "Valence": 0.78, "Acousticness": 0.08},
    {"Title": "Dog Days Are Over",      "Artist": "Florence + The Machine",  "Energy": 0.80, "Valence": 0.82, "Acousticness": 0.20},
    {"Title": "Levitating",             "Artist": "Dua Lipa",                "Energy": 0.85, "Valence": 0.86, "Acousticness": 0.05},
    {"Title": "Good as Hell",           "Artist": "Lizzo",                   "Energy": 0.82, "Valence": 0.84, "Acousticness": 0.10},

    # Euphoria (0.88-1.0)
    {"Title": "Uptown Funk",            "Artist": "Mark Ronson",             "Energy": 0.90, "Valence": 0.92, "Acousticness": 0.03},
    {"Title": "Happy",                  "Artist": "Pharrell Williams",       "Energy": 0.88, "Valence": 0.96, "Acousticness": 0.22},
    {"Title": "Can't Stop the Feeling", "Artist": "Justin Timberlake",       "Energy": 0.88, "Valence": 0.94, "Acousticness": 0.08},
    {"Title": "Walking on Sunshine",    "Artist": "Katrina & The Waves",     "Energy": 0.92, "Valence": 0.98, "Acousticness": 0.05},
])