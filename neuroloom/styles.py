"""Base CSS + palettes + organic overrides for the 30-min sprint."""


BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

#MainMenu, header, footer, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { visibility: hidden; display: none; }

html, body, [class*="css"], .stApp, .stMarkdown, button, input, textarea, p, label {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: var(--bg-grad);
    color: var(--text);
    transition: background 1.4s cubic-bezier(0.2, 0.8, 0.2, 1), color 1.4s ease;
    position: relative;
    overflow-x: hidden;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0, 0 0 0 0 0, 0 0 0 0 0, 0 0 0 0.06 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    pointer-events: none; z-index: 1; opacity: 0.35; mix-blend-mode: overlay;
}
.stApp > div { position: relative; z-index: 2; }

.block-container { max-width: 900px; padding: 3.5rem 1.5rem 10rem 6.5rem; }

/* ============= HERO ============= */
.hero-grid { display: grid; grid-template-columns: 1fr auto; gap: 24px; align-items: end; margin-bottom: 32px; animation: fadeSlideUp 1.1s cubic-bezier(0.2, 0.8, 0.2, 1); }
.hero-grid h1 { font-family: 'Instrument Serif', serif !important; font-size: 4.4rem !important; font-weight: 400 !important; letter-spacing: -0.035em !important; line-height: 0.95 !important; margin: 0 !important; color: var(--text) !important; }
.hero-grid h1 em { font-style: italic; color: var(--accent); }
.hero-tagline { font-family: 'Instrument Serif', serif; font-style: italic; font-size: 1.2rem; opacity: 0.72; margin: 14px 0 0 0; letter-spacing: -0.01em; max-width: 480px; }
.hero-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; padding-bottom: 8px; text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.12em; opacity: 0.6; }
.hero-meta .now { font-size: 1.8rem; font-family: 'Instrument Serif', serif; font-style: italic; font-weight: 400; letter-spacing: -0.02em; opacity: 0.85; margin: 0; line-height: 1; }
.hero-meta .loc-pill { margin-top: 4px; padding: 6px 12px; border-radius: 999px; background: var(--card-bg); border: 1px solid var(--card-border); backdrop-filter: blur(16px); display: flex; align-items: center; gap: 8px; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.18em; }
.hero-meta .loc-pill .pulse { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 10px var(--accent-glow); animation: weatherPulse 2.4s ease-in-out infinite; }
@keyframes weatherPulse { 0%,100% { box-shadow: 0 0 10px var(--accent-glow); opacity: 1; } 50% { box-shadow: 0 0 18px var(--accent-glow); opacity: 0.7; } }

h2, h3, h4 { color: var(--text) !important; font-weight: 500 !important; letter-spacing: -0.015em !important; }
p, label, .stMarkdown { color: var(--text) !important; }
.section-label { display: block; font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; font-weight: 500; letter-spacing: 0.26em; text-transform: uppercase; opacity: 0.5; margin: 42px 0 14px 0; }

.aura-card {
    background: var(--card-bg);
    backdrop-filter: blur(12px) saturate(1.3);
    -webkit-backdrop-filter: blur(12px) saturate(1.3);
    border-radius: 20px;
    padding: 22px 26px;
    margin: 14px 0;
    border: 1px solid var(--card-border);
    box-shadow: 0 1px 0 var(--card-highlight) inset, 0 10px 36px var(--shadow);
    transition: transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.4s ease, backdrop-filter 0.4s ease;
    animation: fadeSlideUp 0.9s cubic-bezier(0.2, 0.8, 0.2, 1);
}

/* ============= TYPING BLOB — lives behind the brain-dump ============= */
.typing-blob-wrap {
    position: relative;
    margin: 0 0 18px 0;
    z-index: 5;
}
.typing-blob {
    position: absolute;
    inset: -40px;
    border-radius: 40px;
    filter: blur(60px);
    opacity: 0.55;
    pointer-events: none;
    z-index: -1;
    background: radial-gradient(ellipse at 20% 30%, var(--blob-a, var(--accent)) 0%, transparent 55%),
                radial-gradient(ellipse at 80% 70%, var(--blob-b, var(--accent-hover)) 0%, transparent 55%),
                radial-gradient(ellipse at 50% 50%, var(--blob-c, var(--accent-glow)) 0%, transparent 60%);
    animation: blobDrift 12s ease-in-out infinite;
    transition: background 1.5s ease;
}
@keyframes blobDrift {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33%      { transform: translate(20px, -10px) scale(1.08); }
    66%      { transform: translate(-15px, 12px) scale(0.95); }
}

