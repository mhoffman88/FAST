import streamlit as st
import datetime
import holidays
import tempfile
import os
from io import BytesIO
from PyPDF2 import PdfMerger
from util import wrap_text_to_width, draw_wrapped_section, generate_pdf, convert_to_pdf, calculate_fbd, create_cover_sheet

def render_annual():
    annual_checkbox_descriptions = {
        "Performance standards did not permit the accurate evaluation of their job performance based on objective criteria related to their position.": {
            "articles": ["Article 12 Section 3", "5 U.S.C §§ 9508", "5 U.S.C. §§ 4302", "5 C.F.R. Part 430"],
            "argument": (
                "     Management is supposed to, to the maximum extent feasible, provide an accurate evaluation of an employee’s job performance based on objective criteria related to the position. By"
                " failing to do this, management has failed to follow the guidance provided through the National Agreement, Article 12 Section 3; 5 USC 4302; 5 USC 9508; 5 CFR Part 430. Each of these specify"
                ' instructions to how the appraisal system is to work. Each of these consistently state that an accurate evaluation must be provided to employees. 5 USC 4302 states "performance standards which'
                " will, to the maximum extent feasible, permit the accurate evaluation of job performance on the basis of objective criteria (which may include the extent of courtesy demonstrated to the public)"
                ' related to the job in question for each employee or position under the system." By not utilizing performance standards to provide an accurate evaluation, not only violates the employee’s rights'
                " granted under the National Agreement, but also violates the laws and regulations intended to protect federal employees from harm. By failing to utilize the performance standards to the degree at"
                " which they were intended to be used to evaluate an employee’s performance to provide an accurate evaluation of their work, management has failed to comply and created an unjust and unfair appraisal"
                " for this grievant and management needs to reconsider the appraisal score given."
            )
        },
        "Management was given specific distribution amounts per level of rating for employees.": {
            "articles": ["Article 12, Section 3", "5 C.F.R. Part 430.208", "IRM 6.430.2.5.7"],
            "argument": (
                "     It is highly inappropriate for management to establish and distribute annual appraisals based upon specific distribution amounts per level of rating of employees. By utilizing this system"
                " of restricting the amount allowed per level of rating, management removes the ability for employees to be fairly and accurately rated upon their performance over the year the annual appraisal period"
                ' covers. IRM 6.430.2.5.7 states "Presumptive ratings, for ratings of record, are prohibited by 5 CFR Section 430.208 (a)(2).” It then goes on to say “A rating of record can be based only on the'
                " evaluation of actual job performance for the designated performance appraisal period. A supervisor must not issue a rating of record that assumes a level of performance by an employee without an"
                ' actual evaluation of that employee’s performance.” Not only is this addressed in the IRM but it is also addressed in C.F.R Part 430.208, which states “The method for deriving and assigning a summary'
                " level may not limit or require the use of particular summary levels (i.e., establish a forced distribution of summary levels). However, methods used to make distinctions among employees or groups of"
                " employees such as comparing, categorizing, and ranking employees or groups on the basis of their performance may be used for purposes other than assigning a summary level including, but not limited"
                ' to, award determinations and promotion decisions.” By not following the guidance provided through the CFR, the Agency is not only violating the National Agreement, the IRM’s, but is also breaking the'
                " law by forcing a set distribution list per level of rating. Management has violated the employee’s rights by failing to provide an accurate reflection upon their service over the last appraisal"
                " period of a year and by utilization of a forced distribution of levels of rating. Management should only utilize the employee’s performance during the period of review and any variation from such"
                " is violating the laws and regulations in place to prevent harm."
            )
        },
        "Employee was not given their annual appraisal on the 6850-BU.": {
            "articles": ["Article 12 Section 4, 5 C.F.R § 430.208"],
            "argument": "Management is meant to keep annual appraisals fair across the Agency. This helps to ensure that employees are treated fairly during the review process. This begins with the"
            " utilization of the form 6850-BU, which allows for the same information to be applied in a strategic way to showcase the employee’s accomplishments and areas of concern over the annual appraisal"
            " year being evaluated. By management choosing to perform the annual appraisal on anything other than the 6850-BU form, it is highly inappropriate and creates unfair and unjust representation for"
            " the employee's appraisal. The form is meant to be utilized by all of management and by choosing to not follow this guidance, management has caused undue harm to the employee and needs to"
            " reevaluate the employee utilizing the correct form to ensure that the appraisal is a fair appraisal for the employee’s appraisal year being evaluated. "
        },
        "Rating was given outside of rating period based on the ending of my social security number. ": {
            "articles": ["Article 12, Section 4, Exhibit 12-2, 5 USC Chapter 43, 5307(d), 5 CFR 430.208 (a) (1), (h), IRM 6.430.3.5.1.1, IRM 6.430.2.4.2, IRM 6.430.2.4.2.1, Document 11678"],
            "argument": "This grievance concerns the current policy of determining the annual performance appraisal period based on the last digit of an employee’s Social Security Number (SSN). Under this"
            " policy, employees receive their annual performance appraisals in different months throughout the fiscal year, resulting in varying evaluation periods. This practice creates inconsistencies in"
            " performance assessment and may lead to inequities in how employees are rated and rewarded. Specifically, employees in similar positions are subject to different performance periods"
            " (e.g., October–September versus June–May), potentially affecting fairness in evaluations, award eligibility, and advancement opportunities. Under 5 CFR § 430.206(b), federal agencies are required"
            " to ensure consistency and fairness in performance appraisals. Management has failed to comply with the guidance issued regarding the annual appraisals and how they are to be performed. Management"
            " needs to reevaluate this annual appraisal and use the guidance given to ensure that a consistent and fair performance evaluation is issued to the employee."
        },
        "Employee changed from one permanent position to another within the last 60 days of the appraisal year and the departure appraisal was not used for the rating of record.": {
            "articles": ["Article 12, Section 4, IRM 6.430.2.4.2, IRM 6.430.2.4.2.1, 5 C.F.R § 430.208"],
            "argument": "When an employee permanently changes positions within the last 60 days of the appraisal year, the departing supervisor is required to complete a departure appraisal, which must then be"
            " used as the basis for the employee's rating of record. In this case, the failure to use the departure appraisal violates 5 C.F.R. § 430.208(a), which mandates that performance be appraised by the"
            " supervisor who had oversight during the relevant appraisal period. Ignoring the departure appraisal removes accountability from the supervisor who observed the employee’s performance for the"
            " majority of the year and places the burden unfairly on a new supervisor with limited observation time. Instead, management should have ensured that the departure appraisal was properly completed"
            " and submitted as the rating of record. Moving forward, all supervisors must be reminded of their responsibility to complete departure appraisals during personnel moves and management must track"
            " such transitions to ensure compliance. A system-level alert or checklist should be implemented to prevent oversight when an employee changes positions near the end of an appraisal period. "
        },
        "Departing supervisor did not comply by performing a departure appraisal.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "When a supervisor leaves their position—regardless of whether the departure is permanent or temporary—they are required to complete a departure appraisal for any employee they"
            " supervised for at least 60 days in the appraisal period. In this case, the supervisor failed to fulfill that obligation, which directly contradicts Article 12 of the National Agreement and 5"
            " C.F.R. § 430.208(b). This creates a gap in documentation and can lead to an inaccurate or incomplete appraisal of the employee’s performance, especially if the incoming supervisor has not"
            " observed the employee’s work long enough to fairly evaluate it. The supervisor should have completed and submitted the departure appraisal before leaving their position, with clear documentation"
            " of the observed performance. To correct this moving forward, management should enforce a departure appraisal checklist for all exiting supervisors and tie its completion to the supervisor's"
            " departure clearance process. Training sessions and reminders should be issued to all management personnel to ensure they understand their obligations under the performance management system. "
        },
        "Supervisor departed from their position during the last 60 days of the appraisal period, and the departure appraisal was not used.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "When a supervisor leaves during the final 60 days of an appraisal period, their departure appraisal must be used as the employees' rating of record if the incoming supervisor has not"
            " observed the employee for the minimum 60-day requirement. In this situation, failing to use the departure appraisal violates both 5 C.F.R. § 430.207 and Article 12 of the National Agreement, as"
            " the appraisal must be based on observed performance by a qualified rater. Instead, relying on an incoming supervisor who lacks sufficient observation time results in an invalid and potentially"
            " grievable rating of record. What should have occurred is that the departing supervisor completes the appraisal, and that rating is used without further modification. Management must implement a"
            " performance appraisal tracking system that flags when supervisors are departing near the end of the appraisal cycle, ensuring that appropriate appraisals are completed and used. A compliance audit"
            " of recent supervisor departures should also be considered to identify and rectify any additional oversights."
        },
        "Supervisor temporarily departed their position during the last 60 days of the employee's appraisal period, but this supervisor did not perform the appraisal.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Even in cases of temporary departure, supervisors who have observed an employee’s performance for at least 60 days in the appraisal period are still responsible for completing a"
            " departure appraisal if they are unavailable during the close of the cycle. In this instance, the failure to conduct an appraisal results in a rating being issued by a manager who did not meet the"
            " observation requirement, violating 5 C.F.R. § 430.208 and the performance appraisal provisions of the National Agreement. An appraisal must be based on actual performance, and that requires"
            " firsthand knowledge from the observing supervisor. Instead, the departing supervisor should have completed the appraisal before leaving or coordinated its completion remotely, if appropriate."
            " To avoid recurrence, management must implement a notification protocol to flag when temporary reassignments or absences intersect with appraisal responsibilities. Clear expectations and"
            " accountability measures should be communicated to all managers, especially during the final quarter of the appraisal period."
        },
        "Supervisor left their position between the 5th and 7th month of the appraisal period, the employees management chain did not utilize the departing appraisal for the employees mid-year review.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "When a supervisor leaves midway through an appraisal year, particularly between the 5th and 7th month, a departure appraisal should be completed and used to inform the employee’s"
            " mid-year review. Failing to incorporate this appraisal results in the new supervisor issuing feedback or mid-year evaluations without sufficient observation, which violates the principle of fair"
            " and meaningful performance evaluation. The departing supervisor had the necessary observation period and context to provide accurate feedback, and that appraisal should have been used as the"
            " foundation for the mid-year. Instead, the management chain ignored a key performance record, resulting in an incomplete review and undermining the appraisal process. Moving forward, management"
            " must ensure that all departure appraisals are properly routed and considered during mid-year reviews when the supervisor leaves mid-cycle. Internal procedures should be implemented to link"
            " mid-year reviews to any available departure appraisals to ensure continuity and accuracy. "
        },
        "Departure appraisal used to disadvantage the employee (e.g., denial of overtime, Telework, or AWS).": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "A departure appraisal, while important, is not a final rating of record and should not be used to take adverse actions against employees, such as denying overtime, Telework, or"
            " Alternative Work Schedules (AWS). When this occurs, it violates the National Agreement and OPM guidance, which clarify that departure appraisals are not final and are subject to further"
            " evaluation. Using them as the basis for punitive actions bypasses procedural safeguards and the opportunity for employee rebuttal, creating an unfair and potentially grievable situation. Instead,"
            " any action that disadvantages the employee must be based on finalized ratings or documented, reviewed misconduct—not interim evaluations. To correct this, managers must receive training that"
            " clearly distinguishes between different types of performance documentation and their appropriate use. Any prior actions taken based on a departure appraisal alone should be reviewed and reversed"
            " if improperly applied. "
        },
        "Departure appraisal improperly becoming a de facto rating of record.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Departure appraisals are meant to document observed performance when a supervisor leaves, but they are not intended to serve as the final rating of record unless the departing"
            " supervisor has observed the employee for the full appraisal period or no other qualified supervisor is available. Improperly treating a departure appraisal as the rating of record undermines the"
            " integrity of the appraisal process, especially if there are months of performance not captured or reviewed. This mistake removes the chance for subsequent supervisors to observe, document, and"
            " provide input, and may result in an inaccurate performance rating. Instead, management should only use the departure appraisal as part of a complete evaluation or if required under 5 C.F.R. §"
            " 430.208. To prevent this issue in the future, supervisors must be educated on the conditions under which departure appraisals can and cannot be converted into ratings of record. Appraisal"
            " timelines and rater assignments should be monitored to ensure proper sequencing and compliance. "
        },
        "Departure appraisal not held until used in an annual rating.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Departure appraisals must be retained and not discarded until the employee's final annual rating of record is completed and any related grievance or appeal rights have expired. When"
            " a departure appraisal is not held for this purpose, it violates federal regulations and the National Agreement, which require all supporting documentation for appraisals to be maintained until"
            " no longer needed. Discarding the appraisal prematurely denies both the employee and future rating officials access to important documentation that may affect the employee’s final rating. Instead,"
            " the Employer must ensure all departure appraisals are stored securely and linked to the appropriate employee records. Moving forward, management should establish a mandatory retention schedule"
            " aligned with the performance management system and require electronic retention of all departure appraisals until the final rating of record and any related proceedings are complete. "
        },
        "Improper use of a recordation before a rating of record. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Evaluative recordations, such as written feedback or monitored contact summaries, may only be used in a rating of record if shared with the employee within 15 workdays of the event and"
            " if the employee was given a chance to respond. Using a recordation that wasn’t disclosed or shared violates Article 12, Section 9 of the National Agreement and basic principles of due process. This"
            " undermines employee rights by denying them the opportunity to rebut or clarify performance events, which could unjustly influence the final rating. Instead, management should only use recordations"
            " that comply fully with notification and response requirements. To correct this, managers should audit all recordations used in ratings and discard any that do not meet notification rules."
            " Additionally, employees should be notified immediately of any recordation that may be used in a future rating to ensure transparency and fairness. "
        },
        "Appraisal period not extended when 60-day minimum not met.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Employees must be under the supervision of a rating official for a minimum of 60 days before a valid performance appraisal can be issued. If no supervisor meets that requirement during"
            " the appraisal period, the Employer must extend the appraisal period until an observing official has supervised the employee for at least 60 days, per 5 C.F.R. § 430.207. Failure to do so results in"
            " an invalid rating of record, as the rater lacks sufficient direct knowledge to fairly evaluate the employee’s performance. Instead of rushing to complete an appraisal without the required"
            " observation period, management should have extended the period as required by regulation. To prevent this from happening again, rating timelines should be tracked, and a flag should be raised"
            " whenever a rater does not meet the 60-day threshold, automatically triggering an appraisal extension until a valid rating can be issued. "
        },
        "Management did not have the minimum 60 calendar days needed to perform an appraisal for an employee.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208, 5 C.F.R. § 430.207 "],
            "argument": "A rating of record cannot be issued unless the employee has been under the supervision of the rating official for at least 60 calendar days. When a rating is issued without meeting this"
            " threshold, it undermines the legitimacy of the performance evaluation, as the rater lacks sufficient observation to make an informed and fair assessment. This premature rating violates both"
            " regulatory guidance and contractual obligations, and can negatively impact employee rights and opportunities. Instead, the Employer should have either extended the appraisal period or reassigned"
            " the rating responsibility to a qualified prior supervisor. To correct this, management should conduct a review of all issued ratings to confirm supervisory timeframes and re-issue any ratings that"
            " fail the 60-day requirement. Training should also be provided to all rating officials on appraisal timing compliance."
        },
        "Failure to use the most recent rating of record during extension.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "When an employee’s appraisal period is extended due to a lack of a qualified rater, the most recent valid rating of record must remain in effect for all personnel decisions until a new"
            " one is issued. Failing to apply the prior rating results in unjust gaps in evaluation history, potentially affecting pay increases, promotions, and awards. This misstep can disadvantage employees"
            " who earned a valid rating within the last appraisal cycle. Instead, the prior rating should be retained and used as the basis for performance-related decisions until a compliant rating is issued."
            " To resolve this, the Employer must audit records to identify instances where prior ratings were not used and retroactively apply the appropriate ratings where necessary. "
        },
        "Improper change to the established annual rating period. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Annual appraisal periods are contractually defined and must not be altered without proper notice, agreement, and adherence to established procedures under Article 12. Arbitrarily changing"
            " the rating period undermines the fairness and consistency of the performance management system and can result in ratings being based on incomplete or inconsistent data. Instead, the established"
            " cycle must be maintained unless officially bargained and documented, with all stakeholders—including the Union—properly notified. To fix this, management should review any deviations from standard"
            " appraisal timelines and reissue any affected appraisals using the correct period. Guidance should be reinforced at the local and national level to ensure adherence to the officially bargained rating"
            " cycle. "
        },
        "Improper impact on within-grade increases, promotions, or other actions due to delay or extension. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Delays or extensions in issuing performance appraisals must not be used to withhold or defer personnel actions such as within-grade increases (WGIs), promotions, or awards unless there"
            " is valid, documented justification. Doing so is both procedurally improper and potentially violates merit system principles and employee rights. The most recent valid rating must be used as the"
            " basis for eligibility determinations until a new rating of record is available. To avoid future violations, management should track appraisal delays and implement safeguards to ensure that"
            " employees are not denied timely personnel actions due to administrative errors. In cases where an action was improperly withheld, corrective actions including back pay or retroactive promotion"
            " should be taken."
        },
        "Use of an expired or non-contractually compliant rating for merit promotion. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Using an expired rating (older than four years) or a rating issued outside of contractual or regulatory standards (e.g., issued without 60 days of observation) violates both Article 12"
            " and Article 13. Such ratings lack validity and should not influence merit promotion or other employment decisions. Doing so introduces bias, unreliability, and opens the Employer to grievances or"
            " equal opportunity complaints. Instead, only ratings that meet all criteria—including timing, observation requirements, and documentation—should be accepted in promotion packages. To prevent"
            " recurrence, selecting officials must receive updated guidance on what constitutes an acceptable rating, and any use of invalid ratings must be rectified through re-competition or other corrective"
            " actions."
        },
        "Inconsistent application of ratings for other personnel actions (e.g., RIFs). ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Ratings of record must be consistently and fairly applied across all personnel actions, including reductions in force (RIFs), reassignments, and eligibility decisions."
            " Inconsistency—such as using an outdated or unverified rating for one employee but not another—violates merit principles and the National Agreement. This creates inequity and exposes the Employer"
            " to grievances, arbitration, or even litigation. Instead, the Employer must develop a standardized process to ensure consistent application and verification of ratings for all actions. Any"
            " inconsistencies identified must be corrected by reapplying decisions with verified, contractually compliant ratings of record and issuing remedies where harm occurred. Going forward,"
            " decision-makers should be required to document their sources and justification for any rating used in such actions. "
        },
        "Failure to provide a merit promotion appraisal upon request when no prior rating exists.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "When an employee has no prior rating of record and requests an appraisal for a merit promotion, management is obligated to provide one based on available performance observations."
            " Failure to do so results in the unjust exclusion of the employee from fair promotional opportunities, disadvantaging them without cause. This action undermines the merit-based principles and"
            " transparency expected in promotion decisions. Instead, management should have provided an interim or summary appraisal reflecting the employee’s observed performance. Moving forward, supervisors"
            " must respond promptly to such requests and provide a fair, timely assessment when no existing rating is available. Clear internal procedures should be established to ensure such requests are never"
            " overlooked. "
        },
        "Refusal to issue Form 6850-BU after 60 days on performance plan. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "When an employee has served on a performance plan for at least 60 days, they are eligible for a formal appraisal using the appropriate form. Refusing to issue the form denies the"
            " employee documentation of their performance and delays critical personnel actions, such as promotions or awards. The appraisal process is intended to recognize work and provide feedback—denying"
            " it weakens employee trust and accountability. Instead, the form should be completed and shared with the employee once the 60-day threshold is reached. To correct this, management should review"
            " any pending cases where forms were withheld and issue them accordingly. Supervisors must be trained to monitor performance plan timelines and fulfill their documentation responsibilities without"
            " delay. "
        },
        "Failure to extend appraisal period for new GS-4 or higher employees who haven’t completed 6 months. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "If an employee in a GS-4 or higher position has not completed 6 months on their performance plan by the end of the appraisal cycle, their rating period should be extended to ensure"
            " adequate observation. Failing to do this results in an unfair and potentially invalid appraisal, as insufficient time was provided to evaluate their performance accurately. The employee is then"
            " judged on a limited sample of work that may not reflect their true capabilities. Instead, the appraisal period should have been formally extended to allow for a full 6 months of observation. To"
            " fix this, supervisors must track new hires and reassigned employees to ensure appraisal timelines are adjusted. Reviews should be conducted to identify and correct any early appraisals issued"
            " under incomplete service periods."
        },
        "Issuance of a “Minimally Successful” rating before 6 months of service.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "A rating of “Minimally Successful” issued before an employee completes 6 months of service lacks sufficient performance data and can unjustly harm their reputation and future"
            " opportunities. This premature assessment does not allow for a fair evaluation of work patterns, adjustment to job expectations, or time to receive necessary feedback. Instead, management should"
            " have either provided coaching or extended the appraisal period to allow the employee to demonstrate improvement. To correct this, the rating should be withdrawn or re-evaluated based on complete"
            " and fair performance data. Supervisors must ensure that negative ratings are never assigned before adequate observation and opportunity for success."
        },
        "Failure to evaluate in accordance with Exhibits 12-1 and 12-2 after 6-month period. (Due date per SSN) ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Once an employee has been on a performance plan for 6 months, they are entitled to a formal appraisal using the correct evaluation criteria. Failure to use the established evaluation"
            " framework results in ratings that are inconsistent, unverifiable, and potentially biased. Instead, the appropriate format and measures should have been applied to ensure the appraisal aligns with"
            " standards used across the agency. This ensures fairness and comparability between employees. To resolve this, any improperly issued appraisals must be redone using the proper framework, and future"
            " evaluations should be reviewed for compliance. Managers must be trained on using the required evaluation forms once the six-month threshold is met. "
        },
        "Negative rating issued prematurely based on insufficient service period. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Issuing a negative appraisal before an employee has been observed for a sufficient period unfairly penalizes them without providing a realistic opportunity to demonstrate their abilities."
            " It indicates a decision was made without enough performance evidence, which undermines both employee morale and the integrity of the appraisal system. The correct approach would have been to extend"
            " the appraisal period until a meaningful evaluation could be completed. To fix this, any premature negative rating should be rescinded and replaced with a fair and substantiated appraisal after the"
            " proper observation period. Future supervisors must confirm the length of time an employee has been on a performance plan before issuing any formal assessment. "
        },
        "Appraisals prepared or recommended by someone other than the employee’s immediate supervisor of record. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Performance appraisals must be prepared by the employee’s designated supervisor, who is most familiar with the individual’s work. When someone outside of the official supervisory chain"
            " prepares or recommends the rating, the credibility and accuracy of the appraisal are compromised. This can result in evaluations that reflect second-hand opinions or unrelated performance"
            " expectations. Instead, the appraisal should have been completed by the official supervisor of record or, if unavailable, by someone in accordance with proper procedures. To correct this, any"
            " improperly issued appraisals should be reviewed and potentially redone. Management should verify that all performance ratings are completed only by those with the proper authority."
        },
        "Bargaining unit employees (e.g., Leads) preparing or recommending any part of an appraisal without meeting the conditions in subsection 4B4.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Bargaining unit employees, such as Leads, may not legally or contractually prepare or influence performance ratings unless specific conditions are met, including voluntary exclusion from"
            " the unit and agreement by the union. When Leads perform these functions without meeting those requirements, it creates a conflict of interest and violates representational protections. These"
            " individuals are peers—not evaluators—and their involvement undermines the neutrality of the appraisal process. Instead, only designated supervisors should assess and document performance. To address"
            " this, management must identify and remove any improperly influenced appraisals and reinforce the separation between bargaining unit roles and supervisory duties. "
        },
        "Rating of record not issued within 30 days after the appraisal due date month. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Timely issuance of the rating of record is critical for ensuring personnel actions are based on current and accurate performance data. When the rating is delayed past the allowed"
            " timeframe, employees may miss out on awards, promotions, or other benefits that rely on the appraisal. It also reflects poorly on management’s ability to complete essential administrative tasks."
            " The rating should have been finalized and delivered within the appropriate period to maintain compliance and avoid unnecessary delays. To correct this, outstanding ratings must be completed"
            " immediately, and internal tracking systems should be implemented to ensure future deadlines are not missed. Supervisors should also be held accountable for completing ratings on time. "
        },
        "Failure to provide the local Chapter, upon request, with a list of employees whose ratings are over 60 days late. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "When the local Chapter requests a list of employees with overdue ratings, it is entitled to that information to perform its representational duties. Failure to provide the list obstructs"
            " transparency, delays potential grievance filings, and prevents the Union from ensuring fair and timely evaluations. This omission weakens employee trust in the process and reduces accountability"
            " for managers who miss deadlines. The proper response would have been to furnish the list promptly upon request. To correct this, management should immediately provide the requested information and"
            " implement a tracking system to ensure timely disclosure in the future. Open communication with the Union is essential for maintaining trust and compliance."
        },
        "Appraisal not made by the next higher-level supervisor when the employee’s immediate supervisor is also a candidate for the same position.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "When a supervisor competes for the same position as the employee they are rating, a conflict of interest arises that can compromise the fairness of the appraisal. Failure to elevate the"
            " appraisal to the next higher-level supervisor in this situation creates the perception, and potential reality, of bias. Instead, the appropriate course of action would have been to assign the"
            " appraisal responsibility to the next higher-level manager to preserve impartiality. To correct this, the appraisal should be re-evaluated by a neutral supervisor with no conflict. Management must"
            " also ensure clear instructions are in place for reassigning appraisal duties in competitive situations. "
        },
        "Appraisal issued by an acting supervisor (bargaining unit employee) who has not served in a managerial capacity for at least 60 days. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Appraisals must be completed by supervisors with adequate observation time and formal authority. Allowing a bargaining unit employee acting in a temporary role for less than 60 days to"
            " issue a rating is inappropriate and does not meet the standard for a valid appraisal. Such appraisals lack the necessary familiarity with the employee’s performance and may violate agreements about"
            " who may issue ratings. The correct process would have been to assign the appraisal to the official supervisor of record or a qualifying acting manager. To fix this, any ratings issued in violation"
            " of this standard should be withdrawn and reassigned appropriately. Supervisors must be trained on the minimum service threshold for rating authority. "
        },
        "Annual rating reflects a period outside the defined appraisal period. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "An annual rating must reflect only the employee’s performance during the official appraisal period. Including work from outside that window skews the evaluation and may unfairly benefit"
            " or disadvantage the employee. This misrepresentation compromises the integrity of the rating and may lead to invalid personnel decisions. The rating should have been limited to the defined appraisal"
            " timeframe, with any earlier or later performance handled separately if needed. Management must review all recent ratings for date accuracy and reissue any that included work outside the appraisal"
            " period. Going forward, supervisors should receive clear training on appraisal boundaries. "
        },
        "Appraisal does not note when it covers less than the full appraisal period.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "When an appraisal reflects less than the full performance year, it must clearly state the period covered to avoid confusion or misuse. Omitting this detail can lead to misinterpretation"
            " of the rating’s scope and inaccurately inform future decisions like promotions or awards. Instead, the appraisal should have included a statement specifying the exact dates of the period evaluated."
            " To resolve this, management should review all recent appraisals and amend any lacking date clarity. Supervisors must be instructed to always indicate coverage dates when issuing partial-period"
            " ratings. "
        },
        "Appraisal not postponed/delayed when necessary information is unavailable. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208, 5 C.F.R. Parts 430 and 531 "],
            "argument": "If key performance data or feedback is unavailable at the time of rating, the appraisal must be delayed to ensure it is accurate and fair. Issuing a rating without necessary information"
            " undermines its validity and may misrepresent the employee’s actual performance. The proper approach would have been to temporarily postpone the rating until sufficient information became available."
            " To fix this, affected ratings should be revisited and corrected, and management should develop a checklist to confirm rating completeness before finalization. Supervisors should also be encouraged"
            " to document delays and communicate timelines clearly with the employee. "
        },
        "Employee not allowed to submit a self-assessment during the final 30 days of the appraisal period. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Self-assessments are a critical opportunity for employees to reflect on their contributions and ensure their voice is part of the appraisal process. Denying access to this process in the"
            " final 30 days robs employees of meaningful participation and may result in incomplete evaluations. Instead, the employee should have been invited and encouraged to submit a self-assessment during"
            " this period. To correct the situation, supervisors should allow the employee to submit a retroactive assessment and consider it in any reevaluation. Going forward, managers must implement a"
            " standard process to prompt self-assessments before the appraisal window closes. "
        },
        "Failure to provide the proper self-assessment form.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "The correct self-assessment form provides structure and consistency across the workforce. If an incorrect or outdated form is provided—or no form at all—employees may struggle to provide"
            " meaningful input or meet expectations. This can result in their contributions being overlooked in the final appraisal. The proper course would have been to distribute the correct form in a timely"
            " manner. To fix this, management should review recent self-assessments for consistency and offer employees a chance to resubmit if needed. Standard operating procedures should include regular updates"
            " to ensure the correct forms are always in circulation. "
        },
        "Employee not granted up to 4 hours of administrative time to prepare the self-assessment. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Employees are entitled to a reasonable amount of time on the clock to prepare their self-assessments. Denying this administrative time forces employees to complete this important task"
            " on personal time, creating inequity and reducing the quality of input. The correct approach would have been to offer up to 4 hours of paid time during the workday to complete the assessment. To"
            " fix this, management should retroactively grant time or consider resubmission with proper support. Moving forward, supervisors should proactively schedule this time and clearly communicate its"
            " availability. "
        },
        "Employee not given appropriate guidance on how to write a self-assessment. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Writing a self-assessment can be challenging without clear instructions or examples. When employees are not given guidance, they may struggle to effectively advocate for themselves or"
            " align their work with performance expectations. Instead, supervisors should have provided a brief explanation, sample responses, or referenced training materials. To correct this, employees who"
            " received no support should be given a chance to revise their self-assessments with proper guidance. Future cycles must include a consistent communication plan outlining how to craft a strong"
            " self-assessment and what to focus on. "
        },
        "Web-based and paper-based tutorials not maintained or provided. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Tutorials for writing self-assessments help standardize expectations and empower employees to contribute meaningfully to their evaluations. Failing to maintain or share these resources"
            " creates confusion, reduces engagement, and leads to inconsistent submissions. The proper course of action would have been to ensure these tutorials were available and distributed regularly. To"
            " fix this, management should audit the availability of training materials and immediately provide them to all employees who missed out. A system should be put in place to update and share these"
            " tutorials annually."
        },
        "Employee denied a one-time opportunity to complete the tutorial on administrative time. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Employees are entitled to administrative time to complete training resources designed to help them prepare for their appraisal process. Denying this opportunity deprives the employee"
            " of the tools necessary to understand how to effectively write a self-assessment or participate meaningfully in the appraisal system. This can result in incomplete or poor-quality submissions and"
            " negatively impact ratings. Instead, the supervisor should have scheduled and approved the administrative time as part of the performance management cycle. To correct this, the employee should be"
            " given administrative time retroactively and allowed to revisit their self-assessment. In the future, all supervisors must ensure employees are made aware of this one-time opportunity and scheduled"
            " accordingly. "
        },
        "Supervisor or designee fails to meet with the employee to explain why their self-assessment was rejected. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "When a self-assessment is rejected without explanation, the employee is left without clarity or the ability to improve future submissions. This lack of communication undermines"
            " transparency and the collaborative intent of the performance review process. The correct procedure would have been for the supervisor or designee to meet with the employee and explain what aspects"
            " were unacceptable or needed revision. To resolve this, management should schedule a meeting with the employee to discuss the issue and offer guidance. Going forward, supervisors must always document"
            " the reason for rejection and offer a timely discussion to ensure the employee understands expectations. "
        },
        "Failure to prepare a merit promotion appraisal when * More than 180 days have passed since the last annual rating, * The employee is applying for a position, and * A midyear review supports a higher rating level. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "When an employee is seeking a promotion and a more recent midyear review supports a higher rating level, failing to issue a merit promotion appraisal places the employee at an unfair"
            " disadvantage. In cases where over 180 days have passed since the last rating, the older appraisal may no longer accurately reflect the employee’s current performance. The correct course would have"
            " been to issue a merit promotion appraisal using the midyear review as a basis, providing a current and fair representation. To remedy the situation, management should issue the appropriate merit"
            " appraisal and consider it in the promotion decision. In the future, supervisors must monitor appraisal timelines and support employees fairly in advancement opportunities. "
        },
        "Failure to prepare a merit promotion appraisal when the current appraisal is used in a competitive action but is not valid or indicative of current performance. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Using an outdated or invalid appraisal in a competitive promotion action misrepresents the employee’s qualifications and can skew selection outcomes. If the appraisal no longer reflects"
            " the employee’s actual performance due to time or changes in duties, a new merit promotion appraisal should be issued to ensure accuracy. Instead, relying on a stale or inaccurate rating denies the"
            " employee a fair evaluation for promotion. To correct this, management should issue a current merit appraisal that reflects the employee’s real performance. In the future, supervisors should assess"
            " the validity of ratings before using them in competitive processes. "
        },
        " Treating a merit promotion appraisal as a rating of record.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "A merit promotion appraisal is meant to support advancement opportunities and is not intended to replace or act as a formal rating of record. Treating it as such creates confusion and"
            " may impact other personnel decisions, such as awards or disciplinary actions. Instead, the merit appraisal should be used solely within the promotion process and kept separate from the annual"
            " performance evaluation. To correct this, any references or uses of the merit appraisal outside of its intended purpose should be withdrawn. Moving forward, supervisors should receive training on"
            " the distinction between merit promotion appraisals and official ratings of record. "
        },
        "Not using the merit promotion appraisal for promotion purposes until the next rating of record is issued. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Delaying the use of a merit promotion appraisal until after a new rating of record is issued defeats its purpose and may block timely advancement. The merit appraisal is specifically"
            " designed to provide a current assessment when no recent rating exists, and withholding it invalidates its utility. The correct approach would have been to use the appraisal immediately to support"
            " the employee’s candidacy. To fix this, the promotion decision should be reexamined using the available merit appraisal. Supervisors must understand that these appraisals are actionable once issued"
            " and should not be deferred. "
        },
        "Appraisal not made in a fair and objective manner. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "An appraisal that lacks fairness or objectivity undermines employee morale, trust in leadership, and the integrity of the evaluation system. Bias, favoritism, or personal conflicts can"
            " distort how performance is rated. Instead, the supervisor should have evaluated the employee strictly on performance outcomes using clear, documented standards. To correct this, a review should be"
            " conducted by an impartial party and the rating revised if needed. In the future, supervisors must be held accountable for maintaining fairness and documenting the rationale behind each rating"
            " decision. "
        },
        "Appraisal does not measure actual work performance in relation to the position’s requirements. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "If an appraisal fails to evaluate the actual duties assigned to an employee, it does not offer an accurate reflection of how well the employee is fulfilling their job. This disconnect"
            " can lead to unfair ratings and personnel decisions based on irrelevant or incomplete criteria. The correct method would have been to assess the employee’s work against their official duties and"
            " performance standards. To correct this, management should revisit the appraisal and ensure all evaluations are tied directly to position responsibilities. Going forward, supervisors must be trained"
            " to align appraisals with job descriptions and expectations. "
        },
        "Appraisal not based on a reasonable and representative sample of the employee’s work.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208"],
            "argument": "Appraisals must be based on a diverse and representative sample of an employee’s tasks to fairly evaluate their overall performance. Focusing only on a limited set of tasks or specific"
            " timeframes skews results and may ignore consistent performance across other areas. The proper approach would have been to review a variety of work products from different times and functions to"
            " provide a complete picture. To fix this, the current appraisal should be reassessed using a broader sample. Supervisors must ensure their evaluations reflect the full range of the employee’s work,"
            " not just isolated instances. "
        },
        "Employer fails to select a reasonable and representative sample when choosing cases for review.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Selecting cases for review in a way that is not balanced or statistically fair can distort performance ratings and cause employees to be judged on unrepresentative work. This creates the"
            " risk of unjustly low or high appraisals. Instead, a sampling method should have been used that gives equal weight to all types of work and reflects the employee’s total output. To correct this,"
            " management should develop and follow consistent sampling practices and re-evaluate ratings where poor sampling was used. Training should be provided to ensure supervisors understand how to collect"
            " fair, representative performance samples. "
        },
        "Supervisor selects only targeted work and fails to include non-targeted work for balance.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Evaluating only targeted work in an appraisal without considering non-targeted tasks leads to an incomplete and potentially biased performance assessment. Many employees perform a mix of"
            " duties, and excluding non-targeted work ignores a significant portion of their contributions. Instead, the supervisor should have included a representative mix of both targeted and non-targeted"
            " tasks in the evaluation. To remedy this, the appraisal should be reviewed and adjusted to reflect the full scope of the employee’s duties. Going forward, supervisors must be reminded to assess all"
            " relevant work activities, not just those subject to higher scrutiny. "
        },
        "Employer fails to supplement the case sample with a reasonable amount of employee-submitted work. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "When management fails to consider employee-submitted work as part of the case sample for performance evaluation, it limits the completeness and fairness of the review. Employees may have"
            " valuable examples that better reflect the quality and scope of their typical work. Ignoring these submissions leads to appraisals based on an incomplete or skewed view of performance. The correct"
            " approach would have been to allow and include a reasonable number of employee-submitted cases in the evaluation sample. To correct this, the appraisal should be revisited and supplemented"
            " accordingly. In the future, supervisors must routinely invite and consider employee-provided examples during the appraisal process."
        },
        "In appraisals based on a limited number of cases (some targeted), Employer does not justify that the sample is representative of the employee’s work. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Using a small and possibly targeted sample without explanation creates the risk of an inaccurate performance rating. If the sample is not clearly shown to represent the full range of"
            " work performed, the appraisal loses credibility and fairness. The correct practice would have been to explain how the sample was selected and why it reasonably reflects the employee’s work. Without"
            " this justification, employees may be evaluated unfairly based on isolated or exceptional cases. The solution is to provide a written rationale for how the sample is representative. Going forward,"
            " all supervisors must document the basis for their sample selection. "
        },
        "Employee is not advised each time an appraisal is used in a personnel action. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Employees have the right to know when their appraisal is being used to make decisions that affect their employment, such as promotions or disciplinary actions. Failing to notify them"
            " removes the opportunity to respond, question accuracy, or seek clarification. Instead, supervisors should inform employees each time an appraisal is used for any personnel action. To address this,"
            " management should retroactively notify affected employees and document any actions taken. Moving forward, a tracking process should be established to ensure employees are kept informed. "
        },
        "Employee is not provided a copy of the appraisal upon request. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "When an employee asks for a copy of their appraisal, denying or delaying that request blocks transparency and undermines trust in the evaluation process. The appraisal is a key document"
            " affecting many aspects of an employee’s career and should be readily available. The proper action would have been to promptly provide a complete and legible copy upon request. To resolve this, the"
            " requested documents should be immediately provided. Moving forward, all supervisors should be reminded that employees have a right to their appraisals and requests must be honored without delay. "
        },
        "Appraisals do not reflect uniform treatment among employees with identical elements and standards within a Division. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Inconsistent ratings among employees performing the same duties under the same standards creates an appearance of favoritism and undermines confidence in the performance management"
            " system. All employees with identical expectations should be evaluated using the same criteria and with a consistent application of those criteria. The supervisor should have ensured that appraisals"
            " across the team reflected a common standard. To fix this, appraisals should be reviewed for fairness and alignment. Going forward, management must train supervisors to apply performance standards"
            " uniformly across the division. "
        },
        "Employees in the same work unit performing the same job are treated inconsistently.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "When employees in the same unit performing the same job receive different ratings without clear justification, it causes confusion and erodes morale. Appraisals should reflect actual performance, not subjective preferences or inconsistencies in evaluation style. The supervisor should have ensured that the same work was judged by the same standards. To address the issue, all affected ratings should be reviewed to ensure consistent treatment. Supervisors must be held accountable for applying standards evenly and explaining any deviations clearly. "
        },
        "Employer fails to maintain uniformity at the Divisional level, even when emphasizing the work unit. ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Even if some emphasis is placed on work unit distinctions, overall consistency at the Divisional level is necessary to ensure fairness and transparency. When uniformity is not maintained across similar roles and standards, employees are subject to unequal treatment based on location or assignment. Instead, the Division should have adopted a consistent interpretation and application of performance expectations. This issue can be addressed by conducting a Division-wide review of ratings and recalibrating where needed. Going forward, all levels of supervision should coordinate to apply standards evenly across the Division. "
        },
        "Supervisor or designee fails to discuss the appraisal with the employee at the time of issuance.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "An appraisal that is not discussed with the employee misses a critical opportunity for communication, clarification, and employee engagement. This discussion allows the employee to understand their rating, ask questions, and provide input if needed. The supervisor should have scheduled a meeting to review the appraisal and ensure the employee had a chance to respond. To correct this, a meeting should be held even after the fact, and a written record of the discussion added to the file. In the future, supervisors must treat the issuance of an appraisal as a two-way conversation, not just a document delivery. "
        },
        "Employee is not allowed to submit written comments within 15 workdays of appraisal issuance.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Employees must be given a fair opportunity to provide written comments or rebuttals to their appraisal, especially if they disagree with any part of it. Denying or cutting short the 15-workday window removes an important safeguard and limits the employee's right to respond. The proper course of action would have been to clearly notify the employee of their right to submit comments and honor the full time period. To remedy this, the employee should be granted a new window to submit comments retroactively. Supervisors should be reminded to always inform employees of this right and time frame. "
        },
        "Employee is not allowed to submit written comments within 3 workdays for appraisals used in a pending competitive action.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "When an appraisal is used in a competitive personnel action, employees must have an expedited opportunity to submit written comments. Denying this right can result in decisions based on unchallenged or incorrect information. The supervisor should have provided notice of the appraisal’s use and the opportunity to submit comments within 3 workdays. To fix this, the appraisal should be reevaluated if the employee’s input was denied, and any decisions based on it reconsidered. In the future, supervisors must act promptly to notify employees and respect the faster comment timeline in these cases."
        },
        "Submitted comments are not attached to and made part of the appraisal.": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "When an employee submits written comments about their appraisal, those comments must be attached and preserved with the original appraisal. Failure to do so removes important context and documentation from the employee's record. Instead, the supervisor should have ensured the comments were formally attached and filed together. To resolve the issue, the submitted comments should be located and added to the appraisal. Moving forward, supervisors must follow a consistent process for retaining and attaching employee input. "
        },
        "Employee not given up to 4 hours of administrative time to prepare rebuttal comments (for appraisals becoming the rating of record).": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Employees must be given adequate time during the workday to prepare rebuttals to performance appraisals, especially when the appraisal will serve as the rating of record. Denying up to 4 hours of administrative time deprives the employee of a meaningful chance to present their perspective. The correct action would have been to schedule this time within three workdays of the request. To fix the issue, the employee should be offered the time now, and their rebuttal added to the appraisal. Supervisors should ensure that employees know about this right and are given time promptly upon request. "
        },
        "Rebuttal comments not attached to and maintained as part of the employee’s performance folder (EPF). ": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "When an employee submits rebuttal comments to their appraisal, those comments must be formally attached and kept in the employee’s performance folder. Failing to maintain them erases the employee’s official response and undermines the integrity of the appraisal record. The appropriate action would have been to immediately file the rebuttal with the performance appraisal. To correct this, the comments must be located and retroactively included in the EPF. Going forward, supervisors and HR staff must ensure that every employee rebuttal is preserved as part of the official record. "
        },
        "Rating is inconsistent with prior feedback": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "The rating is inconsistent with prior feedback, violating Article 21, Section 4."
        },
        "Rating is inconsistent with peer comparisons": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "The rating is inconsistent with peer comparisons, violating Article 21, Section 5."
        },
        "Performance elements were not clearly defined": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "Performance elements were not clearly defined, violating Article 21, Section 2."
        },
        "Employee was not given opportunity to improve": {
            "articles": ["Article 12, Section 4, 5 C.F.R § 430.208 "],
            "argument": "The employee was not given the opportunity to improve, violating Article 12, Section 7."
        }
    }
    measured_checkboxes = {
        "MRating is inconsistent with prior feedback": {
            "articles": ["Article 21, Section 4"],
            "argument": "The rating is inconsistent with prior feedback, violating Article 21, Section 4."
        },
        "MRating is inconsistent with peer comparisons": {
            "articles": ["Article 21, Section 5"],
            "argument": "The rating is inconsistent with peer comparisons, violating Article 21, Section 5."
        },
        "MPerformance elements were not clearly defined": {
            "articles": ["Article 12 Section 3"],
            "argument": "Performance elements were not clearly defined, violating Article 21, Section 2."
        },
        "MEmployee was not given opportunity to improve": {
            "articles": ["Article 12, Section 7"],
            "argument": "The employee was not given the opportunity to improve, violating Article 12, Section 7."
        }
    }
    unmeasured_checkboxes = {
        "UMRating is inconsistent with prior feedback": {
            "articles": ["Article 21, Section 4"],
            "argument": "The rating is inconsistent with prior feedback, violating Article 21, Section 4."
        },
        "UMRating is inconsistent with peer comparisons": {
            "articles": ["Article 21, Section 5"],
            "argument": "The rating is inconsistent with peer comparisons, violating Article 21, Section 5."
        },
        "UMPerformance elements were not clearly defined": {
            "articles": ["Article 12 Section 3"],
            "argument": "Performance elements were not clearly defined, violating Article 21, Section 2."
        },
        "UMEmployee was not given opportunity to improve": {
            "articles": ["Article 12, Section 7"],
            "argument": "The employee was not given the opportunity to improve, violating Article 12, Section 7."
        }
    }
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
        for desc, info in annual_checkbox_descriptions.items():
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
        for article in info["articles"]:
            selected_articles.add(article.strip())
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
