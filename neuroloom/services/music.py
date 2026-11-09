"""YouTube ID lookup (no API key) + embedded playable player."""
import re
import urllib.parse
import requests
import streamlit as st
import streamlit.components.v1 as components


@st.cache_data(ttl=3600, show_spinner=False)
def get_youtube_id(title: str, artist: str) -> str | None:
    """Scrape the first video ID from a YouTube search results page."""
    try:
        query = urllib.parse.quote(f"{title} {artist} official audio")
        url = f"https://www.youtube.com/results?search_query={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers, timeout=6).text
        match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
        return match.group(1) if match else None
    except Exception:
        return None


def render_player(title: str, artist: str) -> None:
    """Embed a full YouTube player inline — play, pause, scrub, fullscreen."""
    video_id = get_youtube_id(title, artist)
    if not video_id:
        st.caption("Player unavailable — try again in a moment.")
        return
    embed = f"""
    <div style="border-radius:14px; overflow:hidden;
                box-shadow:0 8px 28px rgba(0,0,0,0.22); margin-top:12px;">
      <iframe width="100%" height="180"
        src="https://www.youtube.com/embed/{video_id}?controls=1&modestbranding=1&rel=0&showinfo=0"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen>
      </iframe>
    </div>
    """
    components.html(embed, height=200)