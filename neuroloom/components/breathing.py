"""Animated breathing orb — click to begin a 4-4-4-4 box-breathing cycle."""
import streamlit.components.v1 as components


BREATHE_HTML = """
<div style="display:flex; justify-content:center; padding: 20px 0;">
  <div style="text-align:center;">
    <div id="breathe-orb" style="
        width: 200px; height: 200px; border-radius: 50%;
        background: radial-gradient(circle at 35% 35%,
            rgba(255,255,255,0.45), rgba(182,176,220,0.2) 60%, rgba(182,176,220,0.05));
        border: 1.5px solid rgba(255,255,255,0.3);
        margin: 0 auto;
        transform: scale(0.65);
        transition: transform 4s cubic-bezier(0.4, 0, 0.6, 1);
        cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        color: rgba(255,255,255,0.85);
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 300; font-size: 0.95rem; letter-spacing: 0.18em;
        text-transform: uppercase;
        backdrop-filter: blur(18px);
        box-shadow: 0 0 60px rgba(182,176,220,0.25);
    ">tap to begin</div>
    <p id="breathe-phase" style="
        margin-top: 26px; color: rgba(255,255,255,0.55);
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.72rem; letter-spacing: 0.24em; text-transform: uppercase;
        font-weight: 400;
    ">box breathing &middot; 4 &middot; 4 &middot; 4 &middot; 4</p>
  </div>
</div>
<script>
(function() {
    const orb = document.getElementById('breathe-orb');
    const phase = document.getElementById('breathe-phase');
    let running = false;
    function run() {
        phase.textContent = 'breathe in';
        orb.textContent = '';
        orb.style.transition = 'transform 4s cubic-bezier(0.4, 0, 0.6, 1)';
        orb.style.transform = 'scale(1.15)';
        setTimeout(() => { phase.textContent = 'hold'; }, 4000);
        setTimeout(() => {
            phase.textContent = 'breathe out';
            orb.style.transform = 'scale(0.65)';
        }, 8000);
        setTimeout(() => { phase.textContent = 'hold'; }, 12000);
        setTimeout(() => { if (running) run(); }, 16000);
    }
    orb.addEventListener('click', () => {
        if (!running) { running = true; run(); }
    });
})();
</script>
"""


def render_breathing_orb() -> None:
    components.html(BREATHE_HTML, height=340)