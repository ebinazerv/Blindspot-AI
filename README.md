# 👁️ Blindspot AI - The Intelligent Business Validator

**Blindspot AI** is an Autonomous Agent system designed to cure "Founder's Bias."
Most entrepreneurs fall in love with their ideas and ignore risks. Blindspot AI acts as a **Strategic Partner**, using live market data to stress-test business ideas before you invest money.

## 🚀 Key Features
* **Multi-Agent Architecture:** Built using **LangGraph** to orchestrate specialized agents.
* **Live Market Data:** Uses **DuckDuckGo** to fetch real-time competitor analysis (2025 data).
* **Calculated Scoring Engine:** A custom algorithm that evaluates viability based on market saturation, urgency, and uniqueness.
* **Gemini 2.5 Flash:** Powered by Google's latest model for sub-second analysis.

## 🛠️ Tech Stack
* **Orchestration:** LangGraph
* **LLM:** Google Gemini 2.5 Flash
* **Search:** DuckDuckGo API
* **Frontend:** Streamlit (with Custom CSS)

## 🏗️ Architecture Flow
This system uses a **StateGraph** workflow to ensure data quality before analysis.

```mermaid
graph TD
    A[Start] -->|User Input| B(Researcher Agent)
    B -->|DuckDuckGo Search| C{Data Filter}
    C -->|Rejects Noise| B
    C -->|Relevant Data| D(Analyst Agent)
    D -->|Gemini 2.5 Flash| E[Risk Scoring Engine]
    E -->|HTML Report| F[End: UI Display]
    
    style B fill:#00d2ff,stroke:#333,stroke-width:2px,color:black
    style D fill:#ff9900,stroke:#333,stroke-width:2px,color:black
    style E fill:#28a745,stroke:#333,stroke-width:2px,color:black

## The "Why"

I didn't want to build a simple Chatbot. I wanted to build a **Decision Support System**. By using LangGraph, I created a cyclic workflow where data is verified before being analyzed, ensuring high-quality, grounded outputs.
