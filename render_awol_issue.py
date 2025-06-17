import streamlit as st
import datetime
import holidays
import tempfile
import os
from util import wrap_text_to_width, draw_wrapped_section, generate_pdf, convert_to_pdf, calculate_fbd, create_cover_sheet, merge_pdfs

def render_awol():
    st.header("AWOL - Annual or Sick Leave Grievance Intake")
    date_col, fbd_col = st.columns([1, 1])
    with date_col:
        date_received = st.date_input(
            "Date Received",
            value=datetime.date.today(),
            key="date_received",
            help="Date the AWOL notice was given to grievant."
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

    st.subheader("Alleged Violations:\nAnnual Leave")

    # Define AWOL-related checkbox content
    awol_checkbox_descriptions = {
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
        },
        "Use or Lose - Employer provided confirmation in writing to employee of Use or Lose after management canceled requested Use or Lose.": {
            "articles": ["Article 32 Section 1(B)"],
            "argument": "When management cancels previously approved use-or-lose annual leave, they are obligated under the National Agreement and applicable government-wide regulations to provide the"
            " employee with written confirmation of the leave restoration. This requirement ensures that the employee is not unfairly penalized for circumstances beyond their control and preserves their"
            " right to use that leave at a later date without it being forfeited. \n\n Failure by management to issue timely written documentation confirming the restoration of the canceled leave constitutes"
            " a violation of the employee’s rights. The restoration process is not automatic and depends on the existence of a formal record showing that the leave was scheduled in advance, was canceled due"
            " to agency necessity, and is now authorized for restoration. Without this written confirmation, the employee may lose valuable earned leave, despite having followed all procedural requirements."
            "\n\n In this case, management canceled the employee’s scheduled use-or-lose leave but failed to provide written notification or documentation of restoration. This oversight not only violates"
            " procedural obligations but also deprives the employee of their ability to recover and use the leave in the future. Such an action undermines the intent of both the National Agreement and Office"
            " of Personnel Management (OPM) regulations, which are designed to protect employees from unjust forfeiture of their earned benefits. \n"
        },
        "Conflict in requests but EOD order was not utilized.": {
            "articles": ["Article 32 Section 1(C)"],
            "argument": "Management violated the National Agreement by failing to adhere to the established Enter-On-Duty (EOD) date order when approving and denying annual leave requests. The National Agreement provides"
            " that when two or more employees within a work unit request overlapping periods of leave and operational needs prevent approving all requests, priority must be given based on the employees’ EOD"
            " dates, with the employee having the earlier EOD date receiving preference. \n\n In this case, the employee who was denied leave had an earlier EOD date than another employee whose overlapping"
            " leave request was approved. By approving the more junior employee’s request over that of the more senior employee, management failed to apply the required order of consideration, thereby violating"
            " the negotiated leave approval process outlined in the National Agreement. This not only undermines the fairness and consistency of leave administration but also diminishes employee trust in the equitable"
            " application of contract provisions. \n"
        },
        "Annual leave request not timely responded to by management.": {
            "articles": ["Article 32 Section 1(D)"],
            "argument": "It is a violation of the employee’s rights under the National Agreement for management to take an excessive or unreasonable amount of time to respond to a leave request."
            " The National Agreement obligates management to act promptly and reasonably when reviewing and responding to such requests, recognizing that timely responses are essential for employees to plan their personal and"
            " family obligations effectively. \n\n Delays in leave approval or denial decisions can create uncertainty, cause undue stress, and disrupt personal responsibilities, ultimately undermining morale"
            " and the employee’s ability to maintain a healthy work-life balance—an outcome the National Agreement expressly seeks to prevent. The intent of the negotiated provisions surrounding leave administration is to"
            " foster fairness, consistency, and respect for employees’ personal time, which cannot occur when decisions are left pending for prolonged periods. \n\n In this case, management failed to issue"
            " a timely response to the leave request, thereby denying the employee the opportunity to make necessary arrangements. Such inaction is inconsistent with the principles laid out in the National Agreement and"
            " should be addressed to ensure that employees’ rights and well-being are protected moving forward.\n"
        },
        "Employee's leave request was affected by another employee requesting time.": {
            "articles": ["Article 32 Section 2"],
            "argument": "It is a violation of the employee’s rights under the National Agreement for management to alter, deny, or adjust one employee’s leave request based solely on the leave request of"
            " another employee. The National Agreement provides that all leave requests must be considered individually and fairly, and that decisions must be based on legitimate operational needs—not on"
            " favoritism, convenience, or preference tied to another employee’s request. \n\n Allowing one employee’s leave request to directly impact the approval of another’s—particularly when both"
            " employees are otherwise eligible and have followed the correct procedures—undermines the principles of equitable treatment and transparency laid out in the contract. Each employee’s request"
            " should be evaluated on its own merits, and in cases of scheduling conflicts, contractual provisions as outlined in the National Agreement, must be followed. \n\n In this case, management"
            " improperly adjusted or denied the employee’s leave request in response to another employee’s request, without applying the appropriate negotiated criteria. This action represents a failure to"
            " administer leave fairly and consistently and constitutes a breach of the employee’s contractual rights. \n"
        },
        "Seasonal Employees - Placed in non-pay status for 10 days or less and was denied us of annual leave.": {
            "articles": ["Article 32 Section 3(A)"],
            "argument": "Management violated the National Agreement by inappropriately denying a seasonal employee the use of their earned annual leave while in a non-pay status for fewer than 10 workdays."
            " The National Agreement does not contain any provision that permits the blanket denial of annual leave for seasonal employees solely based on a short-term non-pay status. Seasonal employees"
            " are entitled to the same leave rights as other bargaining unit employees, and earned leave cannot be withheld without a valid and contractually supported reason. \n\n By refusing to allow the"
            " employee to use their annual leave during this brief non-pay period, management failed to uphold the contractual standards for equitable and consistent leave administration. This action denied"
            " the employee access to a benefit they had earned and were entitled to use, constituting a direct violation of the National Agreement. Such conduct not only disregards the negotiated rights of"
            " seasonal employees, but also sets a harmful precedent that undermines the fair treatment of all employees under the agreement. \n"
        },
        "Seasonal Employees - Requested leave within the last 10 workdays of any fiscal year was denied based on anything except staffing and budgetary restrictions.": {
            "articles": ["Article 32 Section 3(B)"],
            "argument": "Management violated the National Agreement by denying the employee’s request for annual leave during the final 10 workdays of the fiscal year for reasons unrelated to staffing or"
            " budgetary restrictions. The National Agreement provides that while management may deny annual leave during this specific time period, such denials must be based solely on legitimate staffing"
            " needs or financial constraints. Any other reason for denial during this timeframe is not contractually supported and constitutes a violation of the employee’s rights. \n\n In this case,"
            " management denied the leave request without citing staffing shortages or budgetary limitations, thereby exceeding the authority granted under the National Agreement. This action improperly"
            " restricted the employee’s ability to use their earned leave and disregarded the limited and specific circumstances under which such a denial is permitted. By doing so, management not only"
            " failed to follow the negotiated process but also undermined the principle of fair and transparent leave administration guaranteed to all bargaining unit employees.  \n"
        },
        "Seasonal Employees - Seasonal Employees leave requests are not being handled like a regular employees leave request would be.": {
            "articles": ["Article 32 Section 3(C)"],
            "argument": "Management violated the National Agreement by failing to treat a seasonal employee’s annual leave request with the same consideration afforded to non-probationary employees. The"
            " National Agreement explicitly requires that seasonal employees be granted the same rights and benefits related to leave as any other bargaining unit employee, including during peak season"
            " operations. \n\n By denying or deprioritizing the seasonal employee’s leave request solely based on their employment category, management disregarded the employee’s earned entitlements and"
            " engaged in discriminatory leave administration. The National Agreement does not permit management to impose additional restrictions on seasonal employees beyond what is applied to permanent"
            " staff. All employees, regardless of seasonal status, have the right to fair, equitable, and contractually consistent treatment when requesting annual leave. \n\n In this case, management’s"
            " decision to treat the seasonal employee’s request differently violated those protections and reflects an improper and unequal application of the negotiated agreement. \n"
        },
        "The employee requested annual leave in advance for a religious holiday and it was not timely handled.": {
            "articles": ["Article 32 Section 4"],
            "argument": "Management violated the National Agreement by failing to make every reasonable effort to approve the employee’s request for annual leave to observe a religious holiday. The National"
            " Agreement explicitly requires that management give full and fair consideration to leave requests for religious observances and make every reasonable effort to accommodate such requests, especially"
            " when operational needs allow for it. \n\n In this case, there were no demonstrated issues with workload or staffing that would have justified denying the leave. Despite this, management refused"
            " to approve the request, disregarding the employee’s religious rights and the contractual obligation to support religious accommodation whenever feasible. This constitutes a direct violation of the"
            " employee’s rights under the National Agreement and reflects a failure to uphold the Agency’s commitment to respecting diversity, inclusion, and equal treatment in the workplace. \n"
        },
        "An employee was denied the opportunity to utilize annual leave or LWOP for a death in the immediate family.": {
            "articles": ["Article 32 Section 5"],
            "argument": "     Management should have approved any annual leave request or provided LWOP for up to 5 days for the death of an immediate family member. By failing to do so, management"
            " has failed to comply with the NA and has violated the employees' rights as laid out in the NA.\n"
        },
        "Employee was denied advanced annual and met the following conditions:\n"
        "  • Has less than 40 hours of advanced annual balance.\n"
        "  • Completed 1st year of probationary time.\n"
        "  • Been in current appointment for more than 90 days.\n"
        "  • Is eligible to earn annual leave.\n"
        "  • Did not request more advanced leave than could be earned during the remainder of the leave year.\n"
        "  • Is expected to return to work after having used the leave.": {
            "articles": ["Article 32 Section 6(A)"],
            "argument": f"     {grievant} met all the qualifications to be granted advanced annual leave. According to the NA, the employer will grant advanced annual if all the qualifications listed in"
                " the NA have been met. Management should have approved this advanced annual leave request because the employee qualified for it.\n"
        },
        "Denied additional advanced annual leave over the 40 hours limitation due to:\n"
        "  • A serious health condition.\n"
        "  • Or to care for a family member.": {
            "articles": ["Article 32 Section 6(B); Exhibit 33-1"],
            "argument": "     The NA lists that an exception to the rule of a max of 40 hours of advance annual leave if the employee or a family member is faced with a serious health condition."
            " Management should have approved the request for advanced annual leave based off the requirements listed in the NA.\n"
        },
        "The Agency failed to allow an employee to repay the balance due via earned annual leave or through a cash payment.": {
            "articles": ["Article 32 Section 6(C)"],
            "argument": "     It is a violation of an employee's rights to not allow an employee to repay the advanced annual any other way than described in the NA. Management should"
            f" allow {grievant} to pay back the amount borrowed for the advanced annual either by utilization of earned annual hours or through a cash payment.\n"
        },
        "The employer did not make every reasonable effort to approve advanced annual leave consistent with workload and staffing needs.": {
            "articles": ["Article 32 Section 6(D)"],
            "argument": "     Management failed to uphold the NA because every reasonable effort should have been made to grant the employees advanced annual leave consistent with the workload"
            " and staffing needs. By not following the NA on this, management created unjust harm and violated the employees' rights.\n"
        },
        "The employer granted advanced annual leave for one employee and denied another employee the right to use annual leave.": {
            "articles": ["Article 32 Section 6(D)"],
            "argument": "     Advanced annual is only to be approved after other employees' requests for annual leave have been considered. Failing to approve a request for annual leave for one"
            " employee but approving advanced annual leave for another is a violation of the NA and the employees' rights.\n"
        },
        "The employer failed to notify an employee of an AWOL charge in writing, no later than:"
        "  • The end of a pay period. \n"
        "  • Or 2 workdays from the end of the pay period. - If the AWOL charge occured during the last 2 days of the pay period (Friday or Saturday.)": {
            "articles": ["Article 32 Section 9"],
            "argument": "     Management failed to uphold the NA by failing to properly notify the employee of the AWOL charges. Management should have notified the employee by the end"
            " of the pay period. The exception to this is if the AWOL charges took place 2 days prior to the end of the pay period, either the week two Friday or Saturday of the pay period,"
            f" management is allotted an additional 2 workdays after the end of the pay period. By failing to do this according to the NA, management has caused undue and unjust harm to {grievant}\n"
        }
    }
    sick_awol_checkbox_descriptions = {
        "The employer failed to allow the employee to accumulate leave according to statutes and regulations.": {
            "articles": ["Article 34 Section 1"],
            "argument": "     It is a violation of a federal employee to not allow the employee to earn annual leave according to the laws and regulations for earning annual leave. Management"
            " should allow an individual to earn leave according to these laws and regulations that have been set in place for annual leave accrual.\n"
        },
        "The employer failed to allow the utilization of sick leave in 15-min increments.": {
            "articles": ["Article 34 Section 1"],
            "argument": "     According to the NA, sick leave may only be used in 15-minute increments. Any variation from allowing 15-minute increment requests for sick leave is a violation"
            f" of {grievant}'s rights granted under the NA and laws and regulations regarding the use of sick leave. \n"
        },
        "Approval of sick leave did not comply with Exhibit 34-1 (NA).": {
            "articles": ["Article 34 Section 2(A); Exhibit 34-1"],
            "argument": "     Management failed to uphold the NA by following the guidance provided within the NA. The NA specifies the approval process and guidelines in Article 34 and Exhibit 34-1"
            " located in the back of the NA. Failing to follow this guidance is a violation of the employee's rights.\n"
        },
        "Denied sick leave because the employee requested sick leave outside the 2-hour limit from their normal time to report but the degree of the illness prevented the employee"
        " from meeting this requirement.": {
            "articles": ["Article 34 Section 2(B)"],
            "argument": "     According to the NA, an employee is meant to provide the sick leave request no later than 2 hours from the start of their normal time for reporting unless the degree"
            " of illness prevents this time frame from being achievable. Management should be more understanding of individual circumstances and understand that this employee was not able to comply"
            " with the 2-hour requirement of notification due to the degree of illness they were facing.\n"
        },
        "Denied sick leave despite the employee following the sick leave procedure:\n"
        "  • Current telephone number was included via email or voicemail.\n"
        "  • Not under a sick leave restriction.": {
            "articles": ["Article 34 Section 2(B)"],
            "argument": f"     The NA states that an employee must follow certain procedures when requesting sick leave. {grievant} followed these guidelines as laid out in the NA, including leaving"
            " a number to call them back at via a phone call, voicemail, or through an email. Management should not have denied leave based on the employees failure to follow procedures when the"
            " employee did follow all of the correct procedures as laid out by the NA.\n"
        },
        "The employer did not take into consideration the self-certification from an employee for leave of less than 3 consecutive workdays.": {
            "articles": ["Article 34 Section 3(A)"],
            "argument": "     The NA outlines that management is supposed to take an employee's self certification as to the reason for needing sick leave for absences of three consecutive workdays or"
            f" less unless under a sick leave restriction. {grievant} is not under a sick leave restriction and should not have had their self-certification for the reason for needing the time off not"
            " considered by management. This is a violation of the NA as well as a clear violation of the employee's rights granted by the NA, laws, and regulations. \n"
        },
        "The employer required medical documentation for less than 3 consecutive workdays.": {
            "articles": ["Article 34 Section 3(B)"],
            "argument": "     The NA outlines that management is supposed to take an employee's self certification as to the reason for needing sick leave for absences of three consecutive workdays or less unless under a sick leave restriction."
            f" {grievant} is not under a sick leave restriction and should not have been mandated by management to provide additional documentation to back up their request for sick leave.  \n"
        },
        "Denied based on issues with the medical documentation. Must include: \n"
        "  • Statement employee is under the care of a health professional.\n"
        "  • Statement that the employee was incapacitated.\n"
        "      * DOES NOT HAVE TO USE THE WORD ""INCAPACITATED"" \n"
        "  • Include the duration of incapacitation. \n"
        "  • Sign or stamp of signature by Health Care Provider.": {
            "articles": ["Article 34 Section 3(C)"],
            "argument": "     According to the NA, medical certificates are required to contain a statement that the employee is under the care of a health care provider, state the employee was incapacitated"
            " for duty, expected duration, and a signature or stamped signature from the health care provider. The word incapacitated is referring to a state of an individual and is used in the NA as a way"
            " of describing the nature of the inability to perform their job. The word incapacitated is not a requirement to be included with the statement. Requiring this or anything else outside of the"
            " listed required items is a change to the procedures and is not allowable. This is a clear violation of the NA and an abuse of power by management.\n"
        },
        "Denied leave because employee did not timely provide documentation within 15 days after the date requested but employee did not provide documentation within this time frame.": {
            "articles": ["Article 34 Section 3(D)"],
            "argument": str(f"     Management denied {grievant}'s sick leave request because documentation was not turned in timely. According to the NA, the employee is allowed up to 15-days after the date"
            " the employer requested documentation. Requiring any variation from this guidance laid out by the NA is a violation of the employee's rights granted under the NA. \n")
        },
        "Circumstances of the requested leave prevented the employee from meeting the 15-day deadline and the Agency did not allow for the employee , up to 30 days, after"
        " the requested leave due to circumstances.": {
            "articles": ["Article 34 Section 3(D)"],
            "argument": "     According to the NA, an employee is supposed to be allowed up to 30-days after the date of request made by the employer for medical certification if it is not practicable"
            " to get it sooner. Management should not be requiring this paperwork prior to this deadline and by doing so have violated the empolyee's rights. \n"
        },
        "Employer required an employee to provide medical documentation because of:\n"
        "  • A specific work day or work time. \n"
        "  • High volume day \n"
        "  • Black out day \n"
        "  • Critical day": {
            "articles": ["Article 34 Section 3(E)"],
            "argument": "     The NA clearly specifies that management will not require medical documenation based on a specific workday or specific work time. Examples of this would be high volume"
            " days, blackout days, or critical days. Management should not have requested medical documentation for the absence and the employee should not have been denied for not providing the medical"
            " certificate.\n"
        },
        "The employer placed the employee on a sick leave restriction but failed to provide oral counsel to the employer prior to implementation to allow the employee an opportunity to not"
        " be placed on one.": {
            "articles": ["Article 34 Section 4(A)(1)"],
            "argument": "     The NA lays out the procedures for management on issuing a sick leave restriction to an employee. It is a violation of the employee's rights to not have been given an"
            " oral counseling prior to the issuance of a sick leave restriction. Management should allow for this oral counsel prior to the issuance of a sick leave restriction to allow the employee"
            " an opportunity to correct the behavior. \n"
        },
        "Employee has been placed on a sick leave restriction that has exceeded the maximum limitation of allowed time for a sick leave restriction.": {
            "articles": ["Article 34 Section 4(A)(3)"],
            "argument": "     The maximum amount of time that an employee can be placed under a sick leave restriction at a time is clearly defined in the NA. The maximum amount of time is 6-months."
            " Going beyond the allowed 6-months time on a sick leave restriction is a violation of the employee's rights as laid out by the NA.\n"
        },
        "The employee was placed on a sick leave restriction that utilized the employee's usage of approved annual leave and/or leave under FMLA as reasoning rather than absences due to illnesses.": {
            "articles": ["Article 34 Section 4(A)(4)"],
            "argument": "     A sick leave restriction is supposed to only take into account for the absences that an employee has had for illnesses. Utilizing annual leave or FMLA leave in the sick"
            " leave restriction is a violation of the employee's rights as laid out by the NA. \n"
        },
        "Employee was denied the usage of annual leave or sick leave based on a sick leave restriction.": {
            "articles": ["Article 34 Section 4(A)(4)"],
            "argument": "     A sick leave restriction does not prevent the usage of annual leave or FMLA leave per the NA. Denying the use of any leave other than sick leave based on the sick"
            " leave restriction is a violation of the employee's rights as laid out in the NA. \n"
        },
        "Employee was forced to provide medical documentation for being released from duty due to illness and did not have a sick leave restriction in place.": {
            "articles": ["Article 34 Section 4(B)"],
            "argument": "     It is inappropriate for management to to request additional documentation from an employee who left early from their scheduled TOD and was not on a sick leave"
            " restriction. The self-certification from the employee for this partial day should have been substatiating evidence for the approval of sick leave and would not have warranted management"
            " the rights to ask for additional documentation. By doing so, management has failed to comply with the NA and have violated the rights of the employee.\n"
        },
        "Employee has provided to the Agency proof of a chronic condition, is not on a sick leave restriction, and is still being required to furnish medical documentation for the time off for"
        " the chronic condition. \n"
        "  • A chronic condition does not necessarily mean that it requires medical treatment.": {
            "articles": ["Article 34 Section 4(C)"],
            "argument": "     The NA clearly states that when an employee has a chronic condition that requires continuing absences to occur and is not on a sick leave restriction that management will"
            f" not continually require medical documentation to be furnished. By making {grievant} continually furnish medical certifications for these absences, it is a violation of their rights as"
            " laid out by the NA, applicable laws, and regulations. \n"
        },
        "The employer denied the use of annual leave in lieu of sick and no just cause was present to support the decision.": {
            "articles": ["Article 34 Section 5(A)"],
            "argument": f"     When {grievant} requested the use of annual leave in lieu of utilizing sick leave, management should have granted them this or provided them with the reasoning"
            " to justify the denial. By failing to do this, management has violated the NA and this employee's rights. \n"
        },
        "Employee was on annual leave and became sick but was denied the ability to switch the annual leave to sick leave. Employee must have notified manager on the first day of illness.": {
            "articles": ["Article 34 Section 5(B)"],
            "argument": "     Denying an employee the opportunity to switch their annual leave to sick leave after the employee complied with the outlined requirements to do so in the NA is a violation"
            " of the employee's rights. Management should allow an individual who requested annual leave and got sick during that time to switch their time from annual leave to sick leave.\n"
        },
        "Denied advanced sick leave. Employee met the following conditions: \n"
        "  • Employee is eligible to earn sick leave. \n"
        "  • Employee's request does not exceed 30 workdays; or whatever lesser amount complies with applicable regulations (104 hrs bereavement). \n"
        "  • No reason to suggest the employee would not return to work. \n"
        "  • Employee has provided acceptable medical documentation. \n"
        "  • Employee is: \n"
        "       • Adopting a child. \n"
        "       • Employee or family member has a serious health condition. \n"
        "       • Planning arrangements necessitated by the death of a family member. \n"
        "       • To attend a funeral of a family member. \n"
        "  • Employee is not on a sick leave restriction. \n": {
            "articles": ["Article 34 Section 6(A)"],
            "argument": "     The NA is very clear on when advanced sick leave will be given to an employee. The requirements to be given advanced sick leave is that the employee is eligible to earn"
            " sick leave, requested time does not exceed 30 workdays, no reason to believe the employee would not return to work, the employee has provided acceptable medical documentation for the need"
            " of advanced sick leave, employee is facing a qualifying event, and the employee is not under a sick leave restriction. A qualifying event is listed as adopting a chile, the employee"
            " or family member has a serious health condition, make arangements necessitated by a death of a family member or to attend a funeral of a family member. Denying the request when all of these"
            " have been met is a violation of the employee's rights.\n"
        },
        "Denied an employee advanced sick leave because they are probationary.": {
            "articles": ["Article 34 Section 6(B)"],
            "argument": "     The NA states that when an employee is on probation, that it may deny advanced sick leave. Denying a probationary employee the opportunity for advanced sick leave must be"
            " justifiable beyond just being probationary. By denying a probationary employee just based on the facts that they are probationary, is a violation of the NA and the employee's rights. \n"
        },
        "Denied advanced sick leave because of intended purposes. \n"
        "  • Advanced sick leave is not usable for only routine medical visits or minor illness": {
            "articles": ["Article 34 Section 6(C)"],
            "argument": "     A request for advanced sick leave should not be denied because of the intended purposes unless the request was made for routine medical visits or minor illness."
            " By management denying the request for advanced leave when the employee did not request the leave for a routine medical visit or a minor illness, management has violated the employee's"
            " right as given by the NA.\n"
        },
        "The Agency failed to allow the employee to pay back the advanced sick leave balance due via earned sick leave or through a cash payment.": {
            "articles": ["Article 34 Section 6(D)"],
            "argument": "     It is a violation of an employee's rights to not allow an employee to repay the advanced sick leave any other way than described in the NA. Management should"
            f" allow {grievant} to pay back the amount borrowed for the advanced sick leave either by utilization of earned sick leave hours or through a cash payment. \n"
        },
        "Management required medical information details about the nature of the individuals underlying medical condition to the employer.": {
            "articles": ["Article 34 Section 7(A)"],
            "argument": "     It is inappropriate and a violation of an employees' rights to have management request additional details about a medical condition that the employee has. The NA"
            " outlines the process needed to follow if additional medical information is required for the purposes of sick leave. This process should be followed by management to stay compliant with the NA.\n"
        },
        "Employer refused to provide a medical professional for the employee to turn required medical information over to after the employee requested. When specific medical information is required"
        ", including the diagnosis or prognosis of a medical condition, as part of an employee's request for sick leave, the employee may choose to provide that information only to a medical"
        " professional designated by the employer.": {
            "articles": ["Article 34 Section 7(A)"],
            "argument": "     When specific medical information is required, including the diagnosis or prognosis of a medical condition, as part of an employee's request for sick leave, the EE may"
            " choose to provide that information only to a medical professional designated by the employer. It is a violation of the employee's rights for management to refuse to comply by providing"
            " a medical professional for the employee to handover documentation about their medical information. \n"
        },
        "Management failed to treat the employee's medical information as confidential and released information to parties that did not need to know this information.": {
            "articles": ["Article 34 Section 7(B)"],
            "argument": "     Management failed to comply with the NA, laws, and regulations surrounding the protection of federal worker's and the privacy of medical information. By management"
            " sharing {grievant}'s medical information with parties that did not need this information, management violated the employee's right to privacy as well as the rights granted under the NA."
            " Management should not allow this violation to continue and should take all neccessary precautions to protect the employee from undue harm from this violation of the employee's privacy.\n"
        },
    }

    selected_reasons = []
    selected_articles = []
    selected_arguments = []
    
    for desc, info in awol_checkbox_descriptions.items():
        checked = st.checkbox(desc, key=f"awol_checkbox_{desc}")
        if checked:
            selected_reasons.append(desc)
            selected_articles.extend(info["articles"])
            selected_arguments.append(info["argument"])
            
    st.subheader("Alleged Violations:\nSick Leave")
            
    for desc, info in sick_awol_checkbox_descriptions.items():
        checked = st.checkbox(desc, key=f"sick_awol_checkbox_{desc}")
        if checked:
            selected_reasons.append(desc)
            selected_articles.extend(info["articles"])
            selected_arguments.append(info["argument"])

    if st.button("Generate AWOL Grievance PDF"):
        if not steward or not grievant:
            st.warning("Please fill out all required fields.")
        else:
            full_argument = "\n\n".join(str(arg) for arg in selected_arguments)
            article_list = ", ".join(sorted(set(selected_articles)))
            
            filing_step = str("Step Two - Streamlined Grievance")
            
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
                "Operation": workarea
            }
            
            pdf_data = {
                "Steward": steward,
                "Grievant": grievant,
                "Issue Description": issue_description,
                "Desired Outcome": desired_outcome,
                "Articles of Violation": article_list
            }
            
            grievance_type = st.session_state.get("grievance_type", "AWOL Grievance")
    
            cover_sheet = create_cover_sheet(form_data, grievance_type)
            awol_pdf = generate_pdf(pdf_data, full_argument)  # Should return a BytesIO!
            final_pdf_buffer = merge_pdfs(cover_sheet, awol_pdf)
    
            st.download_button(
                "📄 Download AWOL Grievance PDF",
                final_pdf_buffer.getvalue(),  # use getvalue() for bytes
                file_name=f"{grievant.replace(' ', '_')}_AWOL_Grievance.pdf"
            )
