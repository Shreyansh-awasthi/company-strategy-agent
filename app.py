import os
import time
import json
import re
import streamlit as st
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from customer_intelligence import run_single_url

st.set_page_config(
    page_title="Multi-Competitor Watchlist Engine",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white !important;
        font-weight: 600;
        padding: 0.75rem 2.5rem;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    .metric-card {
        background-color: white;
        padding: 1.25rem;
        border-radius: 10px;
        border-left: 4px solid #10B981;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        margin-bottom: 1rem;
    }
    .metric-title {
        color: #1E293B;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .metric-value ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    .metric-value li {
        margin-bottom: 0.4rem;
    }
    </style>
""", unsafe_allow_html=True)

def format_to_clean_html_list(text: str) -> str:
    items = re.split(r'\s+(?=\d+\.\s+\*\*)|\s+(?=\d+\.\s+)', text.strip())
    if len(items) <= 1:
        items = re.split(r'(?=\b\d+\.\s+)', text.strip())
    
    clean_items = []
    for item in items:
        cleaned = item.strip()
        if cleaned:
            cleaned = re.sub(r'^\d+\.\s*', '', cleaned)
            cleaned = re.sub(r'\*\*(.*?)\*\*:', r'<strong>\1</strong>:', cleaned)
            cleaned = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cleaned)
            clean_items.append(f"<li>{cleaned}</li>")
            
    if clean_items:
        return f"<ul>{''.join(clean_items)}</ul>"
    return text

with st.sidebar:
    st.image("https://flaticon.com", width=80)
    st.title("Watchlist Matrix")
    st.subheader("System Status")
    st.markdown(f"**Groq Cloud Gateway:** `Connected`" if os.getenv("GROQ_API_KEY") else "**Groq Cloud Gateway:** `Missing`")
    st.markdown(f"**Firecrawl Storage Layer:** `Connected`" if os.getenv("FIRECRAWL_API_KEY") else "**Firecrawl Storage Layer:** `Missing`")
    st.divider()
    st.caption("v3.0.0 • Parallel Graph Thread Execution")

st.title(" Multi-Competitor Watchlist Engine")
st.markdown("Monitor multiple target vectors simultaneously. Utilizes asynchronous worker threads to run independent scraping nodes parallelly.")
st.divider()

st.subheader("📝 Target Watchlist Registration")
col_left, col_right = st.columns(2)

urls = []
with col_left:
    url_1 = st.text_input("Competitor Vector 1", "https://nvidia.com", placeholder="Target Domain URL")
    url_2 = st.text_input("Competitor Vector 2", "https://linear.app", placeholder="Target Domain URL")
    url_3 = st.text_input("Competitor Vector 3", "", placeholder="Target Domain URL (Optional)")

with col_right:
    url_4 = st.text_input("Competitor Vector 4", "", placeholder="Target Domain URL (Optional)")
    url_5 = st.text_input("Competitor Vector 5", "", placeholder="Target Domain URL (Optional)")

for u in [url_1, url_2, url_3, url_4, url_5]:
    cleaned = u.strip()
    if cleaned:
        if not urlparse(cleaned).scheme:
            cleaned = "https://" + cleaned
        urls.append(cleaned)

st.divider()

if st.button("🔥 Execute Concurrent Watchlist Scan"):
    if not urls:
        st.error("Execution Aborted: At least one competitor target parameter must be supplied.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.info(f"⚙️ Initializing Async Engine. Spinning up allocation slots for {len(urls)} target nodes...")
        time.sleep(1)
        
        results = {}
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=len(urls)) as executor:
            future_to_url = {executor.submit(run_single_url, url): url for url in urls}
            
            completed = 0
            for future in future_to_url:
                url = future_to_url[future]
                try:
                    data = future.result()
                    results[url] = data
                except Exception as exc:
                    results[url] = {"raw_markdown": None, "analysis_report": None, "error": f"Thread Panic: {str(exc)}"}
                
                completed += 1
                progress_bar.progress(completed / len(urls))
                status_text.info(f"⚡ Processing Target Nodes... Finished execution map ({completed}/{len(urls)})")
                
        elapsed_time = time.time() - start_time
        status_text.empty()
        progress_bar.empty()
        st.success(f"🚀 All threads resolved successfully! Full intelligence batch generated in {elapsed_time:.2f} seconds.")
        st.divider()
        
        st.subheader("📊 Aggregated Intelligence Panel")
        
        tab_names = [urlparse(url).netloc.replace("www.", "") for url in urls]
        tabs = st.tabs(tab_names)
        
        for index, url in enumerate(urls):
            with tabs[index]:
                node_data = results[url]
                
                st.markdown(f"#### 🌐 Report Frame: `{url}`")
                
                if node_data.get("error"):
                    st.error(f"Execution Error: {node_data['error']}")
                else:
                    report = node_data["analysis_report"]
                    
                    pricing = format_to_clean_html_list(report['pricing_changes'])
                    messaging = format_to_clean_html_list(report['messaging_shift'])
                    features = format_to_clean_html_list(report['feature_additions'])
                    intent = format_to_clean_html_list(report['strategic_intent'])
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"""
                            <div class="metric-card" style="border-left-color: #EF4444;">
                                <div class="metric-title">💰 Pricing Changes</div>
                                <div class="metric-value">{pricing}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                            <div class="metric-card" style="border-left-color: #F59E0B;">
                                <div class="metric-title">🎯 Messaging Shift</div>
                                <div class="metric-value">{messaging}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"""
                            <div class="metric-card" style="border-left-color: #10B981;">
                                <div class="metric-title">🛠️ Feature Additions</div>
                                <div class="metric-value">{features}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                            <div class="metric-card" style="border-left-color: #3B82F6;">
                                <div class="metric-title">🔮 Strategic Intent</div>
                                <div class="metric-value">{intent}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    json_string = json.dumps(report, indent=4, ensure_ascii=False)
                    st.download_button(
                        label="📥 Download JSON Map",
                        data=json_string,
                        file_name=f"intel_{tab_names[index].replace('.', '_')}.json",
                        mime="application/json",
                        key=f"dl_{index}"
                    )
