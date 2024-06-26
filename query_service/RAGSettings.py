def Setup():
    import os
    from llama_index.llms.gemini import Gemini
    from llama_index.embeddings.gemini import GeminiEmbedding
    from llama_index.core import Settings
    import dotenv

    dotenv.load_dotenv()
    GEMINI_API = os.getenv("GOOGLE_GEMINI_API")
    EMBED_MODEL = os.getenv("GOOGLE_EMBED_MODEL")

    os.environ["GOOGLE_API_KEY"] = GEMINI_API

    Settings.llm = Gemini(api_key=GEMINI_API, model="models/gemini-pro")
    Settings.embed_model = GeminiEmbedding(model_name=EMBED_MODEL)