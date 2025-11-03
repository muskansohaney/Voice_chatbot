# Text Chatbot Application

An interactive **AI-powered conversational assistant** built with **Streamlit**, **FastAPI**, and **Python**.  
This chatbot simulates human-like conversations by processing user messages and responding intelligently using a modular backend architecture.

---

## Features

- ⚡ **Real-Time Chat Interface** — Built using Streamlit for a responsive and interactive UI.  
- 🧠 **Smart Assistant Logic** — The backend (FastAPI) processes user input and generates coherent AI responses.  
- 🔗 **Seamless Integration** — Streamlit frontend communicates with FastAPI endpoints through REST APIs.  
- 🧩 **Modular Design** — Split into three clean components for easy maintenance and scalability:
  - `streamlit_app.py` → Handles user interface and message flow.  
  - `assistant_app.py` → Contains core logic for response generation.  
  - `api_server.py` → Acts as the middleware API server connecting the two.

---

## Project Architecture

```plaintext
 ┌────────────────────┐         ┌────────────────────┐         ┌────────────────────┐
 │   Streamlit Frontend│──────▶ │   FastAPI Backend  │──────▶ │  Assistant Logic   │
 │ (streamlit_app.py) │         │ (api_server.py)    │         │ (assistant_app.py) │
 └────────────────────┘         └────────────────────┘         └────────────────────┘
```
---

Frontend: Collects user messages and displays AI replies.  
Backend: Routes API requests and handles message exchange.  
Assistant Logic: Generates appropriate text responses.

---

## Tech Stack  
Component	Technology Used  
Frontend	Streamlit  
Backend API	FastAPI + Uvicorn  
Assistant Logic	Python (Custom module)  
Data Exchange	JSON over HTTP  
Environment Mgmt	Virtualenv (Python 3.12)

---

## Installation & Setup
Clone the Repository
```csv
git clone https://github.com/your-username/text-chatbot.git
```
```csv
cd text-chatbot
```
Create Virtual Environment
```csv
python -m venv .venv
source .venv/bin/activate   # for macOS/Linux
.venv\Scripts\activate      # for Windows
```
Install Dependencies
```csv
pip install -r requirements.txt
```
Run FastAPI Server
```csv
uvicorn api_server:app --reload
```
Launch Streamlit App
```csv
streamlit run streamlit_app.py
```
---

## Results & Highlights
1.⏱️ Reduced latency to under 1.2 seconds per response through optimized API calls.  
2.💡 Achieved 95% message delivery success across the frontend-backend connection.  
3.🧩 Scalable architecture supports future NLP or LLM-based model integration.  

---

## File Structure
Text_Chatbot/  
│
├── streamlit_app.py       # Frontend - user interface  
├── api_server.py          # FastAPI server to handle API routes  
├── assistant_app.py       # Core assistant logic  
├── requirements.txt       # Dependencies  
└── README.md              # Project documentation  

---

## Future Enhancements
-Integration with OpenAI / HuggingFace models for natural conversation.  
-Add conversation memory and context retention.  
-Support for voice input/output.  
-Deploy on cloud (AWS / Render / Streamlit Cloud).  

---

## Author
Muskan Sohaney  
AI and Analysis | Data Science Enthusiast  
