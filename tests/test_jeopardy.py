from render_jeopardy import _normalize
from render_jeopardy_questions import (
    JEOPARDY_CATEGORY_COUNT,
    JEOPARDY_QUESTION_BANK,
    JEOPARDY_VALUES,
    get_randomized_jeopardy_board,
)


def test_normalize_accepts_jeopardy_phrasing():
    assert _normalize("What is Form 9142?") == _normalize("form 9142")
    assert _normalize("Who is bargaining-unit employees and IRS retirees?") == _normalize(
        "bargaining unit employees and irs retirees"
    )
    assert _normalize("What are credit hours?") == _normalize("credit hours")


def test_random_board_shape_and_values():
    board = get_randomized_jeopardy_board()

    assert len(board) == min(JEOPARDY_CATEGORY_COUNT, len(JEOPARDY_QUESTION_BANK))

    for category in board:
        assert "category" in category
        assert "clues" in category
        assert len(category["clues"]) == len(JEOPARDY_VALUES)
        assert [clue["value"] for clue in category["clues"]] == JEOPARDY_VALUES
        for clue in category["clues"]:
            assert clue["question"]
            assert clue["answer"]


def test_random_board_categories_are_unique_per_game():
    board = get_randomized_jeopardy_board()
    categories = [category["category"] for category in board]
    assert len(categories) == len(set(categories))


def test_question_bank_contains_expected_training_categories():
    categories = {entry["category"] for entry in JEOPARDY_QUESTION_BANK}
    expected = {
        "Interview & Investigation Rights",
        "Designation of Stewards",
        "Official Time Activities",
        "Bank Time & Steward Categories",
        "Performance-Appraisal Definitions",
        "Prohibited Personnel Practices & Merit System",
        "Travel & Per Diem",
        "Telework & Training for Stewards",
    }
    assert expected.issubset(categories)


def test_normalize_preserves_plain_answers_too():
    assert _normalize("Substantial evidence") == "substantialevidence"
