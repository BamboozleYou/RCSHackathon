"""Fortune cookie card renderer."""
import streamlit as st


def render_fortune(text: str) -> None:
    st.markdown(
        f"""
        <div class='fortune-cookie'>
          <span class='fortune-label'>a small thing for you</span>
          <p class='fortune-text'>{text}</p>
          <span class='fortune-mark'>&#8251;</span>
        </div>
        """,
        unsafe_allow_html=True,
    )