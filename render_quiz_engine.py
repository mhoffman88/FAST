# quiz/quiz_engine.py

import random
from quiz.question_bank import QUESTIONS

def get_randomized_questions():
    """Return a randomized copy of the full question bank."""
    q_copy = QUESTIONS.copy()
    random.shuffle(q_copy)
    return q_copy


def grade_quiz(answers):
    """
    Accepts a list of tuples:
      (question, chosen_answer, correct_answer)
    Returns:
      score, detailed_results
    """
    score = 0
    detailed = []

    for q, chosen, correct in answers:
        is_correct = (chosen == correct)
        if is_correct:
            score += 1

        detailed.append({
            "question": q,
            "your_answer": chosen,
            "correct_answer": correct,
            "result": "Correct" if is_correct else "Incorrect"
        })

    return score, detailed
