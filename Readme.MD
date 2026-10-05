# 💼 Multi-Competitor Strategy Intelligence Engine

An automated, asynchronous multi-agent workspace framework engineered with LangGraph and Streamlit. The system parallelly tracks target competitor digital footprints, extracts web topology matrices, strips marketing text, and isolates actionable strategic shifts into validated schemas via the Groq API gateway.

---

## 🏗️ Project Topology

Ensure your working directory layout maps to this architecture:

```text
Customer_Intelligent_agent/
│
├── .env                        # Local infrastructure credentials
├── requirements.txt            # System dependencies manifest
├── customer_intelligence.py     # LangGraph runtime state orchestration logic
├── app.py                      # Parallel worker Streamlit dashboard layout
└── README.md                   # System configuration and operations index
```

---

## 🛠️ Infrastructure Configuration

1. **Clone or Verify Workspace Directory:**
   ```bash
   cd C:\Users\ayush\OneDrive\Desktop\Customer_Intelligent_agent
   ```

2. **Environment Resource Mapping (`.env`):**
   Create a `.env` file in the root directory and supply your active framework provider keys:
   ```env
   GROQ_API_KEY=gsk_your_live_production_groq_api_credential_here
   FIRECRAWL_API_KEY=fc-your_live_production_firecrawl_api_credential_here
   ```

---

## 🚀 Installation & Deployment

Execute this sequence from an authenticated shell to clear stale background services, mount dependencies, and initialize the concurrent system pipeline:

### 1. Environment Preparation & Cleanup
Forcefully terminate any existing ghost processes on your network interfaces to avoid port allocation blocks:
```powershell
taskkill /IM python.exe /F
taskkill /IM streamlit.exe /F
```

### 2. Dependency Mounting
Install the exact requirements matrix into your active Python environment:
```powershell
pip install -r requirements.txt
```

### 3. Launching the Multi-Thread Engine Dashboard
Boot up your frontend UI server on an isolated port path:
```powershell
streamlit run app.py --server.port 8504
```

Once initialized, navigate directly to **`http://localhost:8504`** inside a web browser window to control your tracking loops.

---

## 📊 Core System Properties

* **Parallel Node Map:** Utilizes a `ThreadPoolExecutor` worker context loop to scrape and process up to 5 corporate endpoints concurrently without core engine latency lag blocks.
* **Structural Guarantee:** Eliminates API JSON parsing failures via LangChain's native `.with_structured_output()` architecture mapped to an underlying Pydantic schema validation frame.
* **Streamlined UI Polish:** Outfitted with an high-fidelity gradient button accents, clean card borders, and distinct metric titles built for effortless navigation.
* **Auto-Reformatting List Layouts:** Integrates a regex processing layer that converts unstructured numerical text summaries natively into beautifully indented HTML bullet matrices.
* **Data Moat Backup:** Automatically serializes every successful scan terminal state into an independent, timestamped `.json` tracking file directly onto local system memory storage.
