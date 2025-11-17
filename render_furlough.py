import streamlit as st
import datetime
import holidays
import tempfile
import os
from io import BytesIO
from PyPDF2 import PdfMerger
from util import wrap_text_to_width, draw_wrapped_section, generate_pdf, convert_to_pdf, calculate_fbd, create_cover_sheet, merge_pdfs

def render_furlough():
  st.header("Furlough")
    date_col, fbd_col = st.columns([1, 1])
    with date_col:
        date_received = st.date_input(
            "Date Received",
            value=datetime.date.today(),
            key="date_received",
            help="Date of Furlough."
        )
    with fbd_col:
        fbd = calculate_fbd(st.session_state["date_received"])
        st.info(f"🗕️ File By Date (15 business days): {fbd}")
        
    case_id = st.text_input("Case Number")
    steward = st.text_input("Steward's Name")
    grievant = st.text_input("Grievant's Name")
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
    
    st.subheader("Alleged Violations:\n")

    # Define Furlough statements
    furlough_checkbox_descriptions = {
        "Annual Leave denied but no statement of reasoning provided after requested by the employee.": {
            "articles": ["Article 32 Section 1(A)(1)"],
            "argument": "It is a violation of the negotiated rights under the National Agreement to deny an employee’s request for annual leave without providing a clear and timely explanation"
            " for the denial. The National Agreement outlines that, while management retains the right to approve or disapprove leave, such decisions must not be arbitrary or capricious and must be based on legitimate"
            " operational needs. When a leave request is denied, the employee has the right to understand the basis for that decision. \n\n Failure to provide the reason(s) for denial upon request"
            " undermines transparency and accountability and prevents the employee from exercising their right to challenge the denial through appropriate channels, such as the grievance process. This"
            " lack of justification also hampers the union’s ability to determine whether the denial was consistent with past practices, equitable treatment, and the principles of fair and reasonable"
            " application of leave policies. \n\n In this case, management did not offer a statement of reasons for denying the annual leave, even after being requested to do so. This omission"
            " constitutes a violation of the National Agreement, which implicitly and through past interpretive guidance, expects management to act in good faith and provide supporting rationale for decisions that impact"
            " bargaining unit employees’ rights. \n\n"
        },
        "Issues with utilzing 15-min increments.": {
            "articles": ["Article 32 Section 1(A)(2)"],
            "argument": "It is a violation of an employee’s rights under the National Agreement to restrict or deny the use of earned annual leave in increments other than those expressly outlined in"
            " the contract. The National Agreement clearly provides that employees may request and use annual leave in 15-minute increments, and any attempt by management to enforce a different standard—such as requiring"
            " leave to be taken in larger blocks is inconsistent with the negotiated language. \n\n Employees earn annual leave as a benefit of federal service, and once accrued, they have the right to use"
            " that leave subject to approval consistent with operational needs—not arbitrary restrictions on increment size. Denying or charging leave in increments larger than 15 minutes without a valid"
            " contractual basis violates the principles of fairness, consistency, and negotiated rights. \n\n In this case, management's decision to either refuse an employee’s request for annual leave in"
            " a 15-minute increment or to charge the employee leave in a greater amount than requested exceeds their authority under the National Agreement. Such action not only infringes on the employee’s rights but also"
            " establishes a concerning precedent that undermines contractually guaranteed flexibilities afforded to bargaining unit employees. \n"
        }
    }

    selected_reasons = []
    selected_articles = []
    selected_arguments = []
    
    for desc, info in furlough_checkbox_descriptions.items():
        checked = st.checkbox(desc, key=f"furlough_checkbox_{desc}")
        if checked:
            selected_reasons.append(desc)
            selected_articles.extend(info["articles"])
            selected_arguments.append(info["argument"])

    if st.button("Generate AWOL Grievance PDF"):
        st.session_state.final_packet_buffer = None
        st.session_state.final_packet_name = None
        if not steward or not grievant:
            st.warning("Please fill out all required fields.")
        else:
            # Collect all arguments and articles
            full_argument = "\n\n".join(str(arg) for arg in selected_arguments)
            article_list = ", ".join(sorted(set(selected_articles)))
            filing_step = "Step Two - Streamlined Grievance"
    
            # All fields for the cover sheet
            form_data = {
                "Step": filing_step,
                "Steward": steward,
                "Grievant": grievant,
                "Issue Description": issue_description,
                "Desired Outcome": desired_outcome,
                "Articles of Violation": article_list,
                "Case ID": case_id,
                "Department Manager": dept_man,
                "Frontline Manager": flmanager,
                "Position": position,
                "Operation": workarea,
                # Add other fields as needed
            }
    
            # Only the fields you want in the main PDF
            pdf_fields = [
                "Steward",
                "Grievant",
                "Issue Description",
                "Desired Outcome",
                "Articles of Violation"
            ]
            pdf_data = {k: form_data[k] for k in pdf_fields if k in form_data}
    
            grievance_type = st.session_state.get("grievance_type", "Furlough Grievance")
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
    
            # Write merged PDF to a BytesIO buffer for download
            merged_buffer = BytesIO()
            merger.write(merged_buffer)
            merger.close()
            merged_buffer.seek(0)
    
            st.session_state.final_packet_buffer = merged_buffer
            st.session_state.final_packet_name = f"{grievant.replace(' ', '_')}_Furlough_Grievance.pdf"
    
    # --- Download button ---
    if (
        "final_packet_buffer" in st.session_state
        and st.session_state.final_packet_buffer is not None
        and st.session_state.final_packet_name
    ):
        st.download_button(
            "📄 Download AWOL Grievance PDF",
            st.session_state.final_packet_buffer.getvalue(),
            file_name=st.session_state.final_packet_name
        )
