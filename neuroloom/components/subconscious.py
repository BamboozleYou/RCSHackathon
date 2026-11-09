"""Subconscious State — full-screen mouse-reactive particle field."""
import streamlit.components.v1 as components


SUBCONSCIOUS_HTML = """
<div id='subconscious-overlay' style='
    position: fixed; inset: 0;
    background: radial-gradient(ellipse at center, #0a0520 0%, #000000 85%);
    z-index: 10000;
    cursor: crosshair;
    overflow: hidden;
'>
  <canvas id='particles' style='position: absolute; inset: 0; width: 100%; height: 100%;'></canvas>
  <div style='
      position: absolute; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      text-align: center; pointer-events: none;
      font-family: "Instrument Serif", serif;
      color: rgba(255, 255, 255, 0.35);
      animation: fadeInGhost 3s ease;
  '>
    <p style='font-size: 2.8rem; font-weight: 400; font-style: italic; margin: 0; letter-spacing: -0.02em;'>
      the subconscious state
    </p>
    <p style='font-family: "JetBrains Mono", monospace;
              font-size: 0.68rem; letter-spacing: 0.3em;
              text-transform: uppercase; opacity: 0.6;
              margin-top: 14px;'>
      move · breathe
    </p>
  </div>
</div>
<style>
@keyframes fadeInGhost { from { opacity: 0; } to { opacity: 1; } }
</style>
<script>
(function() {
    const canvas = document.getElementById('particles');
    const ctx = canvas.getContext('2d');
    const overlay = document.getElementById('subconscious-overlay');
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const N = 140;
    const particles = [];
    const colors = ['#ff6b9d', '#feca57', '#48dbfb', '#a29bfe', '#ff9ff3', '#ffffff'];
    for (let i = 0; i < N; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            r: Math.random() * 2.5 + 0.8,
            c: colors[Math.floor(Math.random() * colors.length)],
            baseA: Math.random() * 0.5 + 0.3,
        });
    }

    const mouse = { x: -9999, y: -9999, active: false };
    overlay.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; mouse.active = true; });
    overlay.addEventListener('mouseleave', () => { mouse.active = false; });

    function tick() {
        ctx.fillStyle = 'rgba(10, 5, 32, 0.12)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < N; i++) {
            const p = particles[i];
            if (mouse.active) {
                const dx = mouse.x - p.x;
                const dy = mouse.y - p.y;
                const d2 = dx * dx + dy * dy;
                if (d2 < 30000) {
                    const f = (1 - d2 / 30000) * 0.08;
                    p.vx += (dx / Math.sqrt(d2 + 1)) * f;
                    p.vy += (dy / Math.sqrt(d2 + 1)) * f;
                }
            }
            p.vx *= 0.985;
            p.vy *= 0.985;
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width) p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.c;
            ctx.globalAlpha = p.baseA;
            ctx.fill();

            for (let j = i + 1; j < N; j++) {
                const q = particles[j];
                const dx = p.x - q.x;
                const dy = p.y - q.y;
                const d2 = dx * dx + dy * dy;
                if (d2 < 10000) {
                    ctx.strokeStyle = p.c;
                    ctx.globalAlpha = (1 - d2 / 10000) * 0.15;
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(q.x, q.y);
                    ctx.stroke();
                }
            }
        }
        ctx.globalAlpha = 1;
        requestAnimationFrame(tick);
    }
    tick();
})();
</script>
"""


def render_subconscious():
    components.html(SUBCONSCIOUS_HTML, height=800, scrolling=False)