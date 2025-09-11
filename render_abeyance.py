import streamlit as st
import datetime
import holidays
import tempfile
import os
from io import BytesIO
from PyPDF2 import PdfMerger
from util import wrap_text_to_width, draw_wrapped_section, generate_pdf, convert_to_pdf, calculate_fbd, create_cover_sheet

def render_abey():
    # --- Date and FBD input/display together ---
    if "date_received" not in st.session_state:
        st.session_state["date_received"] = datetime.date.today()

    st.header("Executive Order Abeyance Tracker")
    date_col, fbd_col = st.columns([1, 1])
    with date_col:
        date_received = st.date_input(
            "Date Received",
            value=st.session_state["date_received"],
            key="date_received",
            help="Date the appraisal was given to grievant."
        )
    with fbd_col:
        fbd = calculate_fbd(st.session_state["date_received"])
        st.info(f"🗕️ File By Date (15 business days): {fbd}")

    with st.form("grievance_form"):
        steward = st.text_input("Steward’s Name", key="Steward")
        grievant = st.text_input("Grievant’s Name", key="Grievant")
        case_id = st.text_input("Case Number")
        workarea = st.text_input("Work Area/ Operation")
        dept_man = st.text_input("Department Manager")
        flmanager = st.text_input("Frontline Manager")
        position = st.text_input("Title/Position")
        issue_description = st.text_area("Summary of Grievance", key="issue_description")
        desired_outcome = st.text_area("Requested Resolution", key="desired_outcome")

        uploaded_files = []
        MAX_UPLOADS = 10
        for i in range(MAX_UPLOADS):
            uploaded_files.append(
                st.file_uploader(
                    f"Supporting Document {i+1}",
                    type=["pdf", "docx", "txt", "jpg", "jpeg", "png"],
                    key=f"file_uploader_{i}",
                )
            )

        selected_reasons = []
        selected_articles = set()
        selected_arguments = []

        st.subheader("Alleged Violations")
        for desc, info in annual_checkboxes.items():
            checked = st.checkbox(desc, key=f"checkbox_{desc}")
            if checked:
                selected_articles.update(info["articles"])
                selected_reasons.append(desc)
                selected_arguments.append(info["argument"])
    
        # Show additional checkboxes based on Measured/Unmeasured selection
        if meas_identify == "Measured":
            st.markdown("**Additional Measured Issues:**")
            for desc, info in measured_checkboxes.items():
                checked = st.checkbox(desc, key=f"measured_{desc}")
                if checked:
                    selected_articles.update(info["articles"])
                    selected_reasons.append(desc)
                    selected_arguments.append(info["argument"])
        elif meas_identify == "Unmeasured":
            st.markdown("**Additional Unmeasured Issues:**")
            for desc, info in unmeasured_checkboxes.items():
                checked = st.checkbox(desc, key=f"unmeasured_{desc}")
                if checked:
                    selected_articles.update(info["articles"])
                    selected_reasons.append(desc)
                    selected_arguments.append(info["argument"])

        submitted = st.form_submit_button("Generate Grievance PDF")
