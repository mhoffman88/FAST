import streamlit as st
import datetime
import holidays
import tempfile
import os
from io import BytesIO
from PyPDF2 import PdfMerger
from util import wrap_text_to_width, draw_wrapped_section, generate_pdf, convert_to_pdf, calculate_fbd, create_cover_sheet
from meas_unmeas_arguments import measured_checkboxes, unmeasured_checkboxes
from annual_arguments import annual_checkboxes

def render_annual():
    # --- Date and FBD input/display together ---
    if "date_received" not in st.session_state:
        st.session_state["date_received"] = datetime.date.today()

    st.header("Appraisal Grievance Intake")
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

    meas_identify = st.selectbox("Measured or Unmeasured?", options=["Measured","Unmeasured"], key="meas_status")

    # --- FORM UI ---
    with st.form("grievance_form"):
        steward = st.text_input("Steward’s Name", key="Steward")
        grievant = st.text_input("Grievant’s Name", key="Grievant")
        years_list = [str(y) for y in range(2023, datetime.date.today().year + 2)]
        appraisal_year = st.selectbox("Appraisal Year", years_list, index=len(years_list)-1, key="appraisal_year")
        ratings = [f"{x:.1f}" for x in [i * 0.1 for i in range(10, 51)]]
        col1, col2 = st.columns(2)
        with col1:
            rating_received = st.selectbox("Current Rating", ratings, index=0, key="rating_received")
        with col2:
            previous_rating = st.selectbox("Prior Year’s Rating", ratings, index=0, key="previous_rating")

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

    # --- PDF Generation / Download ---
    if submitted:
        article_list = ", ".join(sorted(set(selected_articles)))
        full_argument = ""
        if selected_arguments:
            full_argument = "\nThis grievance challenges the annual performance appraisal based on the following concerns:\n\n\n"
            for a in selected_arguments:
                full_argument += f"{a}\n\n"

        filing_step = "Step Two - Streamlined Grievance"
        
        # All fields for the cover sheet (in order)
        form_data = {
            "Step": filing_step,
            "Grievant": grievant,
            "Appraisal Year": appraisal_year,
            "Current Rating": rating_received,
            "Prior Year’s Rating": previous_rating,
            "Issue Description": issue_description,
            "Desired Outcome": desired_outcome,
            "Date Received": str(st.session_state["date_received"]),
            "Articles of Violation": article_list,
            "Steward": steward,
            "Case ID": case_id,
            "Department Manager": dept_man,
            "Frontline Manager": flmanager,
            "Position": position,
            "Operation": workarea
        }

        # Only the fields you want in the main PDF, in order
        pdf_fields = {
            "Grievant": grievant,
            "Steward": steward,
            "Appraisal Year": appraisal_year,
            "Current Rating": rating_received,
            "Prior Year’s Rating": previous_rating,
            "Articles of Violation": article_list,
        }
        pdf_data = {k: form_data[k] for k in pdf_fields if k in form_data}

        grievance_type = st.session_state.get("grievance_type", "Annual Appraisal")
        cover_sheet_buffer = create_cover_sheet(form_data, grievance_type)  # Returns BytesIO
        base_pdf_buffer = generate_pdf(pdf_data, full_argument)            # Returns BytesIO

        # --- Merge PDFs: cover sheet first ---
        merger = PdfMerger()
        merger.append(cover_sheet_buffer)
        merger.append(base_pdf_buffer)

        for file in uploaded_files:
            if file is not None:
                filename = file.name
                ext = os.path.splitext(filename)[1].lower()
                try:
                    if ext == ".pdf":
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(file.read())
                            tmp.flush()
                        with open(tmp.name, "rb") as f:
                            merger.append(f)
                    else:
                        converted_path = convert_to_pdf(file, filename)
                        if converted_path:
                                if isinstance(converted_path, BytesIO):
                                    converted_path.seek(0)
                                    merger.append(converted_path)
                                else:
                                    with open(converted_path, "rb") as f:
                                        merger.append(f)
                except Exception as e:
                    st.warning(f"⚠️ Skipped {filename} due to error: {e}")

        output_name = f"{grievant.replace(' ', '_')}_{appraisal_year}_Annual_Argument.pdf"
        final_path = os.path.join(tempfile.gettempdir(), output_name)
        with open(final_path, "wb") as f:
            merger.write(f)
        merger.close()

        st.session_state.final_packet_path = final_path
        st.session_state.final_packet_name = output_name

    # --- Download button ---
    if "final_packet_path" in st.session_state and st.session_state.final_packet_path:
        with open(st.session_state.final_packet_path, "rb") as f:
            st.download_button("📅 Download Completed Grievance Packet", f, file_name=st.session_state.final_packet_name)
