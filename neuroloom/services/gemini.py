"""Gemini-powered cognitive state analysis + fortune cookie generation."""
import json
import random
import re
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)


# ---------- Cognitive state analysis ----------

ANALYZE_PROMPT = """You are a cognitive state analyst for a music therapy app called NeuroLoom.
Read this journal entry and place the person in a 2D mood space (Energy x Valence, each 0-1),
then decide where they should be guided to via a 5-song musical bridge.

Journal entry: \"\"\"{text}\"\"\"

Return ONLY a JSON object (no markdown fences, no prose) with this exact shape:
{{
  "detected_state": "<short 1-3 word emotional label — examples: 'overwhelmed', 'joyful', 'heavy-hearted', 'excited', 'creatively stuck', 'grateful', 'angry', 'peaceful', 'restless', 'wired but drained'>",
  "start_energy": <float 0.0-1.0>,
  "start_valence": <float 0.0-1.0>,
  "target_energy": <float 0.0-1.0>,
  "target_valence": <float 0.0-1.0>,
  "narrative": "<one warm sentence describing the journey, reflecting their actual emotion>"
}}

Axis definitions:
- Energy: 0 = still / low arousal, 1 = intense / high arousal
- Valence: 0 = very negative emotion, 1 = very positive emotion

Transition guide — match the person's ACTUAL emotion, don't force calm:
- Happy / joyful / excited (high V, med-high E): Amplify it. Target even higher E and V. Keep them in flow.
- Grateful / peaceful / content (mid E, high V): Gentle reinforcement. Small upward moves.
- Sad / heavy-hearted / grieving (low E, low V): Honor the weight first, then slowly walk toward lighter ground (mid E, mid-high V).
- Overwhelmed / anxious / panicked (high E, low V): Guide DOWN in energy, UP in valence. Meditative calm.
- Fatigued / drained / burnt out (low E, low-mid V): Gently lift UP in both. Flow state.
- Stuck / numb / bored / unmotivated (low E, low-mid V): Step UP in both. Momentum.
- Angry / frustrated (high E, low V): Let them feel it, then slowly descend E while raising V. Release.
- Lonely / isolated (low-mid E, low V): Warm, human-sounding path. Raise V steadily.
- Wired / restless / can't sit still (high E, mid V): Bring E down, hold V steady. Grounded focus.

If the person sounds happy and wants to stay there, DO NOT force them into calm. Keep their valence high and let energy ride with it.
"""


