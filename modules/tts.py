import asyncio
import edge_tts
import os

VOICES = {
    # English
    "female_us":   "en-US-JennyNeural",
    "male_us":     "en-US-GuyNeural",
    "female_uk":   "en-GB-SoniaNeural",
    
    # Hindi
    "female_hindi": "hi-IN-SwaraNeural",   # ← Hindi female (best)
    "male_hindi":   "hi-IN-MadhurNeural",  # ← Hindi male
}

async def _synthesize(text, voice, output_path, rate="+10%"):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)

def text_to_speech(text, output_path, voice_key="female_hindi"):
    """Convert script text to MP3 using Edge TTS."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    voice = VOICES.get(voice_key, VOICES["female_hindi"])
    asyncio.run(_synthesize(text, voice, output_path, rate="+10%"))
    print(f"[TTS] Audio saved: {output_path}")
    return output_path

if __name__ == "__main__":
    text_to_speech(
        "क्या आप जानते हैं कि शहद कभी खराब नहीं होता? "
        "मिस्र के पिरामिडों में 3000 साल पुराना शहद मिला था जो अभी भी खाने योग्य था!",
        "output/audio/test_hindi.mp3",
        voice_key="female_hindi"
    )