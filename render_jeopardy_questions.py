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