/* Brain-dump textarea — MAX blur/prominence */
.stTextArea label { display: none !important; }
.stTextArea textarea {
    background: var(--card-bg) !important;
    color: var(--text) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 22px !important;
    padding: 24px !important;
    font-size: 1.08rem !important;
    line-height: 1.6 !important;
    backdrop-filter: blur(28px) saturate(1.6) !important;
    -webkit-backdrop-filter: blur(28px) saturate(1.6) !important;
    box-shadow: 0 1px 0 var(--card-highlight) inset, 0 20px 60px var(--shadow) !important;
    transition: all 0.4s ease !important;
    position: relative;
    z-index: 2;
}
.stTextArea textarea::placeholder { color: var(--text) !important; opacity: 0.4 !important; font-style: italic; }
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 1px 0 var(--card-highlight) inset, 0 0 0 3px var(--accent-glow), 0 20px 60px var(--shadow) !important;
    outline: none !important;
}

.stButton > button { background: var(--accent); color: var(--btn-text); border: none; border-radius: 14px; padding: 14px 36px; font-weight: 600; font-size: 0.94rem; letter-spacing: 0.01em; cursor: pointer; transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.25s ease, background 0.25s ease; box-shadow: 0 1px 0 rgba(255,255,255,0.3) inset, 0 4px 18px var(--accent-shadow); white-space: nowrap; }
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 1px 0 rgba(255,255,255,0.3) inset, 0 12px 30px var(--accent-shadow-hover); background: var(--accent-hover); }
.stButton > button:active { transform: translateY(0); }

.step-label { display: inline-block; font-family: 'JetBrains Mono', monospace; opacity: 0.5; font-size: 0.66rem; letter-spacing: 0.22em; text-transform: uppercase; font-weight: 500; }
.coord-pill { display: inline-block; padding: 5px 12px; border-radius: 999px; background: var(--card-bg); border: 1px solid var(--card-border); font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 500; letter-spacing: 0.03em; margin: 3px 5px 3px 0; }

.mood-card { background: var(--card-bg); backdrop-filter: blur(20px) saturate(1.4); border-radius: 22px; padding: 28px 32px; margin: 16px 0 32px 0; border: 1px solid var(--card-border); box-shadow: 0 1px 0 var(--card-highlight) inset, 0 16px 50px var(--shadow); animation: fadeSlideUp 1.1s cubic-bezier(0.2, 0.8, 0.2, 1); }
.mood-card .mood-state { font-family: 'Instrument Serif', serif; font-size: 2.6rem; font-weight: 400; line-height: 1; margin: 10px 0 12px 0; letter-spacing: -0.02em; color: var(--text); }
.mood-card .mood-narrative { font-size: 0.98rem; line-height: 1.6; opacity: 0.78; margin: 0 0 14px 0; }

/* ============= ORGANIC / STAGGERED SONG CARDS ============= */
.song-card {
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 18px;
    align-items: center;
    padding: 16px 22px !important;
    backdrop-filter: blur(8px) saturate(1.2) !important;
    -webkit-backdrop-filter: blur(8px) saturate(1.2) !important;
    transform-origin: center;
}
.song-card:hover { transform: rotate(0deg) translateY(-3px) scale(1.01) !important; backdrop-filter: blur(18px) saturate(1.4) !important; z-index: 10; position: relative; }
.song-card .song-artwork { width: 46px; height: 46px; border-radius: 10px; background: linear-gradient(135deg, var(--accent), var(--accent-hover)); display: flex; align-items: center; justify-content: center; font-family: 'Instrument Serif', serif; font-size: 1.4rem; color: var(--btn-text); box-shadow: 0 4px 12px var(--accent-shadow); flex-shrink: 0; position: relative; }
.song-card .song-title { font-size: 1.02rem; font-weight: 600; letter-spacing: -0.01em; margin: 0; line-height: 1.2; }
.song-card .song-artist { margin: 3px 0 0 0; opacity: 0.65; font-size: 0.86rem; }
.song-card .song-step { font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; letter-spacing: 0.18em; opacity: 0.4; text-transform: uppercase; white-space: nowrap; }

