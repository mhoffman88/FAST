import streamlit as st
import random
import pandas as pd

# -------------------------
# QUIZ DATA STRUCTURE
# -------------------------

# Format: { "question": "...", "options": [...], "answer": "..." }
QUESTIONS = [
    {
        "question": "An employee is being interviewed as a third-party witness by an employer representative. Which form must the employer provide to the employee before the interview begins?",
        "options": [
            "IRS Form 8111",
            "IRS Form 9142",
            "IRS Form 13442",
            "No form is required for third-party witnesses."
        ],
        "answer": "IRS Form 9142"
    },
    {
        "question": "According to Article 7, after what period of time may a non-disciplinary action, such as a letter of counseling, NOT be relied on by the IRS and should be purged from an employee's drop file?",
        "options": [
            "One (1) year from the issuance date.",
            "After the employee's next annual performance appraisal.",
            "Three (3) years from the issuance date.",
            "Two (2) years from the issuance date."
        ],
        "answer": "Two (2) years from the issuance date."
    },
    {
        "question": "Under Article 8, if a formal discussion will impact 15 or more chapters, how much advance notice must the Employer generally provide to the three Chapter Presidents representing the most impacted employees?",
        "options": [
            "At least 24 hours.",
            "At least two (2) workdays.",
            "No less than five (5) workdays.",
            "No less than ten (10) workdays."
        ],
        "answer": "No less than five (5) workdays."
    },
    {
        "question": "Which of the following activities is a steward permitted to perform using 'Bank Time' under Article 9?",
        "options": [
            "Attending an arbitration hearing.",
            "Conferring with an employee to prepare a grievance.",
            "Participating in negotiations with the Employer.",
            "Attending formal discussions with the Employer."
        ],
        "answer": "Conferring with an employee to prepare a grievance."
    },
    {
        "question": "Under Article 12, what is the minimum number of hours of ratable, direct-time work a full-time steward must perform during a rating period to receive a performance rating of record, if they cannot meet the 60-day minimum appraisal period?",
        "options": [
            "160 hours.",
            "120 hours.",
            "60 hours.",
            "80 hours."
        ],
        "answer": "120 hours."
    },
    {
        "question": "According to Article 13, what is the minimum amount of time a vacancy announcement will normally be open for applications?",
        "options": [
            "Seven (7) calendar days.",
            "Five (5) workdays.",
            "Ten (10) workdays.",
            "Fifteen (15) workdays."
        ],
        "answer": "Ten (10) workdays."
    },
    {
        "question": "Which of the following conditions would make an employee INELIGIBLE for a hardship relocation under Article 15?",
        "options": [
            "The employee is currently on a Performance Improvement Plan (PIP).",
            "The employee's immediate family member has a serious medical condition requiring a move.",
            "The employee has a 'Fully Successful' rating of record.",
            "The employee's hardship is temporary in nature."
        ],
        "answer": "The employee is currently on a Performance Improvement Plan (PIP)."
    },
    {
        "question": "An employee is otherwise eligible for a performance award, but received a written reprimand during the rating period. According to Article 18, how does this affect the award?",
        "options": [
            "The award will be delayed pending an investigation.",
            "The award will not be denied.",
            "The award will be automatically denied.",
            "The award amount will be reduced by 50%."
        ],
        "answer": "The award will not be denied."
    },
    {
        "question": "Under Article 23, if there are too many employee requests for a vacant and available Alternative Work Schedule (AWS), what is the FIRST tie-breaker used to make the decision?",
        "options": [
            "Last four digits of the Social Security Number.",
            "The employee's most recent performance rating.",
            "Service Computation Date (SCD).",
            "IRS Entry on Duty (EOD) date."
        ],
        "answer": "IRS Entry on Duty (EOD) date."
    },
    {
        "question": "Per Article 34, for an absence of three consecutive workdays or less, what will the Employer generally consider as administratively acceptable evidence for sick leave?",
        "options": [
            "An employee's self-certification as to the reason for the absence.",
            "A signed statement from a family member.",
            "A medical certificate from a healthcare provider.",
            "A copy of a prescription for medication."
        ],
        "answer": "An employee's self-certification as to the reason for the absence."
    },
    {
        "question": "An employee receives a letter of proposed suspension for 10 days. According to Article 38, how soon after the employee receives the final decision can the suspension take effect?",
        "options": [
            "No sooner than thirty (30) calendar days.",
            "Immediately upon receipt.",
            "No sooner than seven (7) workdays.",
            "No sooner than three (3) workdays."
        ],
        "answer": "No sooner than seven (7) workdays."
    },
    {
        "question": "Based on Article 41, which of the following matters is specifically excluded from the employee grievance procedure?",
        "options": [
            "A charge of Absent Without Leave (AWOL).",
            "A dispute over the approval of official time under Article 9.",
            "The denial of an outside employment request.",
            "The separation of a probationary employee."
        ],
        "answer": "The separation of a probationary employee."
    },
    {
        "question": "If an employee's request for a telework arrangement is denied, and the employee requests reconsideration, who must provide the final written response after the reconsideration process?",
        "options": [
            "The employee's immediate supervisor.",
            "The Senior Commissioner Representative (SCR).",
            "The local Labor Relations office.",
            "The Executive or designee."
        ],
        "answer": "The Executive or designee."
    },
    {
        "question": "Under Article 56, what is the maximum Total Family Income (TFI) an employee can have to be eligible for the childcare subsidy program?",
        "options": [
            "Less than $90,000.",
            "There is no income limit.",
            "Less than $100,000.",
            "Less than $75,000."
        ],
        "answer": "Less than $90,000."
    },
    {
        "question": "What is the maximum amount of administrative time the Employer will make a reasonable effort to grant employees to participate in Labor Recognition Week activities?",
        "options": [
            "Four (4) hours.",
            "Two (2) hours.",
            "No administrative time is granted.",
            "One (1) hour."
        ],
        "answer": "One (1) hour."
    },
    {
        "question": "According to Article 9, how many stewards per Chapter will the Employer pay travel and per diem for each calendar year to attend NTEU National Office training?",
        "options": [
            "All designated stewards.",
            "One (1) steward per 300 bargaining unit employees.",
            "One (1) steward per Chapter.",
            "Two (2) stewards per Chapter."
        ],
        "answer": "One (1) steward per Chapter."
    },
    {
        "question": "Under Article 16, if an employee is not detailed to a higher-grade position but performs higher-graded duties for 25% or more of their direct time, over what preceding period will the Employer look back to determine if a temporary promotion is warranted?",
        "options": [
            "One (1) calendar year.",
            "One (1) full pay period.",
            "Sixty (60) days.",
            "Four (4) months."
        ],
        "answer": "Four (4) months."
    },
    {
        "question": "According to Article 40, what is the standard of proof the Employer must meet to support an action to remove or downgrade an employee for unacceptable performance?",
        "options": [
            "Beyond a reasonable doubt.",
            "Substantial evidence.",
            "A scintilla of evidence.",
            "Preponderance of the evidence."
        ],
        "answer": "Substantial evidence."
    },
    {
        "question": "Under Article 7, if an employee requests access to their own personnel records, how is that time charged?",
        "options": [
            "On official time.",
            "As administrative leave.",
            "As annual leave.",
            "On the employee's own time (break or lunch)."
        ],
        "answer": "On official time."
    },
    {
        "question": "According to Article 5, an employee requests to withdraw their resignation in writing before its effective date. Which of the following is NOT a legitimate reason for the Employer to deny the request?",
        "options": [
            "Avoidance of an adverse action proceeding.",
            "A valid commitment to hire a replacement.",
            "Administrative disruption.",
            "The hiring of a replacement."
        ],
        "answer": "Avoidance of an adverse action proceeding."
    },
    {
        "question": "Per Article 36, what is the maximum number of administrative leave hours per year an eligible employee may be granted for volunteer activities?",
        "options": [
            "Up to eight (8) hours.",
            "Up to four (4) hours.",
            "Up to sixteen (16) hours.",
            "Up to one (1) hour."
        ],
        "answer": "Up to eight (8) hours."
    },
    {
        "question": "Under Article 13, when an employee is improperly considered for a vacancy and is granted priority consideration as a remedy, what happens if more than one employee is entitled to this consideration for the next appropriate vacancy?",
        "options": [
            "The employee with the earliest IRS EOD date is considered first.",
            "The vacancy is canceled and re-posted.",
            "The names of only those employees entitled to consideration will be submitted on a single certificate to the selecting official.",
            "All employees are reranked with the other applicants."
        ],
        "answer": "The names of only those employees entitled to consideration will be submitted on a single certificate to the selecting official."
    },
    {
        "question": "In accordance with Article 22 and the Part-Time Career Employment Act (PTCA), what is the maximum number of consecutive pay periods an employee's tour of duty can be increased above 32 hours per week (or 64 per pay period)?",
        "options": [
            "One (1) pay period.",
            "Two (2) consecutive pay periods.",
            "There is no limit.",
            "Four (4) pay periods."
        ],
        "answer": "Two (2) consecutive pay periods."
    },
    {
        "question": "An employee is on official travel status. According to Article 29, what personal telephone calls will be reimbursed?",
        "options": [
            "No personal calls are reimbursed.",
            "Only documented emergency calls are reimbursed.",
            "All personal calls are reimbursed without limit.",
            "Brief personal telephone calls each day and emergency personal calls."
        ],
        "answer": "Brief personal telephone calls each day and emergency personal calls."
    },
    {
        "question": "According to Article 22, to maintain health insurance eligibility, the Employer will allow seasonal employees to use what type of accumulated leave to extend their time in work status?",
        "options": [
            "Sick leave.",
            "Annual leave.",
            "Compensatory time.",
            "Credit hours."
        ],
        "answer": "Annual leave."
    },
    {
        "question": "Under Article 23, if an employee is temporarily removed from an Alternative Work Schedule (AWS) due to conduct problems related to the abuse of the AWS agreement, what is the normal maximum duration of the removal?",
        "options": [
            "Three (3) months.",
            "One (1) pay period.",
            "One (1) year.",
            "Six (6) months."
        ],
        "answer": "Three (3) months."
    },
    {
        "question": "Per Article 41, after the Union receives the Employer's final grievance decision, what is the maximum time limit for the Union to invoke arbitration?",
        "options": [
            "Ten (10) workdays.",
            "Thirty (30) days.",
            "Fifteen (15) workdays.",
            "Sixty (60) days."
        ],
        "answer": "Thirty (30) days."
    },
    {
        "question": "A teleworking employee experiences a power outage at their approved telework site, but their assigned Post of Duty (POD) remains open. According to Article 50, what may the employee's manager direct them to do?",
        "options": [
            "Use their own equipment to continue working.",
            "Take unscheduled annual leave for the remainder of the day.",
            "Remain at home and be granted weather and safety leave automatically.",
            "Report to their assigned POD to complete their workday."
        ],
        "answer": "Report to their assigned POD to complete their workday."
    },
    {
        "question": "An IRS employee is called into an interview by their manager and a Special Agent. The employee reasonably believes the interview could result in discipline. According to the National Agreement, what right must the employee be advised of by the Employer?",
        "options": [
            "The right to record the interview for personal records.",
            "The right to Union representation.",
            "The right to receive a copy of the final report within 48 hours.",
            "The right to remain silent without consequence."
        ],
        "answer": "The right to Union representation."
    },
    {
        "question": "How must a supervisor consider the authorized time a union steward spends on representational functions when preparing their annual performance appraisal?",
        "options": [
            "It is completely ignored, and the evaluation is based only on the work produced, regardless of time spent.",
            "The time must be documented as a reason for lower productivity if goals are not met.",
            "The steward must perform at least 50% of their duties on direct time to be eligible for a rating.",
            "It must not be considered a negative factor, and performance standards should be adjusted accordingly."
        ],
        "answer": "It must not be considered a negative factor, and performance standards should be adjusted accordingly."
    },
    {
        "question": "An employee submits a fully completed request to their supervisor to engage in outside employment. According to Article 6, what is the maximum time the Employer has to approve or disapprove this request?",
        "options": [
            "10 workdays",
            "5 workdays",
            "15 calendar days",
            "There is no specified time limit for the response."
        ],
        "answer": "10 workdays"
    },
    {
        "question": "If the Employer determines that an employee will be charged as Absent Without Leave (AWOL), what is a key procedural requirement outlined in the agreement?",
        "options": [
            "The AWOL charge cannot be issued until the end of the pay period.",
            "A union representative must be present when the employee is notified.",
            "The employee must first be given a verbal warning for the same offense.",
            "The employee must be notified of the AWOL charge in writing."
        ],
        "answer": "The employee must be notified of the AWOL charge in writing."
    },
    {
        "question": "For a standard Telework arrangement, what is the maximum radius from the employee's assigned Post of Duty (POD) that their approved telework location can be?",
        "options": [
            "200 miles",
            "There is no mileage limit specified.",
            "50 miles",
            "100 miles"
        ],
        "answer": "200 miles"
    },
    {
        "question": "Under which of the following circumstances is it appropriate for the Employer to utilize the Alternative Discipline process for a bargaining unit employee?",
        "options": [
            "Only if it is the employee's first instance of misconduct.",
            "When the proposed discipline is a reprimand or a suspension of 14 days or less.",
            "For any proposed adverse action, including removal.",
            "Only for performance-based issues under Article 40."
        ],
        "answer": "When the proposed discipline is a reprimand or a suspension of 14 days or less."
    },
    {
        "question": "Which of the following matters is specifically excluded from the employee grievance procedure outlined in Article 41?",
        "options": [
            "The separation of a probationary employee.",
            "A disagreement with a 'Minimally Successful' performance rating.",
            "A dispute over the equitable distribution of overtime.",
            "The denial of a performance award."
        ],
        "answer": "The separation of a probationary employee."
    }
]

