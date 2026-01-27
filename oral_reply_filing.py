import streamlit as st
import datetime
import holidays
import tempfile
import os
from io import BytesIO
from PyPDF2 import PdfMerger
from util import wrap_text_to_width, draw_wrapped_section, generate_pdf, convert_to_pdf, calculate_fbd, create_cover_sheet, calculate_orfbd
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def render_orfiling():
    # initialise proposal date state
    if "proposal_date" not in st.session_state:
        st.session_state["proposal_date"] = datetime.date.today()
    if "date_received" not in st.session_state:
        st.session_state["date_received"] = datetime.date.today()

    st.header("Oral Reply Filing Intake")

    # show proposal received / file‐by date side‑by‑side (your existing FBD code)
    date_col, fbd_col = st.columns([1, 1])
    with date_col:
        date_received = st.date_input(
            "Proposal Received",
            value=st.session_state["date_received"],
            key="date_received",
            help="Date the proposal letter was given to grievant."
        )
    with fbd_col:
        # reuse your existing 15‑business‑day function
        fbd = calculate_fbd(st.session_state["date_received"])
        st.info(f"🗕️ File By Date (15 business days): {fbd}")

    # begin new authorization form
    with st.form("oral_reply_form"):
        proposal_date = st.date_input(
            "Proposal Letter Date",
            value=st.session_state["proposal_date"],
            key="proposal_date",
            help="Date shown on the proposal letter."
        )
        grievant = st.text_input("Grievant’s Name", key="grievant_name")
        steward = st.text_input("Steward’s Name", key="steward_name")
        tax_case = st.checkbox("Tax Case Y/N", key="tax_case")
        tax_periods = ""
        if tax_case:
            tax_periods = st.text_input(
                "Tax periods (e.g., 2018, 2019)",
                help="Enter comma‑separated tax years affected."
            )
        submitted = st.form_submit_button("Generate Authorization PDF")

    if submitted:
        # build the main authorization paragraph
        auth_text = (
            f"I, {grievant}, an employee of the Kansas City IRS Campus, hereby designate "
            "the NTEU Chapter 66 steward identified below as my representative and grant "
            "them all rights and privileges to act lawfully on my behalf pursuant to this "
            "designation. This includes any information requested in connection with the "
            "Union's representational functions specified in 5 U.S.C. Sec. 7101. This "
            "designation of representation shall remain in effect for one year from the date "
            "of execution of this form unless I request, in writing, revocation of this "
            "document at an earlier date."
        )

        # if tax case is checked, append the additional language
        if tax_case:
            auth_text += (
                "\n\nFurthermore, I hereby grant the NTEU Chapter 66 Steward identified access to tax "
                f"information in relation to their representation in connection with the letter dated "
                f"{proposal_date.strftime('%B %d, %Y')} along with any other documents supporting the letter. "
                f"Requesting the Record of Account Transcript for {tax_periods}.\n\n"
                "I understand that the Internal Revenue Code 7431 permits a taxpayer to bring a civil action "
                "against a person who knowingly or negligently discloses tax information in violation of Internal "
                "Revenue Code 6103. Additionally, I understand that the tax information may not be used in any public "
                "proceeding or disclosed to any person, other than a Treasury Department employee in connection with "
                "that employee's official duties with respect to this matter, unless the particular use or proposed "
                "disclosure is approved by the Service upon my separate written request. Upon such a request, the Service "
                "will ordinarily provide authorization to disclose relevant sanitized tax information, as appropriate. "
                "This separate written request is not necessary if I disclose to a third party or at a public proceeding "
                "only the information that has already been disclosed by the Service to that third party, provided that the "
                "extent of such disclosure is limited to the form and extent of the Service's disclosure. For example, the "
                "evidence file submitted by the Service to the Merit Systems Protection Board (MSPB) in response to an "
                "employee's appeal may be used at the hearing without prior request by the employee or representative."
            )

        # prepare the PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=LETTER)
        styles = getSampleStyleSheet()
        story = []
        # body text
        story.append(Paragraph(auth_text.replace("\n", "<br/>"), styles["Normal"]))
        story.append(Spacer(1, 18))
        # signature lines
        story.append(Paragraph(f"{grievant}", styles["Normal"]))
        story.append(Paragraph("______________________________", styles["Normal"]))
        story.append(Paragraph("Grievant Signature", styles["Normal"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"{steward}", styles["Normal"]))
        story.append(Paragraph("______________________________", styles["Normal"]))
        story.append(Paragraph("Steward Signature", styles["Normal"]))
        # optional SSN line for tax case
        if tax_case:
            story.append(Spacer(1, 18))
            story.append(Paragraph(
                "Employee Social Security Number: ____________________________",
                styles["Normal"]
            ))
        # build and return the PDF
        doc.build(story)
        buffer.seek(0)

        # provide download button
        file_name = f"{grievant.replace(' ', '_')}_Authorization.pdf"
        st.download_button(
            label="Download Authorization Form",
            data=buffer,
            file_name=file_name,
            mime="application/pdf"
        )