/* Staggered rotations + widths — applied by data-attr set in Python */
.song-card[data-idx='0'] { transform: rotate(-1.2deg) translateX(-8px); width: 94%; }
.song-card[data-idx='1'] { transform: rotate(0.8deg)  translateX(12px); width: 96%; margin-left: auto; }
.song-card[data-idx='2'] { transform: rotate(-0.6deg) translateX(-4px); width: 98%; }
.song-card[data-idx='3'] { transform: rotate(1.1deg)  translateX(18px); width: 92%; margin-left: auto; }
.song-card[data-idx='4'] { transform: rotate(-0.4deg) translateX(0);    width: 100%; }

/* ============= NEURAL PULSE — next to song artwork, keyed to arousal ============= */
.neural-pulse {
    position: absolute;
    inset: -6px;
    border-radius: 14px;
    border: 2px solid var(--accent);
    opacity: 0;
    animation: neuralPulse var(--pulse-speed, 1.6s) ease-out infinite;
    pointer-events: none;
}
.neural-pulse::after {
    content: '';
    position: absolute;
    inset: 4px;
    border-radius: 10px;
    border: 1.5px solid var(--accent);
    opacity: 0.5;
    animation: neuralPulse var(--pulse-speed, 1.6s) ease-out infinite;
    animation-delay: calc(var(--pulse-speed, 1.6s) * 0.4);
}
@keyframes neuralPulse {
    0%   { transform: scale(0.85); opacity: 0.85; }
    70%  { transform: scale(1.35); opacity: 0; }
    100% { transform: scale(1.35); opacity: 0; }
}

.destination-card { padding: 30px !important; background: var(--card-bg) !important; border: 1px solid var(--accent) !important; box-shadow: 0 1px 0 var(--card-highlight) inset, 0 16px 56px var(--accent-shadow) !important; margin: 24px 0 14px 0 !important; backdrop-filter: blur(24px) saturate(1.5) !important; }
.destination-card .song-artwork { width: 68px; height: 68px; border-radius: 14px; font-size: 2rem; box-shadow: 0 8px 24px var(--accent-shadow-hover); }
.destination-card .song-title { font-family: 'Instrument Serif', serif; font-size: 1.55rem; font-weight: 400; letter-spacing: -0.02em; }
.destination-card .song-artist { font-size: 0.95rem; opacity: 0.72; margin-top: 4px; }
.destination-card .song-step { color: var(--accent); opacity: 0.9; }

iframe { border-radius: 14px !important; }
hr { border: none; height: 1px; background: linear-gradient(90deg, transparent, var(--card-border), transparent); margin: 48px 0; }

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--card-border); border-radius: 999px; border: 2px solid transparent; background-clip: padding-box; }

@keyframes fadeSlideUp { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }

/* ============= CALCULATING... ANIMATION (for ResourceExhausted/any slow op) ============= */
.calculating {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 22px 26px;
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid var(--card-border);
    box-shadow: 0 10px 36px var(--shadow);
    margin: 16px 0;
    animation: fadeSlideUp 0.5s ease;
}
.calculating .calc-dots {
    display: flex; gap: 6px;
}
.calculating .calc-dots span {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--accent);
    animation: calcDot 1.2s ease-in-out infinite;
}
.calculating .calc-dots span:nth-child(2) { animation-delay: 0.15s; }
.calculating .calc-dots span:nth-child(3) { animation-delay: 0.3s; }
.calculating .calc-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    opacity: 0.7;
}
@keyframes calcDot {
    0%, 100% { transform: scale(0.6); opacity: 0.4; }
    50%      { transform: scale(1.1); opacity: 1; }
}

