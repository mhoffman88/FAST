"""Question bank and random board builder for the FAST steward Jeopardy game.

How to add content:
- Add a new category in JEOPARDY_QUESTION_BANK.
- For each category, add clues under values 100, 200, 300, 400, 500.
- Each clue entry needs: question, answer.
- Add multiple clues per value to increase randomness each game.
"""

import random

JEOPARDY_VALUES = [100, 200, 300, 400, 500]
JEOPARDY_CATEGORY_COUNT = 4

JEOPARDY_QUESTION_BANK = [
    {
        "category": "Interview & Investigation Rights",
        "clues_by_value": {
            100: [
                {"question": "Form issued to third-party witnesses before interviews.", "answer": "What is Form 9142?"},
                {"question": "Form for the Miranda rights statement in custodial criminal interviews.", "answer": "What is Form 5228?"},
                {"question": "Form executed by the subject of a conduct interview before the interview begins.", "answer": "What is Form 8111?"},
            ],
            200: [
                {"question": "This rights statement is used at the start of custodial criminal interviews.", "answer": "What is the Miranda rights statement?"},
                {"question": "This form outlines rights in a non-custodial interview for possible criminal conduct.", "answer": "What is Form 12036?"},
                {"question": "This warning compels answers after prosecution is declined for possible criminal conduct.", "answer": "What is the Kalkines warning?"},
            ],
            300: [
                {"question": "An employee must be informed of the right to representation when an interview may result in discipline.", "answer": "What is the right to union representation?"},
                {"question": "When an interview is initiated by the employee, there is no obligation to inform them of representation rights.", "answer": "What is no initial obligation?"},
                {"question": "If the subject of an interview changes, the employee or representative may request a recess to confer.", "answer": "What is a recess request?"},
            ],
            400: [
                {"question": "Form 5228 is used only when the interview is custodial and involves criminal conduct.", "answer": "What is Form 5228?"},
                {"question": "This warning is given only when prosecution is declined and the interview concerns possible criminal conduct.", "answer": "What is the Kalkines warning?"},
                {"question": "This form is executed only by the subject of a conduct interview.", "answer": "What is Form 8111?"},
            ],
            500: [
                {"question": "This warning states that answers cannot be used against the employee criminally except for false statements.", "answer": "What is the Kalkines warning exception rule?"},
                {"question": "A union representative may clarify questions, clarify answers, suggest witnesses and advise the employee during interviews.", "answer": "What is union rep roles?"},
                {"question": "Employees who refuse to answer may be advised that failure could result in severe discipline under 31 CFR 0.207.", "answer": "What is the 31 CFR 0.207 warning?"},
            ],
        },
    },
    {
        "category": "Designation of Stewards",
        "clues_by_value": {
            100: [
                {"question": "Each chapter may appoint this number of stewards.", "answer": "What is an unlimited number?"},
                {"question": "Stewards must be this type of employee or retiree in good standing.", "answer": "Who are bargaining-unit employees and IRS retirees?"},
                {"question": "The steward roster is posted on the union portion of official bulletin boards.", "answer": "What is the steward roster posting?"},
            ],
            200: [
                {"question": "This steward represents a shift or chapter and is designated by the union.", "answer": "What is a chief steward?"},
                {"question": "Steward includes Chapter Presidents, Vice-Presidents, Chief Stewards and authorized employees.", "answer": "What is the steward definition?"},
                {"question": "A retired steward follows security policies and cannot represent if there's a conflict of interest.", "answer": "What is the retired steward rule?"},
            ],
            300: [
                {"question": "The union provides and updates this list of stewards to the employer.", "answer": "What is the steward roster?"},
                {"question": "The human capital officer provides NTEU with electronic organizational charts upon request.", "answer": "What are organizational charts?"},
                {"question": "A steward may cross division lines to represent employees if they are within the chapter's jurisdiction.", "answer": "What is cross-division representation?"},
            ],
            400: [
                {"question": "Each shift may have one chief steward, up to three per chapter; each must work the shift.", "answer": "What is the chief steward rule?"},
                {"question": "Retired stewards may not represent employees if a conflict of interest exists and must follow non-IRS employee security procedures.", "answer": "What is the retired steward restriction?"},
                {"question": "Stewards must be employed within the chapter's jurisdiction to represent employees across divisions.", "answer": "What is the jurisdiction requirement?"},
            ],
            500: [
                {"question": "The steward roster includes names, assigned areas of responsibility and updates whenever changes occur.", "answer": "What is the roster detail?"},
                {"question": "The human capital officer provides electronic organizational charts down to the group or unit level, showing management officials.", "answer": "What are detailed org charts?"},
                {"question": "Stewards may cross divisions but must be within their chapter's jurisdiction; retired stewards follow security procedures and avoid conflicts.", "answer": "What is cross-division stewardship?"},
            ],
        },
    },
    {
        "category": "Official Time Activities",
        "clues_by_value": {
            100: [
                {"question": "Time spent on union duties is recognized as beneficial to both parties.", "answer": "What is mutual benefit recognition?"},
                {"question": "Only this number of stewards may use official time per meeting unless the agreement allows more.", "answer": "What is one steward?"},
                {"question": "Stewards are granted this when participating in meetings with management.", "answer": "What is official time?"},
            ],
            200: [
                {"question": "This term describes time granted to stewards for specified representational activities.", "answer": "What is official time?"},
                {"question": "A discussion with management on grievances or personnel policies under U.S. Code qualifies as this.", "answer": "What is a formal discussion?"},
                {"question": "Questioning an employee when they believe discipline may result qualifies as this.", "answer": "What is an examination?"},
            ],
            300: [
                {"question": "Official time for an examination is granted only when the employee requests representation.", "answer": "What is the representation request rule?"},
                {"question": "Grievance meetings under Articles 41 and 42 entitle stewards to this time.", "answer": "What is official time for grievances?"},
                {"question": "Negotiations with management, including FSIP and mediation, qualify for this time.", "answer": "What is negotiation official time?"},
            ],
            400: [
                {"question": "Only one steward may use official time per meeting unless a specific provision allows more.", "answer": "What is the one-steward limit?"},
                {"question": "Union-conducted training qualifies for official time only when it furthers government interests and is permitted by law.", "answer": "What is the training requirement?"},
                {"question": "An examination triggers official time only when the employee believes discipline may result and requests representation.", "answer": "What is the examination condition?"},
            ],
            500: [
                {"question": "Stewards may earn these hours for official time activities consistent with Article 23 rules.", "answer": "What are credit hours?"},
                {"question": "Stewards cannot earn overtime pay for representational duties unless already in an approved overtime status.", "answer": "What is the overtime restriction?"},
                {"question": "Stewards eligible for frequent or recurring telework may perform official duties while teleworking.", "answer": "What is official time telework?"},
            ],
        },
    },
    {
        "category": "Bank Time & Steward Categories",
        "clues_by_value": {
            100: [
                {"question": "Bank time is allocated by multiplying the number of BUEs by a per-capita rate.", "answer": "What is the allocation formula?"},
                {"question": "Chapters with 1-200 BUEs receive this many hours of bank time per employee.", "answer": "What are six hours?"},
                {"question": "Chapters with 751-1,500 BUEs receive this per-capita bank time rate.", "answer": "What are three hours?"},
            ],
            200: [
                {"question": "Allocated representational time for chapters based on BUE count is called this.", "answer": "What is bank time?"},
                {"question": "A steward authorized to engage in union work on a full-time basis is called this.", "answer": "What is a full-time steward?"},
                {"question": "A steward limited to 1,100 hours of bank and/or official time each fiscal year is called this.", "answer": "What is an OTFT steward?"},
            ],
            300: [
                {"question": "Bank time is allocated at the beginning of each fiscal year based on BUE count.", "answer": "What is allocation timing?"},
                {"question": "After June 1, a chapter may draw from reserve once it uses 90% of its allocation.", "answer": "What is the reserve draw rule?"},
                {"question": "Chapters may not carry unused bank-time hours into the next fiscal year.", "answer": "What is the no carryover rule?"},
            ],
            400: [
                {"question": "Bank time reserve equals 15% of the total and distribution decisions occur when 75% is used.", "answer": "What is the reserve distribution rule?"},
                {"question": "When chapters merge, the continuing chapter inherits unused bank-time hours from the merged chapters.", "answer": "What is the merged chapter allocation?"},
                {"question": "Chapters with 300-599, 600-899 and 900-1,199 BUEs receive one, two and three full-time stewards respectively.", "answer": "What is the full-time steward allotment?"},
            ],
            500: [
                {"question": "Chapters with 150-299 employees are entitled to at least one other-than-full-time steward.", "answer": "What is the OTFT guarantee?"},
                {"question": "Two other-than-full-time positions may be combined at any time to form a full-time steward position.", "answer": "What is the OTFT conversion rule?"},
                {"question": "Part-time stewards are limited to 850 hours of bank and/or official time per year.", "answer": "What is the part-time steward limit?"},
            ],
        },
    },
    {
        "category": "Performance-Appraisal Definitions",
        "clues_by_value": {
            100: [
                {"question": "Written record of critical job elements used for promotions and personnel actions.", "answer": "What is the annual appraisal?"},
                {"question": "Established period for reviewing performance and preparing the rating.", "answer": "What is the appraisal period?"},
                {"question": "Act or process of reviewing and evaluating an employee's performance.", "answer": "What is appraisal?"},
            ],
            200: [
                {"question": "Percentage weight assigned to a critical job element representing its impact on the rating.", "answer": "What is critical job-element weighting?"},
                {"question": "Appraisal prepared when an employee or supervisor moves to a new assignment.", "answer": "What is a departure appraisal?"},
                {"question": "Appraisal prepared for a merit promotion when no rating of record exists.", "answer": "What is a merit promotion appraisal?"},
            ],
            300: [
                {"question": "A supervisor must observe performance under a signed plan for at least 60 days to prepare this appraisal.", "answer": "What is the departure appraisal requirement?"},
                {"question": "At least one progress review is required, usually six months before the end of the rating period.", "answer": "What is progress review timing?"},
                {"question": "Evaluative recordation includes written performance indicators but excludes program-effectiveness measures for individual evaluation.", "answer": "What is the evaluative recordation rule?"},
            ],
            400: [
                {"question": "Measures of program effectiveness may be used for individual evaluations only for employees covered by MEPS.", "answer": "What is the MEPS exception?"},
                {"question": "Critical job elements must be measurable and controllable at the individual level.", "answer": "What is CJE measurability?"},
                {"question": "A merit promotion appraisal is used only until the employee receives a rating of record.", "answer": "What is the MPA limitation?"},
            ],
            500: [
                {"question": "Quantity measures include outcome-neutral data such as cases started, cases closed, items completed, time per case and inventory info.", "answer": "What are quantity measures?"},
                {"question": "Records of tax enforcement results are compilations of enforcement outcomes, excluding individual case results.", "answer": "What are records of tax enforcement results?"},
                {"question": "A performance plan includes assigned critical job elements, performance aspects and the Retention Standard.", "answer": "What are performance plan components?"},
            ],
        },
    },
    {
        "category": "Prohibited Personnel Practices & Merit System",
        "clues_by_value": {
            100: [
                {"question": "Discriminating based on race, religion, sex or national origin is part of these prohibited actions.", "answer": "What are prohibited personnel practices?"},
                {"question": "A recommendation for appointment or promotion must be based on personal knowledge of work performance.", "answer": "What is the personal-knowledge requirement?"},
                {"question": "Appointing or advocating for a relative is a prohibited practice known as this.", "answer": "What is the anti-nepotism provision?"},
            ],
            200: [
                {"question": "Taking or threatening personnel action because an employee discloses violations or cooperates with investigators is called this.", "answer": "What is reprisal?"},
                {"question": "Coercing employees to engage in political activity or punishing them for refusal constitutes this violation.", "answer": "What is political coercion?"},
                {"question": "Required statement preserving rights to communicate with Congress and inspectors general in nondisclosure policies.", "answer": "What is the whistleblower-protection statement?"},
            ],
            300: [
                {"question": "Employees aggrieved under prohibited practices may choose either a statutory procedure or the grievance procedure but not both.", "answer": "What is the procedural choice?"},
                {"question": "Arbitrators reviewing these grievances apply evidence standards used by the Merit Systems Protection Board.", "answer": "What are MSPB standards?"},
                {"question": "An employee must not be punished for refusing to obey an order that requires them to violate a law.", "answer": "What is the refusal protection?"},
            ],
            400: [
                {"question": "Initiating a grievance does not reflect negatively on an employee and is protected from reprisal.", "answer": "What is grievance freedom?"},
                {"question": "Employees must not be discriminated against based on conduct that does not adversely affect job performance, except when considering a criminal conviction.", "answer": "What is the conduct discrimination rule?"},
                {"question": "Implementing a nondisclosure policy is prohibited unless it includes the whistleblower statement.", "answer": "What is the nondisclosure condition?"},
            ],
            500: [
                {"question": "Nondisclosure policies must preserve rights to communicate with Congress, report to an inspector general and maintain whistleblower protections.", "answer": "What is the whistleblower statement requirement?"},
                {"question": "Employers must not take or fail to take personnel actions that violate veterans' preference requirements.", "answer": "What is the veterans' preference protection?"},
                {"question": "Influencing someone to withdraw from competition to improve another person's chances is prohibited.", "answer": "What is the competition influence prohibition?"},
            ],
        },
    },
    {
        "category": "Travel & Per Diem",
        "clues_by_value": {
            100: [
                {"question": "All union-related travel is charged to this purpose code.", "answer": "What is Purpose Code U?"},
                {"question": "Travel vouchers of union stewards are subject to the same approval requirements as other employees.", "answer": "What is equal approval?"},
                {"question": "Union stewards must report official time, travel and related costs accurately and timely.", "answer": "What is accurate cost reporting?"},
            ],
            200: [
                {"question": "Initial meeting in the grievance process is called this.", "answer": "What is a Step 1 grievance meeting?"},
                {"question": "Meeting between management and union on local institutional grievances.", "answer": "What is a local institutional grievance meeting?"},
                {"question": "Meeting addressing grievances affecting multiple employees.", "answer": "What is a mass grievance meeting?"},
            ],
            300: [
                {"question": "Step 1 and Step 2 grievance meetings are electronic unless travel is authorized; within the commuting area they may be face-to-face with no travel reimbursement.", "answer": "What is the electronic Step 1 & 2 rule?"},
                {"question": "For local institutional grievances, management may choose the meeting format; if face-to-face, the employer pays travel and per diem for one steward.", "answer": "What is the local institutional meeting rule?"},
                {"question": "Mass or streamlined grievance meetings allow one steward; employer reimburses travel for Step 3 or Step 2 if an Executive is the hearing official.", "answer": "What is the mass grievance travel rule?"},
            ],
            400: [
                {"question": "Step 3 meetings, or Step 2 when an Executive is the hearing official, may be held telephonically by mutual agreement.", "answer": "What is the telephonic meeting option?"},
                {"question": "Employee appraisal grievance: Step 2 is telephonic unless participants are in the commuting area; Step 3 is telephonic unless participants are in commuting area.", "answer": "What is the appraisal grievance rule?"},
                {"question": "If the union elects a face-to-face Step 2 appraisal grievance, the employer pays travel for one steward; Step 3 will then be telephonic unless participants are in the commuting area.", "answer": "What is the face-to-face Step 2 election?"},
            ],
            500: [
                {"question": "All union travel must be charged to Purpose Code U to support program goals and tracking.", "answer": "What is the Purpose Code U requirement?"},
                {"question": "The travel tracking system collects data and statistics on travel and per diem to assess program efficiency.", "answer": "What is the travel tracking system?"},
                {"question": "The parties commit to reduce travel by scheduling meetings efficiently, consolidating them, and using electronic meetings.", "answer": "What is the travel reduction commitment?"},
            ],
        },
    },
    {
        "category": "Telework & Training for Stewards",
        "clues_by_value": {
            100: [
                {"question": "Stewards in eligible positions may perform union duties while doing this work arrangement.", "answer": "What is telework?"},
                {"question": "Presidents and Chief Stewards may perform union duties up to 40 hours monthly on recurring telework.", "answer": "What is the forty-hour telework allowance?"},
                {"question": "The employer pays travel and per diem for one steward per chapter per year to attend official union training.", "answer": "What is NTEU training reimbursement?"},
            ],
            200: [
                {"question": "Telework arrangement allowing employees to work remotely regularly or frequently is called this.", "answer": "What is frequent or recurring telework?"},
                {"question": "Telework done occasionally or on a scheduled basis for non-eligible positions is called this.", "answer": "What is recurring or ad hoc telework?"},
                {"question": "Official training conducted by the union's national office is known as this.", "answer": "What is NTEU National Office training?"},
            ],
            300: [
                {"question": "Stewards may perform union duties while teleworking only if they meet Article 50 criteria and are in eligible positions.", "answer": "What is the eligibility requirement?"},
                {"question": "Presidents and Chief Stewards may work 40 hours monthly on recurring telework if they meet Article 50 subsections.", "answer": "What is the 40-hour telework requirement?"},
                {"question": "Official time is authorized for stewards attending national training, and attendee names are submitted 60 days in advance.", "answer": "What is the training attendance rule?"},
            ],
            400: [
                {"question": "Employer payment of travel for training is subject to IRS, Treasury and other government policies and approval requirements.", "answer": "What is the approval requirement?"},
                {"question": "Stewards must attend the training session closest to their work location unless a cheaper alternate location exists.", "answer": "What is the nearest training session rule?"},
                {"question": "The employer pays travel and per diem for one steward per chapter per year to attend national training.", "answer": "What is the one-steward limit?"},
            ],
            500: [
                {"question": "Officials in non-eligible positions may perform union duties on recurring telework only if they meet subsections 2A, 2B, 2C, 2D and 2H of Article 50.", "answer": "What is Article 50 compliance?"},
                {"question": "The union must submit the names of training attendees 60 days in advance to receive employer reimbursement.", "answer": "What is the advance notice requirement?"},
                {"question": "For reimbursement, the steward must attend the nearest session or a cheaper alternate location; only one steward per chapter is reimbursed per year.", "answer": "What is the reimbursement rule?"},
            ],
        },
    },
    {
        "category": "Steward Rights",
        "clues_by_value": {
            100: [
                {"question": "Under Article 9, this time type is used by stewards to handle grievances.", "answer": "Official time"},
                {"question": "Stewards use this kind of duty time when conferring with employees on representational matters.", "answer": "Official time"},
            ],
            200: [
                {"question": "This IRS form is provided before interviewing a third-party witness.", "answer": "IRS Form 9142"},
                {"question": "Prior to a third-party witness interview, management provides this numbered IRS form.", "answer": "IRS Form 9142"},
            ],
            300: [
                {"question": "For National Office training, this many stewards per chapter receive paid travel/per diem each year.", "answer": "One"},
                {"question": "The contract provides travel/per diem annually for this number of steward(s) per chapter for NTEU National training.", "answer": "One"},
            ],
            400: [
                {"question": "If a formal discussion impacts 15+ chapters, notice is generally no less than this many workdays.", "answer": "Five workdays"},
                {"question": "For large-scale formal discussions impacting 15 or more chapters, notice is typically this length.", "answer": "Five workdays"},
            ],
            500: [
                {"question": "A full-time steward who cannot meet the 60-day appraisal period needs at least this many hours of ratable direct-time work for a rating of record.", "answer": "120 hours"},
                {"question": "Minimum ratable direct-time hours needed for a rating of record when 60-day appraisal minimum is not met: this number.", "answer": "120"},
            ],
        },
    },
    {
        "category": "Leave & Attendance",
        "clues_by_value": {
            100: [
                {"question": "For an absence of three workdays or less, this is generally acceptable sick leave evidence.", "answer": "Self-certification"},
                {"question": "For short absences (3 days or less), management generally accepts this employee-provided leave proof.", "answer": "Self-certification"},
            ],
            200: [
                {"question": "Seasonal employees may use this leave type to extend work status for health insurance eligibility.", "answer": "Annual leave"},
                {"question": "To maintain health benefits eligibility, seasonal employees may apply accumulated ______ leave.", "answer": "Annual leave"},
            ],
            300: [
                {"question": "Eligible employees may receive up to this many administrative leave hours yearly for volunteer activity.", "answer": "8"},
                {"question": "Maximum volunteer administrative leave per year is this many hours.", "answer": "8 hours"},
            ],
            400: [
                {"question": "Personal calls while on official travel: reimbursable calls include brief daily personal calls and these calls.", "answer": "Emergency personal calls"},
                {"question": "Article 29 permits reimbursement for brief daily calls and this type of urgent personal call.", "answer": "Emergency calls"},
            ],
            500: [
                {"question": "Labor Recognition Week activities: the employer makes a reasonable effort to grant up to this much administrative time.", "answer": "1 hour"},
                {"question": "Maximum admin time for Labor Recognition Week participation is this amount.", "answer": "One hour"},
            ],
        },
    },
    {
        "category": "Performance & Discipline",
        "clues_by_value": {
            100: [
                {"question": "A non-disciplinary letter of counseling is generally not relied on after this long.", "answer": "Two years"},
                {"question": "Drop file counseling material is typically purged after this period.", "answer": "2 years"},
            ],
            200: [
                {"question": "A written reprimand during the rating period does this to an otherwise earned performance award.", "answer": "It does not deny the award"},
                {"question": "True or false in effect: a written reprimand automatically denies performance awards.", "answer": "False"},
            ],
            300: [
                {"question": "Removal/downgrade for unacceptable performance requires this standard of proof.", "answer": "Substantial evidence"},
                {"question": "Under Article 40, management must prove unacceptable performance by this evidentiary standard.", "answer": "Substantial evidence"},
            ],
            400: [
                {"question": "After a final decision on a 10-day suspension, it can take effect no sooner than this.", "answer": "Seven workdays"},
                {"question": "Minimum wait after final decision before a 10-day suspension starts: this many workdays.", "answer": "7 workdays"},
            ],
            500: [
                {"question": "For higher-graded duties at 25%+ direct time, temporary promotion review looks back over this period.", "answer": "Four months"},
                {"question": "Look-back window for higher-graded duty threshold analysis is this long.", "answer": "4 months"},
            ],
        },
    },
    {
        "category": "Hiring & Movement",
        "clues_by_value": {
            100: [
                {"question": "Vacancy announcements are normally open for at least this duration.", "answer": "Ten workdays"},
                {"question": "Standard minimum posting length for vacancy announcements is this many workdays.", "answer": "10 workdays"},
            ],
            200: [
                {"question": "If AWS requests exceed openings, this tie-breaker is used first.", "answer": "IRS EOD date"},
                {"question": "First tie-breaker for limited AWS slots is the employee's ______ date.", "answer": "IRS Entry on Duty date"},
            ],
            300: [
                {"question": "If multiple employees are entitled to priority consideration, their names are sent together on this.", "answer": "A single certificate"},
                {"question": "Priority consideration remedy for multiple employees uses this submission format to the selecting official.", "answer": "Single certificate"},
            ],
            400: [
                {"question": "A hardship relocation is unavailable when an employee is on this plan.", "answer": "Performance Improvement Plan"},
                {"question": "Employees on this status are ineligible for hardship relocation under Article 15.", "answer": "PIP"},
            ],
            500: [
                {"question": "Increased part-time tour above 32 hours/week can continue for at most this many consecutive pay periods.", "answer": "Two consecutive pay periods"},
                {"question": "PTCA limit for consecutive pay periods above 64 hours/pay period is this number.", "answer": "2"},
            ],
        },
    },
    {
        "category": "Contract Process",
        "clues_by_value": {
            100: [
                {"question": "An employee request to review their own personnel records is charged to this type of time.", "answer": "Official time"},
                {"question": "Accessing personal records under the contract is done on this time status.", "answer": "Official time"},
            ],
            200: [
                {"question": "A requested resignation withdrawal before effective date may be denied for valid commitment to hire a replacement, but not for this reason.", "answer": "Avoidance of an adverse action proceeding"},
                {"question": "This is NOT a legitimate reason to deny a timely resignation withdrawal request.", "answer": "Avoidance of adverse action"},
            ],
            300: [
                {"question": "Under grievance exclusions, this role gives final decision authority for an excluded matter: the Executive or this.", "answer": "Designee"},
                {"question": "Article 41 exclusions reference final handling by the Executive or this person.", "answer": "Designee"},
            ],
            400: [
                {"question": "An otherwise eligible childcare subsidy applicant must have total family income less than this amount.", "answer": "$90,000"},
                {"question": "Childcare subsidy TFI threshold is below this figure.", "answer": "90000"},
            ],
            500: [
                {"question": "When too many employees are entitled to priority consideration, names are put on one certificate to this official.", "answer": "Selecting official"},
                {"question": "The single certificate for priority consideration is sent to this role.", "answer": "Selecting official"},
            ],
        },
    },
    {
        "category": "Travel & Scheduling",
        "clues_by_value": {
            100: [
                {"question": "On official travel, reimbursable personal calls include brief daily calls plus this type.", "answer": "Emergency personal calls"},
                {"question": "Article 29 allows reimbursement for brief daily calls and this urgent call category.", "answer": "Emergency calls"},
            ],
            200: [
                {"question": "If AWS ties remain after primary review, tie-breaking begins with this date type.", "answer": "IRS EOD date"},
                {"question": "Alternative Work Schedule first tie-break metric: IRS ______ date.", "answer": "Entry on Duty"},
            ],
            300: [
                {"question": "Part-time tours above 32 hours/week are limited to this many consecutive pay periods.", "answer": "2"},
                {"question": "Maximum consecutive pay periods over 64 hours/pay period under PTCA is this number.", "answer": "Two"},
            ],
            400: [
                {"question": "Vacancy announcements are typically open no fewer than this number of workdays.", "answer": "10 workdays"},
                {"question": "Normal minimum vacancy posting period: this many workdays.", "answer": "Ten workdays"},
            ],
            500: [
                {"question": "When formal discussion impacts 15+ chapters, minimum notice is generally this many workdays.", "answer": "Five"},
                {"question": "Large multi-chapter formal discussion notice period is no less than this.", "answer": "5 workdays"},
            ],
        },
    },
]


def get_randomized_jeopardy_board():
    """Return a randomized board with random categories and random clues."""
    selected_count = min(JEOPARDY_CATEGORY_COUNT, len(JEOPARDY_QUESTION_BANK))
    selected_categories = random.sample(JEOPARDY_QUESTION_BANK, selected_count)

    board = []
    for category in selected_categories:
        clues = []
        for value in JEOPARDY_VALUES:
            pool = category["clues_by_value"][value]
            selected = random.choice(pool)
            clues.append(
                {
                    "value": value,
                    "question": selected["question"],
                    "answer": selected["answer"],
                }
            )

        board.append({"category": category["category"], "clues": clues})

    return board
