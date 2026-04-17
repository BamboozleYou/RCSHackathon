"""Single song card with inline player."""
import streamlit as st
from services.music import render_player


def render_song_card(row, step: int | None = None) -> None:
    prefix = "" if step is None else f"<span class='step-label'>Step {step} of 5</span>"
    st.markdown(
        f"""
        <div class='aura-card'>
          {prefix}
          <h4 style='margin:6px 0 4px 0; font-weight:600;'>{row['Title']}</h4>
          <p style='margin:0; opacity:0.7; font-size:0.9rem;'>{row['Artist']}</p>
          <p style='margin:8px 0 0 0; opacity:0.55; font-size:0.78rem; letter-spacing:0.04em;'>
              Energy {row['Energy']:.2f} &nbsp;&middot;&nbsp; Valence {row['Valence']:.2f}
              &nbsp;&middot;&nbsp; Acousticness {row['Acousticness']:.2f}
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_player(row["Title"], row["Artist"])