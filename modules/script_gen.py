# from google import genai
# from google.genai import types
# import os
# import json
# from config import NICHE, TARGET_AUDIENCE, VIDEO_DURATION_SECONDS

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# SCRIPT_PROMPT = """You are a viral YouTube Shorts script writer specializing in {niche}.

# Write a {duration}-second script for a YouTube Short about: "{topic}"

# Target audience: {audience}

# STRICT FORMAT — respond with valid JSON only, no extra text, no markdown:
# {{
#   "title": "Short catchy title (max 60 chars)",
#   "hook": "Opening line (0-3 sec) — must be shocking, surprising, or question-based",
#   "body": [
#     "Fact/point 1 (1 sentence, punchy)",
#     "Fact/point 2 (1 sentence, punchy)",
#     "Fact/point 3 (1 sentence, punchy)"
#   ],
#   "cta": "Call to action (follow for more facts like this!)",
#   "hashtags": ["#facts", "#didyouknow", "#shorts"],
#   "full_script": "Complete narration text for TTS"
# }}

# Rules:
# - Hook MUST start with a surprising statement or question
# - Each fact must be genuinely surprising
# - Keep total word count under 120 words
# - Use simple, conversational language
# - End with a strong CTA to follow/like
# - Return ONLY the JSON object, nothing else
# """

# def generate_script(topic):
#     """Generate a viral script using Gemini API (free)."""

#     prompt = SCRIPT_PROMPT.format(
#         niche=NICHE,
#         duration=VIDEO_DURATION_SECONDS,
#         topic=topic,
#         audience=TARGET_AUDIENCE
#     )

#     response = client.models.generate_content(
#        model="gemini-2.0-flash-lite",
#         contents=prompt,
#         config=types.GenerateContentConfig(
#             temperature=0.9,
#             max_output_tokens=1000,
#         )
#     )

#     raw = response.text.strip()

#     # Clean up JSON if model adds markdown
#     if raw.startswith("```"):
#         raw = raw.split("```")[1]
#         if raw.startswith("json"):
#             raw = raw[4:]
#     raw = raw.strip()

#     script = json.loads(raw)
#     print(f"[Script] Generated: {script['title']}")
#     return script

# if __name__ == "__main__":
#     script = generate_script("surprising facts about the human brain")
#     print(json.dumps(script, indent=2))






from google import genai
from google.genai import types
import os
import json
import time
from config import NICHE, TARGET_AUDIENCE, VIDEO_DURATION_SECONDS

SCRIPT_PROMPT = """You are a viral YouTube Shorts script writer for Hindi audience.

Write a {duration}-second script in HINDI language for: "{topic}"

Target audience: {audience}

STRICT FORMAT — valid JSON only, no extra text:
{{
  "title": "Catchy Hindi title (max 60 chars)",
  "hook": "Opening line in HINDI — shocking or question-based",
  "body": [
    "Fact 1 in HINDI (1 sentence)",
    "Fact 2 in HINDI (1 sentence)", 
    "Fact 3 in HINDI (1 sentence)"
  ],
  "cta": "CTA in HINDI",
  "hashtags": ["#facts", "#rochaktathy", "#shorts"],
  "full_script": "Complete HINDI narration for TTS"
}}

Rules:
- EVERYTHING must be in Hindi (Devanagari script)
- Hook must be shocking or question-based
- Simple conversational Hindi
- Under 120 words total
- Return ONLY JSON
"""

