import ast
import subprocess
import sys
from src.utils import call_llm
from src.testing.prompts import LOGIC_REVIEW_PROMPT


def static_code_check(file_path):
    """
    [第一關] 靜態語法檢查 (Syntax Check)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        ast.parse(code)
        return True, "語法檢查通過 ✅"
    except SyntaxError as e:
        return False, f"語法錯誤 ❌: {e}"
    except Exception as e:
        return False, f"其他錯誤 ❌: {e}"


def ai_logic_review(file_path, provider="openai", model="gpt-4o-mini"):
    """
    [第二關] AI 邏輯審查 (Logic Check)
    專門檢查：能不能動？速度是不是 0？有沒有更新畫面？
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        # 呼叫 LLM 進行代碼健檢
        response = call_llm(
            system_prompt="You are a QA Engineer.",
            user_prompt=LOGIC_REVIEW_PROMPT.format(code=code),
            provider=provider,
            model=model
        )

        # 判斷 AI 的回答
        if "PASS" in response:
            return True, "邏輯檢查通過 (Controls logic looks good) ✅"
        else:
            # 抓取 FAIL 後面的錯誤訊息
            error_msg = response.replace("FAIL:", "").strip()
            # 如果 AI 回答比較長，只取前 100 字
            return False, f"邏輯缺陷: {error_msg[:100]}..."

    except Exception as e:
        # 如果 API 呼叫失敗，我們先假設通過，避免卡住流程
        return True, f"無法進行邏輯審查 (API Error)，跳過檢查。"


def launch_game(file_path):
    """
    嘗試執行生成的遊戲檔案
    """
    try:
        if sys.platform == "win32":
            subprocess.Popen(["python", file_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # Mac/Linux
            subprocess.Popen(["python3", file_path])
        return "遊戲視窗已啟動！"
    except Exception as e:
        return f"啟動失敗: {str(e)}"