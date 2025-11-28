import re
from src.utils import call_llm
from src.generation.prompts import ART_PROMPT


def generate_assets(gdd_context, provider="openai", model="gpt-4o-mini"):
    """產出 JSON 格式的美術設定"""
    response = call_llm(ART_PROMPT, f"GDD Content:\n{gdd_context}", provider=provider, model=model)

    # 清洗資料：只抓取 JSON 區塊
    try:
        # 尋找 {...} 結構
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            return json_match.group(0)
        return response
    except:
        return "{}"