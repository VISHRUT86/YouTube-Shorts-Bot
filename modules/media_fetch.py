import requests
import os
import random

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
PEXELS_HEADERS = {"Authorization": PEXELS_API_KEY}

TOPIC_IMAGE_MAP = {
    # Science & Body
    "दिल":       ["human heart anatomy red", "heartbeat pulse cardiology"],
    "हड्डी":     ["human skeleton bones xray", "bone structure anatomy"],
    "दिमाग":     ["human brain neuron glowing", "brain science illustration"],
    "DNA":        ["DNA double helix blue", "genetics science laboratory"],
    "आँख":       ["human eye close up", "eye iris macro photography"],
    "नींद":      ["person sleeping night peaceful", "dream sleep dark"],
    "आँत":       ["digestive system anatomy", "gut microbiome science"],
    "खून":       ["blood cells microscope red", "human blood science"],
    "कार्बन":    ["chemistry carbon molecule", "science laboratory"],
    "लोहा":      ["iron metal industrial", "steel structure metal"],
    "शहद":       ["honey golden jar", "beehive honeycomb golden"],
    "एफिल":      ["eiffel tower paris", "paris france landmark"],
    "पेट":       ["stomach anatomy human", "digestive health science"],
    "लार":       ["science laboratory biology", "human biology research"],

    # Space
    "black hole": ["black hole space", "event horizon dark cosmos"],
    "ब्लैक होल": ["black hole space galaxy", "dark cosmos space"],
    "अंतरिक्ष":  ["galaxy nebula space stars", "cosmos universe dark"],
    "सूरज":      ["sun solar flare", "solar system bright star"],
    "चाँद":      ["moon surface lunar crater", "full moon night sky"],
    "मंगल":      ["mars planet red surface", "red planet nasa"],
    "हीरा":      ["diamond crystal sparkling", "gemstone luxury"],
    "बृहस्पति":  ["jupiter planet nasa", "gas giant space"],
    "photon":     ["light rays science", "physics light beam"],
    "तूफान":     ["storm lightning dramatic", "hurricane satellite view"],
    "पृथ्वी":    ["earth planet space blue", "globe world from space"],

    # History
    "पिरामिड":   ["great pyramid egypt giza", "ancient egypt desert"],
    "pyramid":    ["great pyramid egypt", "ancient egypt ruins"],
    "cleopatra":  ["ancient egypt queen", "egypt hieroglyphics"],
    "viking":     ["viking ship ocean", "norse warrior historical"],
    "ninja":      ["japan samurai ancient", "japanese castle dark"],
    "ww2":        ["world war history", "military history vintage"],
    "columbus":   ["ship ocean exploration", "historical sailing ship"],
    "aztec":      ["aztec ruins mexico", "ancient civilization temple"],

    # Animals
    "octopus":    ["octopus underwater ocean", "deep sea octopus"],
    "कौवा":      ["crow bird black intelligent", "raven bird closeup"],
    "shark":      ["shark underwater blue ocean", "great white shark"],
    "हाथी":      ["elephant wildlife africa", "elephant herd nature"],
    "तितली":     ["butterfly colorful flower", "monarch butterfly"],
    "dinosaur":   ["dinosaur fossil museum", "prehistoric creature art"],
    "bacteria":   ["bacteria microscope science", "microbiology lab"],

    # Money
    "bitcoin":    ["bitcoin cryptocurrency", "crypto blockchain digital"],
    "satoshi":    ["cryptocurrency bitcoin digital", "blockchain technology"],
    "amazon":     ["amazon warehouse robot", "ecommerce technology"],
    "dubai":      ["dubai skyline gold luxury", "burj khalifa night"],
    "monaco":     ["monaco luxury harbor yacht", "monte carlo city"],
    "gold":       ["gold bars luxury wealth", "gold coins shining"],
    "robot":      ["warehouse robot automation", "industrial robot technology"],
    "elon":       ["electric car technology", "space rocket launch"],
    "billionaire":["luxury city skyline night", "wealth business success"],

    # Psychology
    "music":      ["person headphones music", "music notes sound wave"],
    "अकेलापन":   ["person alone city night", "solitude lonely"],
    "प्यार":     ["sunset couple silhouette", "romantic warm light"],
    "optical":    ["optical illusion pattern", "mind trick visual"],
    "dopamine":   ["brain chemistry science", "neuroscience illustration"],
    "memory":     ["brain memory neuron", "psychology mind science"],
    "stress":     ["calm meditation peaceful", "nature peaceful water"],
}