def _parse_json_loose(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return json.loads(text)


def _fallback_analysis(text: str) -> dict:
    """Keyword fallback — covers the full emotional spectrum."""
    t = text.lower()

    # Positive emotions first (common mistake is to miss these)
    if any(k in t for k in ["ecstatic", "thrilled", "amazing day", "best day", "on top of the world"]):
        return {"detected_state": "euphoric", "start_energy": 0.75, "start_valence": 0.85,
                "target_energy": 0.90, "target_valence": 0.96,
                "narrative": "You're riding high — let's keep the momentum going."}
    if any(k in t for k in ["happy", "good mood", "great", "wonderful", "fantastic", "cheerful", "bright"]):
        return {"detected_state": "happy", "start_energy": 0.60, "start_valence": 0.78,
                "target_energy": 0.82, "target_valence": 0.92,
                "narrative": "You're in a good place. Let's lift this even higher."}
    if any(k in t for k in ["excited", "pumped", "energized", "can't wait", "stoked"]):
        return {"detected_state": "excited", "start_energy": 0.78, "start_valence": 0.80,
                "target_energy": 0.90, "target_valence": 0.90,
                "narrative": "That energy is electric. Ride it."}
    if any(k in t for k in ["grateful", "thankful", "blessed", "appreciative"]):
        return {"detected_state": "grateful", "start_energy": 0.35, "start_valence": 0.78,
                "target_energy": 0.55, "target_valence": 0.88,
                "narrative": "Gratitude is a soft kind of strength. Let's let it bloom."}
    if any(k in t for k in ["peaceful", "calm", "content", "serene", "at ease"]):
        return {"detected_state": "peaceful", "start_energy": 0.25, "start_valence": 0.72,
                "target_energy": 0.45, "target_valence": 0.82,
                "narrative": "You're grounded. Let's gently add some light."}

    # Negative / heavy emotions
    if any(k in t for k in ["stressed", "overwhelmed", "anxious", "panic", "racing", "too much", "freaking out"]):
        return {"detected_state": "overwhelmed", "start_energy": 0.65, "start_valence": 0.25,
                "target_energy": 0.20, "target_valence": 0.62,
                "narrative": "Your system is overloaded. We'll bring you down into calm."}
    if any(k in t for k in ["angry", "pissed", "furious", "frustrated", "rage", "fed up"]):
        return {"detected_state": "angry", "start_energy": 0.78, "start_valence": 0.20,
                "target_energy": 0.40, "target_valence": 0.65,
                "narrative": "Let it burn through, then we'll walk you to steadier ground."}
    if any(k in t for k in ["sad", "lonely", "empty", "hurt", "heartbroken", "grief", "crying", "miss"]):
        return {"detected_state": "heavy-hearted", "start_energy": 0.20, "start_valence": 0.12,
                "target_energy": 0.55, "target_valence": 0.72,
                "narrative": "We'll honor the weight, then walk you toward lighter ground."}
    if any(k in t for k in ["tired", "exhausted", "drained", "sleepy", "burnt out", "burned out", "no energy"]):
        return {"detected_state": "fatigued", "start_energy": 0.15, "start_valence": 0.32,
                "target_energy": 0.70, "target_valence": 0.80,
                "narrative": "You're running on fumes. We'll gently lift you into flow."}
    if any(k in t for k in ["stuck", "bored", "meh", "unmotivated", "blocked", "flat", "numb", "nothing"]):
        return {"detected_state": "stuck", "start_energy": 0.25, "start_valence": 0.30,
                "target_energy": 0.80, "target_valence": 0.85,
                "narrative": "You're frozen. We'll step you up into momentum."}
    if any(k in t for k in ["restless", "can't sit still", "wired", "jittery", "antsy"]):
        return {"detected_state": "restless", "start_energy": 0.80, "start_valence": 0.50,
                "target_energy": 0.40, "target_valence": 0.70,
                "narrative": "Too much current. Let's ground the signal."}

    return {"detected_state": "reflective", "start_energy": 0.40, "start_valence": 0.50,
            "target_energy": 0.65, "target_valence": 0.78,
            "narrative": "Let's find a thread and follow it somewhere warmer."}


def analyze_with_gemini(text: str) -> dict:
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
Journal entry: \"\"\"{text}\"\"\"
Detected state: {state}

Rules:
- Exactly one sentence, 10-22 words
- Poetic, slightly mysterious, quietly hopeful — like a zen koan crossed with a fortune cookie
- Match the tone to their emotion — joyful entries get celebratory fortunes, sad entries get gentle ones
- No cliches, no emojis, no quotes around the output, no preamble
- Return ONLY the sentence itself

Examples:
- The quietest room in your mind is the one you haven't entered yet.
- What feels like fog is often just the shape of something becoming.
- Your joy today is a small rebellion. Let it be loud.
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
    "Your joy today is a small rebellion. Let it be loud.",
]


def generate_fortune(text: str, state: str) -> str:
    try:
        model = genai.GenerativeModel(GEMINI_MODEL, generation_config={"temperature": 0.95})
        resp = model.generate_content(FORTUNE_PROMPT.format(text=text[:500], state=state))
        fortune = resp.text.strip().strip('"').strip("'")
        return fortune if 5 < len(fortune) < 250 else random.choice(FALLBACK_FORTUNES)
    except Exception:
        return random.choice(FALLBACK_FORTUNES)