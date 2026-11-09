"""Left-edge weather switcher with inline SVGs (no mask-image)."""
import streamlit as st

WEATHERS = ["clear", "clouds", "rain", "thunderstorm", "snow", "mist"]

SVG_ICONS = {
    "clear": """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round'><circle cx='12' cy='12' r='4'/><line x1='12' y1='2' x2='12' y2='4'/><line x1='12' y1='20' x2='12' y2='22'/><line x1='4.93' y1='4.93' x2='6.34' y2='6.34'/><line x1='17.66' y1='17.66' x2='19.07' y2='19.07'/><line x1='2' y1='12' x2='4' y2='12'/><line x1='20' y1='12' x2='22' y2='12'/><line x1='4.93' y1='19.07' x2='6.34' y2='17.66'/><line x1='17.66' y1='6.34' x2='19.07' y2='4.93'/></svg>""",
    "clouds": """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z'/></svg>""",
    "rain": """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25'/><line x1='8' y1='19' x2='8' y2='21'/><line x1='12' y1='19' x2='12' y2='23'/><line x1='16' y1='19' x2='16' y2='21'/></svg>""",
    "thunderstorm": """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M19 16.9A5 5 0 0 0 18 7h-1.26a8 8 0 1 0-11.62 9'/><polyline points='13 11 9 17 15 17 11 23'/></svg>""",
    "snow": """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M20 17.58A5 5 0 0 0 18 8h-1.26A8 8 0 1 0 4 16.25'/><line x1='8' y1='16' x2='8.01' y2='16'/><line x1='8' y1='20' x2='8.01' y2='20'/><line x1='12' y1='18' x2='12.01' y2='18'/><line x1='12' y1='22' x2='12.01' y2='22'/><line x1='16' y1='16' x2='16.01' y2='16'/><line x1='16' y1='20' x2='16.01' y2='20'/></svg>""",
    "mist": """<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round'><line x1='3' y1='8' x2='21' y2='8'/><line x1='3' y1='12' x2='17' y2='12'/><line x1='3' y1='16' x2='19' y2='16'/><line x1='5' y1='20' x2='15' y2='20'/></svg>""",
}


def render_weather_switcher(current_palette: str) -> None:
    """Visual SVG strip + invisible click buttons sharing the same positions."""
    active = st.session_state.get("palette_override") or current_palette

    # Render the visible pill and icons as one HTML block
    icons_html = ""
    for w in WEATHERS:
        is_active = "wx-icon-active" if w == active else ""
        icons_html += (
            f"<div class='wx-icon {is_active}' data-weather='{w}'>"
            f"{SVG_ICONS[w]}"
            f"</div>"
        )

    st.markdown(
        f"<div class='wx-pill'>{icons_html}</div>",
        unsafe_allow_html=True,
    )

    # Invisible Streamlit buttons — CSS pins each one exactly over its SVG icon
    for w in WEATHERS:
        if st.button(" ", key=f"wx_{w}", help=w.capitalize()):
            st.session_state.palette_override = w
            st.rerun()