FALLBACK_SCRIPTS = [

    # ── Science & Human Body ──────────────────────────
    {
        "title": "आपका दिल एक दिन में कितना काम करता है?",
        "hook": "क्या आप जानते हैं कि आपका दिल एक दिन में 100,000 बार धड़कता है?",
        "body": [
            "आपका दिल इतनी ताकत से खून पंप करता है कि वो खून 30 फीट ऊपर उछाल सकता है।",
            "एक इंसान की आँखें 576 मेगापिक्सल की होती हैं — किसी भी कैमरे से बेहतर।",
            "आपका दिमाग जागते वक्त इतनी बिजली बनाता है जो एक LED बल्ब जला सके।"
        ],
        "cta": "ऐसे चौंकाने वाले तथ्यों के लिए FactO को फॉलो करें!",
        "hashtags": ["#science", "#facts", "#shorts", "#FactO", "#rochaktathy"],
        "full_script": "क्या आप जानते हैं कि आपका दिल एक दिन में 100,000 बार धड़कता है? आपका दिल इतनी ताकत से खून पंप करता है कि वो खून 30 फीट ऊपर उछाल सकता है। एक इंसान की आँखें 576 मेगापिक्सल की होती हैं — किसी भी कैमरे से बेहतर। आपका दिमाग जागते वक्त इतनी बिजली बनाता है जो एक LED बल्ब जला सके। ऐसे चौंकाने वाले तथ्यों के लिए FactO को फॉलो करें!"
    },
    {
        "title": "आपकी हड्डियाँ स्टील से भी मजबूत हैं!",
        "hook": "क्या आप जानते हैं कि इंसान की हड्डी स्टील से 4 गुना मजबूत होती है?",
        "body": [
            "आपके शरीर में इतना कार्बन है जिससे 9000 पेंसिल बन सकती हैं।",
            "इंसान का पेट हर 3 से 4 दिन में अपनी परत खुद बदल लेता है।",
            "आपकी जीभ के निशान उँगलियों के निशान जितने unique होते हैं।"
        ],
        "cta": "हर रोज नया तथ्य जानने के लिए FactO फॉलो करें!",
        "hashtags": ["#body", "#facts", "#shorts", "#FactO", "#science"],
        "full_script": "क्या आप जानते हैं कि इंसान की हड्डी स्टील से 4 गुना मजबूत होती है? आपके शरीर में इतना कार्बन है जिससे 9000 पेंसिल बन सकती हैं। इंसान का पेट हर 3 से 4 दिन में अपनी परत खुद बदल लेता है। आपकी जीभ के निशान उँगलियों के निशान जितने unique होते हैं। हर रोज नया तथ्य जानने के लिए FactO फॉलो करें!"
    },
    {
        "title": "नींद में आपका दिमाग क्या करता है?",
        "hook": "नींद में आपका दिमाग यादें delete करता है — और ये सच है!",
        "body": [
            "सोते वक्त दिमाग जहरीले waste products साफ करता है जो दिन भर जमा होते हैं।",
            "इंसान अपनी जिंदगी का एक तिहाई हिस्सा सोने में बिता देता है।",
            "सपने देखना दिमाग की memory processing का हिस्सा है।"
        ],
        "cta": "ऐसे दिमाग हिला देने वाले तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#brain", "#facts", "#shorts", "#FactO", "#science"],
        "full_script": "नींद में आपका दिमाग यादें delete करता है — और ये सच है! सोते वक्त दिमाग जहरीले waste products साफ करता है जो दिन भर जमा होते हैं। इंसान अपनी जिंदगी का एक तिहाई हिस्सा सोने में बिता देता है। सपने देखना दिमाग की memory processing का हिस्सा है। ऐसे दिमाग हिला देने वाले तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "इंसान का DNA कितना अजीब है?",
        "hook": "आप केले से 50% DNA share करते हैं — यकीन नहीं होता ना?",
        "body": [
            "हर इंसान का DNA 99.9% एक जैसा होता है — बस 0.1% में फर्क है।",
            "अगर आपके एक cell का DNA खोल दें तो वो 6 फीट लंबा होगा।",
            "पूरे इंसानी DNA को print करें तो 200 किताबें भर जाएंगी।"
        ],
        "cta": "ऐसे amazing तथ्यों के लिए FactO को like और follow करें!",
        "hashtags": ["#dna", "#science", "#shorts", "#FactO", "#facts"],
        "full_script": "आप केले से 50% DNA share करते हैं — यकीन नहीं होता ना? हर इंसान का DNA 99.9% एक जैसा होता है — बस 0.1% में फर्क है। अगर आपके एक cell का DNA खोल दें तो वो 6 फीट लंबा होगा। पूरे इंसानी DNA को print करें तो 200 किताबें भर जाएंगी। ऐसे amazing तथ्यों के लिए FactO को like और follow करें!"
    },
    {
        "title": "आपकी आँतें दूसरा दिमाग हैं!",
        "hook": "क्या आप जानते हैं कि आपके पेट में 500 मिलियन neurons हैं?",
        "body": [
            "आपकी आँतें इतनी smart हैं कि वो दिमाग के बिना भी काम कर सकती हैं।",
            "आपके शरीर में bacteria की संख्या cells से ज्यादा है।",
            "आँतों में 70% immune system रहता है — असली रक्षक यहीं है।"
        ],
        "cta": "रोज कुछ नया जानने के लिए FactO फॉलो करें!",
        "hashtags": ["#health", "#science", "#shorts", "#FactO", "#facts"],
        "full_script": "क्या आप जानते हैं कि आपके पेट में 500 मिलियन neurons हैं? आपकी आँतें इतनी smart हैं कि वो दिमाग के बिना भी काम कर सकती हैं। आपके शरीर में bacteria की संख्या cells से ज्यादा है। आँतों में 70% immune system रहता है — असली रक्षक यहीं है। रोज कुछ नया जानने के लिए FactO फॉलो करें!"
    },

    # ── Space & Universe ──────────────────────────────
    {
        "title": "ब्रह्मांड में हीरे का पूरा ग्रह है!",
        "hook": "अंतरिक्ष में एक ऐसा ग्रह है जो पूरी तरह हीरे से बना है!",
        "body": [
            "55 Cancri e नाम का ये ग्रह पृथ्वी से दोगुना बड़ा है और हीरे से ढका है।",
            "बृहस्पति ग्रह पर 400 साल से एक तूफान चल रहा है जो पृथ्वी से बड़ा है।",
            "अंतरिक्ष में एक alcohol का बादल है जो 400 trillion trillion पिंट से भरा है।"
        ],
        "cta": "अंतरिक्ष के रहस्य जानने के लिए FactO फॉलो करें!",
        "hashtags": ["#space", "#universe", "#shorts", "#FactO", "#facts"],
        "full_script": "अंतरिक्ष में एक ऐसा ग्रह है जो पूरी तरह हीरे से बना है! 55 Cancri e नाम का ये ग्रह पृथ्वी से दोगुना बड़ा है और हीरे से ढका है। बृहस्पति ग्रह पर 400 साल से एक तूफान चल रहा है जो पृथ्वी से बड़ा है। अंतरिक्ष में एक alcohol का बादल है जो 400 trillion trillion पिंट से भरा है। अंतरिक्ष के रहस्य जानने के लिए FactO फॉलो करें!"
    },
    {
        "title": "Black Hole की आवाज़ सुनी गई है!",
        "hook": "NASA ने Black Hole की आवाज़ record की है — और वो सुनकर रोंगटे खड़े हो जाते हैं!",
        "body": [
            "Perseus galaxy cluster के black hole की आवाज़ इंसानी सुनने से 57 octaves नीची है।",
            "Black hole इतना घना है कि उसमें से रोशनी भी नहीं निकल सकती।",
            "अगर सूरज black hole बन जाए तो वो एक मटर के दाने जितना छोटा होगा।"
        ],
        "cta": "ऐसे रोमांचक तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#blackhole", "#space", "#shorts", "#FactO", "#nasa"],
        "full_script": "NASA ने Black Hole की आवाज़ record की है — और वो सुनकर रोंगटे खड़े हो जाते हैं! Perseus galaxy cluster के black hole की आवाज़ इंसानी सुनने से 57 octaves नीची है। Black hole इतना घना है कि उसमें से रोशनी भी नहीं निकल सकती। अगर सूरज black hole बन जाए तो वो एक मटर के दाने जितना छोटा होगा। ऐसे रोमांचक तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "मंगल पर एक दिन कितना लंबा होता है?",
        "hook": "मंगल ग्रह पर एक साल में 687 दिन होते हैं — आपकी उम्र वहाँ आधी होती!",
        "body": [
            "मंगल पर gravity इतनी कम है कि आप वहाँ 3 गुना ऊँचा कूद सकते हैं।",
            "मंगल का सबसे बड़ा पहाड़ Mount Everest से 3 गुना ऊँचा है।",
            "मंगल पर सूर्यास्त नीले रंग का होता है — बिल्कुल उल्टा पृथ्वी से।"
        ],
        "cta": "अंतरिक्ष के amazing तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#mars", "#space", "#shorts", "#FactO", "#facts"],
        "full_script": "मंगल ग्रह पर एक साल में 687 दिन होते हैं — आपकी उम्र वहाँ आधी होती! मंगल पर gravity इतनी कम है कि आप वहाँ 3 गुना ऊँचा कूद सकते हैं। मंगल का सबसे बड़ा पहाड़ Mount Everest से 3 गुना ऊँचा है। मंगल पर सूर्यास्त नीले रंग का होता है — बिल्कुल उल्टा पृथ्वी से। अंतरिक्ष के amazing तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "चाँद पर पैरों के निशान 10 करोड़ साल रहेंगे!",
        "hook": "चाँद पर Neil Armstrong के पैरों के निशान आज भी वैसे ही हैं!",
        "body": [
            "चाँद पर हवा नहीं है इसलिए वो निशान 10 करोड़ साल तक नहीं मिटेंगे।",
            "चाँद हर साल पृथ्वी से 3.8 सेंटीमीटर दूर होता जा रहा है।",
            "चाँद की gravity की वजह से समुद्र में ज्वार-भाटा आता है।"
        ],
        "cta": "चाँद और अंतरिक्ष के रहस्य जानने के लिए FactO फॉलो करें!",
        "hashtags": ["#moon", "#space", "#shorts", "#FactO", "#facts"],
        "full_script": "चाँद पर Neil Armstrong के पैरों के निशान आज भी वैसे ही हैं! चाँद पर हवा नहीं है इसलिए वो निशान 10 करोड़ साल तक नहीं मिटेंगे। चाँद हर साल पृथ्वी से 3.8 सेंटीमीटर दूर होता जा रहा है। चाँद की gravity की वजह से समुद्र में ज्वार-भाटा आता है। चाँद और अंतरिक्ष के रहस्य जानने के लिए FactO फॉलो करें!"
    },
    {
        "title": "सूरज की रोशनी 8 मिनट पुरानी है!",
        "hook": "अभी आप जो सूरज देख रहे हैं वो 8 मिनट पहले का सूरज है!",
        "body": [
            "सूरज की रोशनी पृथ्वी तक पहुँचने में 8 मिनट 20 सेकंड लगते हैं।",
            "सूरज के अंदर से निकलने में एक photon को 1 लाख साल लगते हैं।",
            "सूरज इतना बड़ा है कि उसमें 13 लाख पृथ्वियाँ समा सकती हैं।"
        ],
        "cta": "ऐसे mind-blowing तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#sun", "#space", "#shorts", "#FactO", "#facts"],
        "full_script": "अभी आप जो सूरज देख रहे हैं वो 8 मिनट पहले का सूरज है! सूरज की रोशनी पृथ्वी तक पहुँचने में 8 मिनट 20 सेकंड लगते हैं। सूरज के अंदर से निकलने में एक photon को 1 लाख साल लगते हैं। सूरज इतना बड़ा है कि उसमें 13 लाख पृथ्वियाँ समा सकती हैं। ऐसे mind-blowing तथ्यों के लिए FactO फॉलो करें!"
    },

    # ── History & Civilization ────────────────────────
    {
        "title": "Cleopatra iPhone से ज्यादा पुरानी नहीं थी!",
        "hook": "Cleopatra iPhone के आविष्कार से ज्यादा पुरानी नहीं थी — यकीन नहीं होता ना?",
        "body": [
            "Cleopatra का जमाना 69 BC था और iPhone 2007 में आया — फर्क सिर्फ 2076 साल।",
            "लेकिन Pyramids 2560 BC में बने — Cleopatra से 2500 साल पहले।",
            "Oxford University Aztec Empire बनने से पहले से exist करती है।"
        ],
        "cta": "इतिहास के चौंकाने वाले तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#history", "#facts", "#shorts", "#FactO", "#cleopatra"],
        "full_script": "Cleopatra iPhone के आविष्कार से ज्यादा पुरानी नहीं थी — यकीन नहीं होता ना? Cleopatra का जमाना 69 BC था और iPhone 2007 में आया — फर्क सिर्फ 2076 साल। लेकिन Pyramids 2560 BC में बने — Cleopatra से 2500 साल पहले। Oxford University Aztec Empire बनने से पहले से exist करती है। इतिहास के चौंकाने वाले तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "Pyramids slaves ने नहीं बनाए थे!",
        "hook": "Pyramids slaves ने नहीं बनाए — ये skilled workers थे जिन्हें तनख्वाह मिलती थी!",
        "body": [
            "Archaeological evidence से पता चला कि workers को अच्छा खाना और medical care मिलती थी।",
            "Great Pyramid बनाने में 20,000 workers ने 20 साल लगाए।",
            "Workers की हड्डियों में fractures के signs मिले जो healed थे — मतलब उनका इलाज होता था।"
        ],
        "cta": "इतिहास के सच जानने के लिए FactO फॉलो करें!",
        "hashtags": ["#egypt", "#history", "#shorts", "#FactO", "#facts"],
        "full_script": "Pyramids slaves ने नहीं बनाए — ये skilled workers थे जिन्हें तनख्वाह मिलती थी! Archaeological evidence से पता चला कि workers को अच्छा खाना और medical care मिलती थी। Great Pyramid बनाने में 20,000 workers ने 20 साल लगाए। Workers की हड्डियों में fractures के signs मिले जो healed थे — मतलब उनका इलाज होता था। इतिहास के सच जानने के लिए FactO फॉलो करें!"
    },
    {
        "title": "Vikings ने Columbus से पहले America खोजा!",
        "hook": "Columbus से 500 साल पहले Vikings America पहुँच गए थे!",
        "body": [
            "Leif Eriksson नाम के Viking ने 1000 AD में North America की धरती पर कदम रखा।",
            "Canada में L'Anse aux Meadows में Viking settlement के सबूत मिले हैं।",
            "Vikings के पास इतने advanced ships थे जो किसी भी दिशा में sail कर सकते थे।"
        ],
        "cta": "इतिहास के hidden तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#vikings", "#history", "#shorts", "#FactO", "#facts"],
        "full_script": "Columbus से 500 साल पहले Vikings America पहुँच गए थे! Leif Eriksson नाम के Viking ने 1000 AD में North America की धरती पर कदम रखा। Canada में L'Anse aux Meadows में Viking settlement के सबूत मिले हैं। Vikings के पास इतने advanced ships थे जो किसी भी दिशा में sail कर सकते थे। इतिहास के hidden तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "WW2 को खत्म हुए सिर्फ 80 साल हुए हैं!",
        "hook": "World War 2 इतिहास में नहीं — हमारे दादा-नाना के जमाने की बात है!",
        "body": [
            "WW2 में 7 करोड़ से ज्यादा लोग मारे गए — इतिहास का सबसे बड़ा नुकसान।",
            "WW2 में इस्तेमाल हुए कुछ bombs आज भी यूरोप की जमीन में दबे हैं।",
            "WW2 के बाद दुनिया इतनी बदली कि आज का नक्शा पूरी तरह अलग है।"
        ],
        "cta": "इतिहास जानने के लिए FactO को फॉलो और share करें!",
        "hashtags": ["#ww2", "#history", "#shorts", "#FactO", "#facts"],
        "full_script": "World War 2 इतिहास में नहीं — हमारे दादा-नाना के जमाने की बात है! WW2 में 7 करोड़ से ज्यादा लोग मारे गए — इतिहास का सबसे बड़ा नुकसान। WW2 में इस्तेमाल हुए कुछ bombs आज भी यूरोप की जमीन में दबे हैं। WW2 के बाद दुनिया इतनी बदली कि आज का नक्शा पूरी तरह अलग है। इतिहास जानने के लिए FactO को फॉलो और share करें!"
    },
    {
        "title": "निंजा असली होते थे — और बेहद खतरनाक!",
        "hook": "Ninja सिर्फ movies में नहीं — ये Japan के असली secret agents थे!",
        "body": [
            "Ninja को shinobi कहा जाता था और वो espionage और assassination के experts थे।",
            "Ninja के weapons इतने unique थे कि उनमें से कुछ आज भी museums में हैं।",
            "Japan में एक आखिरी certified Ninja आज भी जिंदा हैं — Jinichi Kawakami।"
        ],
        "cta": "इतिहास के रोचक रहस्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#ninja", "#history", "#shorts", "#FactO", "#japan"],
        "full_script": "Ninja सिर्फ movies में नहीं — ये Japan के असली secret agents थे! Ninja को shinobi कहा जाता था और वो espionage और assassination के experts थे। Ninja के weapons इतने unique थे कि उनमें से कुछ आज भी museums में हैं। Japan में एक आखिरी certified Ninja आज भी जिंदा हैं — Jinichi Kawakami। इतिहास के रोचक रहस्यों के लिए FactO फॉलो करें!"
    },

    # ── Animals & Nature ──────────────────────────────
    {
        "title": "Octopus के 3 दिल होते हैं!",
        "hook": "Octopus के 3 दिल होते हैं — और नीला खून बहता है उनमें!",
        "body": [
            "Octopus के 2 दिल gills को blood pump करते हैं और एक पूरे body को।",
            "Octopus अपना DNA खुद edit कर सकता है — ये धरती का सबसे intelligent invertebrate है।",
            "Octopus के 9 दिमाग होते हैं — एक main brain और 8 tentacles में एक-एक।"
        ],
        "cta": "जानवरों के अनोखे तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#octopus", "#animals", "#shorts", "#FactO", "#facts"],
        "full_script": "Octopus के 3 दिल होते हैं — और नीला खून बहता है उनमें! Octopus के 2 दिल gills को blood pump करते हैं और एक पूरे body को। Octopus अपना DNA खुद edit कर सकता है — ये धरती का सबसे intelligent invertebrate है। Octopus के 9 दिमाग होते हैं — एक main brain और 8 tentacles में एक-एक। जानवरों के अनोखे तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "कौवे इंसान का चेहरा याद रखते हैं!",
        "hook": "कौवे इंसान का चेहरा याद रखते हैं और सालों तक बदला ले सकते हैं!",
        "body": [
            "Research में पाया गया कि कौवे उन लोगों को target करते हैं जिन्होंने उन्हें परेशान किया।",
            "कौवे tools बनाते और इस्तेमाल करते हैं — ये intelligence का सबसे बड़ा sign है।",
            "कौवे अपने मरे हुए साथियों के लिए funeral भी करते हैं।"
        ],
        "cta": "जानवरों के amazing तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#crow", "#animals", "#shorts", "#FactO", "#facts"],
        "full_script": "कौवे इंसान का चेहरा याद रखते हैं और सालों तक बदला ले सकते हैं! Research में पाया गया कि कौवे उन लोगों को target करते हैं जिन्होंने उन्हें परेशान किया। कौवे tools बनाते और इस्तेमाल करते हैं — ये intelligence का सबसे बड़ा sign है। कौवे अपने मरे हुए साथियों के लिए funeral भी करते हैं। जानवरों के amazing तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "Sharks Dinosaurs से भी पुरानी मछली है!",
        "hook": "Sharks इस धरती पर Dinosaurs से भी 200 million साल पहले से हैं!",
        "body": [
            "Sharks 450 million साल से पृथ्वी पर हैं — 5 mass extinctions survive किए।",
            "Shark की हड्डियाँ नहीं होतीं — उनका पूरा skeleton cartilage से बना है।",
            "Sharks को cancer बहुत कम होता है — scientists इस पर research कर रहे हैं।"
        ],
        "cta": "प्रकृति के रहस्य जानने के लिए FactO फॉलो करें!",
        "hashtags": ["#sharks", "#animals", "#shorts", "#FactO", "#nature"],
        "full_script": "Sharks इस धरती पर Dinosaurs से भी 200 million साल पहले से हैं! Sharks 450 million साल से पृथ्वी पर हैं — 5 mass extinctions survive किए। Shark की हड्डियाँ नहीं होतीं — उनका पूरा skeleton cartilage से बना है। Sharks को cancer बहुत कम होता है — scientists इस पर research कर रहे हैं। प्रकृति के रहस्य जानने के लिए FactO फॉलो करें!"
    },
    {
        "title": "हाथी इंसानों की तरह रोते हैं!",
        "hook": "हाथी अपने मरे हुए साथियों के लिए इंसानों की तरह शोक मनाते हैं!",
        "body": [
            "हाथी अपने मृत परिजनों की हड्डियों को सालों बाद भी पहचान लेते हैं।",
            "हाथियों की memory इतनी strong होती है कि वो 50 साल पुरानी जगह याद रखते हैं।",
            "हाथी खुद को आईने में पहचान सकते हैं — ये बहुत rare ability है।"
        ],
        "cta": "जानवरों की दुनिया के तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#elephant", "#animals", "#shorts", "#FactO", "#nature"],
        "full_script": "हाथी अपने मरे हुए साथियों के लिए इंसानों की तरह शोक मनाते हैं! हाथी अपने मृत परिजनों की हड्डियों को सालों बाद भी पहचान लेते हैं। हाथियों की memory इतनी strong होती है कि वो 50 साल पुरानी जगह याद रखते हैं। हाथी खुद को आईने में पहचान सकते हैं — ये बहुत rare ability है। जानवरों की दुनिया के तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "तितलियाँ पैरों से taste करती हैं!",
        "hook": "तितलियाँ अपने पैरों से खाने का taste लेती हैं — जीभ से नहीं!",
        "body": [
            "तितलियों के पैरों में taste sensors होते हैं जो food detect करते हैं।",
            "तितली का जीवन सिर्फ 2 से 4 हफ्ते का होता है — पर वो हजारों किलोमीटर migrate करती हैं।",
            "Monarch butterfly Mexico से Canada तक 4000 किलोमीटर का सफर करती है।"
        ],
        "cta": "प्रकृति के अनोखे तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#butterfly", "#nature", "#shorts", "#FactO", "#facts"],
        "full_script": "तितलियाँ अपने पैरों से खाने का taste लेती हैं — जीभ से नहीं! तितलियों के पैरों में taste sensors होते हैं जो food detect करते हैं। तितली का जीवन सिर्फ 2 से 4 हफ्ते का होता है — पर वो हजारों किलोमीटर migrate करती हैं। Monarch butterfly Mexico से Canada तक 4000 किलोमीटर का सफर करती है। प्रकृति के अनोखे तथ्यों के लिए FactO फॉलो करें!"
    },

    # ── Money & Economy ───────────────────────────────
    {
        "title": "Bitcoin का inventor आज भी unknown है!",
        "hook": "Bitcoin बनाने वाले Satoshi Nakamoto की असली identity आज भी रहस्य है!",
        "body": [
            "Satoshi के wallet में 1 million Bitcoin हैं जो आज $60 billion से ज्यादा के हैं।",
            "Satoshi ने 2010 के बाद कभी कोई message नहीं किया — बस गायब हो गए।",
            "दुनिया के कई बड़े लोग claim कर चुके हैं कि वो Satoshi हैं — पर कोई prove नहीं कर पाया।"
        ],
        "cta": "पैसे और technology के रहस्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#bitcoin", "#crypto", "#shorts", "#FactO", "#money"],
        "full_script": "Bitcoin बनाने वाले Satoshi Nakamoto की असली identity आज भी रहस्य है! Satoshi के wallet में 1 million Bitcoin हैं जो आज $60 billion से ज्यादा के हैं। Satoshi ने 2010 के बाद कभी कोई message नहीं किया — बस गायब हो गए। दुनिया के कई बड़े लोग claim कर चुके हैं कि वो Satoshi हैं — पर कोई prove नहीं कर पाया। पैसे और technology के रहस्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "दुनिया की 1% population के पास 50% wealth है!",
        "hook": "दुनिया के सबसे अमीर 1% लोगों के पास बाकी सब से ज्यादा पैसा है!",
        "body": [
            "Elon Musk एक second में जितना कमाता है वो एक average worker की 1 महीने की salary है।",
            "अगर दुनिया की सारी दौलत बराबर बाँट दी जाए तो हर इंसान को $23,000 मिलेंगे।",
            "Top 10 billionaires की combined wealth कई देशों की GDP से ज्यादा है।"
        ],
        "cta": "पैसे की दुनिया के सच जानने के लिए FactO फॉलो करें!",
        "hashtags": ["#money", "#wealth", "#shorts", "#FactO", "#facts"],
        "full_script": "दुनिया के सबसे अमीर 1% लोगों के पास बाकी सब से ज्यादा पैसा है! Elon Musk एक second में जितना कमाता है वो एक average worker की 1 महीने की salary है। अगर दुनिया की सारी दौलत बराबर बाँट दी जाए तो हर इंसान को $23,000 मिलेंगे। Top 10 billionaires की combined wealth कई देशों की GDP से ज्यादा है। पैसे की दुनिया के सच जानने के लिए FactO फॉलो करें!"
    },
    {
        "title": "Dubai में ATM से सोना निकलता है!",
        "hook": "Dubai में ATM से cash नहीं — असली सोना निकलता है!",
        "body": [
            "Dubai के Gold ATMs में 24 carat gold bars और coins मिलते हैं।",
            "Dubai में tax नहीं है — इसीलिए दुनिया भर के अमीर लोग वहाँ रहते हैं।",
            "Dubai का Burj Khalifa इतना ऊँचा है कि वहाँ से sunrise दो बार देख सकते हैं।"
        ],
        "cta": "दुनिया के amazing तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#dubai", "#money", "#shorts", "#FactO", "#facts"],
        "full_script": "Dubai में ATM से cash नहीं — असली सोना निकलता है! Dubai के Gold ATMs में 24 carat gold bars और coins मिलते हैं। Dubai में tax नहीं है — इसीलिए दुनिया भर के अमीर लोग वहाँ रहते हैं। Dubai का Burj Khalifa इतना ऊँचा है कि वहाँ से sunrise दो बार देख सकते हैं। दुनिया के amazing तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "Amazon हर second $4,700 कमाता है!",
        "hook": "Amazon हर एक second में $4,700 कमाता है — आपकी सालाना salary से ज्यादा!",
        "body": [
            "Jeff Bezos ने Amazon की शुरुआत एक garage से की थी सिर्फ $10,000 से।",
            "Amazon का एक दिन का revenue कई छोटे देशों की GDP से ज्यादा है।",
            "Amazon के warehouse में robots इंसानों से ज्यादा काम करते हैं।"
        ],
        "cta": "Business और money के तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#amazon", "#business", "#shorts", "#FactO", "#money"],
        "full_script": "Amazon हर एक second में $4,700 कमाता है — आपकी सालाना salary से ज्यादा! Jeff Bezos ने Amazon की शुरुआत एक garage से की थी सिर्फ $10,000 से। Amazon का एक दिन का revenue कई छोटे देशों की GDP से ज्यादा है। Amazon के warehouse में robots इंसानों से ज्यादा काम करते हैं। Business और money के तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "Monaco में एक भी farmer नहीं है!",
        "hook": "Monaco दुनिया का सबसे अमीर देश है — और वहाँ एक भी farmer नहीं है!",
        "body": [
            "Monaco सिर्फ 2 square kilometer का है — दुनिया का दूसरा सबसे छोटा देश।",
            "Monaco की per capita income दुनिया में सबसे ज्यादा है।",
            "Monaco में crime rate लगभग zero है क्योंकि हर जगह CCTV cameras हैं।"
        ],
        "cta": "दुनिया के अनोखे देशों के बारे में जानने के लिए FactO फॉलो करें!",
        "hashtags": ["#monaco", "#world", "#shorts", "#FactO", "#facts"],
        "full_script": "Monaco दुनिया का सबसे अमीर देश है — और वहाँ एक भी farmer नहीं है! Monaco सिर्फ 2 square kilometer का है — दुनिया का दूसरा सबसे छोटा देश। Monaco की per capita income दुनिया में सबसे ज्यादा है। Monaco में crime rate लगभग zero है क्योंकि हर जगह CCTV cameras हैं। दुनिया के अनोखे देशों के बारे में जानने के लिए FactO फॉलो करें!"
    },

    # ── Psychology & Mind ─────────────────────────────
    {
        "title": "इंसान एक दिन में 6000 thoughts सोचता है!",
        "hook": "आप एक दिन में 6,000 से ज्यादा thoughts सोचते हैं — और 80% negative होते हैं!",
        "body": [
            "Research के अनुसार ज्यादातर negative thoughts वही होते हैं जो कल भी सोचे थे।",
            "इंसान का दिमाग हर चीज़ में patterns ढूँढता है — इसीलिए बादलों में shapes दिखते हैं।",
            "Positive सोचने की practice से दिमाग literally बदल जाता है — इसे neuroplasticity कहते हैं।"
        ],
        "cta": "दिमाग के रहस्य जानने के लिए FactO फॉलो करें!",
        "hashtags": ["#psychology", "#mind", "#shorts", "#FactO", "#facts"],
        "full_script": "आप एक दिन में 6,000 से ज्यादा thoughts सोचते हैं — और 80% negative होते हैं! Research के अनुसार ज्यादातर negative thoughts वही होते हैं जो कल भी सोचे थे। इंसान का दिमाग हर चीज़ में patterns ढूँढता है — इसीलिए बादलों में shapes दिखते हैं। Positive सोचने की practice से दिमाग literally बदल जाता है — इसे neuroplasticity कहते हैं। दिमाग के रहस्य जानने के लिए FactO फॉलो करें!"
    },
    {
        "title": "अकेलापन smoking से ज्यादा खतरनाक है!",
        "hook": "Scientists का कहना है कि अकेलापन 15 cigarettes रोज पीने जितना नुकसानदेह है!",
        "body": [
            "Loneliness से heart disease, depression और early death का खतरा बढ़ता है।",
            "Social media ज्यादा use करने वाले लोग actually ज्यादा lonely feel करते हैं।",
            "किसी से हाथ मिलाने या गले मिलने से oxytocin hormone निकलता है जो stress कम करता है।"
        ],
        "cta": "Psychology के amazing तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#psychology", "#health", "#shorts", "#FactO", "#mentalhealth"],
        "full_script": "Scientists का कहना है कि अकेलापन 15 cigarettes रोज पीने जितना नुकसानदेह है! Loneliness से heart disease, depression और early death का खतरा बढ़ता है। Social media ज्यादा use करने वाले लोग actually ज्यादा lonely feel करते हैं। किसी से हाथ मिलाने या गले मिलने से oxytocin hormone निकलता है जो stress कम करता है। Psychology के amazing तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "Music सुनने से दर्द कम होता है!",
        "hook": "Music सुनना एक natural painkiller है — science ने prove किया है!",
        "body": [
            "Music सुनने से दिमाग में dopamine निकलता है — वही chemical जो खाने से निकलता है।",
            "Surgery के बाद patients जो music सुनते हैं उन्हें कम painkillers की जरूरत होती है।",
            "आपकी पसंदीदा song सुनकर जो goosebumps आते हैं — उसे frisson कहते हैं।"
        ],
        "cta": "दिमाग और science के तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#music", "#psychology", "#shorts", "#FactO", "#facts"],
        "full_script": "Music सुनना एक natural painkiller है — science ने prove किया है! Music सुनने से दिमाग में dopamine निकलता है — वही chemical जो खाने से निकलता है। Surgery के बाद patients जो music सुनते हैं उन्हें कम painkillers की जरूरत होती है। आपकी पसंदीदा song सुनकर जो goosebumps आते हैं — उसे frisson कहते हैं। दिमाग और science के तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "पहली नजर में प्यार सिर्फ 4 मिनट में होता है!",
        "hook": "किसी से प्यार होने में सिर्फ 4 मिनट लगते हैं — बाकी सब बहाना है!",
        "body": [
            "Psychology के अनुसार attraction में words सिर्फ 7% role play करते हैं।",
            "Body language 55% और voice tone 38% decide करती है कि आप किसे like करेंगे।",
            "जब आप किसी को पसंद करते हैं तो आपकी pupils automatically बड़ी हो जाती हैं।"
        ],
        "cta": "Psychology के fascinating तथ्यों के लिए FactO फॉलो करें!",
        "hashtags": ["#love", "#psychology", "#shorts", "#FactO", "#facts"],
        "full_script": "किसी से प्यार होने में सिर्फ 4 मिनट लगते हैं — बाकी सब बहाना है! Psychology के अनुसार attraction में words सिर्फ 7% role play करते हैं। Body language 55% और voice tone 38% decide करती है कि आप किसे like करेंगे। जब आप किसी को पसंद करते हैं तो आपकी pupils automatically बड़ी हो जाती हैं। Psychology के fascinating तथ्यों के लिए FactO फॉलो करें!"
    },
    {
        "title": "आपका दिमाग future predict करता रहता है!",
        "hook": "आपका दिमाग हर second future predict करता है — और अक्सर गलत होता है!",
        "body": [
            "Predictive processing के अनुसार दिमाग reality नहीं देखता — बस अपनी prediction confirm करता है।",
            "इसीलिए magic tricks काम करती हैं — दिमाग वो देखता है जो वो expect करता है।",
            "Optical illusions इसीलिए होते हैं क्योंकि दिमाग की prediction गलत होती है।"
        ],
        "cta": "दिमाग के रहस्यों के लिए FactO फॉलो और share करें!",
        "hashtags": ["#brain", "#psychology", "#shorts", "#FactO", "#mind"],
        "full_script": "आपका दिमाग हर second future predict करता है — और अक्सर गलत होता है! Predictive processing के अनुसार दिमाग reality नहीं देखता — बस अपनी prediction confirm करता है। इसीलिए magic tricks काम करती हैं — दिमाग वो देखता है जो वो expect करता है। Optical illusions इसीलिए होते हैं क्योंकि दिमाग की prediction गलत होती है। दिमाग के रहस्यों के लिए FactO फॉलो और share करें!"
    },
]


def generate_script(topic):
    """Try Gemini first, fallback to pre-written scripts if quota exceeded."""

    # Try Gemini API first
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt = SCRIPT_PROMPT.format(
            niche=NICHE,
            duration=VIDEO_DURATION_SECONDS,
            topic=topic,
            audience=TARGET_AUDIENCE
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.9,
                max_output_tokens=1000,
            )
        )
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        script = json.loads(raw)
        print(f"[Script] Gemini Generated: {script['title']}")
        return script

    except Exception as e:
        print(f"[Script] Gemini quota exceeded — using fallback script")
        import random
        script = random.choice(FALLBACK_SCRIPTS)
        print(f"[Script] Fallback: {script['title']}")
        return script

if __name__ == "__main__":
    script = generate_script("surprising facts about the human brain")
    print(json.dumps(script, indent=2))