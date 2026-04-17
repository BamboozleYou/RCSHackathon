"""All CSS: base stylesheet + two dynamic palettes."""

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Hide Streamlit chrome */
#MainMenu, header, footer, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { visibility: hidden; display: none; }

/* Typography */
html, body, [class*="css"], .stApp, .stMarkdown, button, input, textarea, p, h1, h2, h3, h4, label {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.stApp {
    background: var(--bg-grad);
    color: var(--text);
    transition: background 1.4s ease;
}
.block-container { max-width: 860px; padding-top: 3rem; }
h1 { font-size: 2.7rem; font-weight: 700; letter-spacing: -0.03em; }
h1, h2, h3, h4 { color: var(--text) !important; font-weight: 600; letter-spacing: -0.015em; }
p, label, .stMarkdown { color: var(--text) !important; }

/* Glassmorphic cards */
.aura-card {
    background: var(--card-bg);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    border-radius: 20px;
    padding: 22px 26px;
    margin: 14px 0;
    border: 1px solid var(--card-border);
    box-shadow: 0 8px 32px var(--shadow);
    transition: transform 0.35s ease, box-shadow 0.35s ease;
}
.aura-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 44px var(--shadow-hover);
}

/* Weather pill */
.weather-pill {
    background: var(--card-bg);
    padding: 10px 18px;
    border-radius: 999px;
    display: inline-block;
    margin-bottom: 18px;
    border: 1px solid var(--card-border);
    font-size: 0.88rem;
    backdrop-filter: blur(14px);
}

/* Text area */
.stTextArea textarea {
    background: var(--card-bg) !important;
    color: var(--text) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 18px !important;
    padding: 18px !important;
    font-size: 1rem !important;
    backdrop-filter: blur(14px);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 18px var(--shadow);
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow), 0 4px 18px var(--shadow) !important;
    outline: none !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent);
    color: var(--btn-text);
    border: none;
    border-radius: 14px;
    padding: 12px 30px;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.01em;
    cursor: pointer;
    transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1),
                box-shadow 0.25s ease, background 0.25s ease;
    box-shadow: 0 4px 16px var(--accent-shadow);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 26px var(--accent-shadow-hover);
    background: var(--accent-hover);
}
.stButton > button:active { transform: translateY(0); }

/* Pills / labels */
.step-label {
    opacity: 0.55; font-size: 0.7rem;
    letter-spacing: 0.2em; text-transform: uppercase; font-weight: 500;
}
.coord-pill {
    display: inline-block; padding: 4px 12px; border-radius: 999px;
    background: var(--card-bg); border: 1px solid var(--card-border);
    font-size: 0.76rem; margin: 4px 6px 4px 0; font-weight: 500;
}

/* YouTube iframe */
iframe { border-radius: 14px !important; }

/* Fortune cookie */
.fortune-cookie {
    background: var(--card-bg);
    backdrop-filter: blur(24px);
    border: 1px solid var(--card-border);
    border-radius: 22px;
    padding: 36px 40px;
    margin: 28px auto;
    max-width: 620px;
    text-align: center;
    box-shadow: 0 12px 40px var(--shadow);
    position: relative;
    animation: fortuneFadeIn 1.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.fortune-label {
    display: block;
    opacity: 0.45;
    font-size: 0.68rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    margin-bottom: 18px;
    font-weight: 500;
}
.fortune-text {
    font-family: 'Plus Jakarta Sans', serif !important;
    font-size: 1.35rem;
    font-weight: 300;
    line-height: 1.55;
    font-style: italic;
    letter-spacing: -0.005em;
    margin: 0;
    opacity: 0.92;
}
.fortune-mark {
    display: block;
    margin-top: 20px;
    font-size: 1.3rem;
    opacity: 0.35;
    letter-spacing: 0.3em;
}
@keyframes fortuneFadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Section divider */
hr {
    border: none;
    height: 1px;
    background: var(--card-border);
    margin: 32px 0;
}
</style>
"""

PALETTES = {
    "flow": """
    <style>:root {
        --bg-grad: linear-gradient(135deg, #ffd6c7 0%, #fde4d1 35%, #c7dff2 100%);
        --text: #3a2e2a;
        --card-bg: rgba(255, 255, 255, 0.48);
        --card-border: rgba(255, 255, 255, 0.65);
        --shadow: rgba(200, 150, 130, 0.18);
        --shadow-hover: rgba(200, 150, 130, 0.28);
        --accent: #f5a58a;
        --accent-hover: #ee8a69;
        --accent-glow: rgba(245, 165, 138, 0.28);
        --accent-shadow: rgba(245, 165, 138, 0.38);
        --accent-shadow-hover: rgba(245, 165, 138, 0.55);
        --btn-text: #ffffff;
    }</style>
    """,
    "fatigue": """
    <style>:root {
        --bg-grad: linear-gradient(135deg, #2d3142 0%, #4a4e6e 50%, #6b5b7a 100%);
        --text: #e8e6f0;
        --card-bg: rgba(255, 255, 255, 0.07);
        --card-border: rgba(255, 255, 255, 0.14);
        --shadow: rgba(0, 0, 0, 0.3);
        --shadow-hover: rgba(0, 0, 0, 0.45);
        --accent: #b6b0dc;
        --accent-hover: #9e98cd;
        --accent-glow: rgba(182, 176, 220, 0.3);
        --accent-shadow: rgba(182, 176, 220, 0.3);
        --accent-shadow-hover: rgba(182, 176, 220, 0.5);
        --btn-text: #1a1d2e;
    }</style>
    """,
}