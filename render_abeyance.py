import streamlit as st
import datetime
import holidays
import os
from io import BytesIO
from PyPDF2 import PdfMerger
from util import wrap_text_to_width, draw_wrapped_section, generate_pdf, convert_to_pdf, calculate_fbd, create_cover_sheet, create_abeyance_sheet

def render_abeyance():
    # --- Date and FBD input/display together ---
    if "date_received" not in st.session_state:
        st.session_state["date_received"] = datetime.date.today()

    st.header("Executive Order Abeyance Tracker")
    date_received = st.date_input(
        "Date Denied",
        value=st.session_state["date_received"],
        key="date_received",
        help="Date the appraisal was given to grievant."
    )

    with st.form("grievance_form"):
        steward = st.text_input("Steward’s Name", key="Steward")
        case_id = st.text_input("Case ID")
        workarea = st.text_input("Work Area/ Operation")
        manager = st.text_input("Manager Denied")
        issue_description = st.text_area("Summary of Abeyance", key="issue_description")

        uploaded_files = []
        MAX_UPLOADS = 4
        for i in range(MAX_UPLOADS):
            uploaded_files.append(
                st.file_uploader(
                    f"Supporting Document {i+1}",
                    type=["pdf", "docx", "txt", "jpg", "jpeg", "png"],
                    key=f"file_uploader_{i}",
                )
            )

        submitted = st.form_submit_button("Generate Abyeance Tracking Form")

    if submitted:
        filing_step = "EO ABEYANCE"
        
        # All fields for the cover sheet (in order)
        form_data = {
            "Step": filing_step,
            "Case ID": case_id,
            "Manager Denied": manager,
            "Issue Description": issue_description,
            "Date Received": str(date_received),
            "Steward": steward,
            "Operation": workarea
        }

        # Only the fields you want in the main PDF, in order
        pdf_fields = {
            "Steward": steward,
            "Manager Denied": manager
        }
        pdf_data = {k: form_data[k] for k in pdf_fields if k in form_data}

        grievance_type = st.session_state.get("grievance_type", "EO Abeyance")
        cover_sheet_buffer = create_abeyance_sheet(form_data, grievance_type)  # Returns BytesIO

        # --- Merge PDFs: cover sheet first ---
        merger = PdfMerger()
        merger.append(cover_sheet_buffer)

        for file in uploaded_files:
            if file is not None:
                filename = file.name
                ext = os.path.splitext(filename)[1].lower()
                try:
                    if ext == ".pdf":
                        merger.append(BytesIO(file.read()))
                    else:
                        converted_path = convert_to_pdf(file, filename)
                        if converted_path:
                            converted_path.seek(0)
                            merger.append(converted_path)
                except Exception as e:
                    st.warning(f"⚠️ Skipped {filename} due to error: {e}")

        output_name = f"{workarea.replace(' ', '_')}_{manager.replace(' ', '_')}_EO_Abeyance.pdf"
        merged_buffer = BytesIO()
        merger.write(merged_buffer)
        merger.close()
        merged_buffer.seek(0)

        st.session_state.final_packet_buffer = merged_buffer
        st.session_state.final_packet_name = output_name

    # --- Download button ---
    if "final_packet_buffer" in st.session_state and st.session_state.final_packet_buffer is not None:
        st.download_button(
            "📅 Download Completed EO Abeyance Packet",
            st.session_state.final_packet_buffer.getvalue(),
            file_name=st.session_state.final_packet_name
        )
