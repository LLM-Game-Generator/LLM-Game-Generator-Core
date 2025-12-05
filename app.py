import streamlit as st
import os
from src import config

# 更新 Import 路徑
from src.design.chains import run_design_phase
from src.generation.core import run_core_phase
from src.testing.runner import static_code_check, launch_game, ai_logic_review
from src.testing.fixer import run_fix_loop

st.set_page_config(page_title="AI Pygame Generator", page_icon="🎮")

st.title("🎮 ChatDev: Pygame 自動生成工廠 (Config Ver.)")
st.markdown("---")

# Sidebar: 模型設定
st.sidebar.header("Model Settings")
provider = st.sidebar.selectbox("LLM Provider", config.PROVIDERS)
model_name = st.sidebar.text_input("Model Name", value="gpt-4o-mini")

# --- 自動載入與設定 API Key (使用 src.config) ---
if provider == "ollama":
    # 1. Base URL 設定
    default_url = config.get_default_ollama_url()
    ollama_url = st.sidebar.text_input("Ollama Base URL", value=default_url)

    # 2. API Token 設定 (新增)
    default_key = config.get_default_api_key(provider)
    api_key = st.sidebar.text_input("Ollama API Token (Optional)", value=default_key, type="password")

    # 更新環境變數
    config.update_llm_env(provider, api_key=api_key, ollama_url=ollama_url)

else:
    # 取得預設 Key (會自動從 .env 讀取)
    default_key = config.get_default_api_key(provider)

    # 顯示輸入框
    api_key = st.sidebar.text_input(f"{provider.capitalize()} API Key", value=default_key, type="password")

    # 更新環境變數
    config.update_llm_env(provider, api_key=api_key)

user_input = st.text_area("請輸入你想做的遊戲 (例如：一個躲避隕石的太空飛船遊戲)", height=100)

if st.button("🚀 開始生成遊戲"):
    if not user_input:
        st.warning("請輸入遊戲點子！")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        # --- Phase 1: Member A (Design) ---
        status_text.text("👤 Member 1 (設計師) 正在分析需求...")
        try:
            gdd_result = run_design_phase(user_input, provider, model_name)
            st.expander("📄 查看遊戲設計文件 (GDD)").markdown(gdd_result)
            progress_bar.progress(33)

            # --- Phase 2: Member B (Core) ---
            status_text.text("👤 Member 2 (工程師) 正在撰寫程式碼...")
            game_file_path = run_core_phase(gdd_result, provider, model_name)

            if game_file_path:
                st.success(f"程式碼已生成於: {game_file_path}")
                with open(game_file_path, "r", encoding="utf-8") as f:
                    st.code(f.read(), language="python")
                progress_bar.progress(66)

                # --- Phase 3: Member C (QA) ---
                status_text.text("👤 Member 3 (測試員) 正在檢查代碼語法...")

                # 1. 語法檢查
                is_syntax_valid, syntax_msg = static_code_check(game_file_path)

                if is_syntax_valid:
                    status_text.text("👤 Member 3 (測試員) 正在審查遊戲邏輯...")

                    # 2. 邏輯檢查
                    is_logic_valid, logic_msg = ai_logic_review(game_file_path, provider, model_name)

                    if is_logic_valid:
                        progress_bar.progress(100)
                        status_text.text("✅ 測試通過！準備發布。")
                        st.balloons()

                        st.markdown("### 🎮 試玩專區")
                        if st.button("▶️ 啟動遊戲"):
                            msg = launch_game(game_file_path)
                            st.info(msg)
                    else:
                        st.error(f"邏輯測試失敗: {logic_msg}")
                        st.warning("正在呼叫 Programmer 自動修復...")

                        # 自動修復迴圈
                        new_path, fix_msg = run_fix_loop(game_file_path, logic_msg, provider, model_name)
                        if new_path:
                            st.success(f"已修復: {fix_msg}")
                            st.info("請重新點擊「開始生成」或手動執行以測試新代碼。")
                else:
                    st.error(f"語法錯誤: {syntax_msg}")
                    st.warning("正在修復語法錯誤...")
                    new_path, fix_msg = run_fix_loop(game_file_path, syntax_msg, provider, model_name)
                    if new_path:
                        st.success(f"語法已修復: {fix_msg}")

            else:
                st.error("程式碼生成失敗，未能解析出 Python Block。")

        except Exception as e:
            import traceback

            st.error(f"發生系統錯誤: {str(e)}")
            st.code(traceback.format_exc())