/* ============= WEATHER SIDEBAR ============= */
.wx-pill {
    position: fixed;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 99;
    width: 56px;
    padding: 8px 0;
    background: var(--card-bg);
    backdrop-filter: blur(20px) saturate(1.4);
    border: 1px solid var(--card-border);
    border-radius: 100px;
    box-shadow: 0 10px 36px var(--shadow);
    display: flex;
    flex-direction: column;
    gap: 6px;
    align-items: center;
    pointer-events: none;
}
.wx-icon {
    width: 40px; height: 40px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 50%;
    color: var(--text);
    opacity: 0.55;
    transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.wx-icon svg { width: 22px; height: 22px; display: block; }
.wx-icon-active {
    color: var(--accent);
    opacity: 1;
    background: var(--card-highlight);
    transform: scale(1.08);
    box-shadow: 0 0 14px var(--accent-glow);
}
.stApp div[class*="st-key-wx_"] {
    position: fixed !important;
    left: 22px !important;
    width: 40px !important;
    height: 40px !important;
    margin: 0 !important;
    z-index: 100 !important;
}
.stApp div.st-key-wx_clear        { top: calc(50vh - 138px) !important; }
.stApp div.st-key-wx_clouds       { top: calc(50vh - 92px)  !important; }
.stApp div.st-key-wx_rain         { top: calc(50vh - 46px)  !important; }
.stApp div.st-key-wx_thunderstorm { top: calc(50vh + 0px)   !important; }
.stApp div.st-key-wx_snow         { top: calc(50vh + 46px)  !important; }
.stApp div.st-key-wx_mist         { top: calc(50vh + 92px)  !important; }
.stApp div[class*="st-key-wx_"] button {
    width: 40px !important; height: 40px !important;
    min-width: 40px !important; min-height: 40px !important;
    padding: 0 !important; border-radius: 50% !important;
    background: transparent !important; color: transparent !important;
    border: none !important; box-shadow: none !important;
    font-size: 0 !important; cursor: pointer !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}
.stApp div[class*="st-key-wx_"] button:hover {
    opacity: 0.12 !important; background: var(--text) !important; transform: none !important;
}

/* ============= SECRET DOTS ============= */
.stApp div.st-key-secret_1, .stApp div.st-key-secret_2, .stApp div.st-key-secret_3 {
    position: fixed !important; z-index: 98 !important; width: auto !important; margin: 0 !important;
}
.stApp div.st-key-secret_1 { top: 40px !important; right: 40px !important; left: auto !important; bottom: auto !important; }
.stApp div.st-key-secret_2 { top: 50% !important; right: 40px !important; left: auto !important; bottom: auto !important; }
.stApp div.st-key-secret_3 { bottom: 40px !important; right: 40px !important; left: auto !important; top: auto !important; }
.stApp div.st-key-secret_1 button, .stApp div.st-key-secret_2 button, .stApp div.st-key-secret_3 button {
    width: 10px !important; height: 10px !important;
    min-width: 10px !important; min-height: 10px !important;
    padding: 0 !important; border-radius: 50% !important;
    background: var(--text) !important; opacity: 0.25 !important;
    border: none !important; box-shadow: none !important;
    font-size: 0 !important; color: transparent !important;
    transition: all 0.45s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
    animation: dotAppear 0.7s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.stApp div.st-key-secret_1 button:hover, .stApp div.st-key-secret_2 button:hover, .stApp div.st-key-secret_3 button:hover {
    opacity: 0.7 !important;
    transform: scale(1.8) !important;
    box-shadow: 0 0 18px var(--accent-glow), 0 0 36px var(--accent-glow) !important;
}
@keyframes dotAppear { from { opacity: 0; transform: scale(0.2); } to { opacity: 0.25; transform: scale(1); } }

/* ============= SUBCONSCIOUS MODE — full-screen particle field hides UI ============= */
body.subconscious-active .block-container,
body.subconscious-active .wx-pill,
body.subconscious-active div[class*="st-key-wx_"],
body.subconscious-active div[class*="st-key-secret_"] {
    opacity: 0 !important;
    pointer-events: none !important;
    transition: opacity 0.8s ease;
}
body.subconscious-active .stApp::before { opacity: 0.15 !important; }
</style>
"""


PALETTES = {
    "clear": """<style>:root { --bg-grad: linear-gradient(135deg, #ffe5b4 0%, #ffd6c7 30%, #fcb69f 60%, #c7dff2 100%); --text: #3a2e2a; --card-bg: rgba(255,255,255,0.5); --card-border: rgba(255,255,255,0.7); --card-highlight: rgba(255,255,255,0.6); --shadow: rgba(200,150,100,0.18); --shadow-hover: rgba(200,150,100,0.3); --accent: #e88868; --accent-hover: #d66d4a; --accent-glow: rgba(232,136,104,0.4); --accent-shadow: rgba(232,136,104,0.4); --accent-shadow-hover: rgba(232,136,104,0.58); --btn-text: #ffffff; }</style>""",
    "clouds": """<style>:root { --bg-grad: linear-gradient(135deg, #d4d8de 0%, #b2b8c4 50%, #8a919f 100%); --text: #1f2229; --card-bg: rgba(255,255,255,0.4); --card-border: rgba(255,255,255,0.55); --card-highlight: rgba(255,255,255,0.5); --shadow: rgba(60,70,90,0.2); --shadow-hover: rgba(60,70,90,0.32); --accent: #556480; --accent-hover: #44516b; --accent-glow: rgba(85,100,128,0.4); --accent-shadow: rgba(85,100,128,0.4); --accent-shadow-hover: rgba(85,100,128,0.58); --btn-text: #ffffff; }</style>""",
    "rain": """<style>:root { --bg-grad: linear-gradient(135deg, #141a2e 0%, #242b48 45%, #35304f 100%); --text: #dfe3f0; --card-bg: rgba(255,255,255,0.05); --card-border: rgba(255,255,255,0.1); --card-highlight: rgba(255,255,255,0.08); --shadow: rgba(0,0,0,0.4); --shadow-hover: rgba(0,0,0,0.55); --accent: #93a4dd; --accent-hover: #7a8dd0; --accent-glow: rgba(147,164,221,0.4); --accent-shadow: rgba(147,164,221,0.35); --accent-shadow-hover: rgba(147,164,221,0.55); --btn-text: #0b1022; }</style>""",
    "thunderstorm": """<style>:root { --bg-grad: linear-gradient(135deg, #08080f 0%, #1a1033 45%, #2d1b4e 100%); --text: #ebdff7; --card-bg: rgba(255,255,255,0.035); --card-border: rgba(200,160,240,0.18); --card-highlight: rgba(200,160,240,0.1); --shadow: rgba(0,0,0,0.55); --shadow-hover: rgba(140,100,200,0.4); --accent: #c49ee6; --accent-hover: #b588dc; --accent-glow: rgba(196,158,230,0.4); --accent-shadow: rgba(196,158,230,0.45); --accent-shadow-hover: rgba(196,158,230,0.65); --btn-text: #08080f; }</style>""",
    "snow": """<style>:root { --bg-grad: linear-gradient(135deg, #eef3f9 0%, #dbe6f3 50%, #c5d4e8 100%); --text: #1a2a44; --card-bg: rgba(255,255,255,0.6); --card-border: rgba(255,255,255,0.85); --card-highlight: rgba(255,255,255,0.8); --shadow: rgba(100,130,170,0.2); --shadow-hover: rgba(100,130,170,0.32); --accent: #547198; --accent-hover: #3f5c82; --accent-glow: rgba(84,113,152,0.4); --accent-shadow: rgba(84,113,152,0.4); --accent-shadow-hover: rgba(84,113,152,0.58); --btn-text: #ffffff; }</style>""",
    "mist": """<style>:root { --bg-grad: linear-gradient(135deg, #dcd8ce 0%, #c0bbaf 50%, #a39e90 100%); --text: #24221c; --card-bg: rgba(255,255,255,0.4); --card-border: rgba(255,255,255,0.55); --card-highlight: rgba(255,255,255,0.5); --shadow: rgba(90,80,65,0.2); --shadow-hover: rgba(90,80,65,0.32); --accent: #756a58; --accent-hover: #5d5445; --accent-glow: rgba(117,106,88,0.4); --accent-shadow: rgba(117,106,88,0.4); --accent-shadow-hover: rgba(117,106,88,0.58); --btn-text: #ffffff; }</style>""",
    "party": """<style>:root {
        --bg-grad: linear-gradient(125deg, #ff6b9d 0%, #feca57 18%, #48dbfb 36%, #1dd1a1 54%, #a29bfe 72%, #ff9ff3 90%, #ff6b9d 100%);
        --text: #1a0b2e;
        --card-bg: rgba(255, 255, 255, 0.65);
        --card-border: rgba(255, 255, 255, 0.95);
        --card-highlight: rgba(255, 255, 255, 0.85);
        --shadow: rgba(220, 50, 130, 0.25);
        --shadow-hover: rgba(220, 50, 130, 0.4);
        --accent: #ff2975;
        --accent-hover: #ff0055;
        --accent-glow: rgba(255, 41, 117, 0.5);
        --accent-shadow: rgba(255, 41, 117, 0.5);
        --accent-shadow-hover: rgba(255, 41, 117, 0.7);
        --btn-text: #ffffff;
    }
    .stApp {
        background-size: 400% 400% !important;
        animation: partyGradient 8s ease infinite !important;
    }
    @keyframes partyGradient {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>""",
}