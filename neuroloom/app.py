"""NeuroLoom — weaving cognitive states, one song at a time."""
import streamlit as st

from config import OPENWEATHER_API_KEY, DEFAULT_CITY, BRIDGE_LENGTH
from styles import BASE_CSS, PALETTES
from data import SONGS
from core.bridge import build_bridge
from services.gemini import analyze_with_gemini, generate_fortune
from services.weather import fetch_weather, palette_for, mood_label
from components.song_card import render_song_card
from components.breathing import render_breathing_orb
from components.fortune import render_fortune


# ----- Page config -----
st.set_page_config(page_title="NeuroLoom", page_icon=None, layout="wide")


# ----- Session state -----
for key, default in {
    "playlist": None,
    "analysis": None,
    "fortune": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ----- Weather + theming -----
weather = fetch_weather(DEFAULT_CITY, OPENWEATHER_API_KEY)
palette_key = palette_for(weather["condition"])

st.markdown(BASE_CSS, unsafe_allow_html=True)
st.markdown(PALETTES[palette_key], unsafe_allow_html=True)


# ----- Header -----
st.markdown("<h1>NeuroLoom</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='opacity:0.75; font-size:1.05rem; margin-top:-8px;'>"
    "Weaving cognitive states, one song at a time.</p>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<div class='weather-pill'><b>{weather['city']}</b> &middot; {weather['description']} "
    f"&middot; {weather['temp']:.0f}&deg;C &middot; <i>{mood_label(weather['condition'])}</i></div>",
    unsafe_allow_html=True,
)


# ----- Brain dump input -----
st.markdown("<h3>Quick brain-dump</h3>", unsafe_allow_html=True)
st.markdown(
    "<span class='step-label'>Write freely. Gemini reads the signal beneath the words.</span>",
    unsafe_allow_html=True,
)
brain_dump = st.text_area(
    label=" ",
    placeholder="I'm so tired. Everything feels like too much today and I can't focus on anything...",
    height=140,
    key="brain_dump",
)

col_a, _ = st.columns([1, 2])
with col_a:
    if st.button("Build my bridge", use_container_width=True) and brain_dump.strip():
        with st.spinner("Reading the signal beneath your words..."):
            analysis = analyze_with_gemini(brain_dump)
        st.session_state.analysis = analysis
        st.session_state.playlist = build_bridge(
            SONGS,
            (analysis["start_energy"], analysis["start_valence"]),
            (analysis["target_energy"], analysis["target_valence"]),
            n=BRIDGE_LENGTH,
        )
        st.session_state.fortune = generate_fortune(brain_dump, analysis["detected_state"])


# ----- Detected state card -----
if st.session_state.analysis:
    a = st.session_state.analysis
    st.markdown(
        f"""
        <div class='aura-card'>
          <span class='step-label'>Detected state &middot; {a.get('source', 'gemini')}</span>
          <h3 style='margin:6px 0'>{a['detected_state'].title()}</h3>
          <p style='margin:4px 0 12px 0'>{a['narrative']}</p>
          <span class='coord-pill'>Start &middot; E {a['start_energy']:.2f} &middot; V {a['start_valence']:.2f}</span>
          <span class='coord-pill'>Target &middot; E {a['target_energy']:.2f} &middot; V {a['target_valence']:.2f}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----- Playlist -----
if st.session_state.playlist is not None:
    st.markdown("<h3>Your bridge</h3>", unsafe_allow_html=True)
    for i, row in st.session_state.playlist.iterrows():
        render_song_card(row, step=i + 1)


# ----- Fortune cookie -----
if st.session_state.fortune:
    st.markdown("<hr/>", unsafe_allow_html=True)
    render_fortune(st.session_state.fortune)


# ----- Breathing orb -----
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("<h3>Still need to reset?</h3>", unsafe_allow_html=True)
render_breathing_orb()