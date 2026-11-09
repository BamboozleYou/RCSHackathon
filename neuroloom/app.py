"""NeuroLoom — weaving cognitive states, one song at a time."""
from datetime import datetime

import streamlit as st

from config import OPENWEATHER_API_KEY, DEFAULT_CITY, BRIDGE_LENGTH
from styles import BASE_CSS, PALETTES
from data import SONGS
from core.bridge import build_bridge
from services.gemini import analyze_with_gemini, generate_fortune
from services.weather import fetch_weather, palette_for, mood_label
from components.song_card import render_song_card
from components.breathing import render_breathing_orb
from components.weather_switcher import render_weather_switcher
from components.subconscious import render_subconscious


st.set_page_config(page_title="NeuroLoom", page_icon=None, layout="wide")


# ---------- Session state ----------
for key, default in {
    "playlist": None,
    "analysis": None,
    "fortune": None,
    "palette_override": None,
    "secret_progress": 0,
    "fortune_unlocked": False,
    "subconscious_active": False,
    "party_mode": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ---------- Weather + palette selection ----------
# Priority: palette_override (user sidebar click) > party_mode (post-subconscious) > real weather
weather = fetch_weather(DEFAULT_CITY, OPENWEATHER_API_KEY)
real_palette = palette_for(weather["condition"])

if st.session_state.palette_override is not None:
    palette_key = st.session_state.palette_override
elif st.session_state.party_mode:
    palette_key = "party"
else:
    palette_key = real_palette


# ---------- Inject base + active palette ----------
st.markdown(BASE_CSS, unsafe_allow_html=True)
st.markdown(PALETTES[palette_key], unsafe_allow_html=True)


# ==========================================================
# SUBCONSCIOUS MODE — takes over the whole page
# ==========================================================
if st.session_state.subconscious_active:
    # Exit button rendered FIRST so its click handler fires cleanly before st.stop()
    exit_clicked = st.button("exit subconscious", key="exit_sub")

    if exit_clicked:
        st.session_state.subconscious_active = False
        st.session_state.party_mode = True
        # Don't call st.stop() — let Streamlit rerun naturally with the new state
        st.rerun()

    # Render the overlay (visual only, no interactive logic for exit)
    st.markdown(
        "<script>document.body.classList.add('subconscious-active');</script>",
        unsafe_allow_html=True,
    )
    render_subconscious()

    # Style the exit button to sit at bottom-center above the canvas
    st.markdown(
        """<style>
        .st-key-exit_sub {
            position: fixed !important;
            bottom: 40px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            z-index: 10001 !important;
            width: auto !important;
        }
        .st-key-exit_sub button {
            background: rgba(255,255,255,0.1) !important;
            color: rgba(255,255,255,0.7) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255,255,255,0.25) !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.72rem !important;
            letter-spacing: 0.24em !important;
            text-transform: uppercase !important;
            padding: 12px 28px !important;
            border-radius: 999px !important;
            font-weight: 500 !important;
            box-shadow: 0 6px 24px rgba(0,0,0,0.3) !important;
        }
        .st-key-exit_sub button:hover {
            background: rgba(255,255,255,0.2) !important;
            color: rgba(255,255,255,1) !important;
            transform: translateY(-1px) !important;
        }
        </style>""",
        unsafe_allow_html=True,
    )
    st.stop()


# ==========================================================
# NORMAL APP (also runs in party mode)
# ==========================================================

# ---------- Sidebar ----------
render_weather_switcher(real_palette)


# ---------- Hero ----------
now_str = datetime.now().strftime("%H:%M")
if st.session_state.palette_override is not None:
    override_tag = " · you're steering"
elif st.session_state.party_mode:
    override_tag = " · celebration mode"
else:
    override_tag = ""

mood_descriptor = mood_label(
    palette_key if (st.session_state.palette_override or st.session_state.party_mode) else weather["condition"]
)

st.markdown(
    (
        "<div class='hero-grid'>"
        "<div>"
        "<h1>Neuro<em>Loom</em></h1>"
        "<p class='hero-tagline'>Weaving cognitive states, one song at a time.</p>"
        "</div>"
        "<div class='hero-meta'>"
        f"<p class='now'>{now_str}</p>"
        "<div class='loc-pill'>"
        "<span class='pulse'></span>"
        f"<span>{weather['city']} · {weather['temp']:.0f}°</span>"
        "</div>"
        f"<div style='margin-top:6px;'>{weather['description']}{override_tag}</div>"
        f"<div style='font-style:italic; opacity:0.7;'>{mood_descriptor}</div>"
        "</div>"
        "</div>"
    ),
    unsafe_allow_html=True,
)


# ---------- Brain-dump with typing blob ----------
st.markdown("<span class='section-label'>Brain-dump</span>", unsafe_allow_html=True)

current_text = st.session_state.get("brain_dump", "").lower()


def _blob_colors_from_text(text: str) -> tuple[str, str, str]:
    if not text or len(text) < 3:
        return "var(--accent)", "var(--accent-hover)", "var(--accent-glow)"
    positive = ["happy", "great", "amazing", "love", "excited", "good", "wonderful", "grateful", "joy", "peaceful", "bright"]
    negative = ["sad", "tired", "exhausted", "overwhelmed", "stressed", "angry", "hurt", "lonely", "empty", "stuck", "heavy"]
    contemplative = ["thinking", "reflect", "quiet", "alone", "wonder", "deep", "lost", "wander", "drift", "slow"]
    p = sum(k in text for k in positive)
    n = sum(k in text for k in negative)
    c = sum(k in text for k in contemplative)
    if p > n and p > c:
        return "#ffb347", "#ff7e5f", "rgba(255, 179, 71, 0.6)"
    if n > p and n > c:
        return "#4a6fa5", "#2e4a70", "rgba(74, 111, 165, 0.6)"
    if c > 0:
        return "#8e7cc3", "#5d4b8e", "rgba(142, 124, 195, 0.6)"
    return "var(--accent)", "var(--accent-hover)", "var(--accent-glow)"


blob_a, blob_b, blob_c = _blob_colors_from_text(current_text)
st.markdown(
    f"<div class='typing-blob-wrap'><div class='typing-blob' style='--blob-a:{blob_a}; --blob-b:{blob_b}; --blob-c:{blob_c};'></div></div>",
    unsafe_allow_html=True,
)

brain_dump = st.text_area(
    label="brain_dump",
    label_visibility="collapsed",
    placeholder="Write freely. Tell me what's on your mind, how the day has landed, what you're carrying...",
    height=160,
    key="brain_dump",
)


def _show_calculating(message: str = "reading the signal"):
    st.markdown(
        (
            "<div class='calculating'>"
            "<div class='calc-dots'><span></span><span></span><span></span></div>"
            f"<div class='calc-text'>{message}</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


col_a, _ = st.columns([1, 2])
with col_a:
    if st.button("Build my bridge  →", use_container_width=True) and brain_dump.strip():
        placeholder = st.empty()
        with placeholder.container():
            _show_calculating("reading the signal beneath your words")
        try:
            analysis = analyze_with_gemini(brain_dump)
        except Exception:
            analysis = analyze_with_gemini(brain_dump)
        st.session_state.analysis = analysis
        st.session_state.playlist = build_bridge(
            SONGS,
            (analysis["start_energy"], analysis["start_valence"]),
            (analysis["target_energy"], analysis["target_valence"]),
            n=BRIDGE_LENGTH,
        )
        try:
            st.session_state.fortune = generate_fortune(brain_dump, analysis["detected_state"])
        except Exception:
            st.session_state.fortune = "The quietest room in your mind is the one you haven't entered yet."
        placeholder.empty()


# ---------- Detected mood card ----------
if st.session_state.analysis:
    a = st.session_state.analysis
    source = a.get("source", "gemini")
    if "ResourceExhausted" in source:
        source_display = "offline · quota resting"
    elif "fallback" in source:
        source_display = "offline"
    else:
        source_display = source

    mood_html = (
        "<div class='mood-card'>"
        f"<span class='step-label'>Detected mood · {source_display}</span>"
        f"<div class='mood-state'>{a['detected_state'].title()}</div>"
        f"<p class='mood-narrative'>{a['narrative']}</p>"
        f"<span class='coord-pill'>Start · E {a['start_energy']:.2f} · V {a['start_valence']:.2f}</span>"
        f"<span class='coord-pill'>Target · E {a['target_energy']:.2f} · V {a['target_valence']:.2f}</span>"
        "</div>"
    )
    st.markdown(mood_html, unsafe_allow_html=True)


# ---------- Staggered playlist ----------
if st.session_state.playlist is not None:
    total = len(st.session_state.playlist)
    st.markdown("<span class='section-label'>Your bridge</span>", unsafe_allow_html=True)
    for i, row in st.session_state.playlist.iterrows():
        is_final = (i == total - 1)
        render_song_card(row, step=i + 1, destination=is_final, idx=i)


# ---------- Breathing orb ----------
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("<span class='section-label'>Reset</span>", unsafe_allow_html=True)
render_breathing_orb()


# ==========================================================
# Secret sequence — 3 dots unlock subconscious state
# ==========================================================
if st.button(" ", key="secret_1"):
    if st.session_state.secret_progress < 1:
        st.session_state.secret_progress = 1
    st.rerun()

if st.session_state.secret_progress >= 1:
    if st.button(" ", key="secret_2"):
        if st.session_state.secret_progress < 2:
            st.session_state.secret_progress = 2
        st.rerun()

if st.session_state.secret_progress >= 2:
    if st.button(" ", key="secret_3"):
        st.session_state.secret_progress = 3
        st.session_state.fortune_unlocked = True
        st.session_state.subconscious_active = True
        st.rerun()

active = (
    "opacity: 0.9 !important; background: var(--accent) !important; "
    "transform: scale(1.8) !important; "
    "box-shadow: 0 0 20px var(--accent-glow), 0 0 40px var(--accent-glow) !important;"
)
rules = ""
if st.session_state.secret_progress >= 1:
    rules += f".st-key-secret_1 button {{ {active} }} "
if st.session_state.secret_progress >= 2:
    rules += f".st-key-secret_2 button {{ {active} }} "
if rules:
    st.markdown(f"<style>{rules}</style>", unsafe_allow_html=True)