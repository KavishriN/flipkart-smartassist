import streamlit as st
from google import genai
import json
import os
import ast
from dotenv import load_dotenv

# This automatically loads your secret key from the .env file safely!
load_dotenv()



def query_catalog_pipeline(user_query, max_price=None):
    try:
        with open('dummy_catalog.json', 'r') as f:
            catalog = json.load(f)
    except FileNotFoundError:
        return []
    
    results = []
    query_lower = user_query.lower()
    
    for product in catalog:
        match_tag = any(tag in query_lower for tag in product['tags'].split(', '))
        match_name = any(word in product['name'].lower() for word in query_lower.split())
        
        if match_tag or match_name:
            if max_price and product['price'] > max_price:
                continue
            results.append(product)
            
    return results if results else catalog

# Initialize the correct native stable client
client = genai.Client()

st.set_page_config(page_title="Flipkart SmartAssist Engine", page_icon="🛒", layout="wide")

st.title("🛒 Flipkart SmartAssist Engine")
st.markdown("### *Next-Gen Tanglish Vernacular Search Pipeline | Flipkart GRiD Prototype*")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    user_query = st.text_input(
        "Ethavathu thedureengala bro? (Try: 'Enaku nalla watch venum' or 'kurti under 1000')",
        placeholder="Type your query in Tanglish, Tamil, or English..."
    )
    max_price = st.slider("Set Your Budget Filter (INR)", 500, 5000, 5000)

    if st.button("Run Search Pipeline", type="primary"):
        if user_query:
            with st.spinner("Processing data engine pipeline..."):
                filtered_data = query_catalog_pipeline(user_query, max_price)
                
                # Format your system instructions and prompt manually for the native SDK
                prompt = f"""
                You are 'Flipkart SmartAssist', an advanced conversational commerce agent built for South Indian regional markets.
                
                Task: 
                1. Acknowledge what the user wants. They will be speaking in English, Tamil, or Tanglish (Tamil written in English script).
                2. Present the matching products from the pipeline results beautifully with prices.
                3. Respond in a friendly, conversational mix of English and Tanglish (e.g., use terms like 'Bro', 'Unga budget-ku yetha mardhiri', 'Semmaya irukum').
                4. Keep the tone warm, helpful, and distinctly localized. Do not use Hindi.

                User Query: "{user_query}"
                Pipeline Results: {json.dumps(filtered_data)}
                """

                # Call the model natively using the standard stable model ID
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )

                # Extract and format the text content cleanly
                try:
                    # Try parsing if it returns the structured string layout
                    parsed_data = ast.literal_eval(response.text)
                    clean_text = parsed_data[0]["text"]

                    with st.container(border=True):
                        st.subheader("🤖 SmartAssist Agent:")
                        st.markdown(clean_text)

                except Exception:
                    # Direct text fallback wrapper
                    with st.container(border=True):
                        st.subheader("🤖 SmartAssist Agent:")
                        st.markdown(response.text)
        else:
            st.warning("Please type a search query first, bro!")

with col2:
    st.info("💡 **Project Architecture Overview**")
    st.markdown("""
    * **Vernacular NLP Ingestion:** Successfully handles mixed-script Tanglish strings.
    * **Rule-Based Pre-Filtering:** Custom Python functions screen budget barriers before hitting the LLM model to save API context costs.
    * **Context Generation:** Natively organizes payload injections seamlessly for fluid local language generation.
    """)
    
    with st.expander("View Active Inventory Catalog"):
        try:
            with open('dummy_catalog.json', 'r') as f:
                st.json(json.load(f))
        except FileNotFoundError:
            st.error("dummy_catalog.json file not found in directory.")