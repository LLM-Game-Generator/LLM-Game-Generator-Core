import os
import openai
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()


def get_client_config(provider):
    """
    根據 Provider 回傳對應的 Client 設定 (api_key, base_url)
    支援 OpenAI 相容介面的服務 (Groq, Ollama, Mistral)
    """
    provider = provider.lower()

    if provider == "openai":
        return {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": None
        }
    elif provider == "groq":
        return {
            "api_key": os.getenv("GROQ_API_KEY"),
            "base_url": "https://api.groq.com/openai/v1"
        }
    elif provider == "ollama":
        # 這裡修改：優先讀取 OLLAMA_API_KEY，若無則預設為 "ollama"
        return {
            "api_key": os.getenv("OLLAMA_API_KEY", "ollama"),
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        }
    elif provider == "mistral":
        return {
            "api_key": os.getenv("MISTRAL_API_KEY"),
            "base_url": "https://api.mistral.ai/v1"
        }
    return None


def call_google_gemini(system_prompt, user_prompt, model, temperature):
    """處理 Google Gemini 的特殊邏輯"""
    try:
        import google.generativeai as genai
    except ImportError:
        return "Error: 請安裝 google-generativeai 套件"

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: 未設定 GOOGLE_API_KEY"

    try:
        genai.configure(api_key=api_key)
        generation_config = {
            "temperature": temperature,
            "top_p": 0.95,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        gemini_model = genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config,
            system_instruction=system_prompt
        )
        response = gemini_model.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return f"Gemini API Error: {str(e)}"


def call_llm(system_prompt, user_prompt, provider="openai", model="gpt-4o-mini", temperature=0.7):
    """[統一入口] 支援多種 LLM Provider"""
    provider = provider.lower()

    if provider in ["google", "gemini"]:
        if model.startswith("gpt"): model = "gemini-1.5-flash"
        return call_google_gemini(system_prompt, user_prompt, model, temperature)

    config = get_client_config(provider)
    if not config: return f"Error: 不支援的 Provider '{provider}'"

    # Ollama 本地端通常不需要 Key，但遠端或透過 Proxy 可能需要
    # 這裡的邏輯是：只有當 config["api_key"] 是空的且不是 ollama 時才報錯
    # 但因為我們在 get_client_config 裡對 ollama 設定了預設值，所以這裡通常會過
    if not config["api_key"] and provider != "ollama":
        return f"Error: 請在 .env 設定 {provider.upper()}_API_KEY"

    try:
        client = openai.OpenAI(api_key=config["api_key"], base_url=config["base_url"])
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM Call Error ({provider}): {str(e)}"