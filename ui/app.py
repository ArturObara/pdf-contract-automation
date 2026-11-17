import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
REQUEST_TIMEOUT = 120  # AI extraction and PDF rendering can take a while

FIELD_LABELS = {
    "old_contract_number": "Contract number",
    "name": "Name / Company",
    "pesel": "PESEL / NIP",
    "phone": "Phone",
    "email": "E-mail",
    "street": "Street",
    "postal_code": "Postal code",
    "city": "City",
}

st.set_page_config(page_title="VertEnergia - Dashboard")

st.session_state.setdefault("contract_number", "")
st.session_state.setdefault("generated_pdf", None)


def _show_validation_errors(detail) -> None:
    st.error("Some fields could not be read from the PDF or have an invalid format:")
    if isinstance(detail, list):
        for err in detail:
            field = (err.get("loc") or ["?"])[-1]
            st.markdown(f"- **{FIELD_LABELS.get(field, field)}**: {err.get('msg', 'invalid value')}")
    else:
        st.write(detail)


st.title("Upsell Contract Generator")
st.markdown(
    "Upload a legacy contract PDF to extract the client's data, "
    "then generate the new upsell contract in one click."
)

# --- Step 1: upload a legacy contract -------------------------------------
st.header("1. Upload legacy contract")
uploaded_file = st.file_uploader("Legacy contract (PDF)", type=["pdf"])

if st.button("Extract & save client data", disabled=uploaded_file is None):
    with st.spinner("Extracting client data from the PDF..."):
        try:
            response = requests.post(
                f"{API_URL}/contracts/upload",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                timeout=REQUEST_TIMEOUT,
            )
        except requests.exceptions.RequestException:
            st.error("Could not reach the API. Make sure the FastAPI server is running.")
        else:
            if response.status_code == 200:
                contract = response.json()
                st.session_state["contract_number"] = contract["old_contract_number"]
                st.session_state["generated_pdf"] = None
                st.success(f"Saved contract **{contract['old_contract_number']}**.")
                st.table(
                    {FIELD_LABELS[k]: [contract.get(k) or "-"] for k in FIELD_LABELS}
                )
            elif response.status_code == 409:
                st.warning(
                    "This contract is already in the database. "
                    "Enter its number below to generate the upsell contract."
                )
            elif response.status_code == 422:
                _show_validation_errors(response.json().get("detail"))
            elif response.status_code == 400:
                st.error(response.json().get("detail", "Invalid file."))
            else:
                st.error(f"Server error occurred (Code: {response.status_code})")

# --- Step 2: generate the upsell contract ---------------------------------
st.header("2. Generate upsell contract")
contract_number = st.text_input(
    "Old contract number:",
    key="contract_number",
    placeholder="e.g., VERT/2025/123",
    help="Filled in automatically after a successful upload.",
)

if st.button("Generate PDF Contract", type="primary"):
    if not contract_number:
        st.warning("Please enter a contract number before generating the document.")
    else:
        with st.spinner("Fetching data from the database and rendering PDF..."):
            try:
                response = requests.post(
                    f"{API_URL}/contracts/generate-upsell",
                    json={"old_contract_number": contract_number},
                    timeout=REQUEST_TIMEOUT,
                )
            except requests.exceptions.RequestException:
                st.error("Could not reach the API. Make sure the FastAPI server is running.")
            else:
                if response.status_code == 200:
                    st.session_state["generated_pdf"] = (contract_number, response.content)
                elif response.status_code == 404:
                    st.session_state["generated_pdf"] = None
                    st.error("Contract with the given number was not found in the database.")
                else:
                    st.session_state["generated_pdf"] = None
                    st.error(f"Server error occurred (Code: {response.status_code})")

if st.session_state["generated_pdf"]:
    number, pdf_bytes = st.session_state["generated_pdf"]
    st.success(f"Upsell contract for **{number}** is ready.")
    st.download_button(
        label="📥 Download generated PDF",
        data=pdf_bytes,
        file_name=f"Upsell_Contract_{number.replace('/', '_')}.pdf",
        mime="application/pdf",
    )
