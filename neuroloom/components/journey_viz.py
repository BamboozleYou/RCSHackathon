"""Tiny SVG visualization of the start→target journey in (Energy, Valence) space."""


def render_journey_viz(start_e: float, start_v: float, target_e: float, target_v: float) -> str:
    def sx(e): return 20 + e * 140
    def sy(v): return 160 - v * 140

    sx1, sy1 = sx(start_e), sy(start_v)
    sx2, sy2 = sx(target_e), sy(target_v)
    mid_x = (sx1 + sx2) / 2
    mid_y = min(sy1, sy2) - 12

    return (
        "<div class='journey-viz'>"
        "<span class='axis-label lbl-v'>Valence</span>"
        "<span class='axis-label lbl-e'>Energy</span>"
        "<svg viewBox='0 0 180 180'>"
        "<line x1='20' y1='160' x2='160' y2='160' stroke='currentColor' stroke-width='0.5' opacity='0.3'/>"
        "<line x1='20' y1='20' x2='20' y2='160' stroke='currentColor' stroke-width='0.5' opacity='0.3'/>"
        "<line x1='90' y1='20' x2='90' y2='160' stroke='currentColor' stroke-width='0.3' opacity='0.15' stroke-dasharray='2 3'/>"
        "<line x1='20' y1='90' x2='160' y2='90' stroke='currentColor' stroke-width='0.3' opacity='0.15' stroke-dasharray='2 3'/>"
        f"<path d='M {sx1} {sy1} Q {mid_x} {mid_y} {sx2} {sy2}' fill='none' stroke='var(--accent)' stroke-width='1.5' opacity='0.5' stroke-dasharray='3 3'>"
        "<animate attributeName='stroke-dashoffset' from='30' to='0' dur='1.2s' repeatCount='indefinite'/>"
        "</path>"
        f"<circle cx='{sx1}' cy='{sy1}' r='5' fill='currentColor' opacity='0.55'/>"
        f"<circle cx='{sx1}' cy='{sy1}' r='9' fill='none' stroke='currentColor' stroke-width='0.5' opacity='0.3'/>"
        f"<circle cx='{sx2}' cy='{sy2}' r='6' fill='var(--accent)'/>"
        f"<circle cx='{sx2}' cy='{sy2}' r='11' fill='none' stroke='var(--accent)' stroke-width='1' opacity='0.5'>"
        "<animate attributeName='r' from='7' to='14' dur='1.8s' repeatCount='indefinite'/>"
        "<animate attributeName='opacity' from='0.7' to='0' dur='1.8s' repeatCount='indefinite'/>"
        "</circle>"
        "</svg>"
        "</div>"
    )