SAFE_FALLBACKS = [
    "galaxy stars universe dark",
    "science laboratory blue",
    "ancient history monument",
    "deep ocean underwater",
    "lightning storm dramatic sky",
    "microscope science research",
    "northern lights aurora",
    "mountain landscape dramatic",
    "technology circuit glowing blue",
    "space telescope stars nasa",
]

def get_query_for_text(text):
    """Find best image query for a given piece of text."""
    text_lower = text.lower()
    for keyword, queries in TOPIC_IMAGE_MAP.items():
        if keyword.lower() in text_lower:
            return random.choice(queries)
    return None

def fetch_single_image(query, output_path):
    """Download one image from Pexels for a given query."""
    url = (
        f"https://api.pexels.com/v1/search"
        f"?query={requests.utils.quote(query)}"
        f"&per_page=5"
        f"&orientation=portrait"
        f"&size=large"
    )
    try:
        resp   = requests.get(url, headers=PEXELS_HEADERS, timeout=10)
        photos = resp.json().get("photos", [])
        if not photos:
            return None
        photo    = random.choice(photos[:5])
        img_url  = photo["src"]["portrait"]
        img_data = requests.get(img_url, timeout=10).content
        with open(output_path, "wb") as f:
            f.write(img_data)
        return output_path
    except Exception as e:
        print(f"[Media] fetch error: {e}")
        return None

def fetch_pexels_images(query, count=5, output_dir="output/frames", script=None):
    """
    Fetch DIFFERENT images for each section of the script:
    - Image 1: Hook
    - Image 2: Fact 1
    - Image 3: Fact 2
    - Image 4: Fact 3
    - Image 5: CTA
    """
    os.makedirs(output_dir, exist_ok=True)
    paths = []

    if script:
        # Build per-section queries
        sections = [
            script.get("hook", ""),
            script.get("body", [""])[0] if len(script.get("body", [])) > 0 else "",
            script.get("body", [""])[1] if len(script.get("body", [])) > 1 else "",
            script.get("body", [""])[2] if len(script.get("body", [])) > 2 else "",
            script.get("cta", ""),
        ]

        print("[Media] Fetching per-section images...")

        for i, section_text in enumerate(sections[:count]):
            img_path = os.path.join(output_dir, f"frame_{i:03d}.jpg")

            # Find matching query for this section
            section_query = get_query_for_text(section_text)

            if not section_query:
                # Try title as fallback
                section_query = get_query_for_text(
                    script.get("title", "")
                )

            if not section_query:
                section_query = random.choice(SAFE_FALLBACKS)

            print(f"[Media] Section {i+1}: '{section_query}'")

            result = fetch_single_image(section_query, img_path)

            if result:
                paths.append(result)
                print(f"[Media] frame_{i:03d}.jpg ✅")
            else:
                # Fallback background
                bg = _make_background(img_path, i)
                paths.append(bg)

        if paths:
            return paths

    # Default: same query for all images
    return _fetch_all_same(query, count, output_dir)

def _fetch_all_same(query, count, output_dir):
    """Fallback — fetch images with same query."""
    url = (
        f"https://api.pexels.com/v1/search"
        f"?query={requests.utils.quote(query)}"
        f"&per_page={count}"
        f"&orientation=portrait"
        f"&size=large"
    )
    paths = []
    try:
        resp   = requests.get(url, headers=PEXELS_HEADERS, timeout=10)
        photos = resp.json().get("photos", [])
        for i, photo in enumerate(photos[:count]):
            img_path = os.path.join(output_dir, f"frame_{i:03d}.jpg")
            img_data = requests.get(
                photo["src"]["portrait"], timeout=10
            ).content
            with open(img_path, "wb") as f:
                f.write(img_data)
            paths.append(img_path)
            print(f"[Media] Downloaded frame_{i:03d}.jpg")
        if paths:
            return paths
    except Exception as e:
        print(f"[Media] Error: {e}")

    return [_make_background(
        os.path.join(output_dir, f"frame_{i:03d}.jpg"), i
    ) for i in range(count)]

def _make_background(path, index=0):
    """Generate dark background."""
    from PIL import Image
    colors = [
        (5, 10, 30), (10, 5, 25),
        (15, 10, 35), (8, 20, 40), (20, 8, 28)
    ]
    img = Image.new("RGB", (1080, 1920), colors[index % len(colors)])
    img.save(path, quality=95)
    return path