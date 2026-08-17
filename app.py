import streamlit as st
from PIL import Image

from backend.captioning import CaptionGenerator
from backend.rule_story import generate_rule_story
from backend.hf_story import generate_hf_story
from backend.vector_store import add_story, search_similar
from backend.tts import narrate

from config.settings import GENRES, STORY_LENGTHS, STORY_MODES


# -------------------- PAGE SETUP --------------------
st.set_page_config(page_title="Image2Story", layout="centered")
st.title("🖼️ Image2Story – AI Story Generator")


# -------------------- LOAD SERVICES --------------------
@st.cache_resource
def load_captioner():
    return CaptionGenerator()

caption_generator = load_captioner()


# -------------------- UI CONTROLS --------------------
genre = st.selectbox("Select Genre", GENRES)
story_length = st.selectbox("Select Story Length", STORY_LENGTHS)
story_mode = st.radio("Story Mode", STORY_MODES)

uploaded_image = st.file_uploader("Upload Image", ["jpg", "jpeg", "png"])


# -------------------- IMAGE PIPELINE --------------------
MAX_IMAGE_SIZE_MB = 5

if uploaded_image:
    # ---- Validation ----
    file_size = len(uploaded_image.getbuffer())
    if file_size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        st.error("Image too large. Please upload an image under 5MB.")
        st.stop()

    try:
        image = Image.open(uploaded_image).convert("RGB")
    except Exception:
        st.error("Invalid image file.")
        st.stop()

    st.image(image, caption="Uploaded Image", use_column_width=True)


    # -------------------- CAPTION --------------------
    with st.spinner("Analyzing image and extracting features..."):
        caption = caption_generator.generate_caption(image)

    st.subheader("📝 Generated Caption")
    st.write(caption)
    st.caption("Caption generated using BLIP vision-language model")


    # -------------------- STORY GENERATION (AI + FALLBACK) --------------------
    with st.spinner("Generating story using AI..."):
        ai_story = generate_hf_story(caption, genre, story_length)

    if ai_story is None:
        st.warning("AI unavailable. Falling back to rule-based story.")
        ai_story = generate_rule_story(caption, genre, story_length)
        story_source = "Rule-Based"
    else:
        story_source = "AI"

    # Store for semantic search
    add_story(ai_story)


    # -------------------- STORY DISPLAY --------------------
    if story_mode == "Rule-Based":
        st.subheader("🧩 Rule-Based Story")
        st.write(generate_rule_story(caption, genre, story_length))

    elif story_mode == "Compare":
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🧩 Rule-Based Story")
            st.write(generate_rule_story(caption, genre, story_length))

        with col2:
            st.subheader("✨ AI-Generated Story")
            st.write(ai_story)

    else:
        st.subheader(f"✨ {story_source} Story")
        st.write(ai_story)

    st.caption(f"Story source: {story_source}")


    # -------------------- AUDIO NARRATION --------------------
    if st.button("🔊 Listen to Story"):
        narrate(ai_story)


    # -------------------- SIMILAR STORIES --------------------
    with st.expander("🔍 Similar Stories (Semantic Search)"):
        similar_stories = search_similar(caption)

        if not similar_stories:
            st.write("No similar stories found yet.")
        else:
            for i, story in enumerate(similar_stories, start=1):
                st.write(f"{i}. {story}")


