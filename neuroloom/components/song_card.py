"""Song card with organic rotation + neural pulse keyed to arousal."""
import streamlit as st
from services.music import render_player


def render_song_card(row, step: int | None = None, destination: bool = False, idx: int = 0) -> None:
    initial = row["Title"][0].upper() if row["Title"] else "—"
    step_label = "Destination" if destination else (f"Step {step} of 5" if step else "")
    card_class = "aura-card song-card destination-card" if destination else "aura-card song-card"

    # Arousal (Energy) drives pulse speed — high energy = fast pulse, low = slow
    energy = float(row.get("Energy", 0.5))
    # Map energy [0,1] to pulse duration [2.2s slow, 0.7s fast]
    pulse_speed = round(2.2 - (energy * 1.5), 2)

    st.markdown(
        (
            f"<div class='{card_class}' data-idx='{idx}'>"
            f"<div class='song-artwork'>{initial}"
            f"<div class='neural-pulse' style='--pulse-speed:{pulse_speed}s;'></div>"
            f"</div>"
            f"<div class='song-meta'>"
            f"<p class='song-title'>{row['Title']}</p>"
            f"<p class='song-artist'>{row['Artist']}</p>"
            f"</div>"
            f"<div class='song-step'>{step_label}</div>"
            f"</div>"
        ),
        unsafe_allow_html=True,
    )
    render_player(row["Title"], row["Artist"])
    st.markdown(
        (
            "<div style='display:flex; gap:6px; flex-wrap:wrap; margin: 6px 0 20px 0;'>"
            f"<span class='coord-pill'>E {row['Energy']:.2f}</span>"
            f"<span class='coord-pill'>V {row['Valence']:.2f}</span>"
            f"<span class='coord-pill'>A {row['Acousticness']:.2f}</span>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )