import streamlit as st
import os
import google.generativeai as genai
# Ensure you have: pip install duckduckgo-search==6.1.8
from langchain_community.tools import DuckDuckGoSearchResults
from typing import TypedDict
from langgraph.graph import StateGraph, END

# --- CONFIGURATION ---
if "GOOGLE_API_KEY" not in os.environ:
    # PASTE YOUR KEY HERE
    os.environ["GOOGLE_API_KEY"] = "......................"
 
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- UI SETUP ---
st.set_page_config(page_title="Blindspot AI", layout="wide", page_icon="👁️")

st.markdown("""
<style>
    /* Main Background */
    .stApp { background: linear-gradient(to right, #141E30, #243B55); color: #ffffff; }
    
    /* Text Input */
    .stTextArea textarea { background-color: #f0f2f6 !important; color: #000000 !important; border: 2px solid #00d2ff !important; border-radius: 10px; }
    
    /* CARD STYLING */
    .result-card { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #333333; margin-bottom: 20px; height: 100%; }
    
    /* Border Accents */
    .card-left { border-top: 5px solid #00d2ff; }
    .card-right { border-top: 5px solid #ff9900; } 

    /* Typography */
    .result-card h2 { color: #1f2937 !important; font-size: 1.5rem; border-bottom: 1px solid #eee; padding-bottom: 10px; }
    .result-card h3 { color: #374151 !important; font-size: 1.2rem; margin-top: 15px; }
    .result-card p, .result-card li { color: #4b5563 !important; font-size: 1rem; line-height: 1.6; }
    
    /* Score Box */
    .score-box { font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 10px; }

    /* Links */
    .result-card a { color: #0066cc !important; text-decoration: none; font-weight: bold; background-color: #e6f2ff; padding: 2px 6px; border-radius: 4px; }
    .result-card a:hover { background-color: #0066cc; color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    idea: str
    market_data: str 
    critique: str

# --- NODE 1: RESEARCHER ---
def researcher_node(state: AgentState):
    idea = state['idea']
    try:
        search = DuckDuckGoSearchResults(num_results=5)
        query = f"market demand for {idea} competitors failure risks 2025"
        try:
             raw_results = search.invoke(query)
        except:
             raw_results = search.run(query)

        model = genai.GenerativeModel('gemini-2.5-flash')
        
        cleaning_prompt = f"""
        You are a Web Researcher. Raw Results: {raw_results}
        Task: List 3 Relevant Sources for "{idea}".
        Format: HTML List `<ul><li><a href='URL' target='_blank'>TITLE</a> - Summary</li></ul>`.
        If no links, return: `<p>No direct links found. Analysis based on logic.</p>`
        """
        response = model.generate_content(cleaning_prompt)
        clean_data = response.text.replace("```html", "").replace("```", "")
    except Exception as e:
        clean_data = f"<p>⚠️ Search connection error: {str(e)}</p>"
    return {"market_data": clean_data}

# --- NODE 2: THE ANALYST (CALIBRATED RUBRIC) ---
def analyst_node(state: AgentState):
    model = genai.GenerativeModel('gemini-2.5-flash')
    

    prompt = f"""
    You are a Strategic Business Consultant. 
    User Idea: {state['idea']}
    Market Evidence: {state['market_data']}
    
    TASK: Calculate a Viability Score and write a report.
    
    SCORING RUBRIC (Base = 65/100):
    - **Base Score:** Start at 65. (This is a "Passing" grade).
    - **Bonuses:**
      - +15 if it solves an URGENT problem (Health, Money, Time).
      - +10 if it is UNIQUE or Innovative.
      - +5 if the market is Growing.
    - **Penalties:**
      - -10 if the market is Very Crowded/Saturated.
      - -20 if it is Vague or physically Impossible.
      - -10 if Legal risks are high.
    
    **Examples:**
    - A standard Coffee Shop = 65 (Base) - 10 (Crowded) + 15 (Urgent need for coffee) = ~70% (Solid).
    - A cure for Cancer = 65 + 15 + 10 = 90% (Excellent).
    - A DVD Store = 65 - 20 (Obsolete) = 45% (Risk).
    
    OUTPUT FORMAT (HTML):
    1. <div class="score-box" style="color: [IF SCORE > 75 THEN #28a745 ELSE IF SCORE > 55 THEN #ff9900 ELSE #dc3545]">Viability: [Score]%</div>
    
    2. <h3>📊 Market Reality</h3>
       <p>[Is this a Blue Ocean (new) or Red Ocean (crowded)? Be honest.]</p>
       
    3. <h3>⚠️ The Blindspots (Why it might fail)</h3>
       <ul>
         <li>[Risk 1]</li>
         <li>[Risk 2]</li>
       </ul>
       
    4. <h3>💡 The Pivot (How to fix it)</h3>
       <p>[One specific suggestion to improve the score]</p>
    """
    
    response = model.generate_content(prompt)
    critique_html = response.text.replace("```html", "").replace("```", "")
    return {"critique": critique_html}

# --- BUILD GRAPH ---
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", END)
app = workflow.compile()

# --- MAIN APP ---
st.title("👁️ Blindspot AI")
st.markdown("### *Find the flaw before the market does.*")

user_input = st.text_area(f":orange[Pitch your startup idea:]", height=100)

if st.button("Run Viability Check 🚀", type="primary"):
    if not user_input:
        st.warning("Please enter an idea.")
    else:
        with st.spinner("⚖️ Weighing the risks and rewards..."):
            result = app.invoke({"idea": user_input})
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"""<div class="result-card card-left"><h2>🔗 Evidence</h2>{result['market_data']}</div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class="result-card card-right"><h2>📋 Strategic Analysis</h2>{result['critique']}</div>""", unsafe_allow_html=True)