# Shuffle question order every time
def get_randomized_questions():
    randomized = QUESTIONS.copy()
    random.shuffle(randomized)
    return randomized

# -------------------------
# QUIZ SESSION STATE SETUP
# -------------------------

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answers" not in st.session_state:
    st.session_state.answers = []  # stores tuples: (question, chosen_answer, correct_answer, result)

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

# -------------------------
# START QUIZ
# -------------------------

st.title("FAST: Steward Training Quiz")

if not st.session_state.quiz_started:
    st.write("Press start when you're ready. Questions will be randomly selected.")
    if st.button("Start Quiz"):
        st.session_state.quiz_started = True
        st.session_state.quiz_questions = get_randomized_questions()
        st.rerun()
else:
    # -------------------------
    # QUIZ IN PROGRESS
    # -------------------------
    q_list = st.session_state.quiz_questions
    q_num = st.session_state.current_index

    if q_num < len(q_list):
        q = q_list[q_num]

        st.subheader(f"Question {q_num+1} of {len(q_list)}")
        st.write(q["question"])

        choice = st.radio("Choose an answer:", q["options"], key=f"q{q_num}")

        if st.button("Submit Answer", key=f"submit{q_num}"):
            correct = q["answer"]

            if choice == correct:
                st.session_state.score += 1
                result = "Correct"
                st.success("Correct! ✔️")
            else:
                result = "Incorrect"
                st.error(f"Incorrect ❌ — Correct answer: **{correct}**")

            st.session_state.answers.append((q["question"], choice, correct, result))
            st.session_state.current_index += 1
            st.rerun()

    else:
        # -------------------------
        # QUIZ COMPLETE
        # -------------------------

        st.header("🎉 Quiz Complete!")
        score = st.session_state.score
        total = len(q_list)
        st.subheader(f"Final Score: **{score}/{total}** ({round(score/total*100)}%)")

        # -------------------------
        # BUILD RESULTS TABLE
        # -------------------------

        df = pd.DataFrame(st.session_state.answers, columns=[
            "Question", "Your Answer", "Correct Answer", "Result"
        ])

        st.dataframe(df)

        # -------------------------
        # IMPROVEMENT SUMMARY
        # -------------------------

        st.subheader("📌 Areas to Improve")

        missed = df[df["Result"] == "Incorrect"]
        if missed.empty:
            st.success("You answered everything correctly! Great work.")
        else:
            for i, row in missed.iterrows():
                st.write(f"- **{row['Question']}**")

        # -------------------------
        # PRINT / EXPORT
        # -------------------------

        st.subheader("📄 Export Your Results")

        # Convert DataFrame to CSV for easy printing or saving
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="FAST_quiz_results.csv",
            mime="text/csv"
        )

        st.markdown("""
        **To Print:**  
        1. Download the CSV (above)  
        2. Open it in Excel or Google Sheets  
        3. Press **Ctrl+P**  
        """)

        if st.button("Retake Quiz"):
            st.session_state.quiz_started = False
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.rerun()
