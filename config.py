import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    # LLM API keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    # LLM model names
    GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama3-8b-8192")
    GOOGLE_MODEL_NAME = os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash")
    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    MISTRAL_MODEL_NAME = os.getenv("MISTRAL_MODEL_NAME", "codestral-lastest")
    DEEPSEEK_MODEL_NAME = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")

    # OLLAMA
    OLLAMA_BASE_URL =  os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
    OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3:8b")

    # Fuzzer
    FUZZER_RUNNING_TIME = 30

    # Embedding model
    LLM_EMBEDDING_PROVIDER = os.getenv("LLM_EMBEDDING_PROVIDER")
    LLM_EMBEDDING_SERVER_ADDRESS = os.getenv("LLM_EMBEDDING_SERVER_ADDRESS")
    LLM_EMBEDDING_SERVER_PORT = os.getenv("LLM_EMBEDDING_SERVER_PORT", "")
    LLM_EMBEDDING_MODEL_TYPE = os.getenv("LLM_EMBEDDING_MODEL_TYPE")
    LLM_EMBEDDING_CLIENT_TOKEN = os.getenv("LLM_EMBEDDING_CLIENT_TOKEN")

    CHROMA_TOKEN = os.getenv("CHROMA_TOKEN")
    CHROMA_TENANT = os.getenv("CHROMA_TENANT")
    CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")
    CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME")

config = Config()