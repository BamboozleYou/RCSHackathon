"""Gemini-powered cognitive state analysis + fortune cookie generation."""
import json
import random
import re
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)


# ---------- Cognitive state analysis ----------

ANALYZE_PROMPT = """You are a cognitive state analyst for a music therapy app.
Read this journal entry and place the person in a 2D mood space (Energy x Valence, each 0-1),
then decide where they need to be guided to via a 5-song musical bridge.

Journal entry: \"\"\"{text}\"\"\"

Return ONLY a JSON object (no markdown fences, no prose) with this exact shape:
{{
  "detected_state": "<short 1-3 word label, e.g. 'overwhelmed', 'creatively stuck', 'wired but drained'>",
  "start_energy": <float 0.0-1.0>,
  "start_valence": <float 0.0-1.0>,
  "target_energy": <float 0.0-1.0>,
  "target_valence": <float 0.0-1.0>,
  "narrative": "<one warm sentence describing the journey from start to target>"
}}

Axis guide:
- Energy: 0 = still / low arousal, 1 = intense / high arousal
- Valence: 0 = negative mood, 1 = positive mood

Transition heuristics:
- Overwhelmed / anxious (high energy, low valence) -> guide DOWN in energy, UP in valence (meditative calm)
- Fatigued / drained (low energy, low-mid valence) -> guide UP in energy, UP in valence (flow)
- Stuck / numb / bored (low energy, low valence) -> guide UP in both (momentum)
- Already positive -> gentle reinforcement, small moves
"""


def _parse_json_loose(text: str) -> dict:
    """Strip markdown fences and extract first JSON object."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return json.loads(text)


def _fallback_analysis(text: str) -> dict:
    """Keyword fallback so the demo never breaks if the API hiccups."""
    t = text.lower()
    if any(k in t for k in ["stressed", "overwhelmed", "anxious", "panic", "racing", "too much"]):
        return {
            "detected_state": "overwhelmed",
            "start_energy": 0.60, "start_valence": 0.25,
            "target_energy": 0.15, "target_valence": 0.60,
            "narrative": "Your system is overloaded. We'll bring you down into calm.",
        }
    if any(k in t for k in ["tired", "exhausted", "drained", "sleepy", "burnt out", "burned out"]):
        return {
            "detected_state": "fatigued",
            "start_energy": 0.15, "start_valence": 0.30,
            "target_energy": 0.70, "target_valence": 0.80,
            "narrative": "You're running on fumes. We'll gently lift you into flow.",
        }
    if any(k in t for k in ["stuck", "bored", "meh", "unmotivated", "blocked", "flat", "numb"]):
        return {
            "detected_state": "stuck",
            "start_energy": 0.25, "start_valence": 0.30,
            "target_energy": 0.80, "target_valence": 0.85,
            "narrative": "You're frozen. We'll step you up into momentum.",
        }
    if any(k in t for k in ["sad", "lonely", "empty", "hurt", "heartbroken", "grief"]):
        return {
            "detected_state": "heavy-hearted",
            "start_energy": 0.20, "start_valence": 0.12,
            "target_energy": 0.55, "target_valence": 0.70,
            "narrative": "We'll honor the weight, then gently walk you toward lighter ground.",
        }
    return {
        "detected_state": "neutral",
        "start_energy": 0.40, "start_valence": 0.50,
        "target_energy": 0.70, "target_valence": 0.80,
        "narrative": "Balanced start. We'll guide you toward focused flow.",
    }


def analyze_with_gemini(text: str) -> dict:
    """Gemini-first analysis, falls back to keyword matching on any failure."""
    try:
        model = genai.GenerativeModel(
            GEMINI_MODEL,
            generation_config={"response_mime_type": "application/json", "temperature": 0.4},
        )
        resp = model.generate_content(ANALYZE_PROMPT.format(text=text))
        data = _parse_json_loose(resp.text)
        for k in ("start_energy", "start_valence", "target_energy", "target_valence"):
            data[k] = float(max(0.0, min(1.0, data[k])))
        data["source"] = "gemini"
        return data
    except Exception as e:
        fb = _fallback_analysis(text)
        fb["source"] = f"fallback ({type(e).__name__})"
        return fb


# ---------- Fortune cookie ----------

FORTUNE_PROMPT = """Generate ONE fortune cookie message for someone using a music-based cognitive state app.
The journal entry they wrote was: \"\"\"{text}\"\"\"
Their detected state: {state}

Rules:
- Exactly one sentence, 10-22 words
- Poetic, slightly mysterious, quietly hopeful — like a zen koan crossed with a fortune cookie
- No cliches ("every cloud has a silver lining", "this too shall pass")
- No emojis, no quotes around the output, no preamble
- Address the reader in second person when natural
- Return ONLY the sentence itself

Examples of tone:
- The quietest room in your mind is the one you haven't entered yet.
- What feels like fog is often just the shape of something becoming.
- You were not behind. You were gathering.
"""

FALLBACK_FORTUNES = [
    "The quietest room in your mind is the one you haven't entered yet.",
    "What feels like fog is often just the shape of something becoming.",
    "You were not behind. You were gathering.",
    "The tide does not apologize for returning. Neither should you.",
    "Stillness is not the absence of motion; it is motion remembering itself.",
    "The river does not rush to reach the sea, yet it always arrives.",
    "Some doors only open when you stop trying to find the handle.",
]


def generate_fortune(text: str, state: str) -> str:
    """Return a single-sentence fortune, with safe fallbacks."""
    try:
        model = genai.GenerativeModel(
            GEMINI_MODEL, generation_config={"temperature": 0.95}
        )
        resp = model.generate_content(FORTUNE_PROMPT.format(text=text[:500], state=state))
        fortune = resp.text.strip().strip('"').strip("'")
        return fortune if 5 < len(fortune) < 250 else random.choice(FALLBACK_FORTUNES)
    except Exception:
        return random.choice(FALLBACK_FORTUNES)