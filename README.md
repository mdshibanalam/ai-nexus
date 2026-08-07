# 🤖 AI Nexus - The Ultimate AI Search Engine & Directory

**AI Nexus** is a modern, semantic search engine and curated SaaS directory designed to help developers, creators, and engineers discover the exact AI tools and workflows they need. 

Unlike traditional keyword-matching directories, AI Nexus is powered by **Google Gemini 2.5 Flash**, allowing users to search using conversational problem statements and intents (e.g., *"How do I edit videos for free?"* or *"I need to scrape a website"*).

---

## ✨ Key Features

* 🧠 **Semantic Intent Search:** Powered by Google's `gemini-2.5-flash` LLM to understand natural language problem statements and intelligently route queries to the right tools.
* ⚡ **SaaS Submission Workflow:** Allows AI developers and tool creators to submit their apps for platform verification and listing directly through the UI.
* 🛡️ **Graceful Fallback Engineering:** Automatically detects API capacity limits or authentication failures, seamlessly degrading to a manual browsing mode without breaking the user experience.
* 🗂️ **Dynamic Filter & Sort Engine:** Browse 40+ curated AI tools categorized by use-case (*Agents, Audio, Coding, Video, etc.*) and simplified pricing models (*Free, Freemium, Paid*).
* 🚀 **Power Features & Workflows:** Each verified tool card reveals custom **Magic Prompt Templates**, **Integration Workflows**, and curated **Video Tutorials**.
* 🎨 **Hacker-Sane Dark UI:** Engineered with custom Streamlit theming and CSS injections for a clean, modern SaaS interface.

---

## 🏗️ Project Organization Structure

```text
AI_Project/
│
├── .streamlit/
│   ├── config.toml         # UI Dark-mode theme & layout styling settings
│   └── secrets.toml        # Local environment variables 
│
├── app.py                  # Main application dashboard & Gemini AI routing engine
├── tools.csv               # Read/Write database containing curated AI tool cards
├── audit.py                # QA script to programmatically check for broken URLs
├── requirements.txt        # Python package dependencies for deployment
└── README.md               # Project documentation & setup instructions
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

## 🛠️ Built With

* **Frontend & Backend:** [Streamlit](https://streamlit.io/) (Python)
* **Intelligence Engine:** [Google Gemini API](https://ai.google.dev/) (`google-genai` SDK)
* **Data Processing:** [Pandas](https://pandas.pydata.org/)