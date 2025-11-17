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
        # use the date_received variable (populated by the date_input) to calculate the FBD
        fbd = calculate_fbd(date_received)
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
        "The Agency failed to follow EOD order for furloughed employees.": {
            "articles": ["National Agreement Article 48, Section 1(B), 5 CFR Part 752"],
            "argument": "Article 48 of the National Agreement requires that when the Agency recalls employees to excepted duty during a shutdown, it must do so in inverse seniority using"
            " each employee’s Enter-on-Duty (EOD) date and, if there is a tie, the Service Computation Date or the lowest social-security digit. Management’s decision to bypass this"
            " formula and recall employees out of order violates the contractual requirement and undermines the negotiated protections that ensure fairness and prevent favoritism in"
            " furlough recalls. The recall procedures in 5 CFR Part 752 treat furloughs of 30 days or less as adverse actions and require agencies to follow established procedures;"
            " ignoring the National Agreement’s recall order violates those procedures. Employees who were not recalled according to their EOD date suffered lost pay and disruption of"
            " seniority rights, constituting harm that should be remedied. To correct this violation, the Agency should rescind improper recall selections, apply the EOD-based inverse"
            " seniority rule, make affected employees whole for lost pay and benefits, and post a notice affirming its obligation to follow Article 48 in future recalls. \n\n"
        },
        "Employees were furloughed for utilization of annual or sick leave during the shutdown.": {
            "articles": ["31 U.S.C. § 1341(c)(2)-(3), OPM Shutdown Furlough Guidance, 5 CFR Part 752"],
            "argument": "It is a violation of an employee’s rights under the National Agreement to restrict or deny the use of earned annual leave in increments other than those expressly outlined in"
                        " the contract. The National Agreement clearly provides that employees may request and use annual leave in 15-minute increments, and any attempt by management to enforce a different standard—such as requiring"
                        " leave to be taken in larger blocks is inconsistent with the negotiated language. \n\n Employees earn annual leave as a benefit of federal service, and once accrued, they have the right to use"
                        " that leave subject to approval consistent with operational needs—not arbitrary restrictions on increment size. Denying or charging leave in increments larger than 15 minutes without a valid"
                        " contractual basis violates the principles of fairness, consistency, and negotiated rights. \n\n In this case, management's decision to either refuse an employee’s request for annual leave in"
                        " a 15-minute increment or to charge the employee leave in a greater amount than requested exceeds their authority under the National Agreement. Such action not only infringes on the employee’s rights but also"
                        " establishes a concerning precedent that undermines contractually guaranteed flexibilities afforded to bargaining unit employees. \n"
        },
        "Employees were furloughed based on medical discrimination through the use of FMLA.": {
            "articles": ["Family and Medical Leave Act, 5 U.S.C. § 6381-6387 (Title 5 FMLA), 29 U.S.C. § 2615, 5 U.S.C. § 6385, OPM Shutdown Furlough Guidance, 5 CFR Part 630, Subpart L"],
            "argument": "Title 5 and Title 29 of the FMLA prohibit employers from interfering with, restraining or discriminating against employees for exercising FMLA rights and bar"
            " reprisals such as depriving them of pay or benefits. OPM’s shutdown guidance specifies that when a lapse in appropriations occurs, any scheduled paid leave substituted for"
            " FMLA leave must be canceled and converted to furlough or leave‑without‑pay, and the time does not count against the 12‑week FMLA entitlement. Management’s decision to"
            " furlough employees because they were on FMLA leave—rather than simply canceling leave and placing them in furlough status like others—constitutes a discriminatory act that"
            " interfered with their statutory rights. Such a practice chills the exercise of FMLA leave and violates 5 U.S.C. § 6385 and 29 U.S.C. § 2615. Employees affected were deprived"
            " of equal treatment and risked losing medical benefits; the remedy should include back pay, restoration of leave balances, removal of any adverse records, and affirmation"
            " that FMLA use will not be a basis for furlough selection in future shutdowns. \n\n"
        },
        "Employees were furloughed for requesting a Reasonable Accommodation.": {
            "articles": ["Rehabilitation Act of 1973 (29 U.S.C. § 791), IRM 1.20.2.1.1, IRM 1.20.2.2.4, 29 C.F.R. § 1614.203"],
            "argument": "The Rehabilitation Act obligates federal employers to provide reasonable accommodations to qualified employees with disabilities unless doing so would impose an"
            " undue hardship, and it prohibits discrimination based on disability. IRS procedures in IRM 1.20.2 require managers to engage in an interactive process promptly and, absent"
            " extenuating circumstances, process reasonable‑accommodation requests within 20 workdays; delaying or denying an accommodation when one can be provided promptly may violate"
            " the Rehabilitation Act. Furloughing employees because they requested a reasonable accommodation is discriminatory and retaliatory: it punishes individuals for exercising"
            " their right to accommodation instead of evaluating the request on its merits. Such conduct not only violates the Rehabilitation Act but also contravenes IRM policy"
            " requiring accommodation requests to be handled expeditiously. The appropriate remedy is to remove any adverse action taken against the employees, provide them back pay and"
            " benefits, process their accommodation requests in good faith, and reaffirm that requesting reasonable accommodation will not be grounds for furlough or other adverse"
            " treatment. \n\n"
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

    if st.button("Generate Furlough Grievance PDF"):
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
            "📄 Download Furlough Grievance PDF",
            st.session_state.final_packet_buffer.getvalue(),
            file_name=st.session_state.final_packet_name
        )
