Image2Story

Image2Story is an AI-powered application that converts an uploaded image into a creative story.

Features

- Image caption generation using BLIP
- AI-based story generation
- Rule-based fallback
- Multiple genres and story lengths
- Text-to-speech narration
- Semantic search for similar stories

Tech Stack

Python, Streamlit, PyTorch, Hugging Face Transformers, BLIP, FAISS, Sentence Transformers, and Ollama.

Run Locally

pip install -r requirements.txt
streamlit run app.py

Note

The AI story-generation component uses Ollama locally. Ollama and the required model must be installed separately to run the complete application.

Project Structure

Image2Story/
├── app.py
├── backend/
├── config/
├── requirements.txt
└── README.md
