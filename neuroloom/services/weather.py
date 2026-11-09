"""OpenWeatherMap fetch + condition-to-palette mapping."""
import requests
import streamlit as st


@st.cache_data(ttl=600, show_spinner=False)
def fetch_weather(city: str, key: str) -> dict:
    """Fetch weather, with a graceful offline fallback so demos never break."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            d = r.json()
            return {
                "condition": d["weather"][0]["main"],
                "description": d["weather"][0]["description"],
                "temp": d["main"]["temp"],
                "city": d["name"],
            }
    except Exception:
        pass
    return {
        "condition": "Clouds",
        "description": "overcast (offline fallback)",
        "temp": 24,
        "city": city,
    }


def palette_for(condition: str) -> str:
    """Map weather condition to a palette key defined in styles.PALETTES."""
    c = condition.lower()
    if c == "clear":
        return "clear"
    if c == "clouds":
        return "clouds"
    if c in ("rain", "drizzle"):
        return "rain"
    if c == "thunderstorm":
        return "thunderstorm"
    if c == "snow":
        return "snow"
    # mist, haze, fog, smoke, dust, etc.
    return "mist"


def mood_label(condition: str) -> str:
    """Short prose descriptor, used in the weather pill."""
    c = condition.lower()
    if c == "clear":
        return "bright — flow-oriented"
    if c == "clouds":
        return "gentle — contemplative"
    if c in ("rain", "drizzle"):
        return "introspective — meditative"
    if c == "thunderstorm":
        return "charged — electric"
    if c == "snow":
        return "crystalline — still"
    return "soft — hazy"