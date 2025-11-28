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
            "base_url": None  # 使用官方預設
        }
    elif provider == "groq":
        return {
            "api_key": os.getenv("GROQ_API_KEY"),
            "base_url": "https://api.groq.com/openai/v1"
        }
    elif provider == "ollama":
        return {
            "api_key": "ollama",  # Ollama 隨意字串即可
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        }
    elif provider == "mistral":
        return {
            "api_key": os.getenv("MISTRAL_API_KEY"),
            "base_url": "https://api.mistral.ai/v1"
        }
    return None


def call_google_gemini(system_prompt, user_prompt, model, temperature):
    """
    處理 Google Gemini 的特殊邏輯 (需安裝 google-generativeai)
    """
    try:
        import google.generativeai as genai
    except ImportError:
        return "Error: 請安裝 google-generativeai 套件 (pip install google-generativeai)"

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

        # Gemini 1.5 支援 system_instruction
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
    """
    [統一入口] 支援多種 LLM Provider
    Provider: 'openai', 'groq', 'google', 'ollama', 'mistral'
    """
    provider = provider.lower()

    # --- Case A: Google Gemini (獨立 SDK) ---
    if provider in ["google", "gemini"]:
        # 如果使用者傳入的是 OpenAI 的型號名稱，自動切換成 Gemini 預設型號
        if model.startswith("gpt"):
            model = "gemini-1.5-flash"
        return call_google_gemini(system_prompt, user_prompt, model, temperature)

    # --- Case B: OpenAI Compatible APIs (Groq, Ollama, Mistral) ---
    config = get_client_config(provider)

    if not config:
        return f"Error: 不支援的 Provider '{provider}'"

    if not config["api_key"] and provider != "ollama":
        return f"Error: 請在 .env 設定 {provider.upper()}_API_KEY"

    try:
        client = openai.OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )

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


def call_openai(system_prompt, user_prompt, model="gpt-4o-mini"):
    """
    [兼容層] 舊程式碼呼叫這個函式時，預設使用 OpenAI。
    如果你想全域切換成 Groq，只要改這裡的預設參數即可。
    """
    # 例如：想改成全域預設用 Groq，就改成 provider="groq", model="llama3-70b-8192"
    return call_llm(system_prompt, user_prompt, provider="openai", model=model)