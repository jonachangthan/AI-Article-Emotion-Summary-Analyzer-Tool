import streamlit as st
import requests
import json

# ==========================================
# 🔧 設定區 (請務必檢查這裡)
# ==========================================
# 請填入你的 n8n Webhook URL (建議用 Test URL 配合 Execute Workflow)
N8N_WEBHOOK_URL = "https://g113056038.app.n8n.cloud/webhook/110eb6e6-a6de-439f-8f08-9386509c6b08" 
# 注意：上面的 ID (110eb...) 只是範例，請換成你自己的！

# ==========================================
# 🖥️ 頁面設計
# ==========================================
st.set_page_config(page_title="AI 智能分析助手", page_icon="🤖", layout="wide")

st.title("文章情緒摘要分析器")
st.markdown("連接 **n8n Workflow**，輸入文章後，AI 將自動進行摘要、情緒分析與重點提取。")

# 左側輸入區，右側顯示結果
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📥 輸入文章")
    default_text = "在此貼上你想分析的長篇文章..."
    user_input = st.text_area("內容：", value=default_text, height=300)
    
    analyze_btn = st.button("🚀 開始分析", use_container_width=True)

# ==========================================
# ⚙️ 核心邏輯
# ==========================================
if analyze_btn:
    if not user_input or len(user_input) < 10:
        st.warning("⚠️ 內容太短，請輸入更多文字！")
    else:
        with col2:
            st.subheader("📊 分析結果")
            status_box = st.info("🔄 連線中，正在呼叫 n8n AI Agent...")
            
            try:
                # 1. 準備資料 payload (Key 必須對應 n8n 的設定)
                payload = {"content": user_input}
                
                # 2. 發送 POST 請求
                response = requests.post(N8N_WEBHOOK_URL, json=payload)
                
                # 3. 檢查連線狀態
                if response.status_code == 200:
                    status_box.success("✅ 分析完成！")
                    
                    # 嘗試取得 JSON 資料
                    try:
                        raw_data = response.json()
                    except:
                        st.error("❌ 回傳的不是 JSON 格式")
                        st.text(response.text)
                        st.stop()

                    # --- 關鍵修正：資料清洗 ---
                    # 由於 n8n 的結構可能變動，這裡進行智慧搜尋
                    # 優先找 output 欄位，如果沒有，就用整個回傳內容
                    ai_result = raw_data.get('output', raw_data)

                    # 如果 ai_result 是字串 (有時 Groq 會回傳字串型的 JSON)，嘗試再次解析
                    if isinstance(ai_result, str):
                        try:
                            ai_result = json.loads(ai_result)
                        except:
                            # 如果真的解不開，就保持原樣
                            pass

                    # --- 顯示 Debug 資訊 (作業截圖好用) ---
                    with st.expander("🔍 開發者模式：查看原始 JSON"):
                        st.json(raw_data)

                    # --- 4. 視覺化呈現 ---
                    
                    # (A) 情緒分析
                    sentiment = ai_result.get('sentiment', '未偵測').lower()
                    if 'positive' in sentiment:
                        st.success(f"😊 整體情緒：正向 ({sentiment})")
                    elif 'negative' in sentiment:
                        st.error(f"😡 整體情緒：負向 ({sentiment})")
                    else:
                        st.info(f"😐 整體情緒：中立 ({sentiment})")

                    # (B) 摘要
                    st.markdown("### 📝 重點摘要")
                    summary = ai_result.get('summary', '無法讀取摘要，請查看原始 JSON')
                    st.write(summary)

                    # (C) 標籤與洞察
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("### 🏷️ 相關主題")
                        topics = ai_result.get('topics', [])
                        if isinstance(topics, list):
                            for t in topics:
                                st.code(t)
                        else:
                            st.write(topics)

                    with c2:
                        st.markdown("### 💡 核心洞察")
                        insights = ai_result.get('keyInsights', [])
                        if isinstance(insights, list):
                            for i in insights:
                                st.markdown(f"- {i}")
                        else:
                            st.write(insights)

                else:
                    status_box.error(f"❌ 伺服器錯誤：狀態碼 {response.status_code}")
                    st.code(response.text)

            except Exception as e:
                status_box.error(f"❌ 發生連線錯誤：{str(e)}")
                st.warning("💡 提示：請確認 n8n 是否已按下 'Execute Workflow' 且處於 Waiting 狀態？")