import streamlit as st
import os

# 更新後的 Import 路徑
from src.design.chains import run_design_phase
from src.generation.core import run_core_phase
from src.testing.runner import static_code_check, launch_game

st.set_page_config(page_title="AI Pygame Generator", page_icon="🎮")

st.title("🎮 ChatDev: Pygame 自動生成工廠 (Modular Ver.)")
st.markdown("---")

# Sidebar: 模型設定
st.sidebar.header("Model Settings")
provider = st.sidebar.selectbox("LLM Provider", ["openai", "groq", "google", "ollama", "mistral"])
model_name = st.sidebar.text_input("Model Name", value="gpt-4o-mini")
api_key = st.sidebar.text_input("API Key", type="password")

if api_key:
    # 動態設定環境變數
    env_var_name = f"{provider.upper()}_API_KEY"
    os.environ[env_var_name] = api_key

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
                status_text.text("👤 Member 3 (測試員) 正在檢查代碼...")
                is_valid, message = static_code_check(game_file_path)

                if is_valid:
                    progress_bar.progress(100)
                    status_text.text("✅ 全部完成！準備發布。")
                    st.balloons()

                    st.markdown("### 🎮 試玩專區")
                    if st.button("▶️ 啟動遊戲"):
                        msg = launch_game(game_file_path)
                        st.info(msg)
                    else:
                        st.error(f"靜態檢查失敗: {message}")
                        # 新增：自動修復按鈕
                        if st.button("🔧 呼叫 Member 3 自動修復"):
                            # 引用剛寫好的 fixer
                            from src.testing.fixer import run_fix_loop

                            with st.spinner("正在修復中..."):
                                new_path, fix_msg = run_fix_loop(game_file_path, message, provider, model_name)

                            if new_path:
                                st.success(fix_msg)
                                st.experimental_rerun()  # 重新整理頁面以載入新代碼
                            else:
                                st.error("修復失敗，請檢查 Prompt。")
            else:
                st.error("程式碼生成失敗，未能解析出 Python Block。")

        except Exception as e:
            st.error(f"發生系統錯誤: {str(e)}")