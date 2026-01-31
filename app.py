import streamlit as st
import asyncio
import sys
import nest_asyncio
import re
# 1. FIX FOR WINDOWS: This must come before any async calls
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# 2. ALLOW NESTED LOOPS: Required for Streamlit + Async
nest_asyncio.apply()

from eco_scraper import crawl_and_analyze 
from eco_scraper import model  # Import the model from eco_scraper

# Streamlit Page Config
st.set_page_config(page_title="Eco-Agent: Water Saving Assistant", page_icon="💧")

st.title("💧 Eco-Agent Water Saving Dashboard")
st.markdown("Smart research agent powered by watsonx.ai and Crawl4AI.")

if 'total_water' not in st.session_state:
    st.session_state.total_water = 0

with st.sidebar:
    st.header("Savings Statistics")
    st.metric("Total Water Saved", f"{st.session_state.total_water} Liters")
    st.info("Each successful analysis promotes 10 liters of water saving awareness!")

# main page
query = st.text_input("What topic would you like to research for water saving?", placeholder="e.g. Drip irrigation systems")

if st.button("Start Analysis"):
    if query:
        with st.spinner(f"Eco-Agent is researching '{query}'..."):
            try:
                # STEP 1: Ask watsonx.ai for the best 2 URLs
                # We use the 'model' object imported from eco_scraper or defined here
                selection_prompt = f"Identify the 2 most relevant and official website URLs for researching the topic: '{query}'. Return only the URLs separated by a comma."
                
                # Note: Ensure 'model' is accessible here
                urls_raw = model.generate_text(prompt=selection_prompt)
                url_list = re.findall(r'(https?://[^\s,]+)', urls_raw)

                combined_results = ""
                
                # STEP 2: Crawl and Analyze each URL
                for target_url in url_list:
                    st.write(f"🔍 Analyzing: {target_url}")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    # Using your fixed async execution method
                    result = asyncio.run(crawl_and_analyze(target_url))
                    
                    combined_results += f"\n\n--- Source: {target_url} ---\n" + result

                # Display Results
                st.success("Analysis Completed!")
                st.markdown("### 📋 Recommendations")
                st.markdown(combined_results)
                
                # Update Water Counter (10L per site)
                st.session_state.total_water += (len(url_list) * 10)
                st.balloons()
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
    else:
        st.warning("Please enter a topic to start.")