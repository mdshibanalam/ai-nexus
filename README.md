# 🤖 AI Nexus - The Ultimate AI Search Engine

**AI Nexus** is a modern, semantic search engine and curated SaaS directory designed to help developers, creators, and engineers discover the exact AI tools and workflows they need. 

Unlike traditional keyword-matching directories, AI Nexus is powered by **Google Gemini 2.5 Flash**, allowing users to search using conversational problem statements and intents (e.g., *"How do I edit videos for free?"* or *"I need to scrape a website"*).

---

## 🏗️ Architecture Flow

When a user submits a natural language query, the request flows through a decoupled intelligence and data-filtering pipeline:

```text
[ User Query / Problem Intent ]
              │
              ▼
    [ Streamlit Web UI ]
              │
              ▼
   [ Gemini 2.5 Flash LLM ]  ──> (Intent Matching & Schema Alignment)──┐
              │                                                        │
              ▼                                                        ▼
     [ Pandas DataFrame ]  <── (Primary Key Database Filtering)────────┘
              │
              ▼
   [ Rendered UI Tool Cards ]

```

1. **Query Ingestion:** The user inputs a natural language task into the Streamlit frontend.
2. **Semantic Processing:** The query and schema context are dispatched to `gemini-2.5-flash`.
3. **Data Filtering:** The LLM returns structured identifiers matching primary keys in the local database, which Pandas filters instantly.
4. **UI Rendering:** Clean SaaS cards render dynamically with power prompts, workflows, and tutorials.

---

## 🧠 Prompt Engineering & Schema Alignment

A core technical challenge in building LLM-backed search engines is preventing hallucinated tool recommendations. **AI Nexus** solves this through strict **System Prompt Guardrails & Schema Alignment**:

* **Context Injection:** The database's primary keys (`Tool Name`), descriptions, and categories are dynamically compiled into the LLM system prompt on execution.
* **Deterministic Output Formatting:** The LLM is strictly constrained via system instructions to return either a conversational flag (`CHAT: <response>`) for general inquiries, or a clean, comma-separated structured list of primary keys that exist within the database schema.
* **Zero-Hallucination Filtering:** Because the LLM outputs exact database keys rather than arbitrary text, Pandas safely intersects the LLM response against the CSV schema without throwing key errors or surfacing fake URLs.

---

## ✨ Key Features

* 🧠 **Semantic Intent Search:** Powered by Google's `gemini-2.5-flash` LLM to understand natural language problem statements and intelligently route queries to the right tools.
* ⚡ **SaaS Submission Workflow:** Allows AI developers and tool creators to submit their apps for platform verification and listing directly through the UI.
* 🛡️ **Graceful Fallback Engineering:** Automatically detects API capacity limits or authentication failures, seamlessly degrading to a manual browsing mode without breaking the user experience.
* 🗂️ **Dynamic Filter & Sort Engine:** Browse 40+ curated AI tools categorized by use-case (*Agents, Audio, Coding, Video, etc.*) and simplified pricing models (*Free, Freemium, Paid*).
* 🚀 **Power Features & Workflows:** Each verified tool card reveals custom **Magic Prompt Templates**, **Integration Workflows**, and curated **Video Tutorials**.
* 🎨 **Hacker-Sane Dark UI:** Engineered with custom Streamlit theming and CSS injections for a clean, modern SaaS interface.

---

## 📂 Project Organization Structure

```text
ai-nexus/
│
├── .streamlit/
│   ├── config.toml       
│   └── secrets.toml     
├── app.py               
├── tools.csv            
├── audit.py            
├── requirements.txt     
└── README.md           
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mdshibanalam/ai-nexus.git
cd ai-nexus
```

### 2. Install Dependencies

Ensure you have Python 3.10+ installed. Run the following command to install required libraries:

```bash
pip install -r requirements.txt
```

### 3. Configure the AI Engine (API Key)

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. Create a folder named `.streamlit` in the project root.
3. Create a file inside named `secrets.toml` and paste your key:
```toml
GEMINI_API_KEY = "AIzaSyYourActualAPIKeyHere..."
```



### 4. Launch the App

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501` to use **AI Nexus**.

---

## 🗺️ Future Roadmap

* **Database Migration:** Upgrade persistence from local `.csv` storage to a scalable **SQLite / PostgreSQL** database (or Supabase) to support real-time, persistent SaaS tool submissions.
* **Community & Authentication:** Implement user authentication (OAuth), verified developer badges, and a community upvoting/bookmarking system.
* **Automated Maintenance:** Integrate automated daily URL health checking via **GitHub Actions** (extending our local `audit.py` QA script to run continuously in CI/CD).

---

## 🛠️ Built With

* **Frontend & Backend:** [Streamlit](https://streamlit.io/) (Python)
* **Intelligence Engine:** [Google Gemini API](https://ai.google.dev/) (`google-genai` SDK)
* **Data Processing:** [Pandas](https://pandas.pydata.org/)