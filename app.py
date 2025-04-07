import streamlit as st
import requests
import pandas as pd

# Flask API URL
API_URL = "https://shl-backend-1-f20y.onrender.com/recommend"

st.title("SHL Assessment Recommendation System")
query = st.text_area("Enter your query:", "e.g., I need English proficiency.")
max_duration = st.number_input("Max Duration (minutes)", min_value=0, value=0, step=5)

if st.button("Recommend Assessments"):
    if query:
        params = {"query": query}
        if max_duration > 0:
            params["max_duration"] = max_duration
        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            results = response.json()
            if results:
                df = pd.DataFrame(results)
                st.write("### Recommended Assessments")
                st.table(df.style.format({"url": lambda x: f'<a href="{x}" target="_blank">{x}</a>'}, na_rep="N/A"))
            else:
                st.warning("No recommendations found.")
        except requests.RequestException as e:
            st.error(f"API Error: {e}")
    else:
        st.error("Please enter a query.")

if st.checkbox("Show API Response"):
    params = {"query": query}
    if max_duration > 0:
        params["max_duration"] = max_duration
    response = requests.get(API_URL, params=params)
    st.json(response.json() if response.ok else {"error": "API call failed"})