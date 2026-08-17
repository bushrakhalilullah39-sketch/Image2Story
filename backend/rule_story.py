# backend/rule_story.py

def generate_rule_story(caption: str, genre: str, length: str) -> str:
    """
    Generates a deterministic, rule-based story.
    Acts as a baseline and fallback for LLM-based generation.
    """

    # -------------------- COMMON STORY BLOCKS --------------------
    opening = (
        "At first glance, the scene feels quiet and still, as if time has paused for a moment. "
        "There is nothing dramatic happening, yet something about it gently draws attention. "
    )

    grounding = (
        f"The image can be described as {caption}. "
        "This visual detail sets the foundation of the story and gives it a clear sense of place. "
    )

    # -------------------- GENRE-SPECIFIC BLOCKS --------------------
    genre_templates = {
        "Fantasy": {
            "interpretation": (
                "Beyond its surface, the scene feels touched by magic, as if it belongs to another world. "
            ),
            "intrigue": (
                "The atmosphere suggests hidden forces waiting to be discovered. "
            ),
            "ending": (
                "In the end, the scene leaves behind a lingering sense of wonder and mystery. "
            )
        },

        "Sci-Fi": {
            "interpretation": (
                "The scene reflects technological progress and humanity’s endless curiosity. "
            ),
            "intrigue": (
                "It feels like a glimpse into a rapidly evolving future shaped by innovation. "
            ),
            "ending": (
                "The moment hints at a world transformed by discovery and change. "
            )
        },

        "Horror": {
            "interpretation": (
                "Although the scene appears ordinary, something about it feels deeply unsettling. "
            ),
            "intrigue": (
                "The silence grows heavier the longer one observes it, as if something unseen is watching. "
            ),
            "ending": (
                "Nothing moves, yet the unease remains long after the moment has passed. "
            )
        },

        "General": {
            "interpretation": (
                "The scene captures an ordinary moment filled with subtle emotion and meaning. "
            ),
            "intrigue": (
                "It invites quiet reflection and a personal connection to the moment. "
            ),
            "ending": (
                "The story lingers gently, reminding us that even simple moments can be powerful. "
            )
        }
    }

    blocks = genre_templates.get(genre, genre_templates["General"])

    # -------------------- STORY ASSEMBLY BY LENGTH --------------------
    if length == "Short":
        story = (
            opening +
            blocks["ending"]
        )

    elif length == "Medium":
        story = (
            opening +
            grounding +
            blocks["interpretation"] +
            blocks["ending"]
        )

    else:  # Long
        story = (
            opening +
            grounding +
            blocks["interpretation"] +
            blocks["intrigue"] +
            blocks["ending"]
        )

    return story.strip()