# 🧠 AI-Article-Emotion-Summary-Analyzer-Tool (AI 文章情緒摘要分析器)

這是一個自動化內容分析工具，利用 **Streamlit** 作為前端介面，並透過 **n8n** 自動化流程串接 **Groq AI** 模型。
它可以將長篇文章快速轉化為結構化的洞察報告，包括摘要、情緒傾向、關鍵標籤與核心觀點。

## ✨ 功能特色
- **自動摘要**：利用 AI 快速提煉文章重點。
- **情緒分析**：偵測文章的正向、負向或中立情緒。
- **結構化輸出**：自動提取關鍵主題 (Topics) 與核心洞察 (Key Insights)。
- **無縫整合**：前後端分離架構，透過 Webhook 即時溝通。

## 🛠️ 技術棧
- **Frontend**: Python, Streamlit
- **Automation**: n8n (Self-hosted)
- **AI Model**: Groq (Llama-3.3-70b-versatile)
- **Communication**: RESTful Webhook (JSON)

## 🚀 安裝與設定

### 1. n8n 設定
1. 將 `workflow.json` 匯入 n8n。
2. 設定 **Groq API** 憑證。
3. 修改 **Webhook 節點**，確保 Response Mode 設為 `Using 'Respond to Webhook' Node`。
4. 開啟 workflow 右上角的 **Active** 開關 (正式模式)。
5. 複製 **Production Webhook URL**。

### 2. Python 環境設定
確保已安裝 Python 3.8+，然後執行：

```bash
pip install -r requirements.txt
```

### 設定 Webhook URL
打開 app.py，將 N8N_WEBHOOK_URL 變數替換為你的 n8n Production URL。

```python
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/your-webhook-id"
```

## ▶️ 如何執行
在終端機輸入以下指令啟動前端介面：
```bash
streamlit run app.py
```

瀏覽器將自動開啟，輸入文章並點擊「開始分析」即可看到結果。


<img width="1865" height="924" alt="result" src="https://github.com/user-attachments/assets/40ff0664-f55e-4069-a17e-6be6866c5710" />
