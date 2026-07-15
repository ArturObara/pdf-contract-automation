import streamlit as st
import requests
import os

st.set_page_config(page_title="VertEnergia - Dashboard")

st.title("Upsell Contract Generator")
st.markdown("Enter the base contract number from the system to automatically generate and download the new PDF document.")

contract_number = st.text_input("Old contract number:", placeholder="e.g., VERT/2025/123")

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

if st.button("Generate PDF Contract", type="primary"):
    if not contract_number:
        st.warning("Please enter a contract number before generating the document.")
    else:
        with st.spinner("Fetching data from the database and rendering PDF..."):
            try:
                response = requests.post(
                    f"{API_URL}/contracts/generate-upsell",
                    json={"old_contract_number": contract_number}
                )
                
                if response.status_code == 200:
                    st.success("Success! The document has been generated successfully.")
                    
                    safe_name = contract_number.replace('/', '_')
                    
                    st.download_button(
                        label="📥 Download generated PDF",
                        data=response.content,
                        file_name=f"Upsell_Contract_{safe_name}.pdf",
                        mime="application/pdf"
                    )
                elif response.status_code == 404:
                    st.error("Contract with the given number was not found in the database.")
                else:
                    st.error(f"Server error occurred (Code: {response.status_code})")
                    
            except requests.exceptions.ConnectionError:
                st.error("Connection error. Make sure your FastAPI server (Uvicorn) is running!")