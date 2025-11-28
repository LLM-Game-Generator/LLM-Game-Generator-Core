from src.utils import call_llm
from src.testing.prompts import FIXER_PROMPT
from src.generation.file_utils import save_code_to_file
import os


def run_fix_loop(file_path, error_message, provider="openai", model="gpt-4o-mini"):
    """
    自動修復迴圈：讀取代碼 -> 提交錯誤 -> 獲取新代碼 -> 存檔
    """
    print(f"[Member 3] 正在嘗試修復代碼... (Error: {error_message[:50]}...)")

    # 1. 讀取壞掉的代碼
    if not os.path.exists(file_path):
        return None, "找不到原始代碼檔案"

    with open(file_path, "r", encoding="utf-8") as f:
        broken_code = f.read()

    # 2. 組合 Prompt
    full_prompt = FIXER_PROMPT.format(code=broken_code, error=error_message)

    # 3. 呼叫 LLM 進行修復
    response = call_llm("You are a Code Fixer.", full_prompt, provider=provider, model=model)

    # 4. 儲存修復後的代碼 (覆蓋原檔)
    # 我們重用 generation 模組的 save_code_to_file，因為邏輯一樣 (解析 markdown -> 存檔)
    # 這裡假設輸出目錄跟原檔一樣
    output_dir = os.path.dirname(file_path)
    new_path = save_code_to_file(response, output_dir=output_dir)

    if new_path:
        return new_path, "修復完成，已更新代碼。"
    else:
        return None, "AI 無法生成有效的 Python 代碼區塊。"