# pages/quiz_page.py

import streamlit as st
import pandas as pd
from render_quiz_engine import get_randomized_questions, grade_quiz


def run_quiz():

    st.title("FAST: Steward Training Quiz")

    # -------------------------
    # SESSION STATE INIT
    # -------------------------
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "questions" not in st.session_state:
        st.session_state.questions = []

    # -------------------------
    # QUIZ START BUTTON
    # -------------------------
    if not st.session_state.quiz_started:
        st.write("Press start when you're ready. The quiz will randomize questions.")
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            st.session_state.questions = get_randomized_questions()
            st.session_state.current_index = 0
            st.session_state.answers = []
            st.rerun()
        return  # Prevent Streamlit from continuing

    # -------------------------
    # QUIZ IN PROGRESS
    # -------------------------
    index = st.session_state.current_index
    questions = st.session_state.questions

    # If there are questions left
    if index < len(questions):
        q = questions[index]

        st.subheader(f"Question {index + 1} of {len(questions)}")
        st.write(q["question"])

        choice = st.radio(
            "Choose an answer:",
            q["options"],
            key=f"question_{index}"
        )

        if st.button("Submit Answer", key=f"submit_{index}"):
            st.session_state.answers.append(
                (q["question"], choice, q["answer"])
            )
            st.session_state.current_index += 1
            st.rerun()

    # -------------------------
    # QUIZ COMPLETE
    # -------------------------
    else:
        st.header("🎉 Quiz Complete!")

        score, results = grade_quiz(st.session_state.answers)
        percent = round(score / len(results) * 100)

        st.subheader(f"Final Score: {score}/{len(results)} ({percent}%)")

        df = pd.DataFrame(results)
        st.dataframe(df)

        st.subheader("📌 Areas to Improve")
        missed = df[df["result"] == "Incorrect"]

        if missed.empty:
            st.success("Perfect score! Outstanding work!")
        else:
            for _, row in missed.iterrows():
                st.write(f"- **{row['question']}**")

        # CSV DOWNLOAD
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Results",
            csv,
            file_name="FAST_quiz_results.csv",
            mime="text/csv"
        )

        if st.button("Retake Quiz"):
            st.session_state.quiz_started = False
            st.session_state.answers = []
            st.session_state.current_index = 0
            st.session_state.questions = []
            st.rerun()
