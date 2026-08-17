import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def generate_hf_story(caption, genre, story_length):
    length_map = {
        "Short": "5-6 sentences",
        "Medium": "10-12 sentences",
        "Long": "15-18 sentences"
    }

    prompt = f"""
You are a creative storyteller.

Write a vivid, imaginative, emotionally rich {genre.lower()} story
of {length_map[story_length]} inspired by the image below.

Rules:
- Do NOT repeat the image description literally
- Introduce characters
- Include emotions and a narrative arc

Image description:
{caption}

Story:
""".strip()

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if response.status_code != 200:
            return None

        result = response.json()
        story = result.get("response", "").strip()
        return story if len(story) > 50 else None

    except Exception as e:
        print("Ollama error:", e)
        return None


    