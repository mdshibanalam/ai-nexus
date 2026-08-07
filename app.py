import streamlit as st
import pandas as pd
import time
import re

# === PAGE CONFIG & CSS INJECTIONS ===
st.set_page_config(page_title="AI Nexus", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# CSS Hack to permanently hide the overlapping "Press Enter to submit" tooltips
st.markdown("""
    <style>
    div[data-testid="InputInstructions"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# === DATA ENGINE ===
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("tools.csv")
        # Clean up empty Pandas fields to prevent "nan" from appearing
        df = df.fillna("N/A")
        
        def simplify_pricing(p):
            p = str(p).lower()
            if 'freemium' in p: return 'Freemium'
            if 'free' in p: return 'Free'
            if 'trial' in p or 'usage' in p or 'add-on' in p: return 'Paid (Usage/Enterprise)'
            return 'Paid (Standard)'
            
        df['Pricing Model'] = df['Pricing Model'].apply(simplify_pricing)
        return df
    except FileNotFoundError:
        st.error("File 'tools.csv' not found.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # === SIDEBAR: System Status ===
    if "system_key_failed" not in st.session_state:
        st.session_state.system_key_failed = False

    api_key = ""
    try:
        secret_key = st.secrets["GEMINI_API_KEY"]
        if not st.session_state.system_key_failed:
             api_key = secret_key
             st.sidebar.success("🌐 AI Nexus Status: Online")
        else:
             raise ValueError("System key failed.")
    except Exception:
        st.session_state.system_key_failed = True

    if st.session_state.system_key_failed:
        st.sidebar.warning("⚠️ AI Engine unavailable. Enter your own key below.")
        api_key = st.sidebar.text_input("🔑 Gemini API Key", type="password")

    st.sidebar.markdown("---")
    
    # === SIDEBAR: Manual Search ===
    st.sidebar.header("🔍 Manual Search")
    
    existing_cats = sorted([c for c in df['Category'].unique() if c != 'N/A'])
    categories = ["All"] + existing_cats
    selected_category = st.sidebar.selectbox("Category", categories)

    pricing_options = ["All", "Free", "Freemium", "Paid (Standard)", "Paid (Usage/Enterprise)"]
    selected_pricing = st.sidebar.selectbox("Pricing", pricing_options)

    st.sidebar.markdown("---")

    # === SIDEBAR: SaaS Submission Form ===
    with st.sidebar.expander("➕ Submit an AI Tool", expanded=False):
        with st.form("add_tool_form", clear_on_submit=True):
            st.caption("Apply to list a tool on AI Nexus.")
            
            # Core Tool Data (Strict Limits Applied)
            new_name = st.text_input("Tool Name* (Max 20 letters)", max_chars=20, placeholder="E.g., ChatGPT")
            
            cat_options = existing_cats + ["Other (Type Below)"]
            new_cat_selection = st.selectbox("Category*", cat_options)
            custom_category = st.text_input("Custom Category (Max 20 letters)", max_chars=20, placeholder="E.g., 3D Generation")
            
            new_pricing = st.selectbox("Pricing*", ["Free", "Freemium", "Paid (Standard)", "Paid (Usage/Enterprise)"])
            new_link = st.text_input("Website URL*", placeholder="E.g., google.com")
            
            new_desc = st.text_area("Short Description* (Maximum 80 letters)", max_chars=80, placeholder="What does this tool do?")
            
            # Developer Verification Data (Mandatory for SaaS Model)
            st.markdown("**Developer Verification**")
            new_contributor = st.text_input("Your Name/Handle* (Max 20 letters)", max_chars=20, placeholder="E.g., @Shiban")
            new_email = st.text_input("Support/Contact Email*", placeholder="For verification purposes")
            
            # Optional Power Features
            with st.expander("Optional Resources"):
                new_prompt = st.text_area("Magic Prompt (Max 100 letters)", max_chars=100)
                new_workflow = st.text_area("Integration Workflow (Max 100 letters)", max_chars=100)
                new_hindi = st.text_input("Hindi Tutorial URL")
                new_english = st.text_input("English Tutorial URL")
                
            if st.form_submit_button("📤 Submit for Review"):
                final_category = custom_category.strip() if new_cat_selection == "Other (Type Below)" else new_cat_selection
                
                if new_name and final_category and new_link and new_desc and new_contributor and new_email:
                    if not new_link.startswith("http://") and not new_link.startswith("https://"):
                        new_link = "https://" + new_link

                    new_row = {
                        "Category": final_category, "Pricing Model": new_pricing, "Tool Name": new_name,
                        "Direct Link": new_link, "What it does?": new_desc,
                        "Magic Prompt Template": new_prompt if new_prompt else "N/A",
                        "Integration/Workflow": new_workflow if new_workflow else "N/A",
                        "Best Hindi Resource Title": "Community Tutorial" if new_hindi else "N/A", 
                        "Best Hindi Resource Link": new_hindi if new_hindi else "N/A",
                        "Best English Resource Title": "Community Tutorial" if new_english else "N/A", 
                        "Best English Resource Link": new_english if new_english else "N/A",
                        "Contributor": new_contributor,
                        "Contact Email": new_email # Note: We store it, but don't display it to the public!
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df.to_csv("tools.csv", index=False)
                    load_data.clear()
                    
                    st.success(f"✅ {new_name} submitted successfully! Our team will review it shortly.")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Please fill all required fields (*), including Verification.")

    # === MAIN PAGE ===
    st.title("🤖 AI Nexus")
    st.markdown("### The Ultimate AI Search Engine")
    
    search_query = st.text_input("🧠 Ask AI Nexus", placeholder="E.g., 'Free video editor', 'Scrape website data', or 'Coding assistant'")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        sort_by = st.selectbox("Sort Results", ["Newest Added", "Alphabetical (A-Z)"])
    
    st.markdown("---")

    filtered_df = df.copy()

    # === AI ROUTING ENGINE ===
    if search_query:
        if api_key:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                tools_context = "\n".join([f"- {row['Tool Name']}: {row['What it does?']} ({row['Category']})" for _, row in df.iterrows()])
                
                # Upgraded Semantic Prompt to understand intent better
                prompt = f"""
                You are AI Nexus, a highly intelligent semantic search engine.
                Database: {tools_context}
                User intent: "{search_query}"
                
                Rule 1: If the user asks a conversational question (e.g., "What is an LLM?"), reply playfully starting with "CHAT: "
                Rule 2: If the user needs a tool, strictly analyze their INTENT. Match vague concepts (like "make a song") to actual categories (like "Audio").
                Rule 3: Return ONLY a comma-separated list of the relevant 'Tool Name's. If absolutely nothing relates, return NONE.
                """
                
                with st.spinner("🤖 Analyzing your request through the AI Engine..."):
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                    result_text = response.text.strip()
                
                if result_text.startswith("CHAT:"):
                    st.info(f"✨ **AI Nexus says:** {result_text.replace('CHAT:', '').strip()}")
                    st.caption("*Showing your manually filtered tools below...*")
                    if selected_category != "All": filtered_df = filtered_df[filtered_df['Category'] == selected_category]
                    if selected_pricing != "All": filtered_df = filtered_df[filtered_df['Pricing Model'] == selected_pricing]
                else:
                    ai_recs = [t.strip() for t in result_text.split(',')]
                    if 'NONE' not in ai_recs and ai_recs:
                        filtered_df = filtered_df[filtered_df['Tool Name'].isin(ai_recs)]
                        st.success("🎯 Tailored recommendations found!")
                    else:
                        st.warning("No specific tools found for that exact prompt. Try rephrasing.")
                        filtered_df = filtered_df.iloc[0:0]
            except Exception as e:
                if "400" in str(e) or "API_KEY" in str(e):
                    st.session_state.system_key_failed = True
                    st.rerun()
                else:
                    st.error(f"Engine Error: {str(e)}")
                    filtered_df = filtered_df.iloc[0:0]
        else:
            st.error("⚠️ Enter an API key in the sidebar.")
            filtered_df = filtered_df.iloc[0:0] 
    else:
        if selected_category != "All": filtered_df = filtered_df[filtered_df['Category'] == selected_category]
        if selected_pricing != "All": filtered_df = filtered_df[filtered_df['Pricing Model'] == selected_pricing]

    # === APPLY SORTING ===
    if sort_by == "Newest Added":
        filtered_df = filtered_df.iloc[::-1] 
    else:
        filtered_df = filtered_df.sort_values(by="Tool Name")

    st.markdown(f"**Showing {len(filtered_df)} tools**")

    # === DYNAMIC DISPLAY CARDS ===
    cols = st.columns(2)
    for index, (i, row) in enumerate(filtered_df.iterrows()):
        col = cols[index % 2]
        with col:
            with st.container(border=True):
                st.subheader(f"🛠️ {row['Tool Name']}")
                st.caption(f"**{row['Category']}** | {row['Pricing Model']}")
                st.write(f"**What it does:** {row['What it does?']}")
                st.link_button("🔗 Visit Website", row['Direct Link'])
                
                # Dynamic rendering: Only show contributor if it exists
                contributor = str(row.get('Contributor', 'N/A'))
                if contributor not in ['N/A', 'nan', '']:
                    st.caption(f"Verified Contributor: {contributor}")
                
                # Check if ANY power features exist before showing the expander
                magic = str(row.get('Magic Prompt Template', 'N/A'))
                workflow = str(row.get('Integration/Workflow', 'N/A'))
                hindi_url = str(row.get('Best Hindi Resource Link', 'N/A'))
                eng_url = str(row.get('Best English Resource Link', 'N/A'))
                
                has_magic = magic not in ['N/A', 'nan', '']
                has_workflow = workflow not in ['N/A', 'nan', '']
                has_hindi = hindi_url not in ['N/A', 'nan', '']
                has_eng = eng_url not in ['N/A', 'nan', '']
                
                if has_magic or has_workflow or has_hindi or has_eng:
                    with st.expander("🚀 Power Features & Resources"):
                        if has_magic:
                            st.markdown("**✨ Magic Prompt:**")
                            st.code(magic, language="text")
                        if has_workflow:
                            st.markdown("**⚡ Workflow:**")
                            st.info(workflow)
                            
                        if has_hindi or has_eng:
                            st.markdown("---")
                            st.markdown("**📚 Resources:**")
                            if has_hindi:
                                st.markdown(f"🎥 [**Hindi Tutorial**]({hindi_url})")
                            if has_eng:
                                st.markdown(f"🎥 [**English Tutorial**]({eng